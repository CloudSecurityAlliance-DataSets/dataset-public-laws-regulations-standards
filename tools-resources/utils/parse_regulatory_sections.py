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
    # US / State statute sections: "22757.10. Short Title", "715D.1 Short title", "47-18-3201. Short title", "RCW 19.373.010", "NRS 603A.010", "§ 899-aa."
    (re.compile(r"^((?:RCW\s+\d+\.\d+\.\d+|NRS\s+\d+[A-Z]?\.\d+|\d+\s+ILCS\s+\d+/\d+(?:\.\d+)?|§+\s*\d+[\dA-Za-z\.\-]*|\d{1,3}-\d{1,3}-\d{2,5}|\d{2,5}[A-Z]?\.\d+(?:\.\d+)?))\.?\s*[:\-–—]?\s+(.+)$", re.IGNORECASE), "statute"),
    # SECTION 1 / SEC. 101 / Sec. 15 / Section 2-501 / Section (1) / S1.1-01: "SECTION 1. Legislative Findings and Declarations"
    (re.compile(r"^((?:SECTION|SEC\.?)\s+(?:\d+[A-Za-z]?(?:[\.\-–]\d+[A-Za-z]?)*|\(\d+\)|\([ivxlcdm]+\)|[IVXLCDM]+)|S\d+\.\d+-\d+)(?![\.\-–]\d)\s*(?:[:\.\-–—]+|\s+)\s*(.+)$", re.IGNORECASE), "section_word"),
    # Pillar I / Pillar 1 / Pillar (i) / Pillar One / Eje Estratégico 1 / Handlungsfeld 1: "Pillar I: AI Use Restrictions ..."
    (re.compile(r"^((?:Pillar|Pilier|Pilar|Pijler|Eje\s+Estrat[eé]gico|Handlungsfeld)\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+|\(\d+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))(?![\.\-–]\d)\s*(?:[:\.\-–—]+|\s+)\s*(.+)$", re.IGNORECASE), "pillar"),
    # Division A / Title I / Subtitle A / Part I / Part 1 / Part (1) / Part One / Раздел I / Розділ I / Teil 1 / Partie 1: "Part I: ..."
    (re.compile(r"^((?:Division|Title|Subtitle|Part|Partie|Parte|Teil|Deel|Del|Část|Časť|Раздел|Розділ|Часть|Частина)\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+(?:\.\d+)?|\(\d+\)|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))(?![\.\-–]\d)\s*(?:[:\.\-–—]+|\s+)\s*(.+)$", re.IGNORECASE), "part"),
    # CHAPTER 25.1 / Subchapter A / Chapter 1 / Chapter One / Глава 1 / Kapitel 1 / Chapitre 1 / Capítulo 1: "CHAPTER 25.1. Transparency in ..."
    (re.compile(r"^((?:SUBCHAPTER|CHAPTER|Chapitre|Cap[ií]tulo|Capitolo|Kapitel|Hoofdstuk|Kapitola|Poglavje|Rozdzia[łl]|Глава|BAHAGIAN)\s+(?:\d+[A-Za-z]?(?:\.\d+)?|\(\d+\)|[IVXLCDM]+|\([ivxlcdm]+\)|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))(?![\.\-–]\d)\s*(?:[:\.\-–—]+|\s+)\s*(.+)$", re.IGNORECASE), "chapter"),
    # Chinese & Japanese chapter/section/article/supplementary-provision markers: "第一章 ...", "第１ はじめに", "第一节 ...", "第一条（目的）", "附則第一条（施行期日）"
    (re.compile(r"^(第[一二三四五六七八九十百千0-9０-９]+[章篇编部編])\s*[:\.\-–—　]?\s*(.+)$"), "chapter"),
    (re.compile(r"^(第[一二三四五六七八九十百千0-9０-９]+)[\s　]+(.+)$"), "chapter"),
    (re.compile(r"^(第[一二三四五六七八九十百千0-9０-９]+[节節])\s*[:\.\-–—　]?\s*(.+)$"), "part"),
    (re.compile(r"^((?:附則(?:（[^）]+）)?\s*)?第[一二三四五六七八九十百千0-9０-９]+[条條](?:の[一二三四五六七八九十0-9０-９]+)?)\s*[:\.\-–—　]?\s*(.+)$"), "section_word"),
    (re.compile(r"^((?:\d+-)?ИЛОВА)\s*[:\.\-–—]?\s*(.*)$", re.IGNORECASE), "annex"),
    (re.compile(r"^((?:[IVXLCDM]+|\d+)-(?:боб|бўлим|тарау))\s*[:\.\-–—]?\s*(.*)$", re.IGNORECASE), "chapter"),
    # CJK top-level & parenthesized numbering: "一、...", "（一）...", "（１）..." (excluding prose clauses like "一、二线城市...")
    (re.compile(r"^([一二三四五六七八九十壹貳參肆伍陸柒捌玖拾]+)[、．\.]\s*([^，]+)$"), "cjk_major"),
    (re.compile(r"^([（\(][一二三四五六七八九十0-9０-９]+[）\)])\s*(.+)$"), "cjk_sub"),
    # Artículo / Artigo / Article / Điều / Thrust: "ARTÍCULO 1. Objeto..."
    (re.compile(r"^((?:Art[ií]culo|Artigo|Article|Điều|Thrust\s*#?)\s*\d+(?:\.\d+)*[º°]?)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "section_word"),
    # Strategic Objective 1.1 / Objective 1.1 / Objective 2a / Implementation 6.1 / Línea Estratégica 1.1
    (re.compile(r"^((?:Strategic\s+)?Objective\s+\d+[a-z]?(?:\.\d+)*|Implementation\s+\d+(?:\.\d+)*|L[ií]nea\s+Estrat[eé]gica\s+\d+(?:\.\d+)*)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "objective"),
    # Initiative 1.1.1 / Eylem 1.1: Title
    (re.compile(r"^((?:Initiative|Eylem)\s+\d+(?:\.\d+)+)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "initiative"),
    # Goal 1 / Priority 1 / Strategic Priority 1 / Línea de acción 1 / Line of action 1 / Principle 1 / Recommendation 1 / Finding 1: Title
    (re.compile(r"^((?:Goal|Objetivo|(?:Strategic\s+)?Priority|Stratejik\s+Öncelik|L[ií]nea\s+de\s+acci[oó]n|Line\s+of\s+action|Principle|Recommendation|Finding)\s+(?:[IVXLCDM]+|\d+(?:\.\d+)*))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "goal"),
    # Annex / Appendix / Schedule A / 1 / I: Title
    (re.compile(r"^((?:Annex|Annexe|Anexo|Anhang|Bijlage|Appendix|Schedule)\s+(?:[A-Z]|\d+|[IVXLCDM]+))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "annex"),
    # Standalone identifiers without trailing title (e.g., "Principle 1", "Appendix A", "Section 2-501", "附則", "附則（...）")
    (re.compile(r"^(附則(?:（[^）]+）)?|(?:Division|Title|Subtitle|Subchapter|Pillar|Pilier|Pilar|Pijler|Part|Partie|Parte|Teil|Chapter|Chapitre|Cap[ií]tulo|Kapitel|Глава|Раздел|Розділ|Section|Sec\.|Article|Art[ií]culo|Annex|Appendix|Schedule|Principle|Goal|Objetivo|(?:Strategic\s+)?Priority|Stratejik\s+Öncelik|L[ií]nea\s+de\s+acci[oó]n|Line\s+of\s+action|Objective|Finding|Recommendation|(?:附則(?:（[^）]+）)?\s*)?第[一二三四五六七八九十百千0-9０-９]+[章篇编部編节節条條](?:の[一二三四五六七八九十0-9０-９]+)?)\s*(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+[A-Za-z]?(?:[\.\-–]\d+[A-Za-z]?)*|\(\d+\)|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)?)\.?$", re.IGNORECASE), "standalone_id"),
    # Roman-numeral dotted subsection: "I.1 Title" / "II.10 Title"
    (re.compile(r"^([IVX]{1,4}\.\d{1,2})\.?\s*[:\-–—]?\s+(.+)$"), "numbered"),
    # Roman numeral section: "I. Introduction" / "II. Our Vision" / "I Purpose" / "II Japan's National Interests"
    (re.compile(r"^([IVX]{1,4})(?:\.\s+|\s+(?=[A-Z\u00c0-\u024f\u0400-\u04ff][a-z\u00df-\u024f\u0430-\u044f]))(.+)$"), "roman"),
    # Capital-letter section: "A. Innovative Europe" / "B. Making the EU..."
    (re.compile(r"^([A-Z])\.\s+([A-Z\u00c0-\u024f\u0400-\u04ff].+)$"), "letter"),
    # Plain hierarchical numbering "1.1 Title" / "1.1. Title" / "2.3.1 Title"
    (re.compile(r"^(\d{1,2}(?:\.\d{1,2}){1,3})\.?\s*[:\-–—]?\s+(?!(?:M€|B€|€|\$|£|%|million|billion|trillion)\b)(.+)$", re.IGNORECASE), "numbered"),
    # Single-number section heading "1. Introduction" / "1 Introduction" (excluding "4 x SSBN" force counts, "30 June 2018" dates, and "13 QUADRILLION" magnitude callouts)
    (re.compile(r"^(\d{1,3})(?:[:\.\-–—]\s+(?!(?i:quadrillion|trillion|billion|million|thousand|percent)\b)|\s+(?![xX]\b)(?!(?i:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|quadrillion|trillion|billion|million|thousand|percent)\b)(?!.*\b\d+\s+[xX]\s+))([A-Z\u00c0-\u024f\u0400-\u04ff\u0590-\u06ff\u0e00-\u0e7f\u4e00-\u9fff].+)$"), "numbered"),
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
    if len(cleaned) > 310:
        return "", cleaned, ""
    if re.search(r"(?:\.\s*){3,}\d+\s*$", cleaned):
        return "", cleaned, ""
    for pat, kind in ID_PATTERNS:
        m = pat.match(cleaned)
        if m:
            if m.lastindex and m.lastindex >= 2:
                title_part = m.group(2).strip()
                has_delim = bool(re.match(r"^" + re.escape(m.group(1)) + r"\s*[:\.\-–—]+", cleaned))
                if not has_delim and title_part and re.match(r"^[a-z]", title_part):
                    continue
                if (pat is ID_PATTERNS[-1][0] or kind in ("letter", "roman")) and title_part and not (
                    title_part[0].isupper() or "\u0590" <= title_part[0] <= "\u9fff"
                ):
                    continue
                sid_clean = m.group(1).rstrip(".")
                return sid_clean, (title_part or sid_clean), kind
            sid_val = m.group(1).rstrip(".")
            if kind == "standalone_id":
                low_sid = sid_val.lower()
                if re.match(r"^(?:section|sec\.|article|art[ií]culo)\b", low_sid) or re.search(r"[条條](?:の[一二三四五六七八九十0-9０-９]+)?$", sid_val):
                    kind = "section_word"
                elif re.match(r"^(?:subchapter|chapter|chapitre|cap[ií]tulo|kapitel|глава)\b", low_sid) or sid_val.startswith("附則") or re.search(r"[章篇编部編]$", sid_val):
                    kind = "chapter"
                elif re.match(r"^(?:division|title|subtitle|part|partie|parte|teil|раздел|розділ)\b", low_sid) or re.search(r"[节節]$", sid_val):
                    kind = "part"
                elif re.match(r"^(?:pillar|pilier|pilar|pijler)\b", low_sid):
                    kind = "pillar"
                elif re.match(r"^(?:annex|appendix|schedule)\b", low_sid):
                    kind = "annex"
                elif low_sid.startswith("objective"):
                    kind = "objective"
                else:
                    kind = "goal"
            return sid_val, sid_val, kind
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
            f"Strategic Priority {p_num}",
            f"Priority {p_num}",
        ]
        for cand in candidates:
            if cand.strip() in existing_ids:
                return cand.strip()
    m_rsub = re.match(r"^([IVX]{1,4})\.\d+$", section_id)
    if m_rsub and existing_ids:
        r_tok = m_rsub.group(1)
        r_num = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}.get(r_tok, 0)
        for cand in (f"1.{r_num}" if r_num else "", r_tok, f"Objective {r_tok}"):
            if cand and cand in existing_ids:
                return cand
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
        low_p, low_c = pid.lower(), child_id.lower()
        if pkind == "part":
            if low_p.startswith("division") and low_c.startswith(("title", "subtitle", "part")):
                return True
            if low_p.startswith("title") and low_c.startswith(("subtitle", "part")):
                return True
            if low_p.startswith("subtitle") and low_c.startswith("part"):
                return True
        if pkind == "chapter" and low_p.startswith("chapter") and low_c.startswith("subchapter"):
            return True
        if pkind == "section_word" and pid.startswith("SECTION ") and re.search(r"\d+[\-–]\d+", child_id):
            return True
        return False
    if child_kind == "annex":
        return pkind in ("part", "chapter", "roman")
    if child_kind in ("pillar", "part", "chapter", "roman", "letter"):
        return pkind in ("part", "chapter", "roman", "annex") or (
            child_kind == "pillar" and pkind == "numbered"
        )
    if child_kind in ("objective", "section_word", "statute"):
        if re.match(r"^Implementation\s+\d+\.\d+$", child_id, re.IGNORECASE):
            return False
        if child_kind == "section_word" and pkind == "numbered" and "." not in pid:
            return True
        return pkind in ("pillar", "part", "chapter", "roman", "annex")
    if child_kind in ("goal", "standalone_id", "initiative"):
        return pkind in ("pillar", "part", "chapter", "roman", "annex", "section_word", "goal") or (
            pkind == "numbered" and "." not in pid
        )
    if child_kind == "cjk_major":
        return pkind in ("part", "chapter", "roman", "annex")
    if child_kind == "cjk_sub":
        return pkind in ("cjk_major", "part", "chapter", "roman", "annex")
    if child_kind == "numbered":
        if "." in child_id:
            return False
        return pkind in ("roman", "part", "chapter", "pillar", "annex", "section_word", "letter", "cjk_major", "cjk_sub")
    return False


def normalize_body(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"\\([_*\[\]\(\)\-\.])", r"\1", s)
    s = re.sub(r"<a id=\"[^\"]*\"></a>", "", s)
    s = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", s)
    s = re.sub(r"\{\d+\}-+", "", s)
    s = "\n".join(l.rstrip() for l in s.splitlines())
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

    md_files = sorted(
        p for p in doc_dir.glob("*.md")
        if not p.name.endswith(("-metadata.md", "-processed.md", "-definitions.md"))
        and not p.name.startswith("README")
    )
    if not md_files:
        md_files = sorted(
            p for p in doc_dir.glob("*.md")
            if not p.name.endswith("-metadata.md")
            and not p.name.startswith("README")
        )
    if not md_files:
        raise SystemExit(f"No source markdown in {doc_dir}")
    stem_cand = args.out_stem or doc_dir.name
    preferred = [p for p in md_files if p.stem == stem_cand]
    md = (preferred[0] if preferred else md_files[0]).read_text(encoding="utf-8", errors="replace")

    headings = list(HEADING_RE.finditer(md))
    min_enc_depth = 1 if sum(1 for h in headings if len(h.group(1)) == 1) > 1 else 2
    rows = []
    seen_ids: set[str] = set()
    latest_row_by_id: dict[str, int] = {}
    ancestor_row_by_depth: dict[int, int] = {}
    ancestor_id_row_by_depth: dict[int, int] = {}

    for i, m in enumerate(headings):
        depth = len(m.group(1))
        section_id, section_name, id_kind = parse_heading(m.group(2))
        for d in [k for k in list(ancestor_row_by_depth) if k >= depth]:
            del ancestor_row_by_depth[d]
        for d in [k for k in list(ancestor_id_row_by_depth) if k >= depth]:
            del ancestor_id_row_by_depth[d]
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
        elif depth >= 3:
            for d in range(depth - 1, 1, -1):
                if d in ancestor_id_row_by_depth:
                    cand_idx = ancestor_id_row_by_depth[d]
                    if rows[cand_idx].get("section_id"):
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

    # Ensure child section depth is always strictly greater than its parent's depth
    changed_depth = True
    while changed_depth:
        changed_depth = False
        for r in rows:
            pidx = r.get("_parent_row_idx")
            if pidx is not None and rows[pidx]["depth"] >= r["depth"]:
                r["depth"] = rows[pidx]["depth"] + 1
                changed_depth = True

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
                base_pid = re.sub(r"\s*\(\d+\)$", "", pid.split(": ")[-1])
                if sid.startswith(f"{base_pid}.") or sid.startswith(f"{base_pid} "):
                    continue
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
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_id = sum(1 for r in rows if r["section_id"])
    print(f"Sections: {len(rows)}  ({n_id} with identifier, {len(rows) - n_id} headings without)")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
