"""Tests for cwe_to_markdown (CWE edition -> markdown pages)."""

import contextlib
import copy
import dataclasses
import io
import posixpath
import re
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import cwe_to_markdown as ctm  # noqa: E402
import cwe_xml as cx  # noqa: E402

CWE_DIR = SCRIPTS_DIR.parent
VERSIONS = ("4.19.1", "5.0")
CATALOG = {  # weaknesses, categories/groupings, views (spec, Input table)
    "4.19.1": (969, 420, 58),
    "5.0": (984, 431, 62),
}
LICENSE_URL = (
    "https://github.com/CloudSecurityAlliance-DataSets/"
    "dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/{v}/LICENSE.txt"
)
SECTION_ORDER = [
    "Description", "Extended Description", "Alternate Terms", "Related Weaknesses",
    "Weakness Ordinalities", "Applicable Platforms", "Background Details",
    "Modes Of Introduction", "Exploitation Factors", "Likelihood Of Exploit",
    "Common Consequences", "Detection Methods", "Potential Mitigations",
    "Demonstrative Examples", "Observed Examples", "Functional Areas",
    "Affected Resources", "Dimensions", "Technical Nuance", "Taxonomy Mappings",
    "Related Attack Patterns", "References", "Mapping Notes", "Notes",
]

ED = {}
FILES = {}


def setUpModule():
    for v in VERSIONS:
        ED[v] = cx.load_edition(CWE_DIR / v, v)
        FILES[v] = ctm.render_edition(ED[v])


def footer(v):
    return (
        "---\n"
        f"Generated from MITRE's CWE {v} XML (cwec_v{v}.xml) by "
        "weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.\n"
        "Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.\n"
        "Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html "
        f"(full text: {LICENSE_URL.format(v=v)}).\n"
    )


def h2_sections(page):
    """[(heading, body)] for each '## ' heading, outside fenced code."""
    out, cur, body, fence = [], None, [], None
    for line in page.split("\n"):
        m = re.match(r"^(`{3,})", line)
        if m:
            if fence is None:
                fence = m.group(1)
            elif line.strip() == fence:
                fence = None
        if fence is None and line.startswith("## "):
            if cur is not None:
                out.append((cur, "\n".join(body)))
            cur, body = line[3:], []
        elif cur is not None:
            body.append(line)
    if cur is not None:
        out.append((cur, "\n".join(body)))
    return out


def strip_code(page):
    """The page without fenced code blocks and inline code spans."""
    keep, fence = [], None
    for line in page.split("\n"):
        m = re.match(r"^\s*(`{3,})", line)
        if m:
            if fence is None:
                fence = m.group(1)
                continue
            if line.strip() == fence:
                fence = None
                continue
        if fence is None:
            keep.append(line)
    return re.sub(r"(`+)(?!`).*?(?<!`)\1(?!`)", "", "\n".join(keep))


class PageTests(unittest.TestCase):
    def test_front_matter_cwe79(self):
        ed = ED["5.0"]
        w = ed.weaknesses[79]
        name = w.get("Name")
        self.assertEqual(name, "Improper Neutralization of Input During Web Page Generation")
        usage = cx.text(cx.child(cx.child(w, "Mapping_Notes"), "Usage"))
        self.assertEqual(usage, "Allowed")
        expected = (
            "---\n"
            'secid: "secid:weakness/mitre.org/cwe@5.0#CWE-79"\n'
            'cwe_id: "CWE-79"\n'
            "entry_type: weakness\n"
            f'name: "{name}"\n'
            "abstraction: Base\n"
            "structure: Simple\n"
            "status: Stable\n"
            f"mapping_usage: {usage}\n"
            'cwe_version: "5.0"\n'
            'cwe_release_date: "2026-10-28"\n'
            'upstream: "https://cwe.mitre.org/data/definitions/79.html"\n'
            "---\n"
        )
        page = FILES["5.0"]["weaknesses/CWE-79.md"]
        self.assertTrue(page.startswith(expected), page[:600])
        self.assertIn(f"\n# CWE-79: {name}\n", page)

    def test_section_order(self):
        for v in VERSIONS:
            page = FILES[v]["weaknesses/CWE-79.md"]
            sections = h2_sections(page)
            headings = [h for h, _ in sections]
            self.assertGreaterEqual(len(headings), 15, headings)
            for h in headings:
                self.assertIn(h, SECTION_ORDER, f"{v}: unexpected heading {h!r}")
            idx = [SECTION_ORDER.index(h) for h in headings]
            self.assertEqual(idx, sorted(idx), f"{v}: {headings}")
            self.assertEqual(len(set(headings)), len(headings), headings)
            for h, body in sections:
                self.assertTrue(body.strip(), f"{v}: empty section {h!r}")

    def test_no_empty_sections_anywhere(self):
        for v in VERSIONS:
            for path, page in FILES[v].items():
                if not path.endswith(".md"):
                    continue
                for h, body in h2_sections(page.split("\n---\nGenerated from")[0]):
                    self.assertTrue(body.strip(), f"{v} {path}: empty section {h!r}")

    def test_line_hygiene(self):
        for v in VERSIONS:
            for path, page in FILES[v].items():
                if not path.endswith(".md"):
                    continue
                self.assertNotIn("\r", page, path)
                for n, line in enumerate(page.split("\n"), 1):
                    self.assertEqual(line, line.rstrip(" "), f"{v} {path}:{n} trailing space")
                    self.assertNotRegex(line, r"^\s*-\s*$", f"{v} {path}:{n} empty list item")
                    self.assertNotIn("\\<br>", line, f"{v} {path}:{n} escaped <br>")

    def test_new_5_0_sections(self):
        self.assertIn("\n## Technical Nuance\n", FILES["5.0"]["weaknesses/CWE-1039.md"])
        self.assertIn("\n## Dimensions\n", FILES["5.0"]["weaknesses/CWE-1024.md"])
        for path, page in FILES["4.19.1"].items():
            self.assertNotIn("\n## Technical Nuance\n", page, path)
            self.assertNotIn("\n## Dimensions\n", page, path)

    def test_footer_on_every_page(self):
        for v in VERSIONS:
            end = "\n\n" + footer(v)
            md = [p for p in FILES[v] if p.endswith(".md")]
            self.assertGreater(len(md), 1400)
            for path in md:
                self.assertTrue(FILES[v][path].endswith(end), f"{v} {path}")

    def test_all_relative_links_resolve(self):
        link = re.compile(r"\]\(<?([^)\s>]+)>?\)")
        for v in VERSIONS:
            keys = set(FILES[v])
            n = 0
            for path, page in FILES[v].items():
                if not path.endswith(".md"):
                    continue
                for target in link.findall(strip_code(page)):
                    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                        continue
                    n += 1
                    resolved = posixpath.normpath(
                        posixpath.join(posixpath.dirname(path), target.split("#")[0])
                    )
                    self.assertIn(resolved, keys, f"{v} {path} -> {target}")
            self.assertGreater(n, 10000)

    def test_counts(self):
        for v in VERSIONS:
            ed, files = ED[v], FILES[v]
            nw, ng, nv = CATALOG[v]
            self.assertEqual((len(ed.weaknesses), len(ed.groups), len(ed.views)), (nw, ng, nv))
            folders = {}
            for p in files:
                folders.setdefault(p.split("/")[0] if "/" in p else "", []).append(p)
            self.assertEqual(len(folders["weaknesses"]), nw)
            self.assertEqual(len(folders[ed.group_dir]), ng)
            self.assertEqual(len(folders["views"]), nv)
            self.assertEqual(sorted(folders[""]), ["LICENSE.txt", "index.md"])
            self.assertEqual(set(folders), {"", "weaknesses", ed.group_dir, "views"})
            index = dict(h2_sections(files["index.md"]))
            for heading, kind, count in (
                ("Weaknesses", "weaknesses", nw),
                (ed.group_term + "s", ed.group_dir, ng),
                ("Views", "views", nv),
            ):
                rows = [ln for ln in index[heading].split("\n") if ln.startswith("| [CWE-")]
                self.assertEqual(len(rows), count, f"{v} {heading}")
                ids = [int(re.match(r"\| \[CWE-(\d+)\]", r).group(1)) for r in rows]
                self.assertEqual(ids, sorted(ids), f"{v} {heading} not in numeric order")
                self.assertIn(f"]({kind}/CWE-{ids[0]}.md)", rows[0])

    def test_license_copied(self):
        for v in VERSIONS:
            self.assertEqual(
                FILES[v]["LICENSE.txt"].encode("utf-8"),
                (CWE_DIR / v / "LICENSE.txt").read_bytes(),
            )

    def test_index_header(self):
        ed = ED["5.0"]
        page = FILES["5.0"]["index.md"]
        self.assertIn(ed.sha256, page)
        self.assertIn("https://cwe.mitre.org/data/xml/cwec_v5.0.xml.zip", page)
        self.assertIn("2026-10-28", page)
        self.assertIn("](LICENSE.txt)", page)
        self.assertIn("Copyright © The MITRE Corporation", page.split("\n---\nGenerated")[0])

    def test_content_history_has_no_effect(self):
        ed = ED["5.0"]
        ids = sorted(ed.weaknesses)
        picks = sorted({79, 89, 1426, 1039, 1024, 377, *ids[::50]})
        self.assertGreaterEqual(len(picks), 20)
        for i in picks:
            w = ed.weaknesses[i]
            stripped = copy.deepcopy(w)
            history = [c for c in stripped if cx.local(c.tag) == "Content_History"]
            self.assertTrue(history, f"CWE-{i} has no Content_History to remove")
            for c in history:
                stripped.remove(c)
            self.assertEqual(ctm.render_weakness(ed, w), ctm.render_weakness(ed, stripped), i)
        for table, render in ((ed.groups, ctm.render_group), (ed.views, ctm.render_view)):
            for i in sorted(table)[:5]:
                stripped = copy.deepcopy(table[i])
                for c in [c for c in stripped if cx.local(c.tag) == "Content_History"]:
                    stripped.remove(c)
                self.assertEqual(render(ed, table[i]), render(ed, stripped), i)
        for v in VERSIONS:
            for path, page in FILES[v].items():
                self.assertIsNone(
                    re.search(r"^#+\s*Content[ _]History", page, re.M | re.I), f"{v} {path}"
                )

    def test_deterministic(self):
        self.assertEqual(ctm.render_edition(ED["5.0"]), FILES["5.0"])

    def test_check_mode(self):
        files = FILES["4.19.1"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "markdown"
            ctm.write_markdown(files, out)
            self.assertEqual(ctm.diff_markdown(files, out), [])
            (out / "weaknesses" / "CWE-79.md").write_text("changed\n", encoding="utf-8")
            (out / "views" / "stray.md").write_text("stray\n", encoding="utf-8")
            (out / "index.md").unlink()
            self.assertEqual(
                ctm.diff_markdown(files, out),
                ["index.md", "views/stray.md", "weaknesses/CWE-79.md"],
            )
            ctm.write_markdown(files, out)
            self.assertEqual(ctm.diff_markdown(files, out), [])
            self.assertFalse((out / "views" / "stray.md").exists())
            raw = (out / "weaknesses" / "CWE-79.md").read_bytes()
            self.assertNotIn(b"\r", raw)
            self.assertTrue(raw.endswith(b".txt).\n"))

    def test_main_rejects_unknown_version(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertNotEqual(ctm.main(["--version", "0.0-missing"]), 0)
        self.assertIn("0.0-missing", err.getvalue())


class ContentTests(unittest.TestCase):
    def test_cwe79_result_example_order(self):
        page = FILES["5.0"]["weaknesses/CWE-79.md"]
        start = page.index("*Example (Result):*")
        block = page[start:page.index("```", page.index("```", start) + 3)]
        login = block.index("Please Login:")
        form = block.index('<form name="input" action="attack.example.com/stealPassword.php"')
        user = block.index("Username: <input")
        close = block.index("</div></div>")
        self.assertLess(login, form)
        self.assertLess(form, user)
        self.assertLess(user, close)

    def test_cwe79_tables_and_links(self):
        page = FILES["5.0"]["weaknesses/CWE-79.md"]
        self.assertIn("[CVE-2024-49038](https://www.cve.org/CVERecord?id=CVE-2024-49038)", page)
        self.assertIn("[CAPEC-209](https://capec.mitre.org/data/definitions/209.html)", page)
        self.assertIn("](../weaknesses/CWE-74.md)", page)
        self.assertIn("](../views/CWE-1000.md)", page)
        self.assertIn("![", page)
        self.assertIn("https://cwe.mitre.org/data/images/CWE-79-Diagram.png", page)
        self.assertIn("[REF-709]", page)
        self.assertIn('"Sin 2: Web-Server Related Vulnerabilities', page)
        # a one-paragraph description sits below its mitigation label, not run into it
        self.assertIn("**ID:** MIT-15\n\n  For any security checks", page)
        self.assertIn("- **XSS** (Acronym): A common abbreviation", page)

    def test_group_page(self):
        page = FILES["5.0"]["groupings/CWE-1210.md"]
        self.assertIn("entry_type: grouping\n", page)
        self.assertIn("\n## Summary\n", page)
        self.assertIn("\n## Members\n", page)
        self.assertIn("](../weaknesses/CWE-117.md)", page)
        self.assertIn("](../views/CWE-699.md)", page)
        self.assertIn("entry_type: category\n", FILES["4.19.1"]["categories/CWE-1210.md"])

    def test_deprecated_weakness_banner(self):
        page = FILES["5.0"]["weaknesses/CWE-391.md"]
        self.assertIn("status: Deprecated\n", page)
        self.assertIn("> **Deprecated.**", page)
        self.assertIn("](../weaknesses/CWE-252.md)", page.split("## Mapping Notes")[1])

    def test_view_1000_lists_every_active_weakness(self):
        for v in VERSIONS:
            ed = ED[v]
            page = FILES[v]["views/CWE-1000.md"]
            active = [i for i, w in ed.weaknesses.items() if w.get("Status") != "Deprecated"]
            for i in active:
                self.assertIn(f"](../weaknesses/CWE-{i}.md)", page, f"{v} CWE-{i}")
        page = FILES["5.0"]["views/CWE-1000.md"]
        sections = dict(h2_sections(page))
        lost = sections["Not reachable from this view's roots"]
        for i in (378, 379):
            line = next(ln for ln in lost.split("\n") if f"[CWE-{i}](" in ln)
            self.assertIn("[CWE-377](../weaknesses/CWE-377.md)", line)
        self.assertNotIn(
            "Not reachable from this view's roots", FILES["4.19.1"]["views/CWE-1000.md"]
        )

    def test_graph_view_outline_shape(self):
        ed = ED["5.0"]
        page = FILES["5.0"]["views/CWE-1000.md"]
        self.assertIn("view_type: Graph\n", page)
        members = dict(h2_sections(page))["Members"]
        lines = [ln for ln in members.split("\n") if ln.lstrip().startswith("- ")]
        roots = [ln for ln in lines if ln.startswith("- ")]
        self.assertEqual(len(roots), len(cx.explicit_members(ed, 1000)))
        self.assertTrue(roots[0].startswith("- [CWE-284](../weaknesses/CWE-284.md) "), roots[0])
        self.assertIn("(Pillar)", roots[0])
        expanded = [ln for ln in lines if "*(listed in full" not in ln]
        ids = [re.search(r"\[CWE-(\d+)\]", ln).group(1) for ln in expanded]
        self.assertEqual(len(ids), len(set(ids)), "an entry is expanded twice")

    def test_explicit_and_implicit_views(self):
        ed = ED["5.0"]
        explicit = [i for i, x in ed.views.items()
                    if x.get("Type") == "Explicit" and x.get("Status") not in ("Deprecated", "Obsolete")]
        self.assertTrue(explicit)
        for i in explicit:
            members = dict(h2_sections(FILES["5.0"][f"views/CWE-{i}.md"]))["Members"]
            for m in cx.explicit_members(ed, i):
                self.assertIn(f"[CWE-{m}](", members)
        page = FILES["5.0"]["views/CWE-658.md"]
        sections = dict(h2_sections(page))
        self.assertIn("[./Applicable_Platforms/Language/@Name='C']", sections["Filter"])
        rows = [ln for ln in sections["Members"].split("\n") if ln.startswith("- [CWE-")]
        self.assertEqual(len(rows), len(cx.implicit_members(ed, 658)))

    def test_deprecated_and_obsolete_views_description_only(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            for i in (629, 679, 999, 630):
                page = ctm.render_view(ED["5.0"], ED["5.0"].views[i])
                headings = [h for h, _ in h2_sections(page)]
                self.assertEqual(headings, ["Objective"], (i, headings))
                self.assertNotIn("not computed", page)
        self.assertEqual(err.getvalue(), "")
        self.assertIn("members", FILES["5.0"]["views/CWE-629.md"].split("## Objective")[0])

    def test_unknown_filter_on_active_view_says_not_computed(self):
        ed = ED["5.0"]
        view = copy.deepcopy(ed.views[658])
        cx.child(view, "Filter").text = "/Weakness_Catalog/Weaknesses/Weakness[@Brand_New='x']"
        ed2 = dataclasses.replace(ed, views={**ed.views, 658: view})
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            page = ctm.render_view(ed2, view)
        self.assertIn("view 658", err.getvalue())
        self.assertIn("members not computed", err.getvalue())
        sections = dict(h2_sections(page))
        self.assertIn("[@Brand_New='x']", sections["Filter"])
        self.assertTrue(sections["Members"].strip().startswith("Members not computed"))
        self.assertNotIn("[CWE-", sections["Members"])

    def test_dangling_targets_render_as_plain_text(self):
        ed = ED["5.0"]
        w = copy.deepcopy(ed.weaknesses[79])
        rel = cx.child(w, "Related_Weaknesses")
        ns = rel.tag[: rel.tag.index("}") + 1]
        ET.SubElement(rel, ns + "Related_Weakness",
                      {"Nature": "PeerOf", "CWE_ID": "999999", "View_ID": "1000"})
        page = ctm.render_weakness(ed, w)
        self.assertIn("CWE-999999", page)
        self.assertNotIn("[CWE-999999]", page)
        g = copy.deepcopy(ed.groups[1210])
        ET.SubElement(cx.child(g, "Relationships"), ns + "Has_Member",
                      {"CWE_ID": "999998", "View_ID": "699"})
        page = ctm.render_group(ed, g)
        self.assertIn("CWE-999998", page)
        self.assertNotIn("[CWE-999998]", page)

    def test_unknown_element_fails(self):
        ed = ED["5.0"]
        w = copy.deepcopy(ed.weaknesses[79])
        ns = w.tag[: w.tag.index("}") + 1]
        ET.SubElement(w, ns + "Brand_New_Field").text = "x"
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-79.*Brand_New_Field"):
            ctm.render_weakness(ed, w)
        w = copy.deepcopy(ed.weaknesses[79])
        mit = cx.child(cx.child(w, "Potential_Mitigations"), "Mitigation")
        ET.SubElement(mit, ns + "Cost").text = "x"
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-79.*Cost"):
            ctm.render_weakness(ed, w)


if __name__ == "__main__":
    unittest.main()
