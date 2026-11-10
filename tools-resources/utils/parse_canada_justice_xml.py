#!/usr/bin/env python3
"""Reproducible parser for Justice Canada / Parliament of Canada legislative XML.

Converts `<stem>.xml` in a document directory into:
  - `<stem>.md`             (structured ATX Markdown including Parts, Headings, Sections, Enacted Acts, and Schedules)
  - `<stem>-sections.csv`   (structured section rows with part, heading, section_id, marginal_note, subsection_count, body)
  - `<stem>-sections.json`  (JSON array matching the CSV rows)

Handles:
  - Standard consolidated statutes (`<Statute>`) and parliamentary bills/assented acts (`<Bill>`)
  - Nested `<AmendedText>` containing enacted Acts (`<BillInternal>`) or multi-section statutory amendments,
    emitting individual rows for every nested section with containing Act/Clause context so provisions are
    never flattened into single rows
  - Top-level and nested `<Schedule>` elements (including `<TableGroup>` tables, `<Oath>`, and `<BillPiece>`)

Usage:
    python3 tools-resources/utils/parse_canada_justice_xml.py <doc-dir> [--out-stem STEM] [--title TITLE]
"""
import argparse
import copy
import csv
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

BLOCK_TAGS = {
    "Paragraph",
    "Subparagraph",
    "Clause",
    "Subclause",
    "Label",
    "MarginalNote",
    "Definition",
    "HistoricalNote",
    "HistoricalNoteSubItem",
    "ContinuedSectionSubsection",
    "ContinuedParagraph",
    "Provision",
    "Item",
    "Oath",
    "OriginatingRef",
    "TitleText",
}

ENACTED_ACT_ACRONYMS = {
    "Critical Cyber Systems Protection Act": "CCSPA",
    "National Security and Intelligence Review Agency Act": "NSIRA",
    "Avoiding Complicity in Mistreatment by Foreign Entities Act": "ACMFEA",
    "Intelligence Commissioner Act": "ICA",
    "Communications Security Establishment Act": "CSEA",
    "Digital Safety Act": "DSA",
    "Digital Safety Commission of Canada Act": "DSCCA",
    "Protecting Privacy and Consumer Data Act": "PPCDA",
    "Consumer Privacy Protection Act": "CPPA",
    "Personal Information and Data Protection Tribunal Act": "PIDPTA",
    "Artificial Intelligence and Data Act": "AIDA",
}


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def text_of(el) -> str:
    """Extract normalized text from an XML element, preserving spaces around structural child elements."""
    if el is None:
        return ""
    parts: list[str] = []

    def _walk(node):
        t_name = strip_ns(node.tag)
        is_block = t_name in BLOCK_TAGS
        if is_block:
            parts.append(" ")
        if t_name == "Leader":
            parts.append(" ... ")
        if node.text:
            parts.append(node.text)
        for ch in node:
            _walk(ch)
            if ch.tail:
                parts.append(ch.tail)
        if is_block:
            parts.append(" ")

    _walk(el)
    joined = unicodedata.normalize("NFKC", "".join(parts))
    joined = re.sub(r"\s+", " ", joined).strip()
    return joined


def render_table_group(tg_el) -> tuple[list[str], list[str]]:
    """Render a `<TableGroup>` element into Markdown table lines and plain-text lines."""
    md_out: list[str] = []
    txt_out: list[str] = []
    for table in tg_el.findall(".//table"):
        tgroup = table.find("tgroup")
        if tgroup is None:
            continue
        headers: list[str] = []
        thead = tgroup.find("thead")
        if thead is not None:
            thead_rows = [[text_of(entry) for entry in row.findall("entry")] for row in thead.findall("row")]
            if thead_rows:
                n_cols = max(len(r) for r in thead_rows)
                for col_idx in range(n_cols):
                    col_parts = [r[col_idx] for r in thead_rows if col_idx < len(r) and r[col_idx]]
                    headers.append(": ".join(col_parts))
        body_rows: list[list[str]] = []
        tbody = tgroup.find("tbody")
        if tbody is not None:
            for row in tbody.findall("row"):
                cells = [text_of(entry) for entry in row.findall("entry")]
                if any(cells):
                    body_rows.append(cells)
        if not headers and body_rows:
            headers = [f"Column {i + 1}" for i in range(len(body_rows[0]))]
        if headers:
            md_out.append("| " + " | ".join(headers) + " |")
            md_out.append("| " + " | ".join(["---"] * len(headers)) + " |")
            if body_rows:
                for r in body_rows:
                    padded = r + [""] * max(0, len(headers) - len(r))
                    md_out.append("| " + " | ".join(padded[: len(headers)]) + " |")
                    row_txt = " — ".join(c for c in padded[: len(headers)] if c)
                    if row_txt:
                        txt_out.append(row_txt)
            else:
                txt_out.append("Columns: " + " | ".join(headers))
            md_out.append("")
    return md_out, txt_out


def extract_enacted_act_info(bill_internal_el, fallback_clause: str) -> tuple[str, str]:
    """Return (act_short_name, id_prefix) for a `<BillInternal>` element."""
    body = bill_internal_el.find("Body")
    if body is not None:
        for sec in body.findall("Section"):
            mn = text_of(sec.find("MarginalNote"))
            sec_txt = text_of(sec)
            if "short title" in mn.lower() or "may be cited as the" in sec_txt.lower():
                m = re.search(r"may be cited as the\s+([^.]+)\.", sec_txt, re.IGNORECASE)
                if m:
                    act_name = m.group(1).strip()
                    acr = ENACTED_ACT_ACRONYMS.get(act_name)
                    if not acr:
                        words = [w[0].upper() for w in re.findall(r"[A-Z][a-z]+", act_name)]
                        acr = "".join(words) if words else f"s{fallback_clause}"
                    return act_name, acr
    lt = text_of(bill_internal_el.find("LongTitle"))
    return (lt or f"Clause {fallback_clause} Enacted Act"), f"s{fallback_clause}"


def parse_canadian_xml_statute(xml_bytes: bytes, doc_title: str) -> tuple[str, list[dict]]:
    """Parse Justice Canada / Parliament of Canada legislative XML into Markdown and section rows."""
    root = ET.fromstring(xml_bytes)
    rows: list[dict] = []
    md_lines: list[str] = [f"# {doc_title}", ""]
    header_line_by_row: dict[int, int] = {}
    current_part = ""
    current_heading = ""

    def collect_and_strip_nested_amended(el: ET.Element, ctx_lbl: str = "") -> list[tuple[str, ET.Element]]:
        found: list[tuple[str, ET.Element]] = []
        for child in list(el):
            tag = strip_ns(child.tag)
            if tag == "AmendedText" and (child.find(".//Section") is not None or child.find(".//Heading") is not None):
                found.append((ctx_lbl, copy.deepcopy(child)))
                el.remove(child)
            elif tag != "Section":
                sub_l = text_of(child.find("Label")) if tag in ("Subsection", "Paragraph", "Subparagraph") else ""
                next_lbl = f"{ctx_lbl}{sub_l}" if sub_l else ctx_lbl
                found.extend(collect_and_strip_nested_amended(child, next_lbl))
        return found

    def emit_section(sec_el, part_ctx: str, heading_ctx: str, id_prefix: str = ""):
        nonlocal current_part, current_heading
        sec_label = text_of(sec_el.find("Label"))
        marginal = text_of(sec_el.find("MarginalNote"))
        full_sec_id = f"{id_prefix}:{sec_label}" if (id_prefix and sec_label) else (sec_label or id_prefix)

        all_amended: list[tuple[str, ET.Element]] = []

        sec_header = f"Section {full_sec_id}: {marginal}" if marginal else f"Section {full_sec_id}"
        hdr_line_idx = len(md_lines)
        md_lines.append(f"#### {sec_header}")
        md_lines.append("")

        paras: list[str] = []
        subsecs = sec_el.findall("Subsection")
        if subsecs:
            for direct_am in sec_el.findall("AmendedText"):
                if direct_am.find(".//Section") is not None or direct_am.find(".//Heading") is not None:
                    all_amended.append(("", direct_am))
            for sub in subsecs:
                sub_lbl = text_of(sub.find("Label"))
                sub_mn = text_of(sub.find("MarginalNote"))
                sub_copy = copy.deepcopy(sub)
                for rm_tag in ("MarginalNote", "Label"):
                    for rm in list(sub_copy.findall(rm_tag)):
                        sub_copy.remove(rm)
                all_amended.extend(collect_and_strip_nested_amended(sub_copy, sub_lbl))
                sub_body = text_of(sub_copy)
                prefix = f"{sub_lbl} " if sub_lbl else ""
                if sub_mn:
                    prefix = f"[{sub_mn}] {prefix}"
                line_str = f"{prefix}{sub_body}".strip()
                if line_str:
                    paras.append(line_str)
                    md_lines.append(line_str)
                    md_lines.append("")
        else:
            sec_copy = copy.deepcopy(sec_el)
            for rm_tag in ("MarginalNote", "Label"):
                for rm in list(sec_copy.findall(rm_tag)):
                    sec_copy.remove(rm)
            all_amended.extend(collect_and_strip_nested_amended(sec_copy, ""))
            sec_body = text_of(sec_copy)
            if sec_body:
                paras.append(sec_body)
                md_lines.append(sec_body)
                md_lines.append("")

        rows.append(
            {
                "part": part_ctx,
                "heading": heading_ctx,
                "section_id": full_sec_id,
                "marginal_note": marginal,
                "subsection_count": len(subsecs),
                "body": "\n\n".join(paras),
            }
        )
        header_line_by_row[len(rows) - 1] = hdr_line_idx

        for sub_lbl, amended in all_amended:
            bill_internal = amended.find("BillInternal")
            saved_part, saved_heading = current_part, current_heading
            clause_ref = f"{sec_label}{sub_lbl}" if sub_lbl else sec_label
            if bill_internal is not None:
                act_name, act_acr = extract_enacted_act_info(bill_internal, clause_ref)
                base_part = f"{part_ctx} — {act_name} (Clause {clause_ref})" if part_ctx else f"{act_name} (Clause {clause_ref})"
                current_part = base_part
                current_heading = ""
                long_title = text_of(bill_internal.find("LongTitle"))
                preamble_el = bill_internal.find("Preamble")
                preamble_paras = [text_of(p) for p in preamble_el.findall(".//Provision")] if preamble_el is not None else []
                if long_title or preamble_paras:
                    md_lines.append(f"### {act_name} — Long Title and Preamble")
                    md_lines.append("")
                    pre_lines = ([long_title] if long_title else []) + [p for p in preamble_paras if p]
                    for pl in pre_lines:
                        md_lines.append(pl)
                        md_lines.append("")
                    rows.append(
                        {
                            "part": base_part,
                            "heading": "Long Title and Preamble",
                            "section_id": f"{act_acr}:Preamble",
                            "marginal_note": long_title or "Preamble",
                            "subsection_count": len(preamble_paras),
                            "body": "\n\n".join(pre_lines),
                        }
                    )
                bi_body = bill_internal.find("Body")
                if bi_body is not None:
                    walk_container(bi_body, part_prefix=base_part, id_prefix=act_acr)
            else:
                nested_part = f"{part_ctx} (Clause {clause_ref})" if part_ctx else f"Clause {clause_ref}"
                nested_id_prefix = f"{id_prefix}.s{clause_ref}" if id_prefix else f"s{clause_ref}"
                current_part = nested_part
                walk_container(amended, part_prefix=nested_part, id_prefix=nested_id_prefix)
            current_part, current_heading = saved_part, saved_heading

    def walk_container(container, part_prefix: str = "", id_prefix: str = ""):
        nonlocal current_part, current_heading
        for child in container:
            tag = strip_ns(child.tag)
            if tag == "Heading":
                level = child.attrib.get("level", "1")
                label = text_of(child.find("Label"))
                title = text_of(child.find("TitleText"))
                full_h = " — ".join(x for x in (label, title) if x)
                if level == "1":
                    current_part = f"{part_prefix} — {full_h}" if (part_prefix and full_h) else (full_h or part_prefix)
                    current_heading = ""
                    if full_h:
                        md_lines.append(f"## {current_part}")
                        md_lines.append("")
                else:
                    current_heading = full_h
                    if full_h:
                        md_lines.append(f"### {full_h}")
                        md_lines.append("")
            elif tag == "Section":
                emit_section(child, current_part or part_prefix, current_heading, id_prefix=id_prefix)
            elif tag in ("SectionPiece", "RelatedOrNotInForce", "BillPiece"):
                walk_container(child, part_prefix=current_part or part_prefix, id_prefix=id_prefix)

    body = root.find("Body")
    if body is not None:
        walk_container(body)

    # Walk top-level and nested <Schedule> elements
    def walk_schedule(sched_el, parent_label: str = ""):
        nonlocal current_part, current_heading
        sfh = sched_el.find("ScheduleFormHeading")
        lbl = text_of(sfh.find("Label")) if sfh is not None else ""
        orig_ref = text_of(sfh.find("OriginatingRef")) if sfh is not None else ""
        title_txt = text_of(sfh.find("TitleText")) if sfh is not None else ""
        sched_id = lbl or title_txt or sched_el.attrib.get("id", "SCHEDULE")
        if parent_label and lbl and parent_label != lbl:
            sched_part = f"{parent_label} — {lbl}"
        else:
            sched_part = lbl or title_txt or "SCHEDULE"
        if title_txt and title_txt != sched_part:
            sched_heading_str = f"{sched_part}: {title_txt}"
        else:
            sched_heading_str = sched_part
        if orig_ref:
            sched_heading_str = f"{sched_heading_str} {orig_ref}"

        nested_schedules = sched_el.findall("Schedule")
        if nested_schedules and not sched_el.findall("TableGroup") and not sched_el.findall("Oath") and not sched_el.findall("BillPiece"):
            for ns in nested_schedules:
                walk_schedule(ns, parent_label=lbl or parent_label)
            return

        md_lines.append(f"## {sched_heading_str}")
        md_lines.append("")

        body_parts: list[str] = []
        item_count = 0

        for oath in sched_el.findall("Oath"):
            oath_txt = text_of(oath)
            if oath_txt:
                md_lines.append(oath_txt)
                md_lines.append("")
                body_parts.append(oath_txt)
                item_count += 1

        for tg in sched_el.findall("TableGroup"):
            md_tbl, txt_tbl = render_table_group(tg)
            md_lines.extend(md_tbl)
            body_parts.extend(txt_tbl)
            item_count += len(txt_tbl)

        for bp in sched_el.findall("BillPiece"):
            saved_part, saved_heading = current_part, current_heading
            current_part = sched_part
            current_heading = title_txt
            before_len = len(rows)
            walk_container(bp, part_prefix=sched_part, id_prefix=sched_id.replace(" ", "_"))
            current_part, current_heading = saved_part, saved_heading
            if len(rows) > before_len:
                return

        # Emit schedule row (even when schedule is an empty placeholder such as NSA 2017 Schedule)
        if not body_parts and orig_ref:
            body_parts.append(f"{sched_heading_str}")
        rows.append(
            {
                "part": sched_part,
                "heading": orig_ref,
                "section_id": sched_id,
                "marginal_note": title_txt or sched_part,
                "subsection_count": item_count,
                "body": "\n\n".join(body_parts),
            }
        )

        for ns in nested_schedules:
            walk_schedule(ns, parent_label=lbl or parent_label)

    for sched in root.findall("Schedule"):
        walk_schedule(sched)

    # Disambiguate any source-label collisions (e.g., NSIRA Act s. 15.1 or Bill C-59 PART 5 s. 2)
    id_counts: dict[str, int] = {}
    for r in rows:
        sid = r["section_id"]
        id_counts[sid] = id_counts.get(sid, 0) + 1
    dup_ids = {sid for sid, cnt in id_counts.items() if cnt > 1}
    if dup_ids:
        used_ids = {r["section_id"] for r in rows if r["section_id"] not in dup_ids}
        occ_counter: dict[str, int] = {}
        for idx, r in enumerate(rows):
            sid = r["section_id"]
            if sid not in dup_ids:
                continue
            occ_counter[sid] = occ_counter.get(sid, 0) + 1
            part_short = r["part"].split(" — ")[0].strip() if r["part"] else ""
            ctx = part_short or r["heading"] or r["marginal_note"] or f"#{occ_counter[sid]}"
            candidate = f"{sid} ({ctx})"
            if candidate in used_ids:
                candidate = f"{sid} ({ctx} #{occ_counter[sid]})"
            used_ids.add(candidate)
            r["section_id"] = candidate
            if idx in header_line_by_row:
                mn = r["marginal_note"]
                md_lines[header_line_by_row[idx]] = f"#### Section {candidate}: {mn}" if mn else f"#### Section {candidate}"

    return "\n".join(md_lines).strip() + "\n", rows


def main():
    ap = argparse.ArgumentParser(description="Parse Justice Canada / Parliament of Canada XML into Markdown and structured sections.")
    ap.add_argument("doc_dir", help="Document directory containing <stem>.xml")
    ap.add_argument("--out-stem", default=None, help="Output filename stem (default: directory name)")
    ap.add_argument("--title", default=None, help="Document title for H1 heading (default: read from metadata or XML LongTitle)")
    args = ap.parse_args()

    doc_dir = Path(args.doc_dir).resolve()
    stem = args.out_stem or doc_dir.name
    xml_path = doc_dir / f"{stem}.xml"
    if not xml_path.is_file():
        raise SystemExit(f"Missing XML file: {xml_path}")

    doc_title = args.title
    if not doc_title:
        meta_path = doc_dir / f"{stem}-metadata.json"
        if meta_path.is_file():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            doc_title = meta.get("name")
    if not doc_title:
        doc_title = stem

    md, rows = parse_canadian_xml_statute(xml_path.read_bytes(), doc_title)
    (doc_dir / f"{stem}.md").write_text(md, encoding="utf-8")

    fieldnames = ["part", "heading", "section_id", "marginal_note", "subsection_count", "body"]
    csv_path = doc_dir / f"{stem}-sections.csv"
    json_path = doc_dir / f"{stem}-sections.json"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {stem}.md ({len(md):,} chars) and {len(rows)} rows to {csv_path.name} / {json_path.name}")


if __name__ == "__main__":
    main()
