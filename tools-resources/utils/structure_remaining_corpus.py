#!/usr/bin/env python3
"""Batch 1A: Extract and structure all remaining on-disk Markdown-only, raw PDF/text,
CSV-only, and JSON-only dataset editions across dataset-public-laws-regulations-standards
and dataset-private-laws-regulations-standards.
"""
import csv
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UTILS_DIR = Path(__file__).resolve().parent
PUB_ROOT = UTILS_DIR.parent.parent
PRIV_ROOT = PUB_ROOT.parent / "dataset-private-laws-regulations-standards"

sys.path.insert(0, str(UTILS_DIR))
from extract_track2_corpus import pdf_bytes_to_markdown
from extract_track2_wave2 import ensure_hierarchical_headings
from parse_regulatory_sections import HEADING_RE

PARSE_SCRIPT = UTILS_DIR / "parse_regulatory_sections.py"


def run_parse_sections(doc_dir: Path, stem: str) -> int:
    """Run parse_regulatory_sections.py on doc_dir and return row count."""
    subprocess.run(
        [sys.executable, str(PARSE_SCRIPT), str(doc_dir), "--out-stem", stem],
        check=True,
        capture_output=True,
        text=True,
    )
    jpath = doc_dir / f"{stem}-sections.json"
    if jpath.exists():
        return len(json.loads(jpath.read_text(encoding="utf-8")))
    return 0


def write_dict_list_to_csv(rows: list[dict], csv_path: Path) -> None:
    """Write a list of dicts to CSV preserving key order across all rows."""
    if not rows:
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in seen:
                    seen.add(k)
                    fieldnames.append(k)
    flat_rows = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        fr = {}
        for k in fieldnames:
            v = r.get(k, "")
            if isinstance(v, (dict, list)):
                s_val = json.dumps(v, ensure_ascii=False)
            elif v is None:
                s_val = ""
            else:
                s_val = str(v)
            s_val = "\n".join(l.rstrip() for l in s_val.replace("\r\n", "\n").replace("\r", "\n").splitlines()).strip()
            fr[k] = s_val
        flat_rows.append(fr)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(flat_rows)


def process_private_json_no_csv() -> int:
    """Generate <stem>-controls.csv for the 10 JSON-only control editions in dataset-private."""
    count = 0
    for mp in sorted(PRIV_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith("-controls.json")]
        csvs = [f for f in files if f.endswith(".csv")]
        if jsons and not csvs:
            jpath = parent / jsons[0]
            data = json.loads(jpath.read_text(encoding="utf-8"))
            rows = data.get("controls", []) if isinstance(data, dict) else data
            if isinstance(rows, list) and rows:
                cpath = parent / jsons[0].replace("-controls.json", "-controls.csv")
                write_dict_list_to_csv(rows, cpath)
                count += 1
                print(f"[PRIVATE json->csv] {cpath.relative_to(PRIV_ROOT)} ({len(rows)} rows)")
    return count


def process_public_json_no_csv() -> int:
    """Generate companion CSVs for the 9 JSON-only editions in dataset-public."""
    count = 0
    targets = [
        ("control/cloudsecurityalliance.org/aicm/1.0.3", "aicm-1.0.3.json", "controls", "aicm-1.0.3-controls.csv"),
        ("control/cloudsecurityalliance.org/aicm-caiq/1.0.2", "aicm-caiq-1.0.2.json", "questions", "aicm-caiq-1.0.2-questions.csv"),
        ("control/cloudsecurityalliance.org/ccm/4.0.13", "ccm-4.0.13-Controls.json", None, "ccm-4.0.13-controls.csv"),
        ("control/cloudsecurityalliance.org/ccm/4.1.0", "ccm-4.1.0.json", "controls", "ccm-4.1.0-controls.csv"),
        ("control/cloudsecurityalliance.org/ccm-caiq/3.1", "ccm-caiq-3.1.json", "questions", "ccm-caiq-3.1-questions.csv"),
        ("control/cloudsecurityalliance.org/ccm-caiq/4.1.0", "ccm-caiq-4.1.0.json", "questions", "ccm-caiq-4.1.0-questions.csv"),
        ("reference/mitre.org/ctid/cve", "cve-10.21.2021_attack-9.0-enterprise.json", "mapping_objects", "ctid-cve-mapping.csv"),
        ("reference/mitre.org/cve-program/cna-partners", "cve-cna-partners-list.json", "partners", "cve-cna-partners-list.csv"),
        ("ttp/mitre.org/fight", "fight.json", "techniques", "fight-techniques.csv"),
    ]
    for rel, jfn, key, cfn in targets:
        d = PUB_ROOT / rel
        jpath = d / jfn
        if not jpath.exists():
            continue
        data = json.loads(jpath.read_text(encoding="utf-8"))
        rows = data.get(key, []) if key and isinstance(data, dict) else data
        if isinstance(rows, list) and rows:
            cpath = d / cfn
            write_dict_list_to_csv(rows, cpath)
            count += 1
            print(f"[PUBLIC json->csv] {cpath.relative_to(PUB_ROOT)} ({len(rows)} rows)")
    return count


def process_public_csv_no_json() -> int:
    """Generate companion JSON files for the 18 CSV-only editions in dataset-public."""
    count = 0
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith(".json") and f != "README.json"]
        csvs = sorted(f for f in files if f.endswith(".csv"))
        if csvs and not jsons:
            stem = mp.name[: -len("-metadata.json")]
            all_rows = []
            for cfn in csvs:
                cpath = parent / cfn
                sheet_name = cfn[:-4]
                with cpath.open("r", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cleaned = {k: (v or "").strip() for k, v in row.items() if k is not None}
                        if any(cleaned.values()):
                            if len(csvs) > 1:
                                cleaned["_sheet"] = sheet_name
                            all_rows.append(cleaned)
            jpath = parent / f"{stem}-items.json"
            jpath.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            count += 1
            print(f"[PUBLIC csv->json] {jpath.relative_to(PUB_ROOT)} ({len(all_rows)} rows from {len(csvs)} CSVs)")
    return count


def promote_japanese_txt_headings(txt: str, doc_title: str) -> str:
    """Convert raw Japanese/English text files into clean Markdown with hierarchical headings."""
    lines = txt.splitlines()
    out = [f"# {doc_title}", ""]
    for line in lines:
        s = line.strip()
        if not s:
            out.append("")
            continue
        # Chapter / Part / Article in Japanese
        if re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[章篇编部編]?(?:[\s　]|$)", s) and len(s) < 90:
            out.append(f"## {s}")
        elif re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[节節](?:[\s　]|$)", s):
            out.append(f"### {s}")
        elif re.match(r"^第[一二三四五六七八九十百千0-9０-９]+[条條](?:の[一二三四五六七八九十0-9０-９]+)?(?:[\s　（\(]|$)", s):
            out.append(f"#### {s}")
        elif re.match(r"^[（\(][一二三四五六七八九十0-9０-９]+[）\)]\s*[^。]{2,70}$", s):
            out.append(f"### {s}")
        elif re.match(r"^(?:Chapter|Part|Section|CHAPTER|PART|SECTION)\s+(?:[IVXLCDM]+|\d+)\b", s) and len(s) < 120:
            out.append(f"## {s}")
        elif re.match(r"^(?:\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\s+[A-Z\u3000-\u9fff]", s) and len(s) < 120 and ".." not in s:
            depth = 2 + min(s.split()[0].rstrip(".").count("."), 2)
            out.append(f"{'#' * depth} {s}")
        elif re.match(r"^(?:[1-9]|1\d)[\.．]\s+[^\d\.]{2,80}$", s) and ".." not in s:
            out.append(f"## {s}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def process_raw_on_disk() -> int:
    """Extract and structure the 28 Japanese raw PDF/text directories and 2 parent reference dirs."""
    count = 0
    # First handle reference/cisa.gov/govcar and reference/mitre.org/cve-program
    for rel in ["reference/cisa.gov/govcar", "reference/mitre.org/cve-program"]:
        d = PUB_ROOT / rel
        mp = next(d.glob("*-metadata.json"))
        stem = mp.name[: -len("-metadata.json")]
        child_mds = sorted(
            p
            for p in d.rglob("*.md")
            if p.parent != d and p.name != "README.md" and not p.name.endswith("-metadata.md")
        )
        if child_mds:
            parts = []
            for cmd in child_mds:
                parts.append(f"## {cmd.stem.replace('_', ' ')}\n\n" + cmd.read_text(encoding="utf-8", errors="replace"))
            md_path = d / f"{stem}.md"
            md_path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
            nrows = run_parse_sections(d, stem)
            count += 1
            print(f"[PARENT stitched] {rel} -> {nrows} sections")

    # Now handle the 28 raw PDF/text directories
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith(".json") and f != "README.json"]
        csvs = [f for f in files if f.endswith(".csv")]
        mds = [f for f in files if f.endswith(".md")]
        pdfs = sorted(f for f in files if f.endswith(".pdf"))
        txts = sorted(f for f in files if f.endswith(".txt"))
        if jsons or csvs or mds or (not pdfs and not txts):
            continue
        stem = mp.name[: -len("-metadata.json")]
        md_meta = json.loads(mp.read_text(encoding="utf-8"))
        doc_title = md_meta.get("name") or stem

        md_text = ""
        if pdfs:
            raw_md, _ = pdf_bytes_to_markdown((parent / pdfs[0]).read_bytes(), doc_title)
            md_text = ensure_hierarchical_headings(raw_md, doc_title, "")
        if (not md_text or len(HEADING_RE.findall(md_text)) <= 1) and txts:
            # Prefer *-raw.txt if present
            raw_txts = [t for t in txts if t.endswith("-raw.txt")] or txts
            combined_txt = "\n\n".join((parent / t).read_text(encoding="utf-8", errors="replace") for t in raw_txts)
            md_text = promote_japanese_txt_headings(combined_txt, doc_title)
            md_text = ensure_hierarchical_headings(md_text, doc_title, "")

        if not HEADING_RE.search(md_text):
            md_text = f"# {doc_title}\n\n" + md_text

        md_path = parent / f"{stem}.md"
        md_path.write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(parent, stem)
        count += 1
        print(f"[RAW->MD+SECTIONS] {parent.relative_to(PUB_ROOT)} -> {nrows} sections")
    return count


def normalize_statute_markdown(md_text: str, doc_title: str, rel_path: str) -> str:
    """Normalize plain-text statute/bill/whitepaper Markdown files so all structural
    sections have proper `#` headings before running parse_regulatory_sections.py.
    """
    orig = md_text
    # 1. Strip huge base64 data:image blobs (e.g., wa.gov/my-health-my-data-act)
    md_text = re.sub(r"!\[[^\]]*\]\(data:image/[^)]+\)", "", md_text)
    md_text = re.sub(r"data:image/[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]{100,}", "", md_text)

    # 2. Unwrap single outer ``` code block if the statute body was pasted inside ``` ... ```
    # (e.g., iowa.gov/icdpa, tn.gov/tipa, maryland.gov/facial-recognition-laws)
    fences = list(re.finditer(r"^```[^\n]*$", md_text, re.MULTILINE))
    if len(fences) == 2 and fences[1].end() - fences[0].start() > len(md_text) * 0.6:
        before = md_text[: fences[0].start()]
        inside = md_text[fences[0].end() : fences[1].start()]
        after = md_text[fences[1].end() :]
        md_text = before + "\n" + inside + "\n" + after

    # 3. Promote plain-text statute/directive/memorandum headings when heading count is low (< 5)
    headings = HEADING_RE.findall(md_text)
    if len(headings) < 5 or rel_path in (
        "regulation/congress.gov/chips-act",
        "regulation/illinois.gov/bipa",
        "regulation/iowa.gov/icdpa",
        "regulation/tn.gov/tipa",
        "regulation/maryland.gov/facial-recognition-laws",
        "regulation/whitehouse.gov/nsm-ai",
        "regulation/europa.eu/eprivacy",
        "regulation/ny.gov/shield-act",
        "regulation/florida.gov/biometric-privacy-laws",
        "regulation/wa.gov/my-health-my-data-act",
    ):
        lines = md_text.splitlines()
        new_lines = []
        for line in lines:
            s = line.strip()
            if not s or s.startswith("#"):
                new_lines.append(line)
                continue
            # GPO / Congressional bills: DIVISION A—..., TITLE I—..., Subtitle A—..., SEC. 101. ...
            if re.match(r"^DIVISION\s+[A-Z]\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"## {s}")
            elif re.match(r"^(?:TITLE|Title)\s+(?:[IVXLCDM]+|\d+)\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:SUBTITLE|Subtitle|CHAPTER|Chapter|PART|Part)\s+(?:[A-Z]|[IVXLCDM]+|\d+[A-Za-z]?)\b", s) and len(s) < 160 and ".." not in s:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:SEC\.|Sec\.|SECTION|Section)\s+\d+[A-Za-z\-]*(?:[\.\s]|$)", s) and len(s) < 200 and ".." not in s:
                new_lines.append(f"#### {s}")
            elif re.match(r"^(?:Article|ARTICLE)\s+\d+[a-z]?\b", s) and len(s) < 120:
                new_lines.append(f"### {s}")
            elif re.match(r"^(?:715D\.\d+|47-18-\d+|501\.\d+|RCW\s+19\.373\.\d+|§+\s*\d+[\dA-Za-z\.\-]*)\b", s) and len(s) < 180:
                new_lines.append(f"### {s}")
            elif re.match(r"^\*\*(?:[1-9]\d?(?:\.\d+)*\s+)?[A-Z][^*]{3,90}\*\*$", s):
                clean_b = s.strip("*").strip()
                new_lines.append(f"## {clean_b}")
            else:
                new_lines.append(line)
        md_text = "\n".join(new_lines)

    if not HEADING_RE.search(md_text):
        md_text = f"# {doc_title}\n\n" + md_text.lstrip()

    return md_text


def process_markdown_only() -> int:
    """Structure all 193 Markdown-only editions in dataset-public into <stem>-sections.{json,csv}."""
    count = 0
    for mp in sorted(PUB_ROOT.rglob("*-metadata.json")):
        parent = mp.parent
        files = [
            f.name
            for f in parent.iterdir()
            if f.is_file()
            and f.name != "README.md"
            and not f.name.startswith(".")
            and not f.name.endswith(("-metadata.json", "-metadata.md", "_meta.json"))
        ]
        jsons = [f for f in files if f.endswith(".json") and f != "README.json"]
        csvs = [f for f in files if f.endswith(".csv")]
        mds = sorted(f for f in files if f.endswith(".md"))
        if jsons or csvs or not mds:
            continue

        stem = mp.name[: -len("-metadata.json")]
        rel_path = str(parent.relative_to(PUB_ROOT))
        md_meta = json.loads(mp.read_text(encoding="utf-8"))
        doc_title = md_meta.get("name") or stem

        # Pick canonical .md (preferring <stem>.md or non-"-processed"/"-definitions" if multiple)
        chosen_md = parent / mds[0]
        if f"{stem}.md" in mds:
            chosen_md = parent / f"{stem}.md"
        elif len(mds) > 1:
            non_proc = [m for m in mds if not m.endswith(("-processed.md", "-definitions.md"))]
            if non_proc:
                chosen_md = parent / non_proc[0]

        raw_txt = chosen_md.read_text(encoding="utf-8", errors="replace")
        norm_txt = normalize_statute_markdown(raw_txt, doc_title, rel_path)
        if norm_txt != raw_txt:
            chosen_md.write_text(norm_txt, encoding="utf-8")

        # Temporarily ensure parse_regulatory_sections.py reads `chosen_md` if multiple .md exist
        nrows = run_parse_sections(parent, stem)
        count += 1
        print(f"[MD->SECTIONS] {rel_path} ({chosen_md.name}) -> {nrows} sections")
    return count


def egov_xml_to_md(law_id: str, title: str) -> str:
    """Fetch and convert Japan e-Gov Law API v1 XML into hierarchical Markdown."""
    url = f"https://laws.e-gov.go.jp/api/1/lawdata/{law_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    lines = [f"# {title}", ""]
    main_prov = root.find(".//MainProvision")
    if main_prov is None:
        return ""
    for ch in main_prov.findall(".//Chapter"):
        ch_t = "".join(ch.find("ChapterTitle").itertext()).strip() if ch.find("ChapterTitle") is not None else ""
        if ch_t:
            lines.append(f"## {ch_t}")
            lines.append("")
        for child in list(ch):
            if child.tag == "Section":
                sec_t = "".join(child.find("SectionTitle").itertext()).strip() if child.find("SectionTitle") is not None else ""
                if sec_t:
                    lines.append(f"### {sec_t}")
                    lines.append("")
                for art in child.findall("Article"):
                    art_t = "".join(art.find("ArticleTitle").itertext()).strip() if art.find("ArticleTitle") is not None else ""
                    art_c = "".join(art.find("ArticleCaption").itertext()).strip() if art.find("ArticleCaption") is not None else ""
                    lines.append(f"#### {art_t} {art_c}".strip())
                    lines.append("")
                    for para in art.findall("Paragraph"):
                        p_txt = " ".join("".join(para.itertext()).split())
                        if p_txt:
                            lines.append(p_txt)
                            lines.append("")
            elif child.tag == "Article":
                art_t = "".join(child.find("ArticleTitle").itertext()).strip() if child.find("ArticleTitle") is not None else ""
                art_c = "".join(child.find("ArticleCaption").itertext()).strip() if child.find("ArticleCaption") is not None else ""
                lines.append(f"### {art_t} {art_c}".strip())
                lines.append("")
                for para in child.findall("Paragraph"):
                    p_txt = " ".join("".join(para.itertext()).split())
                    if p_txt:
                        lines.append(p_txt)
                        lines.append("")
    return "\n".join(lines) + "\n"


def process_crosswalk_tables_and_statutes() -> int:
    """Structure Markdown pipe-table crosswalks (reference/nist.gov/ai-rmf-crosswalks/*)
    and re-parse supply-chain-partnership, maryland/facial-recognition-laws, and govinfo.gov/cfaa.
    """
    count = 0
    # 1. Re-run supply-chain-partnership from supply-chain-partnership-raw.txt
    scp_dir = PUB_ROOT / "control/meti.go.jp/supply-chain-partnership"
    if scp_dir.exists():
        raw_txt = (scp_dir / "supply-chain-partnership-raw.txt").read_text(encoding="utf-8", errors="replace")
        md_meta = json.loads((scp_dir / "supply-chain-partnership-metadata.json").read_text(encoding="utf-8"))
        md_text = promote_japanese_txt_headings(raw_txt, md_meta.get("name", "Supply Chain Partnership"))
        (scp_dir / "supply-chain-partnership.md").write_text(md_text, encoding="utf-8")
        nrows = run_parse_sections(scp_dir, "supply-chain-partnership")
        count += 1
        print(f"[RE-EXTRACT] control/meti.go.jp/supply-chain-partnership -> {nrows} sections")

    # 2. Maryland HB 338 (strip leading bill line numbers inside the bill block and promote 2-501..2-510 and SECTION 1..2)
    md_law_dir = PUB_ROOT / "regulation/maryland.gov/facial-recognition-laws"
    if md_law_dir.exists():
        md_path = md_law_dir / "facial-recognition-laws.md"
        txt = md_path.read_text(encoding="utf-8", errors="replace")
        txt = re.sub(r"^```[^\n]*\n?", "", txt, flags=re.MULTILINE)
        lines = []
        for l in txt.splitlines():
            clean_l = re.sub(r"^\s*\d{1,2}\s{3,}", "", l).strip()
            if re.match(r"^SECTION\s+\d+\.\s+BE\s+IT\s+ENACTED", clean_l):
                lines.append(f"### {clean_l}")
            elif re.match(r"^2[–\-]5\d{2}\.\s*$", clean_l):
                sec_num = clean_l.rstrip(".").replace("–", "-")
                lines.append(f"#### Section {sec_num}")
            else:
                lines.append(l)
        md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        nrows = run_parse_sections(md_law_dir, "facial-recognition-laws")
        count += 1
        print(f"[RE-EXTRACT] regulation/maryland.gov/facial-recognition-laws -> {nrows} sections")

    # 3. NIST AI RMF Crosswalks (parse Markdown pipe tables into structured rows)
    cw_root = PUB_ROOT / "reference/nist.gov/ai-rmf-crosswalks"
    if cw_root.exists():
        for mp in sorted(cw_root.rglob("*-metadata.json")):
            parent = mp.parent
            if parent == cw_root:
                continue
            stem = mp.name[: -len("-metadata.json")]
            md_files = [p for p in parent.glob("*.md") if p.name != "README.md" and not p.name.endswith("-metadata.md")]
            if not md_files:
                continue
            txt = md_files[0].read_text(encoding="utf-8", errors="replace")
            rows = []
            headers: list[str] = []
            for line in txt.splitlines():
                s = line.strip()
                if not (s.startswith("|") and s.endswith("|")):
                    continue
                cells = [re.sub(r"<br\s*/?>", "\n", c).strip() for c in s.strip("|").split("|")]
                if all(re.match(r"^[:\-\s]*$", c) for c in cells):
                    continue
                if not headers:
                    headers = [re.sub(r"\*+", "", c).strip() or f"col_{i+1}" for i, c in enumerate(cells)]
                    continue
                non_empty = [c for c in cells if c]
                if not non_empty:
                    continue
                first_col = re.sub(r"\*+", "", non_empty[0]).strip()
                m_id = re.match(r"^((?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+(?:\.\d+)?)\s*[:\-–—]?\s*(.*)$", first_col, re.I)
                if m_id:
                    sid = m_id.group(1).upper()
                    sname = m_id.group(2).strip() or sid
                    ikind = "numbered"
                else:
                    sid = ""
                    sname = first_col[:120]
                    ikind = ""
                body_parts = []
                for idx_c, cell_val in enumerate(cells):
                    if not cell_val:
                        continue
                    hdr = headers[idx_c] if idx_c < len(headers) else f"Column {idx_c+1}"
                    body_parts.append(f"{hdr}: {cell_val}")
                rows.append({
                    "depth": 2,
                    "section_id": sid,
                    "section_name": sname,
                    "id_kind": ikind,
                    "parent_id": "",
                    "body": "\n\n".join(body_parts),
                })
            if len(rows) > 2:
                jpath = parent / f"{stem}-sections.json"
                cpath = parent / f"{stem}-sections.csv"
                fields = ["depth", "section_id", "section_name", "id_kind", "parent_id", "body"]
                with cpath.open("w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
                    w.writeheader()
                    w.writerows(rows)
                jpath.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                count += 1
                print(f"[CROSSWALK TABLE] {parent.relative_to(PUB_ROOT)} -> {len(rows)} rows")

    # 4. Japan e-Gov Law XML statutes (Basic Act on Cybersecurity + Active Cyber Defense Act)
    for rel, stem, law_id, title in [
        (
            "regulation/cyber.go.jp/basic-act-cybersecurity",
            "basic-act-cybersecurity",
            "426AC1000000104",
            "サイバーセキュリティ基本法 (Basic Act on Cybersecurity, Act No. 104 of 2014)",
        ),
        (
            "regulation/cyber.go.jp/active-cyber-defense-act",
            "active-cyber-defense-act",
            "507AC0000000042",
            "重要電子計算機に対する不正な行為による被害の防止に関する法律 (Active Cyber Defense Act, Act No. 42 of 2025)",
        ),
    ]:
        d = PUB_ROOT / rel
        if d.exists() and not (d / f"{stem}-sections.json").exists():
            md_text = egov_xml_to_md(law_id, title)
            if len(md_text) > 1000:
                (d / f"{stem}.md").write_text(md_text, encoding="utf-8")
                nrows = run_parse_sections(d, stem)
                count += 1
                print(f"[EGOV XML] {rel} -> {nrows} sections")
    return count


def main():
    c_priv = process_private_json_no_csv()
    c_pub_j2c = process_public_json_no_csv()
    c_pub_c2j = process_public_csv_no_json()
    c_raw = process_raw_on_disk()
    c_md = process_markdown_only()
    c_cw = process_crosswalk_tables_and_statutes()
    print(
        f"\nBatch 1A summary: private_json->csv={c_priv}, public_json->csv={c_pub_j2c}, "
        f"public_csv->json={c_pub_c2j}, raw_extracted={c_raw}, md_structured={c_md}, crosswalk_statutes={c_cw}"
    )


if __name__ == "__main__":
    main()
