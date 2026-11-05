#!/usr/bin/env python3
"""Acquire, extract to Markdown, parse sections, and generate metadata for Track 2 (#131).

Covers all 46 document directories across 5 namespaces:
  1. reference/publicsafety.gc.ca/ (20 directories)
  2. reference/canada.ca/ (5 directories)
  3. regulation/parl.ca/ (4 directories)
  4. reference/whitehouse.gov/ (10 directories)
  5. reference/gov.uk/ (7 directories)
"""
import collections
import csv
import json
import re
import subprocess
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import markdownify
import pymupdf
import requests
from bs4 import BeautifulSoup

_CANDIDATE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = (
    _CANDIDATE_ROOT
    if (_CANDIDATE_ROOT / "tools-resources").is_dir()
    else Path("/Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards")
)
PARSE_SECTIONS_SCRIPT = REPO_ROOT / "tools-resources/utils/parse_regulatory_sections.py"
PARSE_CANADA_XML_SCRIPT = REPO_ROOT / "tools-resources/utils/parse_canada_justice_xml.py"
S3_TIMESTAMP = "2026-11-04T05-00-00Z"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}


def fetch_with_retry(url: str, headers: dict | None = None, timeout: int = 45, retries: int = 4) -> requests.Response:
    hdrs = headers or HEADERS
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=hdrs, timeout=timeout)
            if r.status_code >= 500 and attempt + 1 < retries:
                time.sleep(2 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt + 1 >= retries:
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}")

LICENSE_CA = {
    "spdx": "OGL-Canada-2.0",
    "redistribution": "permitted_with_attribution",
    "derivatives": "permitted",
    "publicly_redistributable": True,
    "license_text_url": "https://open.canada.ca/en/open-government-licence-canada",
    "notes": "Open Government Licence – Canada (and Reproduction of Federal Law Order for federal statutes).",
}

LICENSE_US = {
    "spdx": "LicenseRef-US-Government-Work",
    "redistribution": "permitted",
    "derivatives": "permitted",
    "publicly_redistributable": True,
    "license_text_url": "https://www.usa.gov/government-works",
    "notes": "Work of the U.S. Federal Government; in the public domain in the United States under 17 U.S.C. § 105.",
}

LICENSE_UK = {
    "spdx": "OGL-UK-3.0",
    "redistribution": "permitted_with_attribution",
    "derivatives": "permitted",
    "publicly_redistributable": True,
    "license_text_url": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "notes": "Open Government Licence v3.0 — Crown copyright.",
}


def html_to_clean_markdown(html_text: str, base_url: str, doc_title: str | None = None) -> str:
    """Extract main content from a government HTML page, resolve relative links, and convert to clean ATX Markdown."""
    soup = BeautifulSoup(html_text, "html.parser")
    # Remove scripts, styles, nav, footer, share widgets, breadcrumbs, page details
    for sel in [
        "script", "style", "noscript", "nav", "footer", "header.navbar",
        ".pagedetails", "#wb-dtmd", ".wb-share", ".gc-pg-hlpfl",
        ".gem-c-share-links", ".gem-c-print-link", ".gem-c-contents-list",
        ".govuk-breadcrumbs", ".gem-c-contextual-sidebar",
    ]:
        for tag in soup.select(sel):
            tag.decompose()

    main = (
        soup.select_one("main")
        or soup.select_one("#wb-cont")
        or soup.select_one(".govspeak")
        or soup.select_one("article")
        or soup.body
        or soup
    )
    for a_tag in main.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href:
            continue
        m_wb = re.match(r"^(?:https?://web\.archive\.org)?/web/\d+[a-z_]*/(https?://.+)$", href)
        if m_wb:
            a_tag["href"] = m_wb.group(1)
        elif href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        else:
            a_tag["href"] = urllib.parse.urljoin(base_url, href)

    md = markdownify.markdownify(
        str(main),
        heading_style="ATX",
        bullets="-",
        strip=["img"],
    )
    # Normalize whitespace and blank lines
    lines = [line.rstrip() for line in md.splitlines()]
    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if doc_title and not cleaned.startswith("# "):
        cleaned = f"# {doc_title}\n\n{cleaned}"
    return cleaned + "\n"


def sort_blocks_column_aware(blocks: list[dict], page_w: float, page_h: float, repeated_edges: set[str]) -> list[dict]:
    """Order PDF text blocks cleanly across single-column, two-column, and bridged full-width layouts."""
    text_blocks = []
    for b in blocks:
        if b.get("type") != 0:
            continue
        # Check if entire block is an edge header/footer or page number
        lines_keep = []
        for l in b.get("lines", []):
            l_text = re.sub(r"\s+", " ", "".join(s.get("text", "") for s in l.get("spans", []))).strip()
            if not l_text:
                continue
            lb = l.get("bbox", (0, 0, 0, 0))
            if (lb[1] < 70 or lb[3] > page_h - 70) and (
                l_text.lower() in repeated_edges
                or re.match(r"^(page\s+)?(\d+|[ivxlcdm]+)$", l_text, re.I)
            ):
                continue
            lines_keep.append(l)
        if not lines_keep:
            continue
        b_copy = dict(b)
        b_copy["lines"] = lines_keep
        text_blocks.append(b_copy)

    col_items = []
    for b in text_blocks:
        x0, y0, x1, y1 = b.get("bbox", (0, 0, 0, 0))
        first_l = ""
        if b.get("lines"):
            first_l = re.sub(r"\s+", " ", "".join(s.get("text", "") for s in b["lines"][0].get("spans", []))).strip()
        is_band_heading = (
            x0 <= page_w * 0.20
            and bool(re.match(r"^(?:[IVX]{1,4}\.\d{1,2}|\d{1,2}\.\d{1,2})\s+[A-Z]{2,}", first_l))
            and not any(
                ob is not b
                and ob.get("bbox", (0, 0, 0, 0))[0] >= page_w * 0.46
                and not (ob.get("bbox", (0, 0, 0, 0))[3] < y0 - 2 or ob.get("bbox", (0, 0, 0, 0))[1] > y1 + 2)
                for ob in text_blocks
            )
        )
        if is_band_heading:
            col = "full"
        elif x1 <= page_w * 0.54:
            col = "left"
        elif x0 >= page_w * 0.46:
            col = "right"
        else:
            col = "full"
        col_items.append((col, y0, x0, b))

    def order_band(band_items: list[tuple[str, float, float, dict]]) -> list[dict]:
        has_l = any(c == "left" for c, _, _, _ in band_items)
        has_r = any(c == "right" for c, _, _, _ in band_items)
        if has_l and has_r:
            left_b = [item[3] for item in sorted(band_items, key=lambda t: (t[1], t[2])) if item[0] == "left"]
            right_b = [item[3] for item in sorted(band_items, key=lambda t: (t[1], t[2])) if item[0] == "right"]
            return left_b + right_b
        return [item[3] for item in sorted(band_items, key=lambda t: (round(t[1] / 4), t[2]))]

    full_blocks = sorted([item for item in col_items if item[0] == "full"], key=lambda t: (t[1], t[2]))
    non_full = [item for item in col_items if item[0] != "full"]
    ordered = []
    prev_y = -float("inf")
    for _, fy, fx, fb in full_blocks:
        band = [item for item in non_full if prev_y <= item[1] < fy]
        ordered.extend(order_band(band))
        ordered.append(fb)
        prev_y = fy
    tail_band = [item for item in non_full if item[1] >= prev_y]
    ordered.extend(order_band(tail_band))
    return ordered


def is_toc_or_rollup_page(blocks: list[dict]) -> bool:
    """Detect Table of Contents or Roll-Up summary pages so TOC lines are not promoted into section headings."""
    lines = []
    for b in blocks:
        for l in b.get("lines", []):
            txt = re.sub(r"\s+", " ", "".join(s.get("text", "") for s in l.get("spans", []))).strip()
            if txt:
                lines.append(txt)
    if not lines:
        return False
    head_text = " ".join(lines[:6]).lower()
    if any(k in head_text for k in ("table of contents", "contents", "roll-up of implementation plan initiatives")):
        return True
    dot_leaders = sum(1 for t in lines if " . . " in t or "...." in t or re.search(r"\.{3,}\s*\d+$", t))
    if dot_leaders >= 3:
        return True
    standalone_nums = sum(1 for t in lines if re.match(r"^\d{1,3}$", t))
    if standalone_nums >= 5:
        return True
    # Detect Roll-Up continuation pages in US Implementation Plans (bare X.Y.Z lines without "Initiative Number:")
    has_init_label = any(t.lower().startswith("initiative number:") for t in lines)
    bare_inits = sum(1 for t in lines if re.match(r"^\d+\.\d+\.\d+\s+[A-Z]", t))
    if not has_init_label and bare_inits >= 2:
        return True
    return False


def pdf_bytes_to_markdown(pdf_bytes: bytes, doc_title: str) -> tuple[str, int]:
    """Convert PDF bytes to structured Markdown using column-aware PyMuPDF block ordering + TOC + font-size analysis."""
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    num_pages = len(doc)
    toc = doc.get_toc()
    toc_map = {}
    for lvl, title, _ in toc:
        t_clean = re.sub(r"\s+", " ", title).strip()
        if re.match(r"^Page\s+\d+$", t_clean, re.I):
            continue
        norm = re.sub(r"[^a-z0-9]+", "", t_clean.lower())
        if len(norm) >= 3 and norm not in toc_map:
            toc_map[norm] = min(max(lvl, 1), 4)

    size_counts = collections.Counter()
    edge_line_counts = collections.Counter()
    for page in doc:
        page_h = page.rect.height
        d = page.get_text("dict")
        for b in d.get("blocks", []):
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                l_txt = re.sub(r"\s+", " ", "".join(s.get("text", "") for s in l.get("spans", []))).strip()
                if not l_txt:
                    continue
                lb = l.get("bbox", (0, 0, 0, 0))
                if lb[1] < 70 or lb[3] > page_h - 70:
                    edge_line_counts[l_txt.lower()] += 1
                for s in l.get("spans", []):
                    txt = s.get("text", "").strip()
                    if txt:
                        sz = round(s.get("size", 10.0) * 2) / 2
                        size_counts[sz] += len(txt)
    body_size = size_counts.most_common(1)[0][0] if size_counts else 10.5
    repeated_edges = {k for k, c in edge_line_counts.items() if c >= 2}

    def classify_line(l_text: str, sz: float, is_bold: bool, on_toc_page: bool) -> int | None:
        if len(l_text) > 160 or len(l_text) < 2:
            return None
        if " . . . " in l_text or "....." in l_text or re.search(r"\.{4,}\s*\d+$", l_text):
            return None
        if on_toc_page:
            if re.match(r"^(table of contents|contents|roll-up of implementation plan initiatives)$", l_text, re.I):
                return 2
            return None
        # Do not promote US Implementation Plan field labels into standalone headings
        if re.match(r"^(Initiative Description|NCS Reference|Responsible Agency:.*|Contributing Entities:.*|Completion Date:.*)$", l_text, re.I):
            return None
        norm = re.sub(r"[^a-z0-9]+", "", l_text.lower())
        if norm in toc_map:
            return min(toc_map[norm] + 1, 4)
        # Allow multi-line display headings (sz >= body_size + 1.5) to wrap across lines ending with ','
        if l_text.endswith((".", ";")) and not re.match(r"^(?:[IVX]+|\d+(?:\.\d+)*)\.$", l_text):
            return None
        if l_text.endswith(",") and sz < body_size + 1.5:
            return None
        if sz >= body_size + 3.5:
            return 2
        if sz >= body_size + 1.2:
            return 3
        if (is_bold or sz > body_size) and re.match(
            r"^(?:PART|CHAPTER|SECTION|PILLAR|ANNEX|APPENDIX|STRATEGIC OBJECTIVE|OBJECTIVE|IMPLEMENTATION\s+\d|INITIATIVE|GOAL|PRIORITY|EXECUTIVE SUMMARY|FOREWORD|INTRODUCTION|CONCLUSION|OVERVIEW|BACKGROUND|ABBREVIATIONS|DEFINITIONS|(?:[IVX]{1,4}|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ])(?:\.\s*\S*|\s+[A-Z])|[0-9]+(\.[0-9]+)+\.?$|[0-9]+(\.[0-9]+)+\.?\s+[A-Z]|[0-9]{1,2}\.\s+[A-Z]|\([0-9]{1,2}\)\s+[A-Z]|\([ivx]{1,4}\)\s+[A-Z])",
            l_text,
        ):
            if re.match(r"^(?:PART|CHAPTER|SECTION|PILLAR|(?:[IVX]{1,4}|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ])(?:\.|\s+)[A-Z])", l_text):
                return 2
            if re.match(r"^\((?:[0-9]{1,2}|[ivx]{1,4})\)\s+[A-Z]", l_text):
                return 4
            return 3
        return None

    md_lines = [f"# {doc_title}", ""]
    active_h2_norm = ""

    for page in doc:
        page_w = page.rect.width
        page_h = page.rect.height
        d = page.get_text("dict")
        ordered_blocks = sort_blocks_column_aware(d.get("blocks", []), page_w, page_h, repeated_edges)
        on_toc_page = is_toc_or_rollup_page(ordered_blocks)

        pending_heading_lvl = None
        pending_heading_parts = []
        para_parts = []
        pending_init_num = None

        def flush_para():
            nonlocal para_parts
            if para_parts:
                joined = " ".join(para_parts)
                joined = re.sub(r"-\s+([a-z])", r"-\1", joined)
                md_lines.append(joined)
                md_lines.append("")
                para_parts = []

        def flush_heading(force: bool = True):
            nonlocal pending_heading_lvl, pending_heading_parts, active_h2_norm
            if pending_heading_parts:
                if not force and len(pending_heading_parts) == 1 and re.match(
                    r"^(?:(?:PILLAR|PART|CHAPTER|SECTION|STRATEGIC OBJECTIVE|OBJECTIVE|ANNEX|APPENDIX)\s+[IVX0-9A-Z()]+|\d+(?:\.\d+)*\.?|[IVX]+\.)$",
                    pending_heading_parts[0].strip(),
                    re.I,
                ):
                    return
                combined = " ".join(pending_heading_parts)
                combined = re.sub(r"\s+", " ", combined).strip()
                combined = re.sub(r"\b(INFOR|COMMUNI|ORGANI|OPERATIONALI|ADMINI|INFRA|VULNERA|TELECOMMUNI)-\s+([A-Z]{2,})\b", r"\1\2", combined)
                if len(pending_heading_parts) >= 2 and re.match(
                    r"^(PILLAR|PART|CHAPTER|SECTION|STRATEGIC OBJECTIVE|OBJECTIVE|ANNEX|APPENDIX)\s+([IVX]+|\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|[A-Z])$",
                    pending_heading_parts[0].strip(),
                    re.I,
                ):
                    combined = f"{pending_heading_parts[0].strip()}: {' '.join(p.strip() for p in pending_heading_parts[1:])}"
                lvl_use = min(pending_heading_lvl or 2, 4)
                norm_h = re.sub(r"[^a-z0-9]+", "", combined.lower())
                if norm_h and norm_h == active_h2_norm:
                    # Suppress repeated running chapter header that matches the active level-2 heading
                    pending_heading_lvl = None
                    pending_heading_parts = []
                    return
                if lvl_use == 2 and norm_h:
                    active_h2_norm = norm_h
                h_prefix = "#" * lvl_use
                md_lines.append(f"{h_prefix} {combined}")
                md_lines.append("")
                pending_heading_lvl = None
                pending_heading_parts = []

        for b in ordered_blocks:
            b_lines = []
            for l in b.get("lines", []):
                l_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u2007]+", " ", "".join(s.get("text", "") for s in l.get("spans", [])))
                l_text = re.sub(r"\s+", " ", l_text).strip()
                if not l_text:
                    continue
                max_sz = max((s.get("size", body_size) for s in l.get("spans", []) if s.get("text", "").strip()), default=body_size)
                if max_sz >= body_size + 1.5:
                    l_text = re.sub(
                        r"^([IVX])(?:\s+([IVX]))?(?:\s+([IVX]))?\s*\.\s*$",
                        lambda m_r: "".join(g for g in m_r.groups() if g) + ".",
                        l_text,
                    )
                    l_text = re.sub(r"^(\d)\s*\.\s*$", r"\1.", l_text)
                    l_text = re.sub(r"^(\d)\s*\.\s*(\d)\s+", r"\1.\2 ", l_text)
                total_chars = sum(len(s.get("text", "").strip()) for s in l.get("spans", []))
                bold_chars = sum(
                    len(s.get("text", "").strip())
                    for s in l.get("spans", [])
                    if s.get("text", "").strip() and (bool(s.get("flags", 0) & 16) or "bold" in s.get("font", "").lower())
                )
                is_bold = total_chars > 0 and (bold_chars >= total_chars * 0.6)
                b_lines.append((l_text, max_sz, is_bold))
            if not b_lines:
                continue

            first_txt = b_lines[0][0]
            m_init_num = re.match(r"^Initiative Number:\s*([0-9]+(?:\.[0-9]+)+)\s*$", first_txt, re.I)
            if m_init_num and len(b_lines) == 1:
                flush_heading()
                flush_para()
                pending_init_num = m_init_num.group(1)
                continue

            m_init_title = re.match(r"^Initiative Title:\s*(.+)$", first_txt, re.I)
            if m_init_title:
                flush_heading()
                flush_para()
                title_parts = [m_init_title.group(1)] + [x[0] for x in b_lines[1:]]
                full_title = " ".join(title_parts)
                full_title = re.sub(r"-\s+([a-z])", r"-\1", full_title)
                full_title = re.sub(r"\s+", " ", full_title).strip()
                if pending_init_num:
                    md_lines.append(f"#### Initiative {pending_init_num}: {full_title}")
                    pending_init_num = None
                else:
                    md_lines.append(f"#### {full_title}")
                md_lines.append("")
                continue

            if pending_init_num:
                # Fallback if Initiative Number was not immediately followed by Initiative Title
                md_lines.append(f"#### Initiative {pending_init_num}")
                md_lines.append("")
                pending_init_num = None

            if len(b_lines) == 1 and re.match(r"^(Initiative Description|NCS Reference)$", first_txt, re.I):
                flush_heading()
                flush_para()
                para_parts.append(f"**{first_txt}:**")
                continue

            # Track whether we have entered non-bold body lines in a multi-line body-size block
            seen_body_line_in_block = False

            for l_text, max_sz, is_bold in b_lines:
                if not is_bold and max_sz <= body_size + 0.5:
                    seen_body_line_in_block = True
                allow_heading = (not seen_body_line_in_block) or (
                    is_bold
                    and bool(
                        re.match(
                            r"^(?:(?:PART|CHAPTER|SECTION|PILLAR|ANNEX|APPENDIX)\s+\S+|(?:[IVX]{1,4}|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ])(?:\.|\s+)[A-Z]|\d{1,2}(?:\.\d{1,2})*\.\s+[A-Z]|\(\d{1,2}\)\s+[A-Z]|\([ivx]{1,4}\)\s+[A-Z])",
                            l_text,
                        )
                    )
                )
                h_lvl = classify_line(l_text, max_sz, is_bold, on_toc_page) if allow_heading else None
                if (
                    h_lvl is None
                    and pending_heading_lvl is not None
                    and not seen_body_line_in_block
                    and (is_bold or max_sz > body_size + 0.5)
                    and bool(re.match(r"^[A-Z\s,\-–—\(\)’']+$", l_text))
                ):
                    h_lvl = pending_heading_lvl
                if h_lvl is not None:
                    flush_para()
                    if pending_heading_lvl is not None and (
                        pending_heading_lvl == h_lvl
                        or re.match(r"^(?:(?:PILLAR|PART|CHAPTER|SECTION|STRATEGIC OBJECTIVE|OBJECTIVE|ANNEX|APPENDIX)\s+\S+|\d+(?:\.\d+)*\.?|[IVX]+\.)$", pending_heading_parts[-1].strip(), re.I)
                    ):
                        pending_heading_lvl = min(pending_heading_lvl, h_lvl)
                        pending_heading_parts.append(l_text)
                    else:
                        flush_heading()
                        pending_heading_lvl = h_lvl
                        pending_heading_parts = [l_text]
                else:
                    flush_heading()
                    para_parts.append(l_text)
            flush_heading(force=False)
            # Keep para_parts open if it is only '**Initiative Description:**' or '**NCS Reference:**'
            if para_parts not in (["**Initiative Description:**"], ["**NCS Reference:**"]):
                flush_para()
        flush_heading(force=True)
        flush_para()

    return "\n".join(md_lines).strip() + "\n", num_pages


def run_parse_sections(doc_dir: Path, stem: str) -> tuple[int, int]:
    """Run tools-resources/utils/parse_regulatory_sections.py on doc_dir."""
    subprocess.run(
        [sys.executable, str(PARSE_SECTIONS_SCRIPT), str(doc_dir), "--out-stem", stem],
        check=True,
        capture_output=True,
        text=True,
    )
    sections_json = doc_dir / f"{stem}-sections.json"
    rows = json.loads(sections_json.read_text(encoding="utf-8"))
    with_id = sum(1 for r in rows if r.get("section_id"))
    return len(rows), with_id


def write_metadata(
    doc_dir: Path,
    stem: str,
    *,
    secid: str,
    name: str,
    acronym: str,
    version: str,
    owner: str,
    doc_type: str,
    subtype: list[str],
    description: str,
    cloud_rel: str,
    ai_rel: str,
    license_obj: dict,
    source_url: str,
    text_used_url: str,
    published: str,
    active: bool,
    retired_date: str | None = None,
    supersedes: str | None,
    superseded_by: str | None,
    tool_str: str,
    extraction_notes: str,
    end_state: str,
    end_reason: str,
):
    meta = {
        "secid": secid,
        "name": name,
        "acronym": acronym,
        "alternate_names": [],
        "version": version,
        "publication_id": stem,
        "owner": owner,
        "type": doc_type,
        "subtype": subtype,
        "description": description,
        "relationToCloudSecurity": cloud_rel,
        "relationToAISecurity": ai_rel,
        "license": license_obj,
        "links": {
            "wikipedia": "",
            "source": source_url,
            "textUsed": text_used_url,
            "csaLocation": "",
        },
        "lifecycle": {
            "published": published,
            "active": active,
            "supersedes": supersedes,
            "supersededBy": superseded_by,
            "retiredFromActiveUse": None if active else retired_date,
            "notes": "",
        },
        "current_extraction": (
            {
                "s3_timestamp": S3_TIMESTAMP,
                "tool": tool_str,
                "tool_version": "1.0",
                "extraction_host": "local",
                "flags": [],
                "force_ocr": False,
                "notes": extraction_notes,
            }
            if tool_str
            else None
        ),
        "extraction_history": (
            [
                {
                    "s3_timestamp": S3_TIMESTAMP,
                    "status": "current",
                    "reason": "Track 2 National Security & Cybersecurity Strategy corpus extraction (#131)",
                    "tool": tool_str,
                }
            ]
            if tool_str
            else []
        ),
        "scope": {},
        "notes": "" if tool_str else extraction_notes,
        "desired_end_state": {
            "state": end_state,
            "reason": end_reason,
        },
    }
    meta_path = doc_dir / f"{stem}-metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Manifest of all 46 documents
# ---------------------------------------------------------------------------

PUBLIC_SAFETY_DOCS = [
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy/2025",
        "stem": "national-cyber-security-strategy-2025",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2025",
        "name": "Securing Canada's Digital Future: Canada's National Cyber Security Strategy (2025)",
        "acronym": "NCSS",
        "version": "2025",
        "published": "2025-02-05",
        "active": True,
        "supersedes": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2018",
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-cbr-scrt-strtg-2025/index-en.aspx"],
        "description": "Canada's third National Cyber Security Strategy (2025), establishing a whole-of-society approach to cyber resilience, critical infrastructure protection, cybercrime disruption, and international cyber deterrence.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy/2018",
        "stem": "national-cyber-security-strategy-2018",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2018",
        "name": "National Cyber Security Strategy: Canada's Vision for Security and Prosperity in the Digital Age (2018)",
        "acronym": "NCSS",
        "version": "2018",
        "published": "2018-06-12",
        "active": False,
        "supersedes": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2010",
        "superseded_by": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2025",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-cbr-scrt-strtg/index-en.aspx"],
        "description": "Canada's second National Cyber Security Strategy (2018), organized around three pillars: Secure and Resilient Canadian Systems, an Innovative and Adaptive Cyber Ecosystem, and Effective Leadership and Governance (establishing the Canadian Centre for Cyber Security and RCMP NC3).",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy/2010",
        "stem": "national-cyber-security-strategy-2010",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2010",
        "name": "Canada's Cyber Security Strategy: For a Stronger and More Prosperous Canada (2010)",
        "acronym": "CCSS",
        "version": "2010",
        "published": "2010-10-03",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy@2018",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/archive-cbr-scrt-strtgy/archive-index-en.aspx"],
        "description": "Canada's first National Cyber Security Strategy (2010), structured around three pillars: Securing Government Systems, Partnering to Secure Vital Cyber Systems Outside the Federal Government, and Helping Canadians to be Secure Online.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-action-plan/2019-2024",
        "stem": "national-cyber-security-action-plan-2019-2024",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-action-plan@2019-2024",
        "name": "National Cyber Security Action Plan (2019-2024)",
        "acronym": "NCSAP",
        "version": "2019-2024",
        "published": "2019-06-26",
        "active": True,
        "supersedes": "secid:reference/publicsafety.gc.ca/national-cyber-security-action-plan@2010-2015",
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-cbr-scrt-strtg-2019/index-en.aspx"],
        "description": "Five-year implementation roadmap (2019-2024) for the 2018 National Cyber Security Strategy, detailing funded federal initiatives across Public Safety Canada, CSE, RCMP, ISED, and partner departments.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-action-plan/2010-2015",
        "stem": "national-cyber-security-action-plan-2010-2015",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-action-plan@2010-2015",
        "name": "Action Plan 2010-2015 for Canada's Cyber Security Strategy",
        "acronym": "NCSAP",
        "version": "2010-2015",
        "published": "2013-04-01",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/publicsafety.gc.ca/national-cyber-security-action-plan@2019-2024",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ctn-pln-cbr-scrt/index-en.aspx"],
        "description": "Five-year action plan (2010-2015) tracking the deliverables under Canada's 2010 Cyber Security Strategy.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy-mid-term-review/2022",
        "stem": "national-cyber-security-strategy-mid-term-review-2022",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy-mid-term-review@2022",
        "name": "National Cyber Security Strategy 2019-2024: Report on the Mid-term Review (2022)",
        "acronym": "",
        "version": "2022",
        "published": "2022-09-01",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-cbr-scrt-strtg-2019-md-trm/index-en.aspx"],
        "description": "Public Safety Canada mid-term review report assessing changes in the cyber threat landscape (ransomware, critical infrastructure targeting, supply chain threats) and progress halfway through the 2019-2024 National Cyber Security Action Plan.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation/2022",
        "stem": "national-cyber-security-strategy-evaluation-2022",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation@2022",
        "name": "Mid-Term Evaluation of the National Cyber Security Strategy (2022)",
        "acronym": "",
        "version": "2022",
        "published": "2022-05-19",
        "active": True,
        "supersedes": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation@2017",
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2022-vtn-ntnl-cbr-strtgy/index-en.aspx"],
        "description": "Formal horizontal evaluation of the 2018 National Cyber Security Strategy conducted under the Treasury Board Policy on Results, examining governance, information sharing, and performance measurement.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation/2017",
        "stem": "national-cyber-security-strategy-evaluation-2017",
        "secid": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation@2017",
        "name": "Horizontal Evaluation of Canada's Cyber Security Strategy (2017)",
        "acronym": "",
        "version": "2017",
        "published": "2017-09-29",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/publicsafety.gc.ca/national-cyber-security-strategy-evaluation@2022",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/vltn-cnd-scrt-strtg/index-en.aspx"],
        "description": "Horizontal evaluation of the 2010 Canada's Cyber Security Strategy, identifying fragmentation in federal cyber incident coordination and recommending a consolidated operational model.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/cyber-review-consultations-report-2017",
        "stem": "cyber-review-consultations-report-2017",
        "secid": "secid:reference/publicsafety.gc.ca/cyber-review-consultations-report-2017",
        "name": "Cyber Review Consultations Report (2017)",
        "acronym": "",
        "version": "",
        "published": "2017-02-28",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2017-cybr-rvw-cnslttns-rprt/index-en.aspx"],
        "description": "Summary of public, industry, and academic consultations conducted during the 2016 Cyber Review that informed the 2018 National Cyber Security Strategy.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/federal-cyber-incident-response-plan/2023",
        "stem": "federal-cyber-incident-response-plan-2023",
        "secid": "secid:reference/publicsafety.gc.ca/federal-cyber-incident-response-plan@2023",
        "name": "Federal Cyber Incident Response Plan (2023)",
        "acronym": "FCIRP",
        "version": "2023",
        "published": "2023-02-01",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/fdrl-cbr-ncdnt-rspns-pln-2023/index-en.aspx"],
        "description": "Government of Canada coordination framework for responding to non-government/critical-infrastructure cyber security incidents, defining severity levels, governance committees, and escalation pathways alongside the Federal Emergency Response Plan (FERP).",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-strategy-critical-infrastructure/2009",
        "stem": "national-strategy-critical-infrastructure-2009",
        "secid": "secid:reference/publicsafety.gc.ca/national-strategy-critical-infrastructure@2009",
        "name": "National Strategy for Critical Infrastructure (2009)",
        "acronym": "NSCI",
        "version": "2009",
        "published": "2009-05-01",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/srtg-crtcl-nfrstrctr/index-en.aspx"],
        "description": "Foundational federal-provincial-territorial strategy establishing Canada's 10 critical infrastructure sectors, sector networks, and all-hazards risk management approach.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/action-plan-critical-infrastructure/2021-2023",
        "stem": "action-plan-critical-infrastructure-2021-2023",
        "secid": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2021-2023",
        "name": "Action Plan for Critical Infrastructure (2021-2023)",
        "acronym": "APCI",
        "version": "2021-2023",
        "published": "2021-07-01",
        "active": True,
        "supersedes": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2018-2020",
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2021-ctn-pln-crtcl-nfrstrctr/index-en.aspx"],
        "description": "Fourth multi-year Action Plan implementing Canada's National Strategy for Critical Infrastructure (2021-2023), incorporating COVID-19 pandemic lessons and cyber-physical dependency risk management.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/action-plan-critical-infrastructure/2018-2020",
        "stem": "action-plan-critical-infrastructure-2018-2020",
        "secid": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2018-2020",
        "name": "Action Plan for Critical Infrastructure (2018-2020)",
        "acronym": "APCI",
        "version": "2018-2020",
        "published": "2018-05-01",
        "active": False,
        "supersedes": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2014-2017",
        "superseded_by": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2021-2023",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/archive-pln-crtcl-nfrstrctr-2018-20/index-en.aspx"],
        "description": "Third Action Plan for Critical Infrastructure (2018-2020) under Canada's National Strategy for Critical Infrastructure.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/action-plan-critical-infrastructure/2014-2017",
        "stem": "action-plan-critical-infrastructure-2014-2017",
        "secid": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2014-2017",
        "name": "Action Plan for Critical Infrastructure (2014-2017)",
        "acronym": "APCI",
        "version": "2014-2017",
        "published": "2014-05-01",
        "active": False,
        "supersedes": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2010",
        "superseded_by": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2018-2020",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/archive-pln-crtcl-nfrstrctr-2014-17/index-en.aspx"],
        "description": "Second Action Plan for Critical Infrastructure (2014-2017) under Canada's National Strategy for Critical Infrastructure.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/action-plan-critical-infrastructure/2010",
        "stem": "action-plan-critical-infrastructure-2010",
        "secid": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2010",
        "name": "Action Plan for Critical Infrastructure (2010)",
        "acronym": "APCI",
        "version": "2010",
        "published": "2010-05-01",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/publicsafety.gc.ca/action-plan-critical-infrastructure@2014-2017",
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/archive-pln-crtcl-nfrstrctr/index-en.aspx"],
        "description": "Inaugural Action Plan for Critical Infrastructure (2010) establishing Canada's National Cross Sector Forum and 10 critical infrastructure sector networks.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/critical-infrastructure-consultation-report-2022",
        "stem": "critical-infrastructure-consultation-report-2022",
        "secid": "secid:reference/publicsafety.gc.ca/critical-infrastructure-consultation-report-2022",
        "name": "Renewing Canada's Approach to Critical Infrastructure Resilience: What We Heard Report (2022)",
        "acronym": "",
        "version": "",
        "published": "2022-11-01",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/rnwng-cnd-pprch-crtcl-nfrstrctr-rslnc-2022/index-en.aspx"],
        "description": "Report on Public Safety Canada's targeted and public consultations on modernizing the National Strategy for Critical Infrastructure.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/counter-terrorism-strategy/2012",
        "stem": "counter-terrorism-strategy-2012",
        "secid": "secid:reference/publicsafety.gc.ca/counter-terrorism-strategy@2012",
        "name": "Building Resilience Against Terrorism: Canada's Counter-terrorism Strategy (2012)",
        "acronym": "",
        "version": "2012",
        "published": "2012-02-09",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/rslnc-gnst-trrrsm/index-en.aspx"],
        "description": "Canada's Counter-terrorism Strategy (2012), organized around four mutually reinforcing elements: Prevent, Detect, Deny, and Respond.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-security-green-paper-2016",
        "stem": "national-security-green-paper-2016",
        "secid": "secid:reference/publicsafety.gc.ca/national-security-green-paper-2016",
        "name": "Our Security, Our Rights: National Security Green Paper, 2016",
        "acronym": "",
        "version": "",
        "published": "2016-09-08",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-scrt-grn-ppr-2016/index-en.aspx"],
        "description": "Government of Canada consultation paper examining 10 areas of national security law and policy (including accountability, information sharing, cyber security, and intelligence oversight) prior to the introduction of the National Security Act, 2017 (Bill C-59).",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/national-security-consultations-report-2017",
        "stem": "national-security-consultations-report-2017",
        "secid": "secid:reference/publicsafety.gc.ca/national-security-consultations-report-2017",
        "name": "National Security Consultations: What We Learned Report (2017)",
        "acronym": "",
        "version": "",
        "published": "2017-05-25",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": ["https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2017-nsc-wwlr/index-en.aspx"],
        "description": "Synthesis of over 58,000 online responses and roundtables from the 2016 National Security Consultations, directly shaping the National Security Act, 2017 (Bill C-59) and the National Security Transparency Commitment.",
    },
    {
        "rel_dir": "reference/publicsafety.gc.ca/nstag-reports",
        "stem": "nstag-reports",
        "secid": "secid:reference/publicsafety.gc.ca/nstag-reports",
        "name": "National Security Transparency Advisory Group (NS-TAG) Reports",
        "acronym": "NS-TAG",
        "version": "",
        "published": "2024-03-01",
        "active": True,
        "supersedes": None,
        "superseded_by": None,
        "urls": [
            "https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/nstag-gctsn-dgtztn-ntnl-scrt-2024/index-en.aspx",
            "https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/2022-nstag-nsiirc-isnrccr/index-en.aspx",
        ],
        "description": "Independent advisory reports of the National Security Transparency Advisory Group (NS-TAG) examining digitization, information access, and institutional transparency across Canada's national security and intelligence community.",
    },
]

WHITEHOUSE_DOCS = [
    {
        "rel_dir": "reference/whitehouse.gov/national-security-strategy/2025",
        "stem": "national-security-strategy-2025",
        "secid": "secid:reference/whitehouse.gov/national-security-strategy@2025",
        "name": "National Security Strategy of the United States of America (2025)",
        "acronym": "NSS",
        "version": "2025",
        "published": "2025-12-04",
        "active": True,
        "supersedes": "secid:reference/whitehouse.gov/national-security-strategy@2022",
        "superseded_by": None,
        "pdf_url": "https://www.whitehouse.gov/wp-content/uploads/2025/12/2025-National-Security-Strategy.pdf",
        "source_url": "https://www.whitehouse.gov/wp-content/uploads/2025/12/2025-National-Security-Strategy.pdf",
        "description": "2025 National Security Strategy of the United States of America issued under 50 U.S.C. § 3043 (Goldwater-Nichols Act).",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-security-strategy/2022",
        "stem": "national-security-strategy-2022",
        "secid": "secid:reference/whitehouse.gov/national-security-strategy@2022",
        "name": "National Security Strategy of the United States of America (2022)",
        "acronym": "NSS",
        "version": "2022",
        "published": "2022-10-12",
        "active": False,
        "supersedes": "secid:reference/whitehouse.gov/national-security-strategy@2017",
        "superseded_by": "secid:reference/whitehouse.gov/national-security-strategy@2025",
        "pdf_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/10/Biden-Harris-Administrations-National-Security-Strategy-10.2022.pdf",
        "source_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/10/Biden-Harris-Administrations-National-Security-Strategy-10.2022.pdf",
        "description": "2022 Biden-Harris Administration National Security Strategy of the United States of America.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-security-strategy/2017",
        "stem": "national-security-strategy-2017",
        "secid": "secid:reference/whitehouse.gov/national-security-strategy@2017",
        "name": "National Security Strategy of the United States of America (2017)",
        "acronym": "NSS",
        "version": "2017",
        "published": "2017-12-18",
        "active": False,
        "supersedes": "secid:reference/whitehouse.gov/national-security-strategy@2015",
        "superseded_by": "secid:reference/whitehouse.gov/national-security-strategy@2022",
        "pdf_url": "https://trumpwhitehouse.archives.gov/wp-content/uploads/2017/12/NSS-Final-12-18-2017-0905.pdf",
        "source_url": "https://trumpwhitehouse.archives.gov/wp-content/uploads/2017/12/NSS-Final-12-18-2017-0905.pdf",
        "description": "2017 National Security Strategy of the United States of America structured around four vital national interests (Pillars I–IV).",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-security-strategy/2015",
        "stem": "national-security-strategy-2015",
        "secid": "secid:reference/whitehouse.gov/national-security-strategy@2015",
        "name": "National Security Strategy of the United States of America (2015)",
        "acronym": "NSS",
        "version": "2015",
        "published": "2015-02-06",
        "active": False,
        "supersedes": "secid:reference/whitehouse.gov/national-security-strategy@2010",
        "superseded_by": "secid:reference/whitehouse.gov/national-security-strategy@2017",
        "pdf_url": "https://obamawhitehouse.archives.gov/sites/default/files/docs/2015_national_security_strategy_2.pdf",
        "source_url": "https://obamawhitehouse.archives.gov/sites/default/files/docs/2015_national_security_strategy_2.pdf",
        "description": "2015 Obama Administration National Security Strategy of the United States of America.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-security-strategy/2010",
        "stem": "national-security-strategy-2010",
        "secid": "secid:reference/whitehouse.gov/national-security-strategy@2010",
        "name": "National Security Strategy of the United States of America (2010)",
        "acronym": "NSS",
        "version": "2010",
        "published": "2010-05-27",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/whitehouse.gov/national-security-strategy@2015",
        "pdf_url": "https://obamawhitehouse.archives.gov/sites/default/files/rss_viewer/national_security_strategy.pdf",
        "source_url": "https://obamawhitehouse.archives.gov/sites/default/files/rss_viewer/national_security_strategy.pdf",
        "description": "2010 Obama Administration National Security Strategy of the United States of America, including Securing Cyberspace under Security.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-cybersecurity-strategy/2026",
        "stem": "national-cybersecurity-strategy-2026",
        "secid": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2026",
        "name": "President Trump's Cyber Strategy for America (2026)",
        "acronym": "",
        "version": "2026",
        "published": "2026-03-06",
        "active": True,
        "supersedes": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2023",
        "superseded_by": None,
        "pdf_url": "https://www.whitehouse.gov/wp-content/uploads/2026/03/President-Trumps-Cyber-Strategy-for-America.pdf",
        "source_url": "https://www.whitehouse.gov/releases/2026/03/white-house-unveils-president-trumps-cyber-strategy-for-america/",
        "description": "2026 United States National Cybersecurity Strategy ('President Trump's Cyber Strategy for America'), organized around six policy pillars: Shape Adversary Behavior, Promote Common Sense Regulation, Modernize and Secure Federal Government Networks, Secure Critical Infrastructure, Sustain Superiority in Critical and Emerging Technologies, and Build Talent and Capacity.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-cybersecurity-strategy/2023",
        "stem": "national-cybersecurity-strategy-2023",
        "secid": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2023",
        "name": "National Cybersecurity Strategy (2023)",
        "acronym": "NCS",
        "version": "2023",
        "published": "2023-03-02",
        "active": False,
        "supersedes": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2018",
        "superseded_by": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2026",
        "pdf_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/03/National-Cybersecurity-Strategy-2023.pdf",
        "source_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/03/National-Cybersecurity-Strategy-2023.pdf",
        "description": "2023 United States National Cybersecurity Strategy (Office of the National Cyber Director), organized around five pillars and 27 strategic objectives rebalancing the responsibility to defend cyberspace and realigning incentives to favor long-term investments.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-cybersecurity-strategy/2018",
        "stem": "national-cybersecurity-strategy-2018",
        "secid": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2018",
        "name": "National Cyber Strategy of the United States of America (2018)",
        "acronym": "NCS",
        "version": "2018",
        "published": "2018-09-20",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/whitehouse.gov/national-cybersecurity-strategy@2023",
        "pdf_url": "https://trumpwhitehouse.archives.gov/wp-content/uploads/2018/09/National-Cyber-Strategy.pdf",
        "source_url": "https://trumpwhitehouse.archives.gov/wp-content/uploads/2018/09/National-Cyber-Strategy.pdf",
        "description": "2018 National Cyber Strategy of the United States of America, structured around four pillars: Protect the American People, the Homeland, and the American Way of Life; Promote American Prosperity; Preserve Peace through Strength; and Advance American Influence.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan/2",
        "stem": "national-cybersecurity-strategy-implementation-plan-2",
        "secid": "secid:reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan@2",
        "name": "National Cybersecurity Strategy Implementation Plan Version 2 (2024)",
        "acronym": "NCSIP",
        "version": "2",
        "published": "2024-05-07",
        "active": True,
        "supersedes": "secid:reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan@1",
        "superseded_by": None,
        "pdf_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/05/National-Cybersecurity-Strategy-Implementation-Plan-Version-2.pdf",
        "source_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/05/National-Cybersecurity-Strategy-Implementation-Plan-Version-2.pdf",
        "description": "Office of the National Cyber Director (ONCD) Version 2 Implementation Plan for the 2023 National Cybersecurity Strategy, tracking 100 federal initiatives with responsible agencies and completion timelines.",
    },
    {
        "rel_dir": "reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan/1",
        "stem": "national-cybersecurity-strategy-implementation-plan-1",
        "secid": "secid:reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan@1",
        "name": "National Cybersecurity Strategy Implementation Plan Version 1 (2023)",
        "acronym": "NCSIP",
        "version": "1",
        "published": "2023-07-13",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/whitehouse.gov/national-cybersecurity-strategy-implementation-plan@2",
        "pdf_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/07/National-Cybersecurity-Strategy-Implementation-Plan-WH.gov_.pdf",
        "source_url": "https://bidenwhitehouse.archives.gov/wp-content/uploads/2023/07/National-Cybersecurity-Strategy-Implementation-Plan-WH.gov_.pdf",
        "description": "Office of the National Cyber Director (ONCD) Version 1 Implementation Plan for the 2023 National Cybersecurity Strategy, establishing over 65 high-impact federal initiatives across 18 agencies.",
    },
]

GOV_UK_DOCS = [
    {
        "rel_dir": "reference/gov.uk/national-security-strategy/2025",
        "stem": "national-security-strategy-2025",
        "secid": "secid:reference/gov.uk/national-security-strategy@2025",
        "name": "National Security Strategy 2025: Security for the British People in a Dangerous World",
        "acronym": "NSS",
        "version": "2025",
        "published": "2025-06-24",
        "active": True,
        "supersedes": "secid:reference/gov.uk/integrated-review@2023",
        "superseded_by": None,
        "html_url": "https://www.gov.uk/government/publications/national-security-strategy-2025-security-for-the-british-people-in-a-dangerous-world/national-security-strategy-2025-security-for-the-british-people-in-a-dangerous-world-html",
        "source_url": "https://www.gov.uk/government/publications/national-security-strategy-2025-security-for-the-british-people-in-a-dangerous-world",
        "description": "United Kingdom National Security Strategy 2025 ('Security for the British People in a Dangerous World', Cabinet Office), setting out the UK's overarching national security framework.",
    },
    {
        "rel_dir": "reference/gov.uk/national-security-strategy/2015",
        "stem": "national-security-strategy-2015",
        "secid": "secid:reference/gov.uk/national-security-strategy@2015",
        "name": "National Security Strategy and Strategic Defence and Security Review 2015: A Secure and Prosperous United Kingdom",
        "acronym": "NSS / SDSR",
        "version": "2015",
        "published": "2015-11-23",
        "active": False,
        "supersedes": "secid:reference/gov.uk/national-security-strategy@2010",
        "superseded_by": "secid:reference/gov.uk/integrated-review@2021",
        "pdf_url": "https://assets.publishing.service.gov.uk/media/5a74c796ed915d502d6caefc/52309_Cm_9161_NSS_SD_Review_web_only.pdf",
        "source_url": "https://www.gov.uk/government/publications/national-security-strategy-and-strategic-defence-and-security-review-2015",
        "description": "United Kingdom 2015 National Security Strategy and Strategic Defence and Security Review (Cm 9161), including the creation of the National Cyber Security Centre (NCSC).",
    },
    {
        "rel_dir": "reference/gov.uk/national-security-strategy/2010",
        "stem": "national-security-strategy-2010",
        "secid": "secid:reference/gov.uk/national-security-strategy@2010",
        "name": "A Strong Britain in an Age of Uncertainty: The National Security Strategy (2010)",
        "acronym": "NSS",
        "version": "2010",
        "published": "2010-10-18",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/gov.uk/national-security-strategy@2015",
        "pdf_url": "https://assets.publishing.service.gov.uk/media/5a74cb2de5274a3cb286738d/national-security-strategy.pdf",
        "source_url": "https://www.gov.uk/government/publications/the-national-security-strategy-a-strong-britain-in-an-age-of-uncertainty",
        "description": "United Kingdom 2010 National Security Strategy (Cm 7953), elevating hostile cyber attacks to a Tier One risk to UK national security.",
    },
    {
        "rel_dir": "reference/gov.uk/integrated-review/2023",
        "stem": "integrated-review-2023",
        "secid": "secid:reference/gov.uk/integrated-review@2023",
        "name": "Integrated Review Refresh 2023: Responding to a More Contested and Volatile World",
        "acronym": "IR23",
        "version": "2023",
        "published": "2023-03-13",
        "active": False,
        "supersedes": "secid:reference/gov.uk/integrated-review@2021",
        "superseded_by": "secid:reference/gov.uk/national-security-strategy@2025",
        "html_url": "https://www.gov.uk/government/publications/integrated-review-refresh-2023-responding-to-a-more-contested-and-volatile-world/integrated-review-refresh-2023-responding-to-a-more-contested-and-volatile-world",
        "source_url": "https://www.gov.uk/government/publications/integrated-review-refresh-2023-responding-to-a-more-contested-and-volatile-world",
        "description": "United Kingdom Integrated Review Refresh 2023 (CP 811), updating the 2021 Integrated Review of Security, Defence, Development and Foreign Policy.",
    },
    {
        "rel_dir": "reference/gov.uk/integrated-review/2021",
        "stem": "integrated-review-2021",
        "secid": "secid:reference/gov.uk/integrated-review@2021",
        "name": "Global Britain in a Competitive Age: The Integrated Review of Security, Defence, Development and Foreign Policy (2021)",
        "acronym": "IR21",
        "version": "2021",
        "published": "2021-03-16",
        "active": False,
        "supersedes": "secid:reference/gov.uk/national-security-strategy@2015",
        "superseded_by": "secid:reference/gov.uk/integrated-review@2023",
        "html_url": "https://www.gov.uk/government/publications/global-britain-in-a-competitive-age-the-integrated-review-of-security-defence-development-and-foreign-policy/global-britain-in-a-competitive-age-the-integrated-review-of-security-defence-development-and-foreign-policy",
        "source_url": "https://www.gov.uk/government/publications/global-britain-in-a-competitive-age-the-integrated-review-of-security-defence-development-and-foreign-policy",
        "description": "United Kingdom 2021 Integrated Review of Security, Defence, Development and Foreign Policy (CP 403), establishing the Strategic Framework including Sustaining Strategic Advantage through Science and Technology and Cyber Power.",
    },
    {
        "rel_dir": "reference/gov.uk/national-cyber-strategy/2022",
        "stem": "national-cyber-strategy-2022",
        "secid": "secid:reference/gov.uk/national-cyber-strategy@2022",
        "name": "National Cyber Strategy 2022: Pioneering a Cyber Future with the Whole of the UK",
        "acronym": "NCS",
        "version": "2022",
        "published": "2021-12-15",
        "active": True,
        "supersedes": "secid:reference/gov.uk/national-cyber-strategy@2016-2021",
        "superseded_by": None,
        "html_url": "https://www.gov.uk/government/publications/national-cyber-strategy-2022/national-cyber-security-strategy-2022",
        "source_url": "https://www.gov.uk/government/publications/national-cyber-strategy-2022",
        "description": "United Kingdom National Cyber Strategy 2022, organized around five pillars: Strengthening the UK cyber ecosystem; Building a resilient and prosperous digital UK; Taking the lead in the technologies vital to cyber power; Advancing UK global leadership and influence; and Detecting, disrupting and deterring our adversaries.",
    },
    {
        "rel_dir": "reference/gov.uk/national-cyber-strategy/2016-2021",
        "stem": "national-cyber-strategy-2016-2021",
        "secid": "secid:reference/gov.uk/national-cyber-strategy@2016-2021",
        "name": "National Cyber Security Strategy 2016 to 2021",
        "acronym": "NCSS",
        "version": "2016-2021",
        "published": "2016-11-01",
        "active": False,
        "supersedes": None,
        "superseded_by": "secid:reference/gov.uk/national-cyber-strategy@2022",
        "pdf_url": "https://assets.publishing.service.gov.uk/media/5a81914de5274a2e8ab54ae9/national_cyber_security_strategy_2016.pdf",
        "source_url": "https://www.gov.uk/government/publications/national-cyber-security-strategy-2016-to-2021",
        "description": "United Kingdom National Cyber Security Strategy 2016 to 2021 (HM Government), organized around Defend, Deter, and Develop.",
    },
]


PUB_DATE_BY_SECID = {
    d["secid"]: d["published"]
    for d in PUBLIC_SAFETY_DOCS + WHITEHOUSE_DOCS + GOV_UK_DOCS
}


def process_group1_publicsafety():
    print("\n=== Processing Group 1: reference/publicsafety.gc.ca/ (20 directories) ===")
    for item in PUBLIC_SAFETY_DOCS:
        doc_dir = REPO_ROOT / item["rel_dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = item["stem"]
        md_parts = []
        for idx, url in enumerate(item["urls"]):
            r = fetch_with_retry(url, headers=HEADERS, timeout=30)
            part_md = html_to_clean_markdown(r.text, url, item["name"] if idx == 0 else None)
            md_parts.append(part_md.strip())
        full_md = "\n\n---\n\n".join(md_parts) + "\n"
        (doc_dir / f"{stem}.md").write_text(full_md, encoding="utf-8")
        n_sec, n_id = run_parse_sections(doc_dir, stem)
        retired_date = PUB_DATE_BY_SECID.get(item["superseded_by"] or "") if not item["active"] else None
        write_metadata(
            doc_dir,
            stem,
            secid=item["secid"],
            name=item["name"],
            acronym=item["acronym"],
            version=item["version"],
            owner="Public Safety Canada",
            doc_type="Reference",
            subtype=["strategy"],
            description=item["description"],
            cloud_rel="Defines national cyber resilience, critical infrastructure protection, and government-wide incident coordination relevant to cloud service providers operating in Canada.",
            ai_rel="Addresses emerging digital technology threats, supply-chain security, and national security governance applicable to AI systems.",
            license_obj=LICENSE_CA,
            source_url=item["urls"][0],
            text_used_url=item["urls"][0],
            published=item["published"],
            active=item["active"],
            retired_date=retired_date,
            supersedes=item["supersedes"],
            superseded_by=item["superseded_by"],
            tool_str="requests + markdownify + tools-resources/utils/parse_regulatory_sections.py",
            extraction_notes=f"Extracted official Public Safety Canada HTML publication to Markdown ({len(full_md):,} chars) and parsed {n_sec} sections ({n_id} with explicit section identifiers).",
            end_state="extracted",
            end_reason="policy-doc",
        )
        print(f"  [OK] {item['rel_dir']} -> {len(full_md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")


def process_group2_canada_ca():
    print("\n=== Processing Group 2: reference/canada.ca/ (5 directories) ===")
    # 1. 2004 National Security Policy (PDF)
    for ver, pub_date, pdf_url, src_url, title, sup_by, desc in [
        (
            "2004",
            "2004-04-27",
            "https://publications.gc.ca/collections/Collection/CP22-77-2004E.pdf",
            "https://publications.gc.ca/site/eng/258665/publication.html",
            "Securing an Open Society: Canada's National Security Policy (2004)",
            None,
            "Canada's inaugural 2004 National Security Policy (Privy Council Office), establishing an integrated national security framework across six key strategic areas: intelligence, emergency planning and management, public health emergencies, transport security, border security, and international security.",
        ),
    ]:
        doc_dir = REPO_ROOT / f"reference/canada.ca/national-security-policy/{ver}"
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = f"national-security-policy-{ver}"
        r = fetch_with_retry(pdf_url, headers={**HEADERS, "Referer": "https://publications.gc.ca/site/archivee-archived.html"}, timeout=45)
        md, pages = pdf_bytes_to_markdown(r.content, title)
        (doc_dir / f"{stem}.md").write_text(md, encoding="utf-8")
        n_sec, n_id = run_parse_sections(doc_dir, stem)
        write_metadata(
            doc_dir,
            stem,
            secid=f"secid:reference/canada.ca/national-security-policy@{ver}",
            name=title,
            acronym="NSP",
            version=ver,
            owner="Privy Council Office (Government of Canada)",
            doc_type="Reference",
            subtype=["strategy"],
            description=desc,
            cloud_rel="Foundational national security policy establishing the Government Operations Centre and federal cyber/critical-infrastructure protection mandate.",
            ai_rel="Provides baseline national security intelligence and threat-assessment governance.",
            license_obj=LICENSE_CA,
            source_url=src_url,
            text_used_url=pdf_url,
            published=pub_date,
            active=True,
            supersedes=None,
            superseded_by=sup_by,
            tool_str="pymupdf + tools-resources/utils/parse_regulatory_sections.py",
            extraction_notes=f"Extracted {pages}-page born-digital Government of Canada Publications PDF ({pdf_url}) locally via column-aware PyMuPDF layout analysis ({len(md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
            end_state="extracted",
            end_reason="policy-doc",
        )
        print(f"  [OK] reference/canada.ca/national-security-policy/{ver} -> {len(md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")

    # 2. 2005 NSP Progress Report (PDF)
    doc_dir = REPO_ROOT / "reference/canada.ca/national-security-policy-progress-report/2005"
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = "national-security-policy-progress-report-2005"
    pdf_url = "https://publications.gc.ca/collections/Collection/CP22-77-2005E.pdf"
    src_url = "https://publications.gc.ca/site/eng/272094/publication.html"
    title = "Securing an Open Society: One Year Later — Progress Report on the Implementation of Canada's National Security Policy (2005)"
    r = fetch_with_retry(pdf_url, headers={**HEADERS, "Referer": "https://publications.gc.ca/site/archivee-archived.html"}, timeout=45)
    md, pages = pdf_bytes_to_markdown(r.content, title)
    (doc_dir / f"{stem}.md").write_text(md, encoding="utf-8")
    n_sec, n_id = run_parse_sections(doc_dir, stem)
    write_metadata(
        doc_dir,
        stem,
        secid="secid:reference/canada.ca/national-security-policy-progress-report@2005",
        name=title,
        acronym="",
        version="2005",
        owner="Privy Council Office (Government of Canada)",
        doc_type="Reference",
        subtype=["strategy"],
        description="First-year implementation progress report (April 2005) on Canada's 2004 National Security Policy ('Securing an Open Society: One Year Later').",
        cloud_rel="Tracks early implementation of Canada's Cyber Security Task Force, Government Operations Centre, and critical infrastructure protection framework.",
        ai_rel="",
        license_obj=LICENSE_CA,
        source_url=src_url,
        text_used_url=pdf_url,
        published="2005-04-01",
        active=True,
        supersedes=None,
        superseded_by=None,
        tool_str="pymupdf + tools-resources/utils/parse_regulatory_sections.py",
        extraction_notes=f"Extracted {pages}-page born-digital Government of Canada Publications PDF ({pdf_url}) locally via column-aware PyMuPDF layout analysis ({len(md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
        end_state="extracted",
        end_reason="policy-doc",
    )
    print(f"  [OK] reference/canada.ca/national-security-policy-progress-report/2005 -> {len(md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")

    # 3. Our North, Strong and Free (2024) — stitch landing page + all chapter HTML pages
    doc_dir = REPO_ROOT / "reference/canada.ca/our-north-strong-and-free/2024"
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = "our-north-strong-and-free-2024"
    base_url = "https://www.canada.ca/en/department-national-defence/corporate/reports-publications/north-strong-free-2024"
    chapter_slugs = [
        "message-mnd.html",
        "message-mfa.html",
        "executive-summary.html",
        "introduction.html",
        "canada-time-global-uncertainty.html",
        "our-vision-defence.html",
        "delivering-vision-strengthening-foundations.html",
        "delivering-vision-right-capabilities-canada.html",
        "conclusion.html",
        "annex-a-funding.html",
        "annex-b-accomplished-since-2017-sse.html",
        "annex-c-canada-norad-modernization-plan.html",
        "annex-d-defence-policy-review-consultations.html",
        "addendum-national-defence-funding-and-projected-canadian-defence-spending-to-gdp.html",
        "addendum-funding-cash-basis.html",
    ]
    onsf_parts = ["# Our North, Strong and Free: A Renewed Vision for Canada's Defence (2024)"]
    for slug in chapter_slugs:
        ch_url = f"{base_url}/{slug}"
        r = fetch_with_retry(ch_url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            onsf_parts.append(html_to_clean_markdown(r.text, ch_url).strip())
    onsf_md = "\n\n---\n\n".join(onsf_parts) + "\n"
    (doc_dir / f"{stem}.md").write_text(onsf_md, encoding="utf-8")
    n_sec, n_id = run_parse_sections(doc_dir, stem)
    landing_url = "https://www.canada.ca/en/department-national-defence/corporate/reports-publications/north-strong-free-2024.html"
    write_metadata(
        doc_dir,
        stem,
        secid="secid:reference/canada.ca/our-north-strong-and-free@2024",
        name="Our North, Strong and Free: A Renewed Vision for Canada's Defence (2024)",
        acronym="ONSF",
        version="2024",
        owner="Department of National Defence (Government of Canada)",
        doc_type="Reference",
        subtype=["strategy"],
        description="Canada's 2024 defence policy update ('Our North, Strong and Free'), committing to a four-yearly National Security Strategy cycle and major investments in joint cyber capabilities, cloud/digital modernization, and AI/quantum defence technologies.",
        cloud_rel="Commits to modernizing defence cloud infrastructure, command-and-control networks, and joint DND/CAF/CSE cyber operations.",
        ai_rel="Prioritizes responsible adoption and defence against AI-enabled military and cyber threats.",
        license_obj=LICENSE_CA,
        source_url=landing_url,
        text_used_url=landing_url,
        published="2024-04-08",
        active=True,
        supersedes=None,
        superseded_by=None,
        tool_str="requests + markdownify + tools-resources/utils/parse_regulatory_sections.py",
        extraction_notes=f"Extracted and stitched all 15 official HTML chapter pages linked from {landing_url} ({base_url}/<chapter>.html, {len(onsf_md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
        end_state="extracted",
        end_reason="policy-doc",
    )
    print(f"  [OK] reference/canada.ca/our-north-strong-and-free/2024 -> {len(onsf_md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")

    # 4. National Security Transparency Commitment (landing + 4 subpages)
    doc_dir = REPO_ROOT / "reference/canada.ca/national-security-transparency-commitment"
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = "national-security-transparency-commitment"
    nstc_urls = [
        "https://www.canada.ca/en/services/defence/nationalsecurity/national-security-transparency-commitment.html",
        "https://www.canada.ca/en/services/defence/nationalsecurity/national-security-transparency-commitment/informationtransparency.html",
        "https://www.canada.ca/en/services/defence/nationalsecurity/national-security-transparency-commitment/executivetransparency.html",
        "https://www.canada.ca/en/services/defence/nationalsecurity/national-security-transparency-commitment/policytransparency.html",
        "https://www.canada.ca/en/services/defence/nationalsecurity/national-security-transparency-commitment/national-security-transparency-advisory-group.html",
    ]
    nstc_parts = []
    for u in nstc_urls:
        r = fetch_with_retry(u, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            nstc_parts.append(html_to_clean_markdown(r.text, u).strip())
    nstc_md = "\n\n---\n\n".join(nstc_parts) + "\n"
    (doc_dir / f"{stem}.md").write_text(nstc_md, encoding="utf-8")
    n_sec, n_id = run_parse_sections(doc_dir, stem)
    write_metadata(
        doc_dir,
        stem,
        secid="secid:reference/canada.ca/national-security-transparency-commitment",
        name="National Security Transparency Commitment",
        acronym="NSTC",
        version="",
        owner="Government of Canada (Public Safety Canada)",
        doc_type="Reference",
        subtype=["strategy"],
        description="Government-wide commitment to six national security transparency principles (Information, Executive, and Policy Transparency) across federal departments and agencies with national security responsibilities.",
        cloud_rel="Governs transparency and reporting expectations across federal security and intelligence agencies.",
        ai_rel="",
        license_obj=LICENSE_CA,
        source_url=nstc_urls[0],
        text_used_url=nstc_urls[0],
        published="2017-06-20",
        active=True,
        supersedes=None,
        superseded_by=None,
        tool_str="requests + markdownify + tools-resources/utils/parse_regulatory_sections.py",
        extraction_notes=f"Extracted main commitment page and 4 official subpages (Information, Executive, Policy Transparency, and NS-TAG) from canada.ca ({len(nstc_md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
        end_state="extracted",
        end_reason="policy-doc",
    )
    print(f"  [OK] reference/canada.ca/national-security-transparency-commitment -> {len(nstc_md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")

    # 5. Government of Canada Enterprise Cyber Security Strategy (2024)
    doc_dir = REPO_ROOT / "reference/canada.ca/enterprise-cyber-security-strategy/2024"
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = "enterprise-cyber-security-strategy-2024"
    ecss_url = "https://www.canada.ca/en/government/system/digital-government/online-security-privacy/enterprise-cyber-security-strategy.html"
    r = fetch_with_retry(ecss_url, headers=HEADERS, timeout=30)
    ecss_md = html_to_clean_markdown(r.text, ecss_url, "Government of Canada Enterprise Cyber Security Strategy (2024)")
    (doc_dir / f"{stem}.md").write_text(ecss_md, encoding="utf-8")
    n_sec, n_id = run_parse_sections(doc_dir, stem)
    write_metadata(
        doc_dir,
        stem,
        secid="secid:reference/canada.ca/enterprise-cyber-security-strategy@2024",
        name="Government of Canada Enterprise Cyber Security Strategy (2024)",
        acronym="GCECSS",
        version="2024",
        owner="Treasury Board of Canada Secretariat (Office of the Chief Information Officer)",
        doc_type="Reference",
        subtype=["strategy"],
        description="Internal enterprise cyber security strategy for the Government of Canada (TBS, Shared Services Canada, CSE), establishing an enterprise-wide model for protecting federal cloud workloads, networks, and digital services.",
        cloud_rel="Directly governs how Government of Canada departments and Shared Services Canada secure federal cloud environments, identity, and enterprise telemetry.",
        ai_rel="Addresses modernizing security controls and automation across federal digital infrastructure.",
        license_obj=LICENSE_CA,
        source_url=ecss_url,
        text_used_url=ecss_url,
        published="2024-03-04",
        active=True,
        supersedes=None,
        superseded_by=None,
        tool_str="requests + markdownify + tools-resources/utils/parse_regulatory_sections.py",
        extraction_notes=f"Extracted official Treasury Board Secretariat HTML publication from canada.ca ({len(ecss_md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
        end_state="extracted",
        end_reason="policy-doc",
    )
    print(f"  [OK] reference/canada.ca/enterprise-cyber-security-strategy/2024 -> {len(ecss_md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")


def process_group3_parl_ca():
    print("\n=== Processing Group 3: regulation/parl.ca/ (4 directories) ===")
    parl_items = [
        {
            "rel_dir": "regulation/parl.ca/nsira-act",
            "stem": "nsira-act",
            "secid": "secid:regulation/parl.ca/nsira-act",
            "name": "National Security and Intelligence Review Agency Act (S.C. 2019, c. 13, s. 2)",
            "acronym": "NSIRA Act",
            "published": "2019-06-21",
            "xml_url": "https://laws-lois.justice.gc.ca/eng/XML/N-16.62.xml",
            "source_url": "https://laws-lois.justice.gc.ca/eng/acts/N-16.62/FullText.html",
            "description": "Federal statute establishing the National Security and Intelligence Review Agency (NSIRA) with statutory authority to review any national security or intelligence activity across all Government of Canada departments and agencies (including CSIS, CSE, RCMP, DND/CAF, CBSA, and Global Affairs Canada).",
        },
        {
            "rel_dir": "regulation/parl.ca/nsicop-act",
            "stem": "nsicop-act",
            "secid": "secid:regulation/parl.ca/nsicop-act",
            "name": "National Security and Intelligence Committee of Parliamentarians Act (S.C. 2017, c. 15)",
            "acronym": "NSICOP Act",
            "published": "2017-06-22",
            "xml_url": "https://laws-lois.justice.gc.ca/eng/XML/N-16.6.xml",
            "source_url": "https://laws-lois.justice.gc.ca/eng/acts/N-16.6/",
            "description": "Federal statute (Bill C-22) establishing the National Security and Intelligence Committee of Parliamentarians (NSICOP) to review the legislative, regulatory, policy, administrative, and financial framework for national security and intelligence in Canada.",
        },
        {
            "rel_dir": "regulation/parl.ca/national-security-act-2017",
            "stem": "national-security-act-2017",
            "secid": "secid:regulation/parl.ca/national-security-act-2017",
            "name": "An Act respecting national security matters (National Security Act, 2017, S.C. 2019, c. 13)",
            "acronym": "NSA 2017",
            "published": "2019-06-21",
            "xml_url": "https://www.parl.ca/Content/Bills/421/Government/C-59/C-59_4/C-59_E.xml",
            "source_url": "https://laws-lois.justice.gc.ca/eng/annualstatutes/2019_13/",
            "description": "Comprehensive national security reform statute (Bill C-59, S.C. 2019, c. 13) enacting the NSIRA Act, the Communications Security Establishment Act (CSE Act, establishing statutory active and defensive cyber operations powers), the Avoiding Complicity in Mistreatment by Foreign Entities Act, and the Security of Canada Information Disclosure Act.",
        },
        {
            "rel_dir": "regulation/parl.ca/ccspa",
            "stem": "ccspa",
            "secid": "secid:regulation/parl.ca/ccspa",
            "name": "An Act respecting cyber security, amending the Telecommunications Act and making consequential amendments to other Acts (Critical Cyber Systems Protection Act, Bill C-8 / S.C. 2026, c. 9)",
            "acronym": "CCSPA",
            "published": "2026-06-15",
            "xml_url": "https://www.parl.ca/Content/Bills/451/Government/C-8/C-8_4/C-8_E.xml",
            "source_url": "https://www.parl.ca/legisinfo/en/bill/45-1/c-8",
            "description": "Federal cyber security statute (Bill C-8, 45th Parliament, formerly Bill C-26; Royal Assent S.C. 2026, c. 9) amending the Telecommunications Act to secure Canadian telecommunications networks and enacting the Critical Cyber Systems Protection Act (CCSPA) mandating cyber security programs, supply-chain/third-party risk mitigation, and mandatory incident reporting to CSE for designated operators across federal critical infrastructure sectors.",
        },
    ]

    for item in parl_items:
        doc_dir = REPO_ROOT / item["rel_dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = item["stem"]
        xml_path = doc_dir / f"{stem}.xml"
        if not xml_path.exists():
            r = fetch_with_retry(item["xml_url"], headers=HEADERS, timeout=30)
            xml_path.write_bytes(r.content)

        subprocess.run(
            [
                sys.executable,
                str(PARSE_CANADA_XML_SCRIPT),
                str(doc_dir),
                "--out-stem",
                stem,
                "--title",
                item["name"],
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        md = (doc_dir / f"{stem}.md").read_text(encoding="utf-8")
        rows = json.loads((doc_dir / f"{stem}-sections.json").read_text(encoding="utf-8"))

        write_metadata(
            doc_dir,
            stem,
            secid=item["secid"],
            name=item["name"],
            acronym=item["acronym"],
            version="",
            owner="Parliament of Canada",
            doc_type="Regulation",
            subtype=["legislation"],
            description=item["description"],
            cloud_rel="Governs federal cyber security, intelligence review, and critical cyber system protection obligations affecting cloud and telecommunications infrastructure in Canada.",
            ai_rel="Applies to automated and AI-enabled systems within federally regulated critical infrastructure and national security operations.",
            license_obj=LICENSE_CA,
            source_url=item["source_url"],
            text_used_url=item["xml_url"],
            published=item["published"],
            active=True,
            supersedes=None,
            superseded_by=None,
            tool_str="tools-resources/utils/parse_canada_justice_xml.py",
            extraction_notes=f"Committed authoritative legislative XML ({item['xml_url']}) as {stem}.xml and extracted {len(rows)} statutory sections and schedules via tools-resources/utils/parse_canada_justice_xml.py into {stem}.md, {stem}-sections.csv, and {stem}-sections.json.",
            end_state="structured",
            end_reason="requirement-list",
        )
        print(f"  [OK] {item['rel_dir']} -> {len(md):>7} chars | {len(rows):>3} XML sections")


def process_group4_us_uk():
    print("\n=== Processing Group 4A: reference/whitehouse.gov/ (10 directories) ===")
    for item in WHITEHOUSE_DOCS:
        doc_dir = REPO_ROOT / item["rel_dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = item["stem"]
        r = fetch_with_retry(item["pdf_url"], headers=HEADERS, timeout=45)
        md, pages = pdf_bytes_to_markdown(r.content, item["name"])
        (doc_dir / f"{stem}.md").write_text(md, encoding="utf-8")
        n_sec, n_id = run_parse_sections(doc_dir, stem)
        retired_date = PUB_DATE_BY_SECID.get(item["superseded_by"] or "") if not item["active"] else None
        write_metadata(
            doc_dir,
            stem,
            secid=item["secid"],
            name=item["name"],
            acronym=item["acronym"],
            version=item["version"],
            owner="Executive Office of the President (The White House)",
            doc_type="Reference",
            subtype=["strategy"],
            description=item["description"],
            cloud_rel="Establishes U.S. federal cybersecurity and national security strategic priorities affecting cloud service providers, critical infrastructure, and federal IT modernization.",
            ai_rel="Addresses strategic competition and security in critical and emerging technologies including artificial intelligence and quantum computing.",
            license_obj=LICENSE_US,
            source_url=item["source_url"],
            text_used_url=item["pdf_url"],
            published=item["published"],
            active=item["active"],
            retired_date=retired_date,
            supersedes=item["supersedes"],
            superseded_by=item["superseded_by"],
            tool_str="pymupdf + tools-resources/utils/parse_regulatory_sections.py",
            extraction_notes=f"Extracted {pages}-page born-digital White House PDF ({item['pdf_url']}) locally via column-aware PyMuPDF layout analysis ({len(md):,} chars) and parsed {n_sec} sections ({n_id} with ID).",
            end_state="extracted",
            end_reason="policy-doc",
        )
        print(f"  [OK] {item['rel_dir']} -> {len(md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")

    print("\n=== Processing Group 4B: reference/gov.uk/ (7 directories) ===")
    for item in GOV_UK_DOCS:
        doc_dir = REPO_ROOT / item["rel_dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = item["stem"]
        if "html_url" in item:
            text_url = item["html_url"]
            r = fetch_with_retry(text_url, headers=HEADERS, timeout=30)
            md = html_to_clean_markdown(r.text, text_url, item["name"])
            tool_used = "requests + markdownify + tools-resources/utils/parse_regulatory_sections.py"
            note_prefix = f"Extracted official GOV.UK HTML publication ({text_url}) to Markdown ({len(md):,} chars)"
        else:
            text_url = item["pdf_url"]
            r = fetch_with_retry(text_url, headers=HEADERS, timeout=45)
            md, pages = pdf_bytes_to_markdown(r.content, item["name"])
            tool_used = "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
            note_prefix = f"Extracted {pages}-page born-digital GOV.UK Command Paper PDF ({text_url}) locally via column-aware PyMuPDF layout analysis ({len(md):,} chars)"
        (doc_dir / f"{stem}.md").write_text(md, encoding="utf-8")
        n_sec, n_id = run_parse_sections(doc_dir, stem)
        retired_date = PUB_DATE_BY_SECID.get(item["superseded_by"] or "") if not item["active"] else None
        write_metadata(
            doc_dir,
            stem,
            secid=item["secid"],
            name=item["name"],
            acronym=item["acronym"],
            version=item["version"],
            owner="HM Government (Cabinet Office, United Kingdom)",
            doc_type="Reference",
            subtype=["strategy"],
            description=item["description"],
            cloud_rel="Defines UK national cyber resilience, critical national infrastructure protection, and public-sector security architecture expectations.",
            ai_rel="Addresses UK strategic advantage in science and technology, AI security, and cyber power.",
            license_obj=LICENSE_UK,
            source_url=item["source_url"],
            text_used_url=text_url,
            published=item["published"],
            active=item["active"],
            retired_date=retired_date,
            supersedes=item["supersedes"],
            superseded_by=item["superseded_by"],
            tool_str=tool_used,
            extraction_notes=f"{note_prefix} and parsed {n_sec} sections ({n_id} with ID).",
            end_state="extracted",
            end_reason="policy-doc",
        )
        print(f"  [OK] {item['rel_dir']} -> {len(md):>7} chars | {n_sec:>3} sections ({n_id} with ID)")


if __name__ == "__main__":
    process_group1_publicsafety()
    process_group2_canada_ca()
    process_group3_parl_ca()
    process_group4_us_uk()
    print("\nALL 46 DOCUMENTS EXTRACTED SUCCESSFULLY.")
