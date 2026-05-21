#!/usr/bin/env python3
"""Parse the OpenAI Model Spec into structured per-provision rows.

The Model Spec is a hierarchical control-catalog-shaped document. The top of
the markdown has a Table of Contents that lists every provision with:

    * [ Title AuthorityLevel ](#anchor_slug)

where AuthorityLevel is one of: Root, Root+N (1..3), System, Developer,
User, User+N, Guideline. The body of the document mirrors the TOC structure
with `# H1` for top-level sections and `## H2` (and deeper) for provisions.
Body headings carry only the title — the authority level lives only in the
TOC. We join the two.

Output: model-spec-provisions.{csv,json} — one row per provision with:
    provision_id        canonical slug from the anchor (e.g., "avoid_info_hazards")
    title               human-readable provision title
    parent_id           slug of the enclosing provision (or "")
    depth               TOC nesting depth (1 = top-level section)
    section             top-level section name this provision lives under
    authority_level     Root / Root+1 / Root+2 / Root+3 / System / Developer /
                        Guideline / User / User+1 (or "" for definitions)
    body                prose text under the provision's heading, up to the
                        next heading of equal or higher level
"""
import csv
import json
import re
from pathlib import Path


TOC_ENTRY_RE = re.compile(
    r"^(?P<indent>\s*)\*\s+\[\s*(?P<title>.+?)\s*\]\(#(?P<anchor>[a-z0-9_]+)\)\s*$",
    re.IGNORECASE,
)
# A top-level numbered TOC entry: "  1. [ Overview ](#overview)" or with level
TOC_TOP_RE = re.compile(
    r"^\s*\d+\.\s+\[\s*(?P<title>.+?)\s*\]\(#(?P<anchor>[a-z0-9_]+)\)\s*$",
    re.IGNORECASE,
)
LEVEL_RE = re.compile(
    r"\s+(?P<level>Root(?:\+\d+)?|System|Developer|Guideline|User(?:\+\d+)?)\s*$"
)
HEADING_RE = re.compile(r"^(#+)\s+(.+?)\s*$", re.MULTILINE)


def find_headings_with_continuation(body):
    """Marker often hard-wraps long headings across lines. Find every `^#+ ` and
    if the next non-blank line is also non-`#+ ` prose, join it as continuation.

    Returns list of dicts with: start (heading start offset), end (offset just
    after the title block), depth, title."""
    lines = body.splitlines(keepends=True)
    out = []
    offset = 0
    line_offsets = []
    for ln in lines:
        line_offsets.append(offset)
        offset += len(ln)
    line_offsets.append(offset)

    for i, ln in enumerate(lines):
        m = re.match(r"^(#+)\s+(.+?)\s*$", ln)
        if not m:
            continue
        depth = len(m.group(1))
        title_parts = [m.group(2).strip()]
        end_line = i
        # Wrap continuation: next line non-blank, not a heading itself, not
        # the next paragraph (i.e., the line immediately after with no blank
        # gap and not starting with `#`)
        j = i + 1
        while j < len(lines):
            nxt = lines[j].rstrip("\n")
            if not nxt.strip():
                break
            if re.match(r"^#+\s+", nxt):
                break
            # Avoid swallowing list items or other markdown blocks
            if re.match(r"^\s*[-*]\s", nxt):
                break
            title_parts.append(nxt.strip())
            end_line = j
            j += 1
        out.append({
            "start": line_offsets[i],
            "title_end": line_offsets[end_line + 1],
            "depth": depth,
            "title": " ".join(title_parts),
        })
    return out


def split_title_level(title_with_level: str):
    """Split 'Title AuthorityLevel' → ('Title', 'AuthorityLevel'). If no
    trailing level, returns (title, '')."""
    m = LEVEL_RE.search(title_with_level)
    if m:
        return title_with_level[: m.start()].rstrip(), m.group("level")
    return title_with_level, ""


def slugify_heading(text: str) -> str:
    """Best-effort: match a body heading to a TOC anchor by normalizing.
    This is informational only — we resolve via title equality rather than
    relying on the slug."""
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def parse_toc(md: str):
    """Return [(depth, title, level, anchor)] entries from the TOC.

    The TOC ends at the first H1 (`^# `). Indentation level inside list
    items determines depth (2-space units after the `*`).
    """
    end_match = re.search(r"^#\s+", md, re.MULTILINE)
    toc_block = md[: end_match.start()] if end_match else md
    entries = []

    for line in toc_block.splitlines():
        m_top = TOC_TOP_RE.match(line)
        if m_top:
            title, level = split_title_level(m_top.group("title"))
            entries.append({
                "depth": 1,
                "title": title.strip(),
                "level": level,
                "anchor": m_top.group("anchor"),
            })
            continue

        m = TOC_ENTRY_RE.match(line)
        if not m:
            continue
        indent = m.group("indent")
        # The TOC indents by 2-space increments. The minimum nested-item
        # indent is "     " (5 spaces for the first nested level) — fold
        # that to depth=2, then each +2 spaces adds a level.
        n_spaces = len(indent.expandtabs(4))
        if n_spaces <= 2:
            depth = 1
        else:
            depth = 1 + max(1, (n_spaces - 3) // 2)
        title, level = split_title_level(m.group("title"))
        entries.append({
            "depth": depth,
            "title": title.strip(),
            "level": level,
            "anchor": m.group("anchor"),
        })
    return entries


def compute_parents(entries):
    """Assign parent_id (anchor of enclosing entry by depth) to each."""
    stack = []  # list of (depth, anchor)
    for e in entries:
        while stack and stack[-1][0] >= e["depth"]:
            stack.pop()
        e["parent_id"] = stack[-1][1] if stack else ""
        e["section"] = stack[0][1] if stack else e["anchor"]
        stack.append((e["depth"], e["anchor"]))
    return entries


def extract_bodies(md: str, entries):
    """For each entry, locate the body heading and slice prose up to the
    next heading of equal or higher level (smaller `#` count).

    Body headings carry the bare title without the authority level. Match by
    case-insensitive title equality.
    """
    end_match = re.search(r"^#\s+", md, re.MULTILINE)
    body = md[end_match.start():] if end_match else md

    headings = find_headings_with_continuation(body)

    title_index = {}
    for i, h in enumerate(headings):
        norm = h["title"].strip().lower()
        title_index.setdefault(norm, []).append(i)

    used = set()
    for e in entries:
        wanted = e["title"].strip().lower()
        candidates = title_index.get(wanted, [])
        chosen = None
        for idx in candidates:
            if idx in used:
                continue
            chosen = idx
            break
        if chosen is None:
            e["body"] = ""
            continue
        used.add(chosen)
        depth_md = headings[chosen]["depth"]
        start = headings[chosen]["title_end"]
        next_start = len(body)
        for j in range(chosen + 1, len(headings)):
            if headings[j]["depth"] <= depth_md:
                next_start = headings[j]["start"]
                break
        text = body[start:next_start].strip()
        # The first non-blank line is often the lone authority-level label
        # (e.g., "Root", "Guideline") that the marker conversion lifts out
        # of the heading. Strip it if present and matches the TOC level.
        lines = text.split("\n", 2)
        if lines and lines[0].strip() == e["level"]:
            text = "\n".join(lines[1:]).lstrip("\n").strip()
        e["body"] = text
    return entries


def main():
    here = Path(__file__).parent
    md = (here / "model-spec.md").read_text(encoding="utf-8")

    entries = parse_toc(md)
    compute_parents(entries)
    extract_bodies(md, entries)

    # Resolve section anchor to its title (better readability)
    by_anchor = {e["anchor"]: e for e in entries}
    for e in entries:
        sec = by_anchor.get(e["section"])
        e["section"] = sec["title"] if sec else e["section"]

    fields = ["provision_id", "title", "parent_id", "depth", "section",
              "authority_level", "body"]
    rows = []
    for e in entries:
        rows.append({
            "provision_id": e["anchor"],
            "title": e["title"],
            "parent_id": e["parent_id"],
            "depth": e["depth"],
            "section": e["section"],
            "authority_level": e["level"],
            "body": e["body"],
        })

    csv_path = here / "model-spec-provisions.csv"
    json_path = here / "model-spec-provisions.json"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_total = len(rows)
    n_with_body = sum(1 for r in rows if r["body"])
    n_with_level = sum(1 for r in rows if r["authority_level"])
    by_level = {}
    for r in rows:
        by_level[r["authority_level"]] = by_level.get(r["authority_level"], 0) + 1
    print(f"Provisions: {n_total}")
    print(f"  with body text: {n_with_body}")
    print(f"  with authority level: {n_with_level}")
    print(f"  by authority level:")
    for k in sorted(by_level.keys()):
        print(f"    {k or '(none)':12} {by_level[k]:>4}")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
