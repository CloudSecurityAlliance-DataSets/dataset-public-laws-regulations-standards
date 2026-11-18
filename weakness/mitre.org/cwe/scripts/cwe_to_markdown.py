"""Render one MITRE CWE edition as markdown.

    python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0
    python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0 --check

The edition directory is this script's ``../<version>``. Its ``cwec_v<version>.xml.zip``
must match the SHA-256 in the committed sidecar (see ``cwe_xml.load_edition``). The run
rewrites ``<edition>/markdown/`` completely: ``index.md``, ``LICENSE.txt`` (a copy of the
edition's), ``weaknesses/CWE-<id>.md``, ``categories/`` (schema 7) or ``groupings/``
(schema 8) and ``views/``. Files it no longer produces are deleted. ``--check`` renders in
memory and exits 1, listing every file that differs, is missing or is extra.

Layout and wording follow docs/superpowers/specs/2026-11-18-cwe-markdown-design.md.
MITRE's Content_History (people's names) is never read. An element or attribute this
script does not know fails the run with the CWE ID, so nothing is dropped silently.
Output is UTF-8 with LF line endings, has no timestamps or local paths, and lists files
in numeric ID order. Python 3.10+ standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin
from xml.etree.ElementTree import Element

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:  # also works under python3 -I
    sys.path.insert(0, str(SCRIPTS_DIR))

import cwe_structured_text as st  # noqa: E402
import cwe_xml as cx  # noqa: E402
from cwe_xml import Edition, child, children, local  # noqa: E402

SCRIPT_REL = "weakness/mitre.org/cwe/scripts/cwe_to_markdown.py"
LICENSE_BASE = (
    "https://github.com/CloudSecurityAlliance-DataSets/"
    "dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe"
)
TERMS_URL = "https://cwe.mitre.org/about/termsofuse.html"
MITRE_SITE = "https://cwe.mitre.org/"
DEFINITION_URL = "https://cwe.mitre.org/data/definitions/{}.html"
XML_URL = "https://cwe.mitre.org/data/xml/{}"
CAPEC_URL = "https://capec.mitre.org/data/definitions/{}.html"
ATTRIBUTION = (
    "Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation."
)
XHTML_NS = "{http://www.w3.org/1999/xhtml}"
SEP = " · "

INACTIVE = ("Deprecated", "Obsolete")
ABSTRACTION_ORDER = ("Pillar", "Class", "Base", "Variant", "Compound")
STATUS_ORDER = ("Stable", "Usable", "Draft", "Incomplete", "Obsolete", "Deprecated")


class UnexpectedMarkupError(ValueError):
    """The XML holds an element or attribute this script does not render."""


# ------------------------------------------------------------------ helpers


def _check(elem: Element, ctx: str, kids: tuple[str, ...] = (), attrs: tuple[str, ...] = ()) -> None:
    """Fail on any child element or attribute of ``elem`` not listed (XHTML is skipped:
    the structured-text converter checks it)."""
    for c in elem:
        if not isinstance(c.tag, str) or c.tag.startswith(XHTML_NS):
            continue
        if local(c.tag) not in kids:
            raise UnexpectedMarkupError(f"{ctx}: unexpected element <{local(c.tag)}>")
    for a in elem.attrib:
        if local(a) not in attrs:
            raise UnexpectedMarkupError(f"{ctx}: unexpected attribute {local(a)}= on <{local(elem.tag)}>")


def _leaf(elem: Element | None, ctx: str) -> str:
    """Whitespace-collapsed text of an element that must hold text only."""
    if elem is None:
        return ""
    for c in elem:
        if isinstance(c.tag, str):
            raise UnexpectedMarkupError(f"{ctx}/{local(elem.tag)}: unexpected markup <{local(c.tag)}>")
    if elem.attrib:
        raise UnexpectedMarkupError(f"{ctx}/{local(elem.tag)}: unexpected attributes {sorted(elem.attrib)}")
    return " ".join((elem.text or "").split())


def _leaves(parent: Element | None, name: str, ctx: str) -> list[str]:
    return [_leaf(e, ctx) for e in children(parent, name)]


def _esc(s: str) -> str:
    """Escape one line of prose (whitespace collapsed); ``|`` too, so it is table-safe."""
    return st.escape_inline(" ".join(s.split()), at_line_start=False).replace("|", "\\|")


def _md(elem: Element | None, ctx: str) -> str:
    """Structured text (or plain text) as markdown blocks."""
    if elem is None:
        return ""
    return st.structured_text_to_md(elem, f"{ctx}/{local(elem.tag)}")


def _cell_md(elem: Element | None, ctx: str) -> str:
    """Structured text squeezed into one table cell (blocks and breaks become <br>)."""
    md = _md(elem, ctx)
    return st.escape_table_cell(re.sub(r"\\\n", "\n", md)) if md else ""


def _table(header: list[str], rows: list[list[str]]) -> str:
    """A markdown table; columns empty in every row (except the first) are left out."""
    keep = [i for i in range(len(header)) if i == 0 or any(r[i] for r in rows)]
    out = ["| " + " | ".join(header[i] for i in keep) + " |",
           "| " + " | ".join("---" for _ in keep) + " |"]
    out += ["| " + " | ".join(r[i] for i in keep) + " |" for r in rows]
    return "\n".join(out)


def _indent(text: str, pad: str) -> str:
    return "\n".join(pad + ln if ln else "" for ln in text.split("\n"))


def _is_single_paragraph(md: str) -> bool:
    return bool(md) and "\n\n" not in md and not re.match(r"(- |\d+\. |\| )", md)


def _item(label: str, body: str = "") -> str:
    """One list item: a label, then a body. A one-paragraph body follows a label that ends
    with a colon on its line; anything else goes below the label, indented to the item."""
    if not body:
        return f"- {label}"
    if not label:
        return "- " + _indent(body, "  ")[2:]
    if _is_single_paragraph(body) and label.rstrip("*").endswith(":"):
        return _indent(f"- {label} {body}", "  ")[2:]
    return f"- {label}\n\n{_indent(body, '  ')}"


def _join_items(items: list[str]) -> str:
    """List items, one per line; a blank line between them if any spans several blocks."""
    return ("\n\n" if any("\n\n" in i for i in items) else "\n").join(items)


def _labelled(label: str, md: str) -> str:
    """``**Label:** text`` for one paragraph; the label above the blocks otherwise."""
    if not md:
        return ""
    if _is_single_paragraph(md):
        return f"**{label}:** {md}"
    return f"**{label}:**\n\n{md}"


def _yaml(s: str) -> str:
    """A YAML scalar: plain for simple enumeration words, double-quoted otherwise."""
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", s):
        return s
    return json.dumps(s, ensure_ascii=False)


def _autolink(url: str) -> str:
    url = url.strip()
    if not re.match(r"https?://", url):
        return _esc(url)
    return "<" + url.replace(" ", "%20").replace("<", "%3C").replace(">", "%3E") + ">"


def _link(text: str, url: str) -> str:
    text = text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    if re.search(r"[\s()<>]", url):
        url = "<" + url.replace(" ", "%20").replace("<", "%3C").replace(">", "%3E") + ">"
    return f"[{text}]({url})"


def _plural(n: int, word: str) -> str:
    if n == 1:
        return f"1 {word}"
    if word == "weakness":
        return f"{n} weaknesses"
    if word == "category":
        return f"{n} categories"
    return f"{n} {word}s"


# ------------------------------------------------------------ entry links


def _entry(ed: Edition, cwe_id: int) -> Element | None:
    for table in (ed.weaknesses, ed.groups, ed.views):
        if cwe_id in table:
            return table[cwe_id]
    return None


def cwe_link(ed: Edition, cwe_id: int, base: str = "../") -> str:
    """``[CWE-n](<base><folder>/CWE-n.md)``, or plain ``CWE-n`` if not in the edition."""
    path = cx.entry_path(ed, cwe_id)
    return f"CWE-{cwe_id}" if path is None else f"[CWE-{cwe_id}]({base}{path})"


def _kind_label(ed: Edition, cwe_id: int) -> str:
    e = _entry(ed, cwe_id)
    kind = cx.entry_kind(ed, cwe_id)
    if kind == "weakness":
        label = e.get("Abstraction") or "Weakness"
    elif kind == "view":
        label = "View"
    else:
        label = ed.group_term
    if e.get("Status") in INACTIVE:
        label += f", {e.get('Status')}"
    return label


def entry_line(ed: Edition, cwe_id: int, base: str = "../") -> str:
    """``[CWE-79](../weaknesses/CWE-79.md) Name (Base)``; plain text when the ID is absent."""
    e = _entry(ed, cwe_id)
    if e is None:
        return f"CWE-{cwe_id} (not in CWE {ed.version})"
    return f"{cwe_link(ed, cwe_id, base)} {_esc(e.get('Name') or '')} ({_kind_label(ed, cwe_id)})"


# ---------------------------------------------------------------- pages


def footer(ed: Edition) -> str:
    v = ed.version
    return (
        "---\n"
        f"Generated from MITRE's CWE {v} XML (cwec_v{v}.xml) by {SCRIPT_REL}. "
        "Content history is omitted.\n"
        f"{ATTRIBUTION}\n"
        f"Used under the CWE Terms of Use: {TERMS_URL} "
        f"(full text: {LICENSE_BASE}/{v}/LICENSE.txt).\n"
    )


def _front_matter(ed: Edition, e: Element, kind: str) -> list[str]:
    i = int(e.get("ID"))
    fm = [
        f'secid: "secid:weakness/mitre.org/cwe@{ed.version}#CWE-{i}"',
        f'cwe_id: "CWE-{i}"',
        f"entry_type: {kind}",
        f"name: {json.dumps(e.get('Name') or '', ensure_ascii=False)}",
    ]
    if kind == "weakness":
        fm += [f"abstraction: {_yaml(e.get('Abstraction'))}", f"structure: {_yaml(e.get('Structure'))}"]
    if kind == "view":
        fm.append(f"view_type: {_yaml(e.get('Type'))}")
    fm.append(f"status: {_yaml(e.get('Status'))}")
    usage = " ".join(cx.text(child(child(e, "Mapping_Notes"), "Usage")).split())
    if usage:
        fm.append(f"mapping_usage: {_yaml(usage)}")
    fm += [
        f"cwe_version: {json.dumps(ed.version)}",
        f"cwe_release_date: {json.dumps(ed.date)}",
        f'upstream: "{DEFINITION_URL.format(i)}"',
    ]
    return fm


def _page(ed: Edition, front: list[str], title: str, sections: list[tuple[str | None, str]]) -> str:
    out = ["---", *front, "---", "", f"# {title}", ""]
    for heading, body in sections:
        if not body or not body.strip():
            continue
        if heading:
            out += [f"## {heading}", ""]
        out += [body.strip("\n"), ""]
    return "\n".join(out) + "\n" + footer(ed)


def _banner(e: Element, what: str) -> str:
    status = e.get("Status")
    if status == "Deprecated":
        pointer = "" if what == "view" else " The sections below may name a replacement."
        return (f"> **Deprecated.** MITRE has deprecated this {what} and keeps it for "
                f"reference only.{pointer}")
    if status == "Obsolete":
        return f"> **Obsolete.** MITRE marks this {what} as obsolete: kept for reference, no longer maintained."
    return ""


# ------------------------------------------------- shared entry sections


def _reference(ed: Edition, ref_id: str, section: str, ctx: str) -> str:
    r = ed.references.get(ref_id)
    if r is None:
        return f"[{ref_id}] (not in this edition's external references)" + (
            f". {_esc(section)}" if section else ""
        )
    c = f"{ctx}/{ref_id}"
    _check(r, c, kids=("Author", "Title", "Edition", "Publication", "Publisher",
                       "Publication_Year", "Publication_Month", "Publication_Day",
                       "URL", "URL_Date", "Alt_URL", "Alt_URL_Date",
                       "Access_Restrictions", "Media_Type", "Rationale"),
           attrs=("Reference_ID",))
    one = lambda name: _leaf(child(r, name), c)  # noqa: E731
    authors = [_esc(a) for a in _leaves(r, "Author", c)]
    parts = []
    if authors:
        parts.append(authors[0] if len(authors) == 1 else ", ".join(authors[:-1]) + " and " + authors[-1])
    if one("Title"):
        parts.append(f'"{_esc(one("Title"))}"')
    if section:
        parts.append(_esc(section))
    for name in ("Edition", "Publication", "Publisher"):
        if one(name):
            parts.append(_esc(one(name)))
    # XSD gYear / gMonth ("--03") / gDay ("---26") -> 2013-03-26
    date = "-".join(x for x in (one("Publication_Year"), one("Publication_Month").lstrip("-"),
                                one("Publication_Day").lstrip("-")) if x)
    if date:
        parts.append(_esc(date))
    for url_el, date_el, label in (("URL", "URL_Date", ""), ("Alt_URL", "Alt_URL_Date", "Alternate URL: ")):
        if one(url_el):
            s = label + _autolink(one(url_el))
            if one(date_el):
                s += f" (URL validated: {_esc(one(date_el))})"
            parts.append(s)
    if one("Access_Restrictions"):
        parts.append(f"Access restrictions: {_esc(one('Access_Restrictions'))}")
    if one("Media_Type"):
        parts.append(f"Media type: {_esc(one('Media_Type'))}")
    rationale = _leaves(r, "Rationale", c)
    if rationale:
        parts.append("Rationale: " + "; ".join(_esc(x) for x in rationale))
    text = f"[{ref_id}]"
    for p in parts:
        text += (" " if text.endswith(".") or text == f"[{ref_id}]" else ". ") + p
    return text if text.endswith(".") else text + "."


def _references(ed: Edition, refs: Element | None, ctx: str) -> str:
    if refs is None:
        return ""
    _check(refs, ctx, kids=("Reference",))
    items = []
    for ref in children(refs, "Reference"):
        _check(ref, ctx, attrs=("External_Reference_ID", "Section"))
        items.append("- " + _reference(ed, ref.get("External_Reference_ID"), ref.get("Section") or "", ctx))
    return _join_items(items)


def _taxonomy_mappings(tm: Element | None, ctx: str) -> str:
    if tm is None:
        return ""
    _check(tm, ctx, kids=("Taxonomy_Mapping",))
    rows = []
    for m in children(tm, "Taxonomy_Mapping"):
        _check(m, ctx, kids=("Entry_ID", "Entry_Name", "Mapping_Fit"), attrs=("Taxonomy_Name",))
        rows.append([
            _esc(m.get("Taxonomy_Name") or ""),
            _esc(_leaf(child(m, "Entry_ID"), ctx)),
            _esc(_leaf(child(m, "Entry_Name"), ctx)),
            _esc(_leaf(child(m, "Mapping_Fit"), ctx)),
        ])
    return _table(["Taxonomy", "Entry ID", "Entry Name", "Mapping Fit"], rows) if rows else ""


def _mapping_notes(ed: Edition, mn: Element | None, ctx: str) -> str:
    if mn is None:
        return ""
    c = f"{ctx}/Mapping_Notes"
    _check(mn, c, kids=("Usage", "Rationale", "Comments", "Reasons", "Suggestions"))
    items = []
    usage = _leaf(child(mn, "Usage"), c)
    if usage:
        items.append(_item("**Usage:**", _esc(usage)))
    for name in ("Rationale", "Comments"):
        body = _md(child(mn, name), c)
        if body:
            items.append(_item(f"**{name}:**", body))
    reasons = child(mn, "Reasons")
    if reasons is not None:
        _check(reasons, c, kids=("Reason",))
        types = []
        for r in children(reasons, "Reason"):
            _check(r, c, attrs=("Type",))
            types.append(_esc(r.get("Type") or ""))
        if types:
            items.append(_item("**Reasons:**", ", ".join(types)))
    sugg = child(mn, "Suggestions")
    if sugg is not None:
        _check(sugg, c, kids=("Suggestion",))
        lines = []
        for s in children(sugg, "Suggestion"):
            _check(s, c, attrs=("CWE_ID", "Comment"))
            sid = int(s.get("CWE_ID"))
            line = "- " + entry_line(ed, sid)
            comment = " ".join((s.get("Comment") or "").split())
            if comment and comment != cx.entry_name(ed, sid):
                line += f": {_esc(comment)}"
            lines.append(line)
        if lines:
            items.append(_item("**Suggestions:**", "\n".join(lines)))
    return _join_items(items)


def _notes(notes: Element | None, ctx: str) -> str:
    if notes is None:
        return ""
    _check(notes, ctx, kids=("Note",))
    items = []
    for n in children(notes, "Note"):
        _check(n, ctx, attrs=("Type", "Version", "ReleaseDate"))
        label = f"**{_esc(n.get('Type') or 'Note')}**"
        stamp = ", ".join(x for x in (
            f"CWE {n.get('Version')}" if n.get("Version") else "", n.get("ReleaseDate") or "") if x)
        if stamp:
            label += f" ({_esc(stamp)})"
        items.append(_item(label + ":", _md(n, ctx)))
    return "\n\n".join(items)


# ------------------------------------------------------- weakness sections


def _phases(parent: Element, ctx: str) -> str:
    out = [_esc(p) for p in _leaves(parent, "Phase", ctx)]
    for cp in children(parent, "Custom_Phase"):
        _check(cp, ctx, attrs=("Domain",))
        if len(cp):
            raise UnexpectedMarkupError(f"{ctx}/Custom_Phase: unexpected markup")
        out.append(f"{_esc(cp.text or '')} ({_esc(cp.get('Domain') or '')})")
    return "; ".join(out)


def _alternate_terms(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Alternate_Term",))
    items = []
    for t in children(e, "Alternate_Term"):
        _check(t, ctx, kids=("Term", "Role", "Description"))
        label = f"**{_esc(_leaf(child(t, 'Term'), ctx))}**"
        roles = _leaves(t, "Role", ctx)
        if roles:
            label += f" ({', '.join(_esc(r) for r in roles)})"
        body = _md(child(t, "Description"), ctx)
        items.append(_item(label + (":" if body else ""), body))
    return _join_items(items)


def _dims(parent: Element | None, ctx: str) -> list[tuple[str, str]]:
    if parent is None:
        return []
    _check(parent, ctx, kids=("Dimension",))
    out = []
    for d in children(parent, "Dimension"):
        _check(d, ctx, attrs=("Type",))
        if len(d):
            raise UnexpectedMarkupError(f"{ctx}/Dimension: unexpected markup")
        out.append((d.get("Type") or "", " ".join((d.text or "").split())))
    return out


def _related_weaknesses(ed: Edition, e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Related_Weakness",))
    rows = []
    for r in children(e, "Related_Weakness"):
        _check(r, ctx, kids=("Dimensions",), attrs=("Nature", "CWE_ID", "View_ID", "Ordinal", "Chain_ID"))
        dims = _dims(child(r, "Dimensions"), ctx)
        rows.append([
            _esc(r.get("Nature") or ""),
            entry_line(ed, int(r.get("CWE_ID"))),
            cwe_link(ed, int(r.get("View_ID"))),
            _esc(r.get("Ordinal") or ""),
            _esc(r.get("Chain_ID") or ""),
            "; ".join(f"{_esc(t)}: {_esc(v)}" for t, v in dims),
        ])
    return _table(["Nature", "Entry", "View", "Ordinal", "Chain", "Dimensions"], rows) if rows else ""


def _ordinalities(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Weakness_Ordinality",))
    items = []
    for o in children(e, "Weakness_Ordinality"):
        _check(o, ctx, kids=("Ordinality", "Description"))
        desc = _md(child(o, "Description"), ctx)
        label = f"**{_esc(_leaf(child(o, 'Ordinality'), ctx))}**"
        items.append(_item(label + (":" if desc else ""), desc))
    return _join_items(items)


def _platforms(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    kinds = ("Language", "Operating_System", "Architecture", "Technology")
    _check(e, ctx, kids=kinds)
    rows = []
    for p in e:
        if not isinstance(p.tag, str) or p.tag.startswith(XHTML_NS):
            continue
        _check(p, ctx, kids=("Note",), attrs=("Name", "Class", "Prevalence"))
        rows.append([
            local(p.tag).replace("_", " "),
            _esc(p.get("Name") or ""),
            _esc(p.get("Class") or ""),
            _esc(p.get("Prevalence") or ""),
            "<br>".join(_cell_md(n, ctx) for n in children(p, "Note")),
        ])
    return _table(["Type", "Name", "Class", "Prevalence", "Note"], rows) if rows else ""


def _structured_list(e: Element | None, item: str, ctx: str) -> str:
    """Each ``item`` child as structured text, blocks separated by a blank line."""
    if e is None:
        return ""
    _check(e, ctx, kids=(item,))
    return "\n\n".join(b for b in (_md(x, ctx) for x in children(e, item)) if b)


def _modes(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Introduction",))
    items = []
    for i in children(e, "Introduction"):
        _check(i, ctx, kids=("Phase", "Custom_Phase", "Note"))
        note = _md(child(i, "Note"), ctx)
        items.append(_item(f"**{_phases(i, ctx)}**" + (":" if note else ""), note))
    return _join_items(items)


def _consequences(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Consequence",))
    rows = []
    for c in children(e, "Consequence"):
        _check(c, ctx, kids=("Scope", "Impact", "Likelihood", "Note"), attrs=("Consequence_ID",))
        rows.append([
            "<br>".join(_esc(s) for s in _leaves(c, "Scope", ctx)),
            "<br>".join(_esc(s) for s in _leaves(c, "Impact", ctx)),
            "<br>".join(_esc(s) for s in _leaves(c, "Likelihood", ctx)),
            "<br><br>".join(_cell_md(n, ctx) for n in children(c, "Note")),
        ])
    return _table(["Scope", "Impact", "Likelihood", "Note"], rows) if rows else ""


def _effectiveness(e: Element, ctx: str) -> list[str]:
    out = []
    eff = _leaf(child(e, "Effectiveness"), ctx)
    if eff:
        out.append(f"**Effectiveness:** {_esc(eff)}")
    notes = _md(child(e, "Effectiveness_Notes"), ctx)
    if notes:
        out.append(_labelled("Effectiveness Notes", notes))
    return out


def _detection_methods(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Detection_Method",))
    items = []
    for d in children(e, "Detection_Method"):
        _check(d, ctx, kids=("Method", "Phase", "Custom_Phase", "Description", "Effectiveness",
                             "Effectiveness_Notes"), attrs=("Detection_Method_ID",))
        label = [f"**Method:** {_esc(_leaf(child(d, 'Method'), ctx))}"]
        phases = _phases(d, ctx)
        if phases:
            label.append(f"**Phase:** {phases}")
        if d.get("Detection_Method_ID"):
            label.append(f"**ID:** {_esc(d.get('Detection_Method_ID'))}")
        body = [b for b in [_md(child(d, "Description"), ctx), *_effectiveness(d, ctx)] if b]
        items.append(_item(SEP.join(label), "\n\n".join(body)))
    return "\n\n".join(items)


def _mitigations(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Mitigation",))
    items = []
    for m in children(e, "Mitigation"):
        _check(m, ctx, kids=("Phase", "Custom_Phase", "Strategy", "Description", "Effectiveness",
                             "Effectiveness_Notes"), attrs=("Mitigation_ID",))
        label = []
        phases = _phases(m, ctx)
        if phases:
            label.append(f"**Phase:** {phases}")
        strategy = _leaf(child(m, "Strategy"), ctx)
        if strategy:
            label.append(f"**Strategy:** {_esc(strategy)}")
        if m.get("Mitigation_ID"):
            label.append(f"**ID:** {_esc(m.get('Mitigation_ID'))}")
        body = [b for b in [_md(child(m, "Description"), ctx), *_effectiveness(m, ctx)] if b]
        items.append(_item(SEP.join(label), "\n\n".join(body)))
    return "\n\n".join(items)


def _demonstrative_examples(ed: Edition, e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Demonstrative_Example",))
    out = []
    for n, dx in enumerate(children(e, "Demonstrative_Example"), 1):
        c = f"{ctx}/Demonstrative_Example[{n}]"
        _check(dx, c, kids=("Title_Text", "Intro_Text", "Example_Code", "Body_Text", "References"),
               attrs=("Demonstrative_Example_ID",))
        title = f"### Example {n}"
        if dx.get("Demonstrative_Example_ID"):
            title += f" ({_esc(dx.get('Demonstrative_Example_ID'))})"
        blocks = [title]
        for part in dx:
            if not isinstance(part.tag, str):
                continue
            name = local(part.tag)
            if name == "Example_Code":
                _check(part, c, attrs=("Nature", "Language"))
                blocks.append(st.example_code_to_md(part, f"{c}/Example_Code"))
            elif name == "References":
                refs = _references(ed, part, c)
                if refs:
                    blocks.append("*References:*\n\n" + refs)
            elif name == "Title_Text":
                blocks.append(f"**{_esc(_leaf(part, c))}**")
            else:
                md = _md(part, c)
                if md:
                    blocks.append(md)
        out.append("\n\n".join(blocks))
    return "\n\n".join(out)


def _observed_examples(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Observed_Example",))
    rows = []
    for o in children(e, "Observed_Example"):
        _check(o, ctx, kids=("Reference", "Description", "Link", "Rationale"))
        ref = _leaf(child(o, "Reference"), ctx)
        link = _leaf(child(o, "Link"), ctx)
        rows.append([
            _link(ref, link) if link else _esc(ref),
            _cell_md(child(o, "Description"), ctx),
            _cell_md(child(o, "Rationale"), ctx),
        ])
    return _table(["Reference", "Description", "Rationale"], rows) if rows else ""


def _simple_list(e: Element | None, item: str, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=(item,))
    return "\n".join(f"- {_esc(x)}" for x in _leaves(e, item, ctx) if x)


def _dimensions(e: Element | None, ctx: str) -> str:
    return "\n".join(f"- **{_esc(t)}:** {_esc(v)}" for t, v in _dims(e, ctx))


def _attack_patterns(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Related_Attack_Pattern",))
    out = []
    for p in children(e, "Related_Attack_Pattern"):
        _check(p, ctx, attrs=("CAPEC_ID",))
        i = p.get("CAPEC_ID")
        out.append(f"- {_link(f'CAPEC-{i}', CAPEC_URL.format(i))}")
    return "\n".join(out)


WEAKNESS_CHILDREN = (
    "Description", "Extended_Description", "Alternate_Terms", "Related_Weaknesses",
    "Weakness_Ordinalities", "Applicable_Platforms", "Background_Details",
    "Modes_Of_Introduction", "Exploitation_Factors", "Likelihood_Of_Exploit",
    "Common_Consequences", "Detection_Methods", "Potential_Mitigations",
    "Demonstrative_Examples", "Observed_Examples", "Functional_Areas", "Affected_Resources",
    "Dimensions", "Technical_Nuance", "Taxonomy_Mappings", "Related_Attack_Patterns",
    "References", "Mapping_Notes", "Notes", "Content_History",
)


def render_weakness(ed: Edition, elem: Element) -> str:
    i = int(elem.get("ID"))
    ctx = f"CWE-{i}"
    _check(elem, ctx, kids=WEAKNESS_CHILDREN,
           attrs=("ID", "Name", "Abstraction", "Structure", "Status", "Diagram"))
    get = lambda name: child(elem, name)  # noqa: E731
    description = _md(get("Description"), ctx)
    if elem.get("Diagram"):
        image = urljoin(MITRE_SITE, elem.get("Diagram"))
        description += f"\n\n![Diagram for CWE-{i}]({image})"
    sections = [
        (None, _banner(elem, "entry")),
        ("Description", description),
        ("Extended Description", _md(get("Extended_Description"), ctx)),
        ("Alternate Terms", _alternate_terms(get("Alternate_Terms"), ctx)),
        ("Related Weaknesses", _related_weaknesses(ed, get("Related_Weaknesses"), ctx)),
        ("Weakness Ordinalities", _ordinalities(get("Weakness_Ordinalities"), ctx)),
        ("Applicable Platforms", _platforms(get("Applicable_Platforms"), ctx)),
        ("Background Details", _structured_list(get("Background_Details"), "Background_Detail", ctx)),
        ("Modes Of Introduction", _modes(get("Modes_Of_Introduction"), ctx)),
        ("Exploitation Factors", _structured_list(get("Exploitation_Factors"), "Exploitation_Factor", ctx)),
        ("Likelihood Of Exploit", _esc(_leaf(get("Likelihood_Of_Exploit"), ctx))),
        ("Common Consequences", _consequences(get("Common_Consequences"), ctx)),
        ("Detection Methods", _detection_methods(get("Detection_Methods"), ctx)),
        ("Potential Mitigations", _mitigations(get("Potential_Mitigations"), ctx)),
        ("Demonstrative Examples", _demonstrative_examples(ed, get("Demonstrative_Examples"), ctx)),
        ("Observed Examples", _observed_examples(get("Observed_Examples"), ctx)),
        ("Functional Areas", _simple_list(get("Functional_Areas"), "Functional_Area", ctx)),
        ("Affected Resources", _simple_list(get("Affected_Resources"), "Affected_Resource", ctx)),
        ("Dimensions", _dimensions(get("Dimensions"), ctx)),
        ("Technical Nuance", _md(get("Technical_Nuance"), ctx)),
        ("Taxonomy Mappings", _taxonomy_mappings(get("Taxonomy_Mappings"), ctx)),
        ("Related Attack Patterns", _attack_patterns(get("Related_Attack_Patterns"), ctx)),
        ("References", _references(ed, get("References"), ctx)),
        ("Mapping Notes", _mapping_notes(ed, get("Mapping_Notes"), ctx)),
        ("Notes", _notes(get("Notes"), ctx)),
    ]
    title = f"CWE-{i}: {_esc(elem.get('Name') or '')}"
    return _page(ed, _front_matter(ed, elem, "weakness"), title, sections)


# ------------------------------------------------------- category/grouping


def render_group(ed: Edition, elem: Element) -> str:
    i = int(elem.get("ID"))
    ctx = f"CWE-{i}"
    _check(elem, ctx, kids=("Summary", "Relationships", "Taxonomy_Mappings", "References",
                            "Mapping_Notes", "Notes", "Content_History"),
           attrs=("ID", "Name", "Status"))
    rels = child(elem, "Relationships")
    rows = []
    if rels is not None:
        _check(rels, ctx, kids=("Has_Member",))
        for m in children(rels, "Has_Member"):
            _check(m, ctx, attrs=("CWE_ID", "View_ID"))
            vid = int(m.get("View_ID"))
            view = ed.views.get(vid)
            view_cell = cwe_link(ed, vid) + (f" {_esc(view.get('Name') or '')}" if view is not None else "")
            rows.append([entry_line(ed, int(m.get("CWE_ID"))), view_cell])
    sections = [
        (None, _banner(elem, ed.group_term.lower())),
        ("Summary", _md(child(elem, "Summary"), ctx)),
        ("Members", _table(["Member", "View"], rows) if rows else ""),
        ("Taxonomy Mappings", _taxonomy_mappings(child(elem, "Taxonomy_Mappings"), ctx)),
        ("References", _references(ed, child(elem, "References"), ctx)),
        ("Mapping Notes", _mapping_notes(ed, child(elem, "Mapping_Notes"), ctx)),
        ("Notes", _notes(child(elem, "Notes"), ctx)),
    ]
    title = f"CWE-{i}: {_esc(elem.get('Name') or '')}"
    return _page(ed, _front_matter(ed, elem, ed.group_term.lower()), title, sections)


# ------------------------------------------------------------------ views


def _count_phrase(ed: Edition, ids) -> str:
    ids = set(ids)
    parts = []
    for word, table in (("weakness", ed.weaknesses), (ed.group_term.lower(), ed.groups),
                        ("view", ed.views)):
        n = sum(1 for i in ids if i in table)
        if n:
            parts.append(_plural(n, word))
    total = len(ids)
    if len(parts) > 1:
        return f"{total} ({', '.join(parts)})"
    return parts[0] if parts else "0"


def _walk(nodes):
    for n in nodes:
        yield n
        yield from _walk(n.children)


def _outline_md(ed: Edition, roots) -> str:
    where: dict[int, int | None] = {}

    def index(nodes, parent):
        for n in nodes:
            if n.expanded:
                where[n.cwe_id] = parent
                index(n.children, n.cwe_id)

    index(roots, None)
    lines: list[str] = []

    def emit(nodes, depth):
        for n in nodes:
            line = "  " * depth + "- " + entry_line(ed, n.cwe_id)
            if not n.expanded:
                p = where.get(n.cwe_id)
                line += " *(listed in full at the top level)*" if p is None else f" *(listed in full under CWE-{p})*"
            lines.append(line)
            if n.expanded:
                emit(n.children, depth + 1)

    emit(roots, 0)
    return "\n".join(lines)


def _stated_parents(ed: Edition, view_id: int, cwe_id: int) -> list[int]:
    """Parents of ``cwe_id`` in the view: ChildOf targets, or groups naming it a member."""
    vid = str(view_id)
    out = []
    w = ed.weaknesses.get(cwe_id)
    for r in children(child(w, "Related_Weaknesses"), "Related_Weakness"):
        if r.get("Nature") == "ChildOf" and r.get("View_ID") == vid:
            out.append(int(r.get("CWE_ID")))
    for gid, g in sorted(ed.groups.items()):
        for m in children(child(g, "Relationships"), "Has_Member"):
            if m.get("View_ID") == vid and int(m.get("CWE_ID")) == cwe_id:
                out.append(gid)
    return sorted(set(out))


def _audience(e: Element | None, ctx: str) -> str:
    if e is None:
        return ""
    _check(e, ctx, kids=("Stakeholder",))
    items = []
    for s in children(e, "Stakeholder"):
        _check(s, ctx, kids=("Type", "Description"))
        desc = _md(child(s, "Description"), ctx)
        label = f"**{_esc(_leaf(child(s, 'Type'), ctx))}**"
        items.append(_item(label + (":" if desc else ""), desc))
    return _join_items(items)


def render_view(ed: Edition, elem: Element) -> str:
    i = int(elem.get("ID"))
    ctx = f"CWE-{i}"
    _check(elem, ctx, kids=("Objective", "Audience", "Members", "Filter", "References",
                            "Mapping_Notes", "Notes", "Content_History"),
           attrs=("ID", "Name", "Type", "Status"))
    vtype, status = elem.get("Type") or "", elem.get("Status") or ""
    title = f"CWE-{i}: {_esc(elem.get('Name') or '')}"
    front = _front_matter(ed, elem, "view")
    objective = _md(child(elem, "Objective"), ctx)
    head = [f"**View type:** {_esc(vtype)}", f"**Status:** {_esc(status)}"]

    if status in INACTIVE:
        omitted = [label for name, label in (
            ("Audience", "audience"), ("Members", "members"), ("Filter", "filter"),
            ("References", "references"), ("Mapping_Notes", "mapping notes"), ("Notes", "notes"),
        ) if child(elem, name) is not None]
        note = _banner(elem, "view")
        if omitted:
            listed = omitted[0] if len(omitted) == 1 else ", ".join(omitted[:-1]) + " and " + omitted[-1]
            note += (f"\n>\n> Only the objective and status of an obsolete or deprecated view are "
                     f"rendered here. Not rendered from MITRE's XML for this view: {listed}. "
                     f"MITRE's page: <{DEFINITION_URL.format(i)}>")
        return _page(ed, front, title, [(None, SEP.join(head)), (None, note), ("Objective", objective)])

    members_md, extra = "", []
    filter_md = ""
    if vtype == "Graph":
        roots = cx.view_outline(ed, i)
        lost = cx.unreachable_in_view(ed, i)
        ids = {n.cwe_id for n in _walk(roots)} | set(lost)
        head.append(f"**Members:** {_count_phrase(ed, ids)}")
        members_md = _outline_md(ed, roots)
        if lost:
            lines = []
            for x in lost:
                parents = _stated_parents(ed, i, x)
                word = "parent" if len(parents) == 1 else "parents"
                lines.append(f"- {entry_line(ed, x)}; {word} in this view: "
                             + ", ".join(entry_line(ed, p) for p in parents))
            extra.append((
                "Not reachable from this view's roots",
                "These entries have a parent in this view, but no chain of parents leads to "
                "one of the view's top-level members, so the outline above cannot reach them.\n\n"
                + "\n".join(lines),
            ))
    elif vtype == "Explicit":
        ids = cx.explicit_members(ed, i)
        head.append(f"**Members:** {_count_phrase(ed, ids)}")
        members_md = "\n".join("- " + entry_line(ed, x) for x in ids)
    elif vtype == "Implicit":
        flt = " ".join(cx.text(child(elem, "Filter")).split())
        filter_md = st.fence(flt, "xpath") if flt else ""
        ids = cx.implicit_members(ed, i)
        if ids is None:
            print(f"warning: CWE {ed.version} view {i}: unknown filter {flt!r}; members not computed",
                  file=sys.stderr)
            head.append("**Members:** not computed")
            members_md = ("Members not computed: this script has no evaluator for this filter, so "
                          "the entries it selects are not listed. MITRE's page lists them: "
                          f"{DEFINITION_URL.format(i)}")
        else:
            head.append(f"**Members:** {_count_phrase(ed, ids)}")
            members_md = "\n".join("- " + entry_line(ed, x) for x in ids)
    else:
        raise UnexpectedMarkupError(f"{ctx}: unknown view Type {vtype!r}")

    sections = [
        (None, SEP.join(head)),
        ("Objective", objective),
        ("Audience", _audience(child(elem, "Audience"), ctx)),
        ("Filter", filter_md),
        ("Members", members_md),
        *extra,
        ("References", _references(ed, child(elem, "References"), ctx)),
        ("Mapping Notes", _mapping_notes(ed, child(elem, "Mapping_Notes"), ctx)),
        ("Notes", _notes(child(elem, "Notes"), ctx)),
    ]
    return _page(ed, front, title, sections)


# ------------------------------------------------------------------ index


def _ordered(values, order) -> list[str]:
    seen = set(values)
    return [v for v in order if v in seen] + sorted(seen - set(order))


def render_index(ed: Edition) -> str:
    v = ed.version
    gt = ed.group_term
    front = [
        f'secid: "secid:weakness/mitre.org/cwe@{v}"',
        "entry_type: index",
        f"cwe_version: {json.dumps(v)}",
        f"cwe_release_date: {json.dumps(ed.date)}",
        f'source: "{XML_URL.format(ed.zip_name)}"',
        f'sha256: "{ed.sha256}"',
    ]
    intro = "\n".join([
        f"MITRE's Common Weakness Enumeration (CWE) version {v}, released {ed.date}, as markdown: "
        f"this index and one page per weakness (`weaknesses/`), {gt.lower()} (`{ed.group_dir}/`) "
        "and view (`views/`).",
        "",
        f"- **Edition:** CWE {v}, released {ed.date}",
        f"- **Source:** `cwec_v{v}.xml` in {_link(ed.zip_name, XML_URL.format(ed.zip_name))}, "
        f"SHA-256 `{ed.sha256}`",
        f"- **Licence:** CWE Terms of Use, <{TERMS_URL}>; full text in [LICENSE.txt](LICENSE.txt)",
        f"- **Attribution:** {ATTRIBUTION}",
        "- **Omitted:** MITRE's content history (who submitted or modified each entry, and when)",
        f"- **Upstream pages:** <https://cwe.mitre.org/data/definitions/> (MITRE's site shows the "
        f"latest CWE version, which may differ from {v})",
    ])

    counts = ["### By entry type", "", _table(["Entry type", "Count"], [
        ["Weaknesses", str(len(ed.weaknesses))],
        [f"{gt}s", str(len(ed.groups))],
        ["Views", str(len(ed.views))],
    ])]
    abstractions = [w.get("Abstraction") or "" for w in ed.weaknesses.values()]
    counts += ["", "### Weaknesses by abstraction", "", _table(["Abstraction", "Weaknesses"], [
        [_esc(a), str(abstractions.count(a))] for a in _ordered(abstractions, ABSTRACTION_ORDER)
    ])]
    statuses = {k: [e.get("Status") or "" for e in t.values()]
                for k, t in (("w", ed.weaknesses), ("g", ed.groups), ("v", ed.views))}
    all_status = statuses["w"] + statuses["g"] + statuses["v"]
    counts += ["", "### By status", "", _table(["Status", "Weaknesses", f"{gt}s", "Views"], [
        [_esc(s)] + [str(statuses[k].count(s)) for k in ("w", "g", "v")]
        for s in _ordered(all_status, STATUS_ORDER)
    ])]

    def usage(e):
        return _esc(cx.text(child(child(e, "Mapping_Notes"), "Usage")))

    weaknesses = _table(["ID", "Name", "Abstraction", "Status", "Mapping usage"], [
        [cwe_link(ed, i, ""), _esc(w.get("Name") or ""), _esc(w.get("Abstraction") or ""),
         _esc(w.get("Status") or ""), usage(w)]
        for i, w in sorted(ed.weaknesses.items())
    ])
    groups = _table(["ID", "Name", "Status"], [
        [cwe_link(ed, i, ""), _esc(g.get("Name") or ""), _esc(g.get("Status") or "")]
        for i, g in sorted(ed.groups.items())
    ])
    views = _table(["ID", "Name", "Type", "Status"], [
        [cwe_link(ed, i, ""), _esc(x.get("Name") or ""), _esc(x.get("Type") or ""),
         _esc(x.get("Status") or "")]
        for i, x in sorted(ed.views.items())
    ])
    return _page(ed, front, f"CWE {v}", [
        (None, intro),
        ("Counts", "\n".join(counts)),
        ("Weaknesses", weaknesses),
        (f"{gt}s", groups),
        ("Views", views),
    ])


# ---------------------------------------------------------------- edition


def render_edition(ed: Edition) -> dict[str, str]:
    """Every file of ``markdown/``: relative POSIX path -> text, in numeric ID order."""
    files = {
        "index.md": render_index(ed),
        "LICENSE.txt": (ed.edition_dir / "LICENSE.txt").read_bytes().decode("utf-8"),
    }
    for i, w in sorted(ed.weaknesses.items()):
        files[f"weaknesses/CWE-{i}.md"] = render_weakness(ed, w)
    for i, g in sorted(ed.groups.items()):
        files[f"{ed.group_dir}/CWE-{i}.md"] = render_group(ed, g)
    for i, x in sorted(ed.views.items()):
        files[f"views/CWE-{i}.md"] = render_view(ed, x)
    return files


def _existing(out_dir: Path) -> list[str]:
    if not out_dir.is_dir():
        return []
    return sorted(p.relative_to(out_dir).as_posix() for p in out_dir.rglob("*") if not p.is_dir())


def write_markdown(files: dict[str, str], out_dir: Path) -> None:
    """Write every file (UTF-8, LF) under ``out_dir`` and delete files it does not list."""
    out_dir = Path(out_dir)
    for rel, text in files.items():
        path = out_dir / rel
        data = text.encode("utf-8")
        if path.is_file() and path.read_bytes() == data:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for rel in _existing(out_dir):
        if rel not in files:
            (out_dir / rel).unlink()
    for d in sorted((p for p in out_dir.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def diff_markdown(files: dict[str, str], out_dir: Path) -> list[str]:
    """Sorted relative paths that differ from ``files``, are missing, or are extra."""
    out_dir = Path(out_dir)
    bad = set()
    for rel, text in files.items():
        path = out_dir / rel
        if not path.is_file() or path.read_bytes() != text.encode("utf-8"):
            bad.add(rel)
    bad.update(rel for rel in _existing(out_dir) if rel not in files)
    return sorted(bad)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Render one CWE edition as markdown.")
    ap.add_argument("--version", required=True, help="edition, e.g. 5.0 (directory ../<version>)")
    ap.add_argument("--check", action="store_true",
                    help="render in memory; exit 1 if markdown/ differs, listing the files")
    args = ap.parse_args(argv)
    edition_dir = SCRIPTS_DIR.parent / args.version
    rel_out = f"weakness/mitre.org/cwe/{args.version}/markdown"
    try:
        ed = cx.load_edition(edition_dir, args.version)
        files = render_edition(ed)
    except (cx.SourceVerificationError, cx.DanglingReferenceError,
            st.UnsupportedMarkupError, UnexpectedMarkupError, OSError) as exc:
        print(f"error: CWE {args.version}: {exc}", file=sys.stderr)
        return 2
    out_dir = edition_dir / "markdown"
    if args.check:
        diff = diff_markdown(files, out_dir)
        for rel in diff:
            print(f"{rel_out}/{rel}")
        if diff:
            print(f"{len(diff)} file(s) differ from a fresh render of CWE {args.version}", file=sys.stderr)
            return 1
        print(f"{rel_out}: {len(files)} files match")
        return 0
    changed = diff_markdown(files, out_dir)
    write_markdown(files, out_dir)
    print(f"{rel_out}: {len(files)} files, {len(changed)} written or removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
