"""Convert MITRE CWE "Structured_Text" elements (text mixed with XHTML) to markdown.

MITRE's XML holds fields such as Extended_Description, Mitigation Description,
Intro_Text and Example_Code as text interleaved with XHTML elements. This module
walks ``elem.text``, each child and ``child.tail`` in document order, so the order
of prose, lists, tables and code is exactly MITRE's.

Elements are matched by local name (the XHTML namespace is
``http://www.w3.org/1999/xhtml``). Supported tags: p div br ul ol li b i table
tbody tr th td caption img sup span. Anything else raises UnsupportedMarkupError
naming the context, so new markup in a future CWE release fails loudly.

Python 3.10+ standard library only. Output is deterministic, with LF line endings.
"""

from __future__ import annotations

import re
import textwrap
from urllib.parse import urljoin
from xml.etree.ElementTree import Element

IMAGE_BASE = "https://cwe.mitre.org/data/definitions/"

SUPPORTED_TAGS = frozenset(
    "p div br ul ol li b i table tbody tr th td caption img sup span".split()
)
_BLOCK_TAGS = frozenset({"p", "div", "ul", "ol", "table"})
_TABLE_PARTS = frozenset({"tbody", "thead", "tfoot"})
# Example_Code that holds these is real structured content, not source code.
_STRUCTURAL_IN_CODE = frozenset({"p", "ul", "ol", "table"})


class UnsupportedMarkupError(ValueError):
    """Markup the converter does not know how to render."""


def _local(tag) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


# --------------------------------------------------------------------------
# Escaping and fencing
# --------------------------------------------------------------------------

_ENTITY_AMP = re.compile(r"&(?=#?[A-Za-z0-9]+;)")
_LINE_START_ESCAPES = (
    (re.compile(r"^(\s*)(#{1,6})(?=\s|$)"), r"\1\\\2"),
    (re.compile(r"^(\s*)(>)"), r"\1\\\2"),
    (re.compile(r"^(\s*)([-+*])(?=\s|$)"), r"\1\\\2"),
    (re.compile(r"^(\s*)(\d+)([.)])(?=\s|$)"), r"\1\2\\\3"),
    (re.compile(r"^(\s*)(-{3,}|={3,}|\*{3,}|_{3,})\s*$"), r"\1\\\2"),
    (re.compile(r"^(\s*)(`{3,}|~{3,})"), r"\1\\\2"),
)


def escape_inline(text: str, at_line_start: bool = True) -> str:
    """Escape prose so it renders as written, keeping it readable as plain text.

    ``<`` becomes ``&lt;``; ``&`` is escaped only where it would start an HTML
    entity; a line-initial ``#``, ``>``, ``-``, ``+``, ``*`` or ``N.`` gets a
    backslash. Ordinary mid-line punctuation is left alone. ``at_line_start``
    says whether the first line of ``text`` begins a markdown line.
    """
    text = _ENTITY_AMP.sub("&amp;", text).replace("<", "&lt;")
    out = []
    for i, line in enumerate(text.split("\n")):
        if i > 0 or at_line_start:
            for pattern, repl in _LINE_START_ESCAPES:
                new = pattern.sub(repl, line, count=1)
                if new != line:
                    line = new
                    break
        out.append(line)
    return "\n".join(out)


def escape_table_cell(text: str) -> str:
    """Make text safe inside one markdown table cell: ``|`` escaped, newlines to ``<br>``."""
    text = re.sub(r"[ \t]*\r?\n[ \t]*", "<br>", text.strip())
    return text.replace("|", "\\|")


def fence(code: str, lang: str) -> str:
    """Fenced code block; the fence is longer than any backtick run in the code."""
    longest = max((len(m) for m in re.findall(r"`+", code)), default=0)
    ticks = "`" * max(3, longest + 1)
    return f"{ticks}{lang}\n{code}\n{ticks}"


# --------------------------------------------------------------------------
# Prose (inline runs and blocks)
# --------------------------------------------------------------------------

_BR = object()


class _Inline:
    """Accumulates one paragraph's pieces: collapsed text, raw markup, line breaks."""

    def __init__(self) -> None:
        self.pieces: list = []

    def text(self, s: str | None) -> None:
        if s:
            self.pieces.append(("text", s))

    def raw(self, s: str) -> None:
        if s:
            self.pieces.append(("raw", s))

    def br(self) -> None:
        self.pieces.append(("br", None))

    def render(self, at_line_start: bool = True, br: str = "  \n") -> str:
        out: list[str] = []
        line_start = at_line_start
        for kind, val in self.pieces:
            if kind == "br":
                if out and out[-1].endswith(" "):
                    out[-1] = out[-1].rstrip(" ")
                if out:  # a leading break adds nothing
                    out.append(br)
                    line_start = True
                continue
            if kind == "raw":
                out.append(val)
                line_start = False
                continue
            t = re.sub(r"\s+", " ", val)
            if line_start or (out and out[-1].endswith((" ", "\n"))):
                t = t.lstrip(" ")
            if not t:
                continue
            out.append(escape_inline(t, at_line_start=line_start))
            line_start = False
        s = "".join(out).strip(" \n")
        return re.sub(r" +\n", "\n", s) if br == "\n" else s


def _is_monospace(e: Element) -> bool:
    style = (e.get("style") or "").lower()
    return "courier" in style or "monospace" in style


def _inline_code(s: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", s)), default=0)
    ticks = "`" * (longest + 1)
    pad = " " if s.startswith("`") or s.endswith("`") else ""
    return f"{ticks}{pad}{s}{pad}{ticks}"


def _plain_text(e: Element, ctx: str) -> str:
    """Text of an element with all markup flattened (for code spans and alt text)."""
    parts = [e.text or ""]
    for c in e:
        if isinstance(c.tag, str):
            name = _local(c.tag)
            if name not in SUPPORTED_TAGS:
                raise UnsupportedMarkupError(f"{ctx}: unsupported markup <{name}>")
            parts.append("\n" if name == "br" else _plain_text(c, ctx))
        parts.append(c.tail or "")
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def _fill_inline(run: _Inline, e: Element, ctx: str, cell: bool) -> None:
    """Add e's text, children and tails to ``run``; children must be inline."""
    run.text(e.text)
    for c in e:
        if isinstance(c.tag, str):
            name = _local(c.tag)
            if name in _BLOCK_TAGS:
                raise UnsupportedMarkupError(
                    f"{ctx}: block element <{name}> inside inline markup"
                )
            _inline_child(run, c, name, ctx, cell)
        run.text(c.tail)


def _inline_child(run: _Inline, c: Element, name: str, ctx: str, cell: bool) -> None:
    if name == "br":
        run.br()
    elif name == "img":
        src = urljoin(IMAGE_BASE, c.get("src") or "")
        alt = (c.get("alt") or "").replace("]", "\\]")
        run.raw(f"![{alt}]({src})")
    elif name in ("b", "i", "sup", "span"):
        if name == "span" and _is_monospace(c):
            code = _plain_text(c, ctx)
            if code:
                run.raw(_inline_code(code))
            return
        sub = _Inline()
        _fill_inline(sub, c, ctx, cell)
        inner = sub.render(at_line_start=False, br="\n" if cell else "  \n")
        if not inner:
            run.text(" " if sub.pieces else "")
            return
        first, last = sub.pieces[0], sub.pieces[-1]
        if first[0] == "text" and first[1][:1].isspace():
            run.text(" ")
        if name == "span":
            run.raw(inner)
        elif name == "sup":
            run.raw(f"<sup>{inner}</sup>")
        else:
            mark = "**" if name == "b" else "*"
            run.raw(f"{mark}{inner}{mark}")
        if last[0] == "text" and last[1][-1:].isspace():
            run.text(" ")
    elif name in SUPPORTED_TAGS:
        raise UnsupportedMarkupError(f"{ctx}: <{name}> is not valid here")
    else:
        raise UnsupportedMarkupError(f"{ctx}: unsupported markup <{name}>")


def _blocks(e: Element, ctx: str, cell: bool = False) -> list[tuple[str, str]]:
    """Markdown blocks (kind, text) for e's content, kind in {"text", "list", "table"}."""
    blocks: list[tuple[str, str]] = []
    run = _Inline()

    def flush() -> None:
        nonlocal run
        s = run.render(br="\n" if cell else "  \n")
        if s:
            blocks.append(("text", s))
        run = _Inline()

    run.text(e.text)
    for c in e:
        if isinstance(c.tag, str):
            name = _local(c.tag)
            if name in ("p", "div"):
                flush()
                blocks.extend(_blocks(c, ctx, cell))
            elif name in ("ul", "ol"):
                flush()
                blocks.append(("list", _list_md(c, name, ctx)))
            elif name == "table":
                flush()
                blocks.extend(_table_md(c, ctx))
            elif name in ("li", "tr", "td", "th", "tbody", "caption"):
                raise UnsupportedMarkupError(
                    f"{ctx}: <{name}> outside its list or table"
                )
            else:
                _inline_child(run, c, name, ctx, cell)
        run.text(c.tail)
    flush()
    return blocks


def _list_md(e: Element, kind: str, ctx: str) -> str:
    items = []
    n = 0
    if e.text and e.text.strip():
        raise UnsupportedMarkupError(f"{ctx}: text directly inside <{kind}>")
    for c in e:
        if not isinstance(c.tag, str):
            continue
        name = _local(c.tag)
        if name != "li":
            raise UnsupportedMarkupError(f"{ctx}: <{name}> inside <{kind}>")
        n += 1
        marker = f"{n}. " if kind == "ol" else "- "
        body = ""
        for i, (bkind, text) in enumerate(_blocks(c, ctx)):
            if i:
                body += "\n" if bkind == "list" else "\n\n"
            body += text
        pad = " " * len(marker)
        lines = body.split("\n") or [""]
        out = [marker + lines[0]] + [pad + ln if ln else "" for ln in lines[1:]]
        items.append("\n".join(out))
    return "\n".join(items)


def _table_md(e: Element, ctx: str) -> list[tuple[str, str]]:
    caption = ""
    rows: list[tuple[bool, list[str]]] = []  # (all cells are th, cell markdown)

    def add_rows(parent: Element) -> None:
        nonlocal caption
        if parent.text and parent.text.strip():
            raise UnsupportedMarkupError(f"{ctx}: text directly inside <table>")
        for c in parent:
            if not isinstance(c.tag, str):
                continue
            name = _local(c.tag)
            if name == "caption":
                caption = " ".join(
                    t for _, t in _blocks(c, ctx, cell=True)
                ).replace("\n", " ")
            elif name in _TABLE_PARTS:
                add_rows(c)
            elif name == "tr":
                cells: list[str] = []
                all_th = True
                for cell in c:
                    if not isinstance(cell.tag, str):
                        continue
                    cname = _local(cell.tag)
                    if cname not in ("td", "th"):
                        raise UnsupportedMarkupError(f"{ctx}: <{cname}> inside <tr>")
                    text = "\n".join(t for _, t in _blocks(cell, ctx, cell=True))
                    if cname != "th":
                        all_th = False
                    cells.append(escape_table_cell(text))
                    span = int(cell.get("colspan") or 1)
                    cells.extend([""] * (span - 1))
                rows.append((all_th and bool(cells), cells))
            else:
                raise UnsupportedMarkupError(f"{ctx}: <{name}> inside <table>")

    add_rows(e)
    out: list[tuple[str, str]] = []
    if caption:
        out.append(("text", f"*{escape_inline(caption, at_line_start=False)}*"))
    if not rows:
        return out
    width = max(len(cells) for _, cells in rows)
    padded = [cells + [""] * (width - len(cells)) for _, cells in rows]
    if rows[0][0]:
        header, body = padded[0], padded[1:]
    else:
        header, body = [""] * width, padded

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(cells) + " |"

    table = [line(header), line(["---"] * width)] + [line(r) for r in body]
    out.append(("table", "\n".join(table)))
    return out


def structured_text_to_md(elem: Element, context: str) -> str:
    """Convert a Structured_Text element to markdown blocks separated by one blank line.

    ``context`` (e.g. ``"CWE-79/Extended_Description"``) appears in errors.
    """
    return "\n\n".join(text for _, text in _blocks(elem, context))


# --------------------------------------------------------------------------
# Code (Example_Code)
# --------------------------------------------------------------------------


class _Code:
    """Line emitter for code: text as written, ``br`` a newline, nested divs indent."""

    INDENT = "    "

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.cur: list[str] = []
        self.indent = 0
        self.boundary = True  # at a block edge: a following br adds nothing

    def _has_content(self) -> bool:
        return any(p for p in self.cur)

    def finish_line(self) -> None:
        self.lines.append("".join(self.cur).rstrip())
        self.cur = []

    def _write(self, s: str) -> None:
        if not self.cur:
            self.cur.append(self.INDENT * self.indent)
        self.cur.append(s)

    def text(self, s: str | None) -> None:
        if not s:
            return
        if not s.strip():
            if "\n" not in s and self._has_content():
                self._write(s)
            return
        lead_nl = re.match(r"(?:[ \t]*\r?\n)+", s)
        if lead_nl:
            s = s[lead_nl.end():]
        elif not self._has_content():
            s = s.lstrip(" \t")
        s = re.sub(r"\s*\r?\n\s*$", "", s)
        s = s.replace("\r\n", "\n")
        lines = s.split("\n")
        if lead_nl and len(lines) > 1:
            lines = textwrap.dedent("\n".join(lines)).split("\n")
        for i, ln in enumerate(lines):
            if i:
                self.finish_line()
            if ln.strip():
                self._write(ln)
        self.boundary = False

    def br(self) -> None:
        if self.boundary:
            return
        self.finish_line()

    def block_start(self, indent: bool) -> None:
        if self._has_content():
            self.finish_line()
        else:
            self.cur = []
        if indent:
            self.indent += 1
        self.boundary = True

    def block_end(self, indent: bool) -> None:
        if self._has_content():
            self.finish_line()
        else:
            self.cur = []
        if indent:
            self.indent -= 1
        self.boundary = True

    def result(self) -> str:
        if self._has_content():
            self.finish_line()
        lines = self.lines
        while lines and not lines[0]:
            lines = lines[1:]
        while lines and not lines[-1]:
            lines = lines[:-1]
        return "\n".join(lines)


def _walk_code(code: _Code, e: Element, ctx: str) -> None:
    code.text(e.text)
    for c in e:
        if isinstance(c.tag, str):
            name = _local(c.tag)
            if name == "br":
                code.br()
            elif name == "div":
                indented = "margin-left" in (c.get("style") or "")
                code.block_start(indented)
                _walk_code(code, c, ctx)
                code.block_end(indented)
            elif name in ("b", "i", "span", "sup"):
                _walk_code(code, c, ctx)
            elif name in SUPPORTED_TAGS:
                raise UnsupportedMarkupError(f"{ctx}: <{name}> is not valid inside code")
            else:
                raise UnsupportedMarkupError(f"{ctx}: unsupported markup <{name}>")
        code.text(c.tail)


def _lang_tag(language: str) -> str:
    return re.sub(r"[^a-z0-9+#._-]+", "-", language.lower()).strip("-")


def example_code_to_md(elem: Element, context: str) -> str:
    """One ``Example_Code`` element: a label line, then a fenced code block.

    The label is ``*Example (Nature, Language):*`` (Nature, then Language when
    present; ``*Example (Attack):*`` with no Language). The fence is tagged with
    the lower-cased Language. An Example_Code that holds a paragraph, list or
    table is real structured content, so it renders as prose under the label.
    """
    parts = [p for p in (elem.get("Nature"), elem.get("Language")) if p]
    label = f"*Example ({', '.join(parts)}):*" if parts else "*Example:*"
    if any(_local(d.tag) in _STRUCTURAL_IN_CODE for d in elem.iter() if d is not elem):
        body = structured_text_to_md(elem, context)
        return f"{label}\n\n{body}" if body else label
    code = _Code()
    _walk_code(code, elem, context)
    return f"{label}\n\n{fence(code.result(), _lang_tag(elem.get('Language') or ''))}"
