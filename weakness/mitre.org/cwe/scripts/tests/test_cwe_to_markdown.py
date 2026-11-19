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
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cwe_test_editions as eds  # noqa: E402
import cwe_to_markdown as ctm  # noqa: E402
import cwe_xml as cx  # noqa: E402

CWE_DIR = SCRIPTS_DIR.parent
# Every edition folder with a zip sidecar; the tests that need one whose zip is
# absent skip (or fail, with CWE_REQUIRE_ZIPS=1).
VERSIONS = tuple(eds.editions())
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
    "Related Attack Patterns", "References", "Mapping Notes", "Notes", "Content History",
]
HISTORY_KINDS = ("Submission", "Contribution", "Modification")

class _ByEdition(dict):
    """Loaded editions (ED) or their rendered files (FILES). Reading an edition whose
    zip is absent skips the test, or fails it with CWE_REQUIRE_ZIPS=1."""

    def __missing__(self, version):
        eds.require(version)
        raise KeyError(version)


ED = _ByEdition()
FILES = _ByEdition()


def setUpModule():
    for v in VERSIONS:
        if eds.present(v):
            ED[v] = cx.load_edition(CWE_DIR / v, v)
            FILES[v] = ctm.render_edition(ED[v])


def footer(v):
    return (
        "---\n"
        f"Generated from MITRE's CWE {v} XML (cwec_v{v}.xml) by "
        "weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.\n"
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


def history_section(page):
    """The body of the page's '## Content History' section, footer excluded."""
    return dict(h2_sections(page.split("\n---\nGenerated from")[0]))["Content History"]


def history_rows(section):
    """The Content History table as [{column: cell}], in page order."""
    lines = [ln for ln in section.split("\n") if ln.startswith("| ")]
    split = lambda ln: [c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]]  # noqa: E731
    header = split(lines[0])
    return [dict(zip(header, split(ln))) for ln in lines[2:]]


def history_events(elem):
    """The Submission, Contribution and Modification elements of an entry's
    Content_History, in the page's order (by kind, then MITRE's document order)."""
    ch = cx.child(elem, "Content_History")
    return [e for kind in HISTORY_KINDS for e in cx.children(ch, kind)]


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
            with self.subTest(edition=v):
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
            with self.subTest(edition=v):
                for path, page in FILES[v].items():
                    if not path.endswith(".md"):
                        continue
                    for h, body in h2_sections(page.split("\n---\nGenerated from")[0]):
                        self.assertTrue(body.strip(), f"{v} {path}: empty section {h!r}")

    def test_line_hygiene(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
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
        for v in VERSIONS:
            with self.subTest(edition=v):
                if ED[v].schema_major != 7:
                    continue
                for path, page in FILES[v].items():
                    self.assertNotIn("\n## Technical Nuance\n", page, path)
                    self.assertNotIn("\n## Dimensions\n", page, path)

    def test_footer_on_every_page(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                end = "\n\n" + footer(v)
                md = [p for p in FILES[v] if p.endswith(".md")]
                self.assertGreater(len(md), 1400)
                for path in md:
                    self.assertTrue(FILES[v][path].endswith(end), f"{v} {path}")

    def test_all_relative_links_resolve(self):
        link = re.compile(r"\]\(<?([^)\s>]+)>?\)")
        for v in VERSIONS:
            with self.subTest(edition=v):
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
            with self.subTest(edition=v):
                ed, files = ED[v], FILES[v]
                self.assertIn(v, eds.EXPECTED, f"add CWE {v}'s catalog counts to EXPECTED")
                exp = eds.EXPECTED[v]
                nw, ng, nv = exp["weaknesses"], exp["groups"], exp["views"]
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
                    ({"Category": "Categories", "Grouping": "Groupings"}[ed.group_term],
                     ed.group_dir, ng),
                    ("Views", "views", nv),
                ):
                    rows = [ln for ln in index[heading].split("\n") if ln.startswith("| [CWE-")]
                    self.assertEqual(len(rows), count, f"{v} {heading}")
                    ids = [int(re.match(r"\| \[CWE-(\d+)\]", r).group(1)) for r in rows]
                    self.assertEqual(ids, sorted(ids), f"{v} {heading} not in numeric order")
                    self.assertIn(f"]({kind}/CWE-{ids[0]}.md)", rows[0])

    def test_index_plurals(self):
        plural = {7: "Categories", 8: "Groupings"}  # MITRE's term per schema major
        for v in VERSIONS:
            with self.subTest(edition=v):
                term = plural[ED[v].schema_major]
                page = FILES[v]["index.md"]
                self.assertIn(f"\n## {term}\n", page)
                self.assertIn(f"| {term} | {len(ED[v].groups)} |", page)
                self.assertIn(f"| Status | Weaknesses | {term} | Views |", page)
                for path, text in FILES[v].items():
                    self.assertNotIn("Categorys", text, f"{v} {path}")
                    self.assertNotIn("Groupings s", text, f"{v} {path}")

    def test_license_copied(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
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
            with self.subTest(edition=v):
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
                self.assertEqual(headings, ["Objective", "Content History"], (i, headings))
                self.assertNotIn("not computed", page)
        self.assertEqual(err.getvalue(), "")
        note = FILES["5.0"]["views/CWE-629.md"].split("## Objective")[0]
        self.assertIn("members", note)
        self.assertIn("Only the objective, status and content history of an obsolete", note)

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

    def test_repeated_values_all_rendered(self):
        # Observed_Example/Rationale repeats (schema 8): both values on CWE-125's Heartbleed row
        page = FILES["5.0"]["weaknesses/CWE-125.md"]
        row = next(ln for ln in page.split("\n") if ln.startswith("| [CVE-2014-0160]("))
        self.assertIn("Influential/Newsworthy; Chain", row)
        # External_Reference/Media_Type repeats: REF-1556 lists two media types
        page = FILES["5.0"]["weaknesses/CWE-1461.md"]
        ref = next(ln for ln in page.split("\n") if ln.startswith("- [REF-1556]"))
        self.assertIn("Media types: Common-Proprietary-Text; Video", ref)

    def test_repeated_single_valued_element_fails(self):
        ed = ED["5.0"]
        ns = ed.weaknesses[79].tag[: ed.weaknesses[79].tag.index("}") + 1]
        w = copy.deepcopy(ed.weaknesses[79])
        w.append(copy.deepcopy(cx.child(w, "Description")))
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-79.*<Description> appears 2 times"):
            ctm.render_weakness(ed, w)
        w = copy.deepcopy(ed.weaknesses[79])
        mn = cx.child(w, "Mapping_Notes")
        ET.SubElement(mn, ns + "Usage").text = "Prohibited"
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-79.*<Usage> appears 2 times"):
            ctm.render_weakness(ed, w)
        w = copy.deepcopy(ed.weaknesses[79])
        mit = cx.child(cx.child(w, "Potential_Mitigations"), "Mitigation")
        ET.SubElement(mit, ns + "Strategy").text = "One"
        ET.SubElement(mit, ns + "Strategy").text = "Two"
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-79.*<Strategy> appears"):
            ctm.render_weakness(ed, w)
        view = copy.deepcopy(ed.views[1000])
        view.append(copy.deepcopy(cx.child(view, "Members")))
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"CWE-1000.*<Members> appears 2 times"):
            ctm.render_view(ed, view)
        ref = copy.deepcopy(ed.references["REF-709"])
        ET.SubElement(ref, ns + "Title").text = "Second title"
        ed2 = dataclasses.replace(ed, references={**ed.references, "REF-709": ref})
        with self.assertRaisesRegex(ctm.UnexpectedMarkupError, r"REF-709.*<Title> appears 2 times"):
            ctm.render_weakness(ed2, ed.weaknesses[79])

    def test_no_unchecked_single_reads(self):
        # Every single-valued read goes through _one(), which fails on a repeat.
        src = Path(ctm.__file__).read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?<![\w.])child\(|cx\.child\(", src))

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


def _entries(ed):
    """(folder, CWE ID, element) for every weakness, category/grouping and view."""
    for table, folder in ((ed.weaknesses, "weaknesses"), (ed.groups, ed.group_dir),
                          (ed.views, "views")):
        for i, e in sorted(table.items()):
            yield folder, i, e


class ContentHistoryTests(unittest.TestCase):
    """MITRE's Content_History, rendered as the last section of every entry page
    (Kurt, 2026-11-19: "lets default to mirroring data faithfully")."""

    def test_cwe79_history_is_last_section(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                ch = cx.child(ED[v].weaknesses[79], "Content_History")
                page = FILES[v]["weaknesses/CWE-79.md"]
                headings = [h for h, _ in h2_sections(page)]
                self.assertEqual(headings[-1], "Content History", f"{v}: {headings}")
                self.assertEqual(headings.count("Content History"), 1, headings)
                tail = page.split("\n## Content History\n", 1)[1]
                self.assertTrue(tail.endswith("\n\n" + footer(v)), f"{v}: not directly above the footer")
                section = history_section(page)
                subs = cx.children(ch, "Submission")
                names = [x for s in subs for x in cx.children(s, "Submission_Name")]
                orgs = [x for s in subs for x in cx.children(s, "Submission_Organization")]
                self.assertTrue(names, f"{v}: CWE-79 has no Submission_Name to look for")
                for x in names + orgs:
                    self.assertIn(ctm._esc(cx.text(x)), section, f"{v}: {cx.local(x.tag)}")
                mods = cx.children(ch, "Modification")
                self.assertGreater(len(mods), 10, v)
                rows = history_rows(section)
                self.assertEqual(
                    [r["Date"] for r in rows if r["Event"] == "Modification"],
                    [cx.text(cx.child(m, "Modification_Date")) for m in mods],
                    v,
                )

    def test_every_entry_page_ends_with_history(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                n = {}
                for folder, i, e in _entries(ED[v]):
                    ch = cx.child(e, "Content_History")
                    headings = [h for h, _ in h2_sections(FILES[v][f"{folder}/CWE-{i}.md"])]
                    if ch is not None and len(ch):
                        self.assertEqual(headings[-1:], ["Content History"], f"{v} {folder}/CWE-{i}")
                        n[folder] = n.get(folder, 0) + 1
                    else:
                        self.assertNotIn("Content History", headings, f"{v} {folder}/CWE-{i}")
                self.assertEqual(set(n), {"weaknesses", ED[v].group_dir, "views"}, n)
        self.assertIn("\n## Content History\n", FILES["4.19.1"]["categories/CWE-1210.md"])
        self.assertIn("\n## Content History\n", FILES["5.0"]["groupings/CWE-1210.md"])
        self.assertIn("\n## Content History\n", FILES["5.0"]["views/CWE-1000.md"])

    def test_every_history_value_in_its_row(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                n = 0
                for folder, i, e in _entries(ED[v]):
                    events = history_events(e)
                    if not events:
                        continue
                    where = f"{v} {folder}/CWE-{i}"
                    rows = history_rows(history_section(FILES[v][f"{folder}/CWE-{i}.md"]))
                    self.assertEqual(len(rows), len(events), where)
                    for ev, row in zip(events, rows):
                        kind = cx.local(ev.tag)
                        label = f"Contribution ({ev.get('Type')})" if kind == "Contribution" else kind
                        self.assertEqual(row["Event"], label, where)
                        self.assertEqual(row["Date"], cx.text(cx.child(ev, f"{kind}_Date")), where)
                        line = " | ".join(row.values())
                        for leaf in ev:
                            self.assertIn(ctm._esc(leaf.text or ""), line, f"{where} {cx.local(leaf.tag)}")
                        n += 1
                self.assertGreater(n, 16000, v)

    def test_previous_entry_names(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                n = versioned = 0
                for folder, i, e in _entries(ED[v]):
                    prev = cx.children(cx.child(e, "Content_History"), "Previous_Entry_Name")
                    if not prev:
                        continue
                    section = history_section(FILES[v][f"{folder}/CWE-{i}.md"])
                    self.assertIn("**Previous Entry Names:**", section)
                    items = [ln for ln in section.split("\n") if ln.startswith("- ")]
                    expect = []
                    for p in prev:
                        item = f"- {ctm._esc(p.text or '')} — {p.get('Date')}"
                        if p.get("Version"):
                            item += f", CWE {p.get('Version')}"
                            versioned += 1
                        expect.append(item)
                    self.assertEqual(items, expect, f"{v} CWE-{i}")
                    n += len(prev)
                self.assertGreater(n, 900, v)
                self.assertEqual(versioned, 4, v)
        section = history_section(FILES["5.0"]["weaknesses/CWE-113.md"])
        self.assertIn("- HTTP Response Splitting — 2008-04-11, CWE Draft 9\n", section)

    def test_two_submissions_both_shown(self):
        ed = ED["5.0"]
        found = [(folder, i, e) for folder, i, e in _entries(ed)
                 if len(cx.children(cx.child(e, "Content_History"), "Submission")) > 1]
        self.assertEqual([i for _, i, _ in found], [1461])
        folder, i, e = found[0]
        subs = cx.children(cx.child(e, "Content_History"), "Submission")
        self.assertEqual(len(subs), 2)
        rows = [r for r in history_rows(history_section(FILES["5.0"][f"{folder}/CWE-{i}.md"]))
                if r["Event"] == "Submission"]
        self.assertEqual(len(rows), 2)
        for s, row in zip(subs, rows):
            self.assertEqual(row["Name"], "<br>".join(
                ctm._esc(cx.text(x)) for x in cx.children(s, "Submission_Name")))
            self.assertEqual(row["Organization"], ctm._esc(cx.text(cx.child(s, "Submission_Organization"))))
            self.assertEqual(row["Date"], cx.text(cx.child(s, "Submission_Date")))
        self.assertNotEqual(rows[0]["Name"], rows[1]["Name"])
        for v in VERSIONS:
            if v != "5.0":
                with self.subTest(edition=v):
                    for folder, i, e in _entries(ED[v]):
                        self.assertEqual(len(cx.children(cx.child(e, "Content_History"), "Submission")), 1)

    def test_repeated_names_all_shown(self):
        # Schema 8 lets Submission_Name and Contribution_Name repeat.
        multi = []
        for folder, i, e in _entries(ED["5.0"]):
            for ev in history_events(e):
                names = cx.children(ev, cx.local(ev.tag) + "_Name")
                if len(names) > 1:
                    multi.append((folder, i, ev, names))
        self.assertEqual({cx.local(ev.tag) for _, _, ev, _ in multi}, {"Submission", "Contribution"})
        for folder, i, ev, names in multi:
            rows = history_rows(history_section(FILES["5.0"][f"{folder}/CWE-{i}.md"]))
            want = "<br>".join(ctm._esc(cx.text(x)) for x in names)
            self.assertIn(want, [r["Name"] for r in rows], f"CWE-{i}")

    def test_multiline_comment_collapses_into_one_cell(self):
        section = history_section(FILES["5.0"]["weaknesses/CWE-1461.md"])
        self.assertIn(
            "| Participated in a series of meetings betwee March 2026 and September 26, in which "
            "members contributed significant feedback related to this entry as it evolved before "
            "publication in CWE 5.0. |",
            section,
        )

    def test_history_cells_escaped(self):
        ed = ED["5.0"]
        w = copy.deepcopy(ed.weaknesses[79])
        mod = cx.child(cx.child(w, "Content_History"), "Modification")
        cx.child(mod, "Modification_Comment").text = "a | b *c*\n\t\tnext <tag>"
        rows = history_rows(history_section(ctm.render_weakness(ed, w)))
        self.assertEqual(len(rows), len(history_events(w)))
        first = next(r for r in rows if r["Event"] == "Modification")
        self.assertEqual(first["Comment"], "a \\| b \\*c\\* next &lt;tag>")

    def test_no_page_says_history_omitted(self):
        for v in VERSIONS:
            with self.subTest(edition=v):
                for path, page in FILES[v].items():
                    found = re.search(r"(?i)content history is omitted|\*\*Omitted:\*\*", page)
                    self.assertIsNone(found, f"{v} {path}")

    def test_unknown_or_repeated_history_markup_fails(self):
        ed = ED["5.0"]
        ns = ed.weaknesses[79].tag[: ed.weaknesses[79].tag.index("}") + 1]

        def history(elem):
            return cx.child(elem, "Content_History")

        def fails(pattern, mutate, render=ctm.render_weakness, elem=ed.weaknesses[79]):
            e = copy.deepcopy(elem)
            mutate(e)
            with self.assertRaisesRegex(ctm.UnexpectedMarkupError, pattern):
                render(ed, e)

        fails(r"CWE-79.*Content_History.*<Review>",
              lambda e: ET.SubElement(history(e), ns + "Review"))
        fails(r"CWE-79.*<Modification_Reviewer>",
              lambda e: ET.SubElement(cx.child(history(e), "Modification"), ns + "Modification_Reviewer"))
        fails(r"CWE-79.*Status=",
              lambda e: cx.child(history(e), "Submission").set("Status", "x"))
        fails(r"CWE-79.*Reason=",
              lambda e: cx.child(history(e), "Previous_Entry_Name").set("Reason", "x"))
        fails(r"CWE-79.*Previous_Entry_Name.*markup",
              lambda e: ET.SubElement(cx.child(history(e), "Previous_Entry_Name"),
                                      "{http://www.w3.org/1999/xhtml}b"))
        fails(r"CWE-79.*Modification_Comment.*attributes",
              lambda e: cx.child(cx.child(history(e), "Modification"), "Modification_Comment").set("x", "y"))
        fails(r"CWE-79.*<Modification_Date> appears 2 times",
              lambda e: ET.SubElement(cx.child(history(e), "Modification"), ns + "Modification_Date"))
        fails(r"CWE-79.*<Submission_Organization> appears 2 times",  # CWE-79 has none; add two
              lambda e: [ET.SubElement(cx.child(history(e), "Submission"), ns + "Submission_Organization")
                         for _ in range(2)])
        fails(r"CWE-79.*<Modification_Name> appears 2 times",
              lambda e: ET.SubElement(cx.child(history(e), "Modification"), ns + "Modification_Name"))
        fails(r"CWE-79.*<Content_History> appears 2 times",
              lambda e: e.append(copy.deepcopy(history(e))))
        fails(r"CWE-1210.*<Review>", lambda e: ET.SubElement(history(e), ns + "Review"),
              ctm.render_group, ed.groups[1210])
        fails(r"CWE-1000.*<Review>", lambda e: ET.SubElement(history(e), ns + "Review"),
              ctm.render_view, ed.views[1000])
        fails(r"CWE-629.*<Review>", lambda e: ET.SubElement(history(e), ns + "Review"),
              ctm.render_view, ed.views[629])

    def test_xhtml_inside_history_containers_fails(self):
        # _check skips XHTML children (structured text checks them), but no Content_History
        # container holds structured text, so XHTML there must fail, not vanish.
        ed = ED["5.0"]
        xhtml = "{http://www.w3.org/1999/xhtml}p"
        cases = [
            (ctm.render_weakness, ed.weaknesses[79], lambda ch: ch, r"CWE-79/Content_History"),
            (ctm.render_weakness, ed.weaknesses[79], lambda ch: cx.child(ch, "Submission"),
             r"CWE-79/Content_History/Submission\[1\]"),
            (ctm.render_weakness, ed.weaknesses[79], lambda ch: cx.children(ch, "Modification")[2],
             r"CWE-79/Content_History/Modification\[3\]"),
            (ctm.render_weakness, ed.weaknesses[79], lambda ch: cx.child(ch, "Contribution"),
             r"CWE-79/Content_History/Contribution\[1\]"),
            (ctm.render_group, ed.groups[1210], lambda ch: ch, r"CWE-1210/Content_History"),
            (ctm.render_view, ed.views[629], lambda ch: ch, r"CWE-629/Content_History"),
        ]
        for render, elem, target, where in cases:
            with self.subTest(where=where):
                e = copy.deepcopy(elem)
                ET.SubElement(target(cx.child(e, "Content_History")), xhtml).text = "lost text"
                with self.assertRaisesRegex(ctm.UnexpectedMarkupError, where + r".*xhtml:p"):
                    render(ed, e)


if __name__ == "__main__":
    unittest.main()
