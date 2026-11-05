#!/usr/bin/env python3
"""Generic per-section extractor for hierarchical regulatory documents.

Walks a markdown file for `#`-level headings, captures each as a row with:
  - section_id     (numeric/textual identifier pulled from the heading)
  - section_name   (heading title, with the id stripped)
  - depth          (heading level)
  - parent_id      (derived from hierarchical numbering, or empty)
  - body           (prose under the heading until the next heading)

Identifier patterns are heuristic: tries to match common shapes like
"1.1", "22757.10", "Pillar I", "SECTION 2". If no recognizable identifier
prefixes the heading, section_id is left empty (rows still emitted).

Usage:
    python3 parse_regulatory_sections.py <doc-dir> [--out-stem PREFIX]

Output: <doc-dir>/<PREFIX>-sections.{csv,json}
  PREFIX defaults to the dir name.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#+)\s+(.+?)\s*$", re.MULTILINE)

# Identifier patterns tried in order. First match wins. Each returns the id
# string from the heading text.
ID_PATTERNS = [
    # SB-53 style: "22757.10. Short Title" or "22757.10 Short Title"
    (re.compile(r"^(\d{4,5}\.\d+(?:\.\d+)?)\.?\s+(.+)$"), "statute"),
    # SECTION 1 / SECTION 2 / Section (1): "SECTION 1. Legislative Findings and Declarations"
    (re.compile(r"^(SECTION\s+(?:\d+(?:\.\d+)*|\(\d+\)|\([ivxlcdm]+\)|[IVXLCDM]+))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "section_word"),
    # Pillar I / Pillar 1 / Pillar (i) / Pillar One: "Pillar I: AI Use Restrictions ..."
    (re.compile(r"^(Pillar\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+|\(\d+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "pillar"),
    # Part I / Part 1 / Part (1) / Part One: "Part I: ..."
    (re.compile(r"^(Part\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+|\(\d+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "part"),
    # CHAPTER 25.1 / Chapter 1 / Chapter One: "CHAPTER 25.1. Transparency in ..."
    (re.compile(r"^(CHAPTER\s+(?:\d+(?:\.\d+)?|\(\d+\)|[IVXLCDM]+|\([ivxlcdm]+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "chapter"),
    # Strategic Objective 1.1 / Objective 1.1 / Objective 2a / Implementation 6.1
    (re.compile(r"^((?:Strategic\s+)?Objective\s+\d+[a-z]?(?:\.\d+)*|Implementation\s+\d+(?:\.\d+)*)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "objective"),
    # Initiative 1.1.1: Title
    (re.compile(r"^(Initiative\s+\d+(?:\.\d+)+)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "initiative"),
    # Goal 1 / Priority 1 / Principle 1 / Recommendation 1 / Finding 1: Title
    (re.compile(r"^((?:Goal|Priority|Principle|Recommendation|Finding)\s+\d+(?:\.\d+)*)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "goal"),
    # Annex / Appendix / Schedule A / 1 / I: Title
    (re.compile(r"^((?:Annex|Appendix|Schedule)\s+(?:[A-Z]|\d+|[IVXLCDM]+))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "annex"),
    # Standalone identifiers without trailing title (e.g., "Principle 1", "Appendix A", "Part One.")
    (re.compile(r"^((?:Pillar|Part|Chapter|Section|Annex|Appendix|Schedule|Principle|Goal|Objective|Finding|Recommendation)\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+[a-z]?|\(\d+\)|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\.?$", re.IGNORECASE), "standalone_id"),
    # Roman numeral section: "I. Introduction" / "II. Our Vision" / "I Purpose" / "II Japan's National Interests"
    (re.compile(r"^([IVX]{1,4})(?:\.\s+|\s+(?=[A-Z][a-z]))(.+)$"), "roman"),
    # Capital-letter section: "A. Innovative Europe" / "B. Making the EU..."
    (re.compile(r"^([A-Z])\.\s+([A-Z].+)$"), "letter"),
    # Plain hierarchical numbering "1.1 Title" / "1.1. Title" / "2.3.1 Title"
    (re.compile(r"^(\d{1,2}(?:\.\d{1,2}){1,3})\.?\s*[:\-–—]?\s+(?!(?:M€|B€|€|\$|£|%|million|billion|trillion)\b)(.+)$", re.IGNORECASE), "numbered"),
    # Single-number section heading "1. Introduction" / "1 Introduction" (excluding "4 x SSBN" force counts and "30 June 2018" dates)
    (re.compile(r"^(\d{1,3})(?:[:\.\-–—]\s+|\s+(?![xX]\b)(?!(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b)(?!.*\b\d+\s+[xX]\s+))([A-Z].+)$"), "numbered"),
]


_UNICODE_ROMAN_MAP = str.maketrans({
    "Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "Ⅳ": "IV", "Ⅴ": "V",
    "Ⅵ": "VI", "Ⅶ": "VII", "Ⅷ": "VIII", "Ⅸ": "IX", "Ⅹ": "X",
})


def clean_heading_text(s: str) -> str:
    """Strip markdown bold/italic + anchor tags + leading numbering punctuation."""
    s = s.translate(_UNICODE_ROMAN_MAP)
    s = re.sub(r"<a id=\"[^\"]*\"></a>", "", s)
    s = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"\\([_*\[\]\(\)])", r"\1", s)
    return s.strip()


def parse_heading(text: str):
    """Return (section_id, section_name, id_kind) for a heading text. If no id
    pattern matches, section_id and id_kind are empty strings."""
    cleaned = clean_heading_text(text)
    for pat, kind in ID_PATTERNS:
        m = pat.match(cleaned)
        if m:
            if m.lastindex and m.lastindex >= 2:
                return m.group(1).rstrip("."), m.group(2).strip(), kind
            return m.group(1).rstrip("."), m.group(1).rstrip("."), kind
    return "", cleaned, ""


_NUM_TO_WORD = {
    "1": "One", "2": "Two", "3": "Three", "4": "Four", "5": "Five",
    "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine", "10": "Ten",
}
_NUM_TO_ROMAN = {
    "1": "I", "2": "II", "3": "III", "4": "IV", "5": "V",
    "6": "VI", "7": "VII", "8": "VIII", "9": "IX", "10": "X",
}


def derive_parent_id(section_id: str, existing_ids: set[str] | None = None) -> str:
    """For numeric ids like '1.2.3' or '22757.10', return the parent ('1.2',
    '22757') if present in existing_ids (or matching Chapter/Part/Section/Pillar).
    For 'Initiative X.Y.Z' return 'Strategic Objective X.Y' (or
    'Implementation X.Y' if present). For '(Strategic )?Objective X.Y' return
    the matching 'Pillar <X>' if present in existing_ids."""
    parts = section_id.split(".")
    if len(parts) > 1 and all(re.match(r"^\d+$", p) for p in parts):
        cand_parent = ".".join(parts[:-1])
        if existing_ids is None or cand_parent in existing_ids:
            return cand_parent
        if len(parts) == 2:
            p_num = parts[0]
            for prefix in ("Chapter", "CHAPTER", "Part", "PART", "Section", "SECTION", "Pillar", "PILLAR", "Goal", "Objective"):
                for suffix in (p_num, _NUM_TO_ROMAN.get(p_num, ""), _NUM_TO_WORD.get(p_num, ""), _NUM_TO_WORD.get(p_num, "").upper()):
                    if suffix and f"{prefix} {suffix}" in existing_ids:
                        return f"{prefix} {suffix}"
            if _NUM_TO_ROMAN.get(p_num, "") and _NUM_TO_ROMAN[p_num] in existing_ids:
                return _NUM_TO_ROMAN[p_num]
        return ""
    m = re.match(r"^Initiative\s+(\d+\.\d+)\.\d+$", section_id, re.IGNORECASE)
    if m:
        xy = m.group(1)
        if existing_ids and f"Implementation {xy}" in existing_ids:
            return f"Implementation {xy}"
        if existing_ids is None or f"Strategic Objective {xy}" in existing_ids:
            return f"Strategic Objective {xy}"
        if existing_ids and f"Objective {xy}" in existing_ids:
            return f"Objective {xy}"
        return ""
    m_obj = re.match(r"^(?:Strategic\s+)?Objective\s+(\d+)\.\d+[a-z]?$", section_id, re.IGNORECASE)
    if m_obj and existing_ids:
        p_num = m_obj.group(1)
        candidates = [
            f"Pillar {_NUM_TO_WORD.get(p_num, '')}",
            f"Pillar {_NUM_TO_ROMAN.get(p_num, '')}",
            f"Pillar {p_num}",
            f"PILLAR {_NUM_TO_WORD.get(p_num, '').upper()}",
            f"PILLAR {_NUM_TO_ROMAN.get(p_num, '')}",
            f"PILLAR {p_num}",
        ]
        for cand in candidates:
            if cand.strip() in existing_ids:
                return cand.strip()
    return ""


def is_valid_container(parent_row: dict, child_kind: str, child_id: str) -> bool:
    """Return True if parent_row is a valid semantic container for (child_kind, child_id)."""
    pid = parent_row.get("section_id", "")
    pkind = parent_row.get("id_kind", "")
    if not pid or not child_id:
        return False
    if pid == child_id:
        return True
    if pkind == child_kind:
        return False
    if child_kind == "annex":
        return pkind in ("part", "chapter", "roman")
    if child_kind in ("pillar", "part", "chapter", "roman", "letter"):
        return pkind in ("part", "chapter", "roman", "annex")
    if child_kind in ("objective", "section_word"):
        if re.match(r"^Implementation\s+\d+\.\d+$", child_id, re.IGNORECASE):
            return False
        return pkind in ("pillar", "part", "chapter", "roman", "annex")
    if child_kind == "goal":
        return pkind in ("pillar", "part", "chapter", "roman", "annex", "section_word") or (
            pkind == "numbered" and "." not in pid
        )
    if child_kind == "numbered":
        if "." in child_id:
            return False
        return pkind in ("roman", "part", "chapter", "pillar", "annex", "section_word", "letter")
    return False


def normalize_body(s: str) -> str:
    s = re.sub(r"\\([_*\[\]\(\)\-\.])", r"\1", s)
    s = re.sub(r"<a id=\"[^\"]*\"></a>", "", s)
    s = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", s)
    s = re.sub(r"\{\d+\}-+", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_dir", help="Document directory containing the .md file")
    ap.add_argument("--out-stem", default=None,
                    help="Output filename prefix (default: dir name)")
    args = ap.parse_args()

    doc_dir = Path(args.doc_dir).resolve()
    if not doc_dir.is_dir():
        raise SystemExit(f"Not a directory: {doc_dir}")

    md_files = [p for p in doc_dir.glob("*.md")
                if not p.name.endswith("-metadata.md")
                and not p.name.startswith("README")]
    if not md_files:
        raise SystemExit(f"No source markdown in {doc_dir}")
    md = md_files[0].read_text(encoding="utf-8")

    headings = list(HEADING_RE.finditer(md))
    min_enc_depth = 1 if sum(1 for h in headings if len(h.group(1)) == 1) > 1 else 2
    rows = []
    seen_ids: set[str] = set()
    latest_row_by_id: dict[str, int] = {}
    ancestor_row_by_depth: dict[int, int] = {}
    ancestor_id_row_by_depth: dict[int, int] = {}

    for i, m in enumerate(headings):
        depth = len(m.group(1))
        for d in [k for k in list(ancestor_row_by_depth) if k >= depth]:
            del ancestor_row_by_depth[d]
        for d in [k for k in list(ancestor_id_row_by_depth) if k >= depth]:
            del ancestor_id_row_by_depth[d]

        section_id, section_name, id_kind = parse_heading(m.group(2))
        if id_kind == "annex":
            seen_ids = {
                rows[ancestor_id_row_by_depth[d]]["section_id"]
                for d in ancestor_id_row_by_depth
                if rows[ancestor_id_row_by_depth[d]]["section_id"]
            }
        derived_parent = derive_parent_id(section_id, seen_ids) if section_id else ""
        parent_row_idx = None
        parent_id = ""
        if derived_parent:
            parent_id = derived_parent
            parent_row_idx = latest_row_by_id.get(derived_parent)
        elif section_id:
            for d in range(depth - 1, 0, -1):
                if d in ancestor_id_row_by_depth:
                    cand_idx = ancestor_id_row_by_depth[d]
                    if is_valid_container(rows[cand_idx], id_kind, section_id):
                        parent_row_idx = cand_idx
                        parent_id = rows[cand_idx]["section_id"]
                        break

        enclosing_any_idx = next(
            (ancestor_row_by_depth[d] for d in range(depth - 1, min_enc_depth - 1, -1) if d in ancestor_row_by_depth),
            None,
        )

        if section_id:
            seen_ids.add(section_id)
            latest_row_by_id[section_id] = i

        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(md)
        body = normalize_body(md[body_start:body_end])
        rows.append({
            "depth": depth,
            "section_id": section_id,
            "section_name": section_name,
            "id_kind": id_kind,
            "parent_id": parent_id,
            "body": body,
            "_parent_row_idx": parent_row_idx,
            "_enclosing_any_idx": enclosing_any_idx,
        })
        ancestor_row_by_depth[depth] = i
        if section_id:
            ancestor_id_row_by_depth[depth] = i

    # Disambiguate duplicate section_ids top-down by depth so child parent_ids stay synchronized
    from collections import Counter
    max_depth = max((r["depth"] for r in rows), default=0)
    for d in range(1, max_depth + 1):
        # First refresh parent_id from _parent_row_idx in case parent's section_id was disambiguated
        for r in rows:
            if r["depth"] == d and r["_parent_row_idx"] is not None:
                r["parent_id"] = rows[r["_parent_row_idx"]]["section_id"]

        # Check global duplicates involving rows at or above depth d
        id_counts = Counter(r["section_id"] for r in rows if r["section_id"])
        dup_ids = {sid for sid, cnt in id_counts.items() if cnt > 1}
        if not dup_ids:
            continue

        for idx, r in enumerate(rows):
            if r["depth"] != d or not r["section_id"] or r["section_id"] not in dup_ids:
                continue
            sid = r["section_id"]
            pid = r["parent_id"]
            if pid and pid != sid:
                if re.match(r"^(?:[IVX]+|\d+(?:\.\d+)*)$", pid) and re.match(r"^\d+(?:\.\d+)*$", sid):
                    r["section_id"] = f"{pid}.{sid}"
                else:
                    r["section_id"] = f"{pid} {sid}"
            elif pid == sid and r["section_name"]:
                r["section_id"] = f"{sid} ({r['section_name']})"

    # Final pass if any section_ids remain duplicated (e.g. repeated top-level sections across stitched reports or unnumbered themes)
    id_counts = Counter(r["section_id"] for r in rows if r["section_id"])
    still_dup = {sid for sid, cnt in id_counts.items() if cnt > 1}
    if still_dup:
        for r in rows:
            sid = r["section_id"]
            if sid in still_dup:
                enc_idx = r["_enclosing_any_idx"]
                enc_name = rows[enc_idx]["section_name"] if enc_idx is not None else ""
                enc_short = enc_name.split(":")[0].strip() if len(enc_name) > 48 and ":" in enc_name else enc_name
                if enc_short and len(enc_short) <= 48 and not enc_short.lower().startswith("national security transparency advisory group"):
                    r["section_id"] = f"{enc_short}: {sid}"
        # Refresh child parent_ids and ensure 100% uniqueness if any collide
        for r in rows:
            if r["_parent_row_idx"] is not None:
                r["parent_id"] = rows[r["_parent_row_idx"]]["section_id"]
        id_counts2 = Counter(r["section_id"] for r in rows if r["section_id"])
        still_dup2 = {sid for sid, cnt in id_counts2.items() if cnt > 1}
        if still_dup2:
            seen_occ: dict[str, int] = {}
            for r in rows:
                sid = r["section_id"]
                if sid in still_dup2:
                    seen_occ[sid] = seen_occ.get(sid, 0) + 1
                    r["section_id"] = f"{sid} ({seen_occ[sid]})"
            for r in rows:
                if r["_parent_row_idx"] is not None:
                    r["parent_id"] = rows[r["_parent_row_idx"]]["section_id"]

    for r in rows:
        if r["_parent_row_idx"] is not None:
            r["parent_id"] = rows[r["_parent_row_idx"]]["section_id"]
    final_ids = {r["section_id"] for r in rows if r["section_id"]}
    for r in rows:
        if r["parent_id"] and (r["parent_id"] not in final_ids or r["parent_id"] == r["section_id"]):
            r["parent_id"] = ""
        r.pop("_parent_row_idx", None)
        r.pop("_enclosing_any_idx", None)

    stem = args.out_stem or doc_dir.name
    csv_path = doc_dir / f"{stem}-sections.csv"
    json_path = doc_dir / f"{stem}-sections.json"
    fields = ["depth", "section_id", "section_name", "id_kind", "parent_id", "body"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_id = sum(1 for r in rows if r["section_id"])
    print(f"Sections: {len(rows)}  ({n_id} with identifier, {len(rows) - n_id} headings without)")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
