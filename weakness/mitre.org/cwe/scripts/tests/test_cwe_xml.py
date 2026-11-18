"""Tests for cwe_xml (edition loader, view outlines, implicit views)."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import cwe_xml as cx  # noqa: E402

CWE_DIR = SCRIPTS_DIR.parent
_CACHE = {}


def edition(version):
    if version not in _CACHE:
        _CACHE[version] = cx.load_edition(CWE_DIR / version, version)
    return _CACHE[version]


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.children)


def graph_views(ed):
    return [i for i, v in sorted(ed.views.items()) if v.get("Type") == "Graph"]


class LoadTests(unittest.TestCase):
    def test_load_counts(self):
        ed = edition("4.19.1")
        self.assertEqual(
            (len(ed.weaknesses), len(ed.groups), len(ed.views), len(ed.references)),
            (969, 420, 58, 1012),
        )
        self.assertEqual((ed.group_term, ed.group_dir, ed.schema_major), ("Category", "categories", 7))
        ed = edition("5.0")
        self.assertEqual(
            (len(ed.weaknesses), len(ed.groups), len(ed.views), len(ed.references)),
            (984, 431, 62, 1081),
        )
        self.assertEqual((ed.group_term, ed.group_dir, ed.schema_major), ("Grouping", "groupings", 8))

    def _copy(self, tmp, version):
        src = CWE_DIR / version
        name = f"cwec_v{version}.xml.zip"
        shutil.copyfile(src / name, Path(tmp) / name)
        side = Path(tmp) / f"{name}-file-metadata.json"
        shutil.copyfile(src / f"{name}-file-metadata.json", side)
        return side

    def test_sha_mismatch_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            side = self._copy(tmp, "5.0")
            data = json.loads(side.read_text())
            data["sha256"] = "0" * 64
            side.write_text(json.dumps(data))
            with self.assertRaises(cx.SourceVerificationError):
                cx.load_edition(Path(tmp), "5.0")

    def test_version_mismatch_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._copy(tmp, "5.0")
            with self.assertRaises(cx.SourceVerificationError):
                cx.load_edition(Path(tmp), "9.9")

    def test_entry_helpers(self):
        ed = edition("5.0")
        self.assertEqual(cx.entry_kind(ed, 79), "weakness")
        self.assertEqual(cx.entry_kind(ed, 1006), "grouping")
        self.assertEqual(cx.entry_kind(ed, 1000), "view")
        self.assertIsNone(cx.entry_kind(ed, 999999))
        self.assertEqual(cx.entry_path(ed, 79), "weaknesses/CWE-79.md")
        self.assertEqual(cx.entry_path(ed, 1006), "groupings/CWE-1006.md")
        self.assertEqual(cx.entry_path(ed, 1000), "views/CWE-1000.md")
        self.assertEqual(cx.entry_path(edition("4.19.1"), 16), "categories/CWE-16.md")
        self.assertTrue(cx.entry_name(ed, 79))


class OutlineTests(unittest.TestCase):
    def test_outline_expands_each_entry_once(self):
        for version, n_active, n_roots, orphans in (
            ("4.19.1", 944, 10, []),
            # In 5.0, 378 and 379 are children only of deprecated CWE-377,
            # which has no parent in view 1000, so no root reaches them.
            ("5.0", 956, 10, [378, 379]),
        ):
            ed = edition(version)
            for vid in graph_views(ed):
                nodes = list(walk(cx.view_outline(ed, vid)))
                exp = [n.cwe_id for n in nodes if n.expanded]
                self.assertEqual(len(exp), len(set(exp)), (version, vid))
                for n in nodes:
                    if not n.expanded:
                        self.assertEqual(n.children, ())
                        self.assertIn(n.cwe_id, exp, (version, vid))
            roots = cx.view_outline(ed, 1000)
            self.assertEqual(len(roots), n_roots)
            exp = {n.cwe_id for n in walk(roots) if n.expanded}
            active = {
                i for i, w in ed.weaknesses.items() if w.get("Status") != "Deprecated"
            }
            self.assertEqual(len(active), n_active)
            self.assertEqual(cx.unreachable_in_view(ed, 1000), orphans)
            self.assertEqual(exp | set(orphans), active)
            self.assertFalse(exp & set(orphans))
            for r in roots:
                self.assertEqual(ed.weaknesses[r.cwe_id].get("Abstraction"), "Pillar")

    def test_view_699_roots_are_groups(self):
        ed = edition("4.19.1")
        roots = cx.view_outline(ed, 699)
        self.assertEqual(len(roots), 40)
        for r in roots:
            self.assertEqual(cx.entry_kind(ed, r.cwe_id), "category")

    def test_outline_is_deterministic(self):
        ed = edition("5.0")
        self.assertEqual(cx.view_outline(ed, 1000), cx.view_outline(ed, 1000))
        for n in walk(cx.view_outline(ed, 1000)):
            ids = [c.cwe_id for c in n.children]
            self.assertEqual(ids, sorted(ids))


class ImplicitTests(unittest.TestCase):
    def test_implicit_658_is_c(self):
        ed = edition("4.19.1")
        members = cx.implicit_members(ed, 658)
        self.assertTrue(members)
        self.assertEqual(members, sorted(members))
        for i in members:
            langs = [
                a.get("Name")
                for p in cx.children(cx.child(ed.weaknesses[i], "Applicable_Platforms"), "Language")
                for a in [p]
            ]
            self.assertIn("C", langs)

    def test_implicit_604_is_deprecated(self):
        for version in ("4.19.1", "5.0"):
            ed = edition(version)
            expected = sorted(
                i
                for d in (ed.weaknesses, ed.groups, ed.views)
                for i, e in d.items()
                if e.get("Status") == "Deprecated"
            )
            self.assertEqual(cx.implicit_members(ed, 604), expected)

    def test_all_active_implicit_filters_known(self):
        for version in ("4.19.1", "5.0"):
            ed = edition(version)
            for vid, v in ed.views.items():
                if v.get("Type") != "Implicit":
                    continue
                flt = cx.text(cx.child(v, "Filter"))
                if flt == "/Weakness_Catalog[false()]":
                    continue
                self.assertIsNotNone(cx.implicit_members(ed, vid), (version, vid))

    def test_unknown_filter_returns_none(self):
        ed = edition("4.19.1")
        flt = cx.child(ed.views[658], "Filter")
        original = flt.text
        try:
            flt.text = original + " [altered]"
            self.assertIsNone(cx.implicit_members(ed, 658))
        finally:
            flt.text = original
        self.assertTrue(cx.implicit_members(ed, 658))


if __name__ == "__main__":
    unittest.main()
