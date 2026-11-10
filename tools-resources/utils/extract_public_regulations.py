#!/usr/bin/env python3
"""Extract, structure, and clean public government regulations for Issue #145.

1. Cleans and re-extracts the existing regulation directories in
   `dataset-public-laws-regulations-standards/regulation/` that had portal
   navigation wrappers, duplicate TOC sections, or missing `section_id`s.
2. Extracts the remaining unextracted public government bills, statutes,
   decrees, and regulations registered in `CloudSecurityAlliance/SecID/registry/regulation/`
   into `dataset-public-laws-regulations-standards/regulation/<namespace>/<name>/`.

Usage:
    python3 tools-resources/utils/extract_public_regulations.py --step clean
    python3 tools-resources/utils/extract_public_regulations.py --step extract
    python3 tools-resources/utils/extract_public_regulations.py --step all
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_track2_corpus import (  # noqa: E402
    REPO_ROOT,
    html_to_clean_markdown,
    pdf_bytes_to_markdown,
    run_parse_sections,
    write_metadata,
)
from extract_track2_wave2 import (  # noqa: E402
    _decode_html_bytes,
    derive_published_date,
    ensure_hierarchical_headings,
    fallback_pdf_text_to_markdown,
    fetch_url_bytes,
    find_embedded_pdf_urls,
    license_for_tld,
    postprocess_markdown_structure,
)
from structure_remaining_corpus import (  # noqa: E402
    egov_xml_to_md,
    normalize_statute_markdown,
)

SECID_REG_DIR = Path("/Users/kurt/GitHub/CloudSecurityAlliance/SecID/registry/regulation")
PUB_REG_DIR = REPO_ROOT / "regulation"
PARSE_CANADA_XML = SCRIPT_DIR / "parse_canada_justice_xml.py"

# Direct full-text URL overrides for regulations whose registry URL points to a landing page,
# bill overview page, or moved file.
REGULATION_URL_OVERRIDES: dict[str, list[str]] = {
    # Australia
    "oaic.gov.au/privacy-act": [
        "https://www.legislation.gov.au/C2004A03712/latest/downloads",
    ],
    "industry.gov.au/ai-action-plan": [
        "https://wp.oecd.ai/app/uploads/2021/12/Australia_AI_Action_Plan_2021.pdf",
    ],
    "esafety.gov.au/online-safety-act-2021": [
        "https://www.legislation.gov.au/C2021A00076/latest/downloads",
    ],
    "homeaffairs.gov.au/soci-act": [
        "https://www.legislation.gov.au/C2018A00029/latest/downloads",
    ],
    "homeaffairs.gov.au/cirmp-rules": [
        "https://www.legislation.gov.au/F2023L00112/latest/downloads",
    ],
    "homeaffairs.gov.au/cyber-security-act-2024": [
        "https://www.legislation.gov.au/C2024A00098/latest/downloads",
    ],
    # Canada
    "parl.ca/aida": [
        "https://www.parl.ca/Content/Bills/441/Government/C-27/C-27_1/C-27_E.xml",
    ],
    # California & US States
    "ca.gov/caloppa": [
        "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=BPC&division=8.&title=&part=&chapter=22.&article=",
    ],
    "oregon.gov/ocpa": [
        "https://olis.oregonlegislature.gov/liz/2023R1/Downloads/MeasureDocument/SB619/Enrolled",
    ],
    "oregon.gov/sb-1546": [
        "https://olis.oregonlegislature.gov/liz/2026R1/Downloads/MeasureDocument/SB1546/Introduced",
    ],
    "wa.gov/my-health-my-data-act": [
        "https://app.leg.wa.gov/RCW/default.aspx?cite=19.373&full=true",
    ],
    "wa.gov/hb-2225": [
        "https://lawfilesext.leg.wa.gov/biennium/2025-26/Pdf/Bills/House%20Passed%20Legislature/2225-S.PL.pdf",
    ],
    "ny.gov/shield-act": [
        "https://legislation.nysenate.gov/pdf/bills/2019/S5575B",
    ],
    "ny.gov/nybcl": [
        "https://legislation.nysenate.gov/pdf/bills/2021/A27",
    ],
    "ny.gov/local-law-144-ai-hiring": [
        "https://rules.cityofnewyork.us/wp-content/uploads/2023/04/DCWP-NOA-for-Use-of-Automated-Employment-Decisionmaking-Tools.pdf",
    ],
    "ny.gov/ai-companion-models-law": [
        "https://legislation.nysenate.gov/pdf/bills/2025/S3008C",
    ],
    "in.gov/incdpa": [
        "https://web.archive.org/web/20250610002709id_/https://iga.in.gov/pdf-documents/123/2023/senate/bills/SB0005/SB0005.05.ENRH.pdf",
    ],
    "nv.gov/privacy-amendments": [
        "https://web.archive.org/web/20261109075716id_/https://www.leg.state.nv.us/NRS/NRS-603A.html",
    ],
    "texas.gov/cubi-biometric-privacy": [
        "https://capitol.texas.gov/tlodocs/81R/billtext/html/HB03186F.htm",
    ],
    "texas.gov/tdpsa": [
        "https://capitol.texas.gov/tlodocs/88R/billtext/html/HB00004F.htm",
    ],
    "texas.gov/hb-149": [
        "https://capitol.texas.gov/tlodocs/89R/billtext/html/HB00149I.htm",
    ],
    "florida.gov/fdbr": [
        "https://www.flsenate.gov/Session/Bill/2023/262/BillText/er/HTML",
    ],
    "kentucky.gov/kcdpa": [
        "https://apps.legislature.ky.gov/recorddocuments/bill/24RS/hb15/bill.pdf",
    ],
    "maryland.gov/modpa": [
        "https://mgaleg.maryland.gov/2024RS/bills/sb/sb0541e.pdf",
    ],
    "nebraska.gov/lb-525": [
        "https://nebraskalegislature.gov/FloorDocs/109/PDF/Intro/LB525.pdf",
    ],
    "nebraska.gov/ndpa": [
        "https://nebraskalegislature.gov/FloorDocs/108/PDF/Slip/LB1074.pdf",
    ],
    "vermont.gov/vdpa": [
        "https://legislature.vermont.gov/Documents/2026/Docs/BILLS/S-0071/S-0071%20As%20Introduced.pdf",
    ],
    # US Federal
    "congress.gov/guard-act-s3062": [
        "https://www.govinfo.gov/content/pkg/BILLS-119s3062is/html/BILLS-119s3062is.htm",
    ],
    "congress.gov/chat-act-s2714": [
        "https://www.govinfo.gov/content/pkg/BILLS-119s2714is/html/BILLS-119s2714is.htm",
    ],
    "govinfo.gov/sox": [
        "https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm",
    ],
    "bis.gov/ear-advanced-computing": [
        "https://www.govinfo.gov/content/pkg/FR-2025-01-15/pdf/2025-00636.pdf",
    ],
    # Germany
    "gesetze-im-internet.de/bsig-2009": [
        "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/BSI/BSI_Act_BSIG.pdf?__blob=publicationFile&v=2",
    ],
    # International / Treaties / Regional
    "au.int/malabo-convention": [
        "https://au.int/sites/default/files/treaties/29560-treaty-0048_-_african_union_convention_on_cyber_security_and_personal_data_protection_e.pdf",
    ],
    "coe.int/ets-185": [
        "https://rm.coe.int/1680081561",
    ],
    "coe.int/cets-225": [
        "https://rm.coe.int/1680a49dab",
    ],
    # South Africa
    "gov.za/popia": [
        "https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf",
    ],
    "gov.za/cybercrimes-act": [
        "https://www.gov.za/sites/default/files/gcis_document/202106/44651gon324.pdf",
    ],
    # Chile
    "bcn.cl/ley-21663": [
        "https://www.bcn.cl/leychile/Servicios/Navegar/get_html_norma?idNorma=1202434",
    ],
    # UK publications
    "gov.uk/critical-third-parties-regime": [
        "https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2024/november/ps1624.pdf",
    ],
}

# Japan e-Gov Law API IDs for Japanese statutes
JAPAN_EGOV_LAW_IDS: dict[str, tuple[str, str]] = {
    "cao.go.jp/economic-security-promotion": (
        "504AC0000000043",
        "経済施策を一体的に講ずることによる安全保障の確保の推進に関する法律 (Economic Security Promotion Act, Act No. 43 of 2022)",
    ),
    "cas.go.jp/specified-secret-protection": (
        "425AC0000000108",
        "特定秘密の保護に関する法律 (Act on the Protection of Specially Designated Secrets, Act No. 108 of 2013)",
    ),
    "soumu.go.jp/telecommunications-business-act": (
        "359AC0000000086",
        "電気通信事業法 (Telecommunications Business Act, Act No. 86 of 1984)",
    ),
    "cas.go.jp/ai-promotion-act": (
        "507AC0000000053",
        "人工知能関連技術の研究開発及び活用の推進に関する法律 (AI Promotion Act, Act No. 53 of 2025)",
    ),
    "cas.go.jp/ucal": (
        "411AC0000000128",
        "不正アクセス行為の禁止等に関する法律 (Unauthorized Computer Access Law, Act No. 128 of 1999)",
    ),
    "fsa.go.jp/payment-services-act": (
        "421AC0000000059",
        "資金決済に関する法律 (Payment Services Act, Act No. 59 of 2009)",
    ),
    "meti.go.jp/unfair-competition-prevention": (
        "405AC0000000047",
        "不正競争防止法 (Unfair Competition Prevention Act, Act No. 47 of 1993)",
    ),
    "meti.go.jp/installment-sales": (
        "336AC0000000159",
        "割賦販売法 (Installment Sales Act, Act No. 159 of 1961)",
    ),
}

# Aliases mapping SecID match_node slugs to existing dataset-public/regulation directories
EXISTING_SLUG_ALIASES: dict[str, str] = {
    "ny.gov/dfs-500": "ny.gov/nydfs-500",
    "ny.gov/ll144": "ny.gov/local-law-144-ai-hiring",
    "ca.gov/ccpa": "ca.gov/ccpa-cpra",
    "ca.gov/cpra": "ca.gov/ccpa-cpra",
    "ca.gov/sb-53": "ca.gov/sb-53-transparency-in-frontier-ai-act",
    "cac.gov.cn/generative-ai-measures": "cac.gov.cn/genai-interim-measures",
    "priv.gc.ca/pipeda": "canada.ca/pipeda",
    "colorado.gov/cpa": "colorado.gov/cpa-privacy-act",
    "gov.uk/ai-action-plan": "gov.uk/ai-opportunities-action-plan",
    "gov.uk/dpa-2018": "gov.uk/data-protection-act-2018",
    "gov.uk/cma": "gov.uk/computer-misuse-act",
    "gov.uk/nis-regs-2018": "gov.uk/nis-regulations",
    "canada.ca/aida": "parl.ca/aida",
}


def find_wayback_clean_url(orig_url: str, min_compressed_bytes: int = 3000) -> str | None:
    """Query Wayback Machine CDX API for the most recent HTTP 200 capture with payload > min_compressed_bytes."""
    cdx_url = (
        f"http://web.archive.org/cdx/search/cdx?url={urllib.parse.quote(orig_url, safe='')}"
        f"&filter=statuscode:200&output=json&limit=-20"
    )
    try:
        req = urllib.request.Request(cdx_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            rows = json.loads(r.read().decode("utf-8", errors="ignore"))
        for row in reversed(rows[1:]):
            if len(row) >= 7 and str(row[6]).isdigit() and int(row[6]) >= min_compressed_bytes:
                ts = row[1]
                return f"https://web.archive.org/web/{ts}id_/{orig_url}"
    except Exception:
        pass
    return None


def parse_german_xml_zip(zip_bytes: bytes, doc_title: str) -> str:
    """Convert a Gesetze-im-Internet `xml.zip` archive into hierarchical Markdown."""
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    xml_names = [n for n in z.namelist() if n.endswith(".xml")]
    if not xml_names:
        return ""
    root = ET.fromstring(z.read(xml_names[0]))
    lines = [f"# {doc_title}", ""]
    for norm in root.findall("norm"):
        enbez = (norm.findtext(".//metadaten/enbez") or "").strip()
        titel = " ".join((norm.findtext(".//metadaten/titel") or "").split())
        gl_bez = " ".join((norm.findtext(".//metadaten/gliederungseinheit/gliederungsbez") or "").split())
        gl_tit = " ".join((norm.findtext(".//metadaten/gliederungseinheit/gliederungstitel") or "").split())
        if enbez == "Inhaltsübersicht":
            continue
        if gl_bez:
            lvl = "##" if re.match(r"^(?:Teil|Buch)\b", gl_bez, re.I) else "###"
            h_txt = f"{gl_bez}: {gl_tit}" if gl_tit else gl_bez
            lines.append(f"{lvl} {h_txt}")
            lines.append("")
        if enbez:
            h_txt = f"{enbez} {titel}".strip()
            lines.append(f"#### {h_txt}")
            lines.append("")
        content_el = norm.find(".//textdaten/text/Content")
        if content_el is not None:
            for p_el in content_el.findall(".//P"):
                p_txt = " ".join("".join(p_el.itertext()).split())
                if p_txt:
                    lines.append(p_txt)
                    lines.append("")
            if not content_el.findall(".//P"):
                raw_t = " ".join("".join(content_el.itertext()).split())
                if raw_t:
                    lines.append(raw_t)
                    lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_uk_clml_xml(xml_bytes: bytes, doc_title: str) -> str:
    """Convert UK legislation.gov.uk CLML `/data.xml` into hierarchical Markdown."""
    root = ET.fromstring(xml_bytes)
    ns = {"leg": "http://www.legislation.gov.uk/namespaces/legislation"}
    lines = [f"# {doc_title}", ""]

    def _emit_p1group(p1g: ET.Element, sec_prefix: str = "Section", heading_hashes: str = "####") -> None:
        title_el = p1g.find("leg:Title", ns)
        g_title = " ".join("".join(title_el.itertext()).split()) if title_el is not None else ""
        for p1 in p1g.findall(".//leg:P1", ns):
            pnum_el = p1.find("leg:Pnumber", ns)
            pnum = " ".join("".join(pnum_el.itertext()).split()) if pnum_el is not None else ""
            if pnum:
                h_str = f"{sec_prefix} {pnum}: {g_title}" if g_title else f"{sec_prefix} {pnum}"
                lines.append(f"{heading_hashes} {h_str}")
                lines.append("")
            paras = []
            for p2 in p1.findall(".//leg:P2", ns):
                p2num = " ".join("".join(p2.find("leg:Pnumber", ns).itertext()).split()) if p2.find("leg:Pnumber", ns) is not None else ""
                p2para = " ".join("".join(p2.find("leg:P2para", ns).itertext()).split()) if p2.find("leg:P2para", ns) is not None else ""
                if p2para:
                    paras.append(f"({p2num}) {p2para}" if p2num else p2para)
            if not paras:
                for p1p in p1.findall("leg:P1para", ns):
                    t_str = " ".join("".join(p1p.itertext()).split())
                    if t_str:
                        paras.append(t_str)
            for p_line in paras:
                lines.append(p_line)
                lines.append("")

    body = root.find(".//leg:Body", ns)
    if body is not None:
        parts = body.findall("leg:Part", ns)
        if parts:
            for part in parts:
                p_num = " ".join("".join(part.find("leg:Number", ns).itertext()).split()) if part.find("leg:Number", ns) is not None else ""
                p_tit = " ".join("".join(part.find("leg:Title", ns).itertext()).split()) if part.find("leg:Title", ns) is not None else ""
                if p_num or p_tit:
                    lines.append(f"## {p_num}: {p_tit}".strip(": "))
                    lines.append("")
                chapters = part.findall("leg:Chapter", ns)
                if chapters:
                    for ch in chapters:
                        c_num = " ".join("".join(ch.find("leg:Number", ns).itertext()).split()) if ch.find("leg:Number", ns) is not None else ""
                        c_tit = " ".join("".join(ch.find("leg:Title", ns).itertext()).split()) if ch.find("leg:Title", ns) is not None else ""
                        if c_num or c_tit:
                            lines.append(f"### {c_num}: {c_tit}".strip(": "))
                            lines.append("")
                        for p1g in ch.findall(".//leg:P1group", ns):
                            _emit_p1group(p1g, "Section", "####")
                else:
                    for p1g in part.findall(".//leg:P1group", ns):
                        _emit_p1group(p1g, "Section", "###")
        else:
            for p1g in body.findall(".//leg:P1group", ns):
                _emit_p1group(p1g, "Section", "##")

    schedules = root.find(".//leg:Schedules", ns)
    if schedules is not None:
        for sched in schedules.findall("leg:Schedule", ns):
            s_num = " ".join("".join(sched.find("leg:Number", ns).itertext()).split()) if sched.find("leg:Number", ns) is not None else ""
            s_tit = " ".join("".join(sched.find("leg:TitleBlock/leg:Title", ns).itertext()).split()) if sched.find("leg:TitleBlock/leg:Title", ns) is not None else ""
            if s_num:
                lines.append(f"## {s_num}: {s_tit}".strip(": "))
                lines.append("")
                s_body = " ".join("".join(sched.itertext()).split())
                if s_body:
                    lines.append(s_body[:4000])
                    lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_utah_bill_xml(xml_bytes: bytes, doc_title: str) -> str:
    """Convert Utah Legislative General Counsel `<leg>` bill XML into hierarchical Markdown."""
    xml_str = xml_bytes.decode("utf-8", errors="ignore").replace('encoding="UTF-16"', 'encoding="UTF-8"')
    root = ET.fromstring(xml_str)
    lines = [f"# {doc_title}", ""]
    lt = root.find("lt")
    if lt is not None:
        lt_txt = " ".join("".join(lt.itertext()).split())
        if lt_txt:
            lines.append(lt_txt)
            lines.append("")
    for bsec in root.findall(".//bsec"):
        sec_el = bsec.find("section")
        if sec_el is not None:
            hchap = " ".join("".join(sec_el.find("headchap").itertext()).split()) if sec_el.find("headchap") is not None else ""
            hpart = " ".join("".join(sec_el.find("headpart").itertext()).split()) if sec_el.find("headpart") is not None else ""
            catline = " ".join("".join(sec_el.find("catline").itertext()).split()) if sec_el.find("catline") is not None else ""
            if hchap:
                lines.append(f"## Chapter {hchap}")
                lines.append("")
            if hpart:
                lines.append(f"### Part {hpart}")
                lines.append("")
            if catline:
                lines.append(f"#### {catline}")
                lines.append("")
            else:
                sn = bsec.attrib.get("sn", "")
                num = bsec.attrib.get("num", "")
                lines.append(f"#### {num or ('Section ' + sn)}")
                lines.append("")
            for child in sec_el:
                if child.tag in ("secline", "headchap", "headpart", "catline"):
                    continue
                c_txt = " ".join("".join(child.itertext()).split())
                if c_txt:
                    lines.append(c_txt)
                    lines.append("")
        else:
            sn = bsec.attrib.get("sn", "")
            raw_b = " ".join("".join(bsec.itertext()).split())
            if raw_b:
                m_sec = re.match(r"^(Section\s+\d+\.?\s*[^\.]+)\.\s*(.*)$", raw_b)
                if m_sec:
                    lines.append(f"#### {m_sec.group(1)}")
                    lines.append("")
                    if m_sec.group(2):
                        lines.append(m_sec.group(2))
                        lines.append("")
                else:
                    lines.append(f"#### Section {sn}" if sn else "#### Provision")
                    lines.append("")
                    lines.append(raw_b)
                    lines.append("")
    return "\n".join(lines).strip() + "\n"


def promote_multilingual_statute_headings(md: str, doc_title: str) -> str:
    """Promote statutory Part/Chapter/Section/Article headings across English, European, Latin American, and Asian laws."""
    # 1. Strip California Leginfo javascript:submitCodesValues(...) links while keeping the section number
    md = re.sub(r"\[(\d{3,5}[A-Za-z]?(?:\.\d+(?:\.\d+)?)?\.?)\]\(javascript:submitCodesValues\([^\n]+\)", r"\1", md)
    # 2. Strip Washington RCW [PDF](...) badge before RCW section link and merge consecutive RCW + Title headings
    md = re.sub(r"\[PDF\]\([^)]+\)\s*", "", md)
    md = re.sub(
        r"(?m)^###\s+RCW\s+\[?(\d+\.\d+\.\d+)\]?(?:\([^)]+\))?\s*\n+###\s+([^\n]+)$",
        r"### RCW \1: \2",
        md,
    )
    # 2b. Promote Washington bill "NEW SECTION. Sec. N." headings
    md = re.sub(
        r"(?m)^(?:\*\*)?NEW\s+SECTION\.(?:\*\*)?\s+(?:\*\*)?(Sec\.\s+\d+\.)(?:\*\*)?\s*(.*)$",
        r"### \1\n\n\2",
        md,
    )
    # 2c. Promote Taiwan law.moj.gov.tw linked article headings ("[第 1 條](...)")
    md = re.sub(r"(?m)^\[(第\s*\d+(?:-\d+)?\s*條)\]\([^)]+\)\s*$", r"### \1", md)
    # 2d. Promote France Légifrance bulleted Titre/Chapitre/Section and Article links
    md = re.sub(
        r"(?m)^\s*-\s+(?:Déplier)?((?:Titre|TITRE|Chapitre|CHAPITRE)\s+(?:[IVXLCDM]+(?:er)?|\d+)[^\n]*)$",
        r"## \1",
        md,
    )
    md = re.sub(
        r"(?m)^\s*-\s+(?:Déplier)?((?:Section|SECTION|Sous-section)\s+(?:[IVXLCDM]+(?:er)?|\d+)[^\n]*)$",
        r"### \1",
        md,
    )
    md = re.sub(r"(?m)^\s*-\s+\[(Article\s+[^\]]+)\]\([^)]+\)\s*$", r"#### \1", md)
    # 3. Unwrap Texas TLO layout pipe tables ("|  | SECTION 1. ... | |")
    if "|  | AN ACT | |" in md or "|  | BE IT ENACTED BY THE LEGISLATURE OF THE STATE OF TEXAS:" in md:
        tx_lines = []
        for l in md.splitlines():
            s = l.strip()
            if re.match(r"^\|\s*(?:---\s*\|\s*)+$", s) or re.match(r"^\|\s*\|\s*\|\s*\|?$", s):
                continue
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|") if c.strip()]
                s = " ".join(cells)
            tx_lines.append(s)
        # Reflow wrapped Texas bill lines into paragraphs before promoting SECTION / Sec. headings
        md = "\n".join(tx_lines)
        md = re.sub(r"\n(?=[a-z0-9\(\[]|[A-Z][a-z])", " ", md)
        md = re.sub(r"\s+(SECTION\s+\d+\.)", r"\n\n### \1", md)
        md = re.sub(r"\s+(Sec\.\s+\d+\.\d+[A-Za-z\-]*\.)", r"\n\n#### \1", md)
    # 4. Split inline New York bill section markers ("1 Section 1.", "3 § 2.", "6 § 899-aa.") onto heading lines
    if "The People of the State of New York, represented in Senate and Assembly" in md:
        md = re.sub(r"(?:^|\s)(?:\d{1,2}\s+)?(Section\s+\d+\.)", r"\n\n### \1", md)
        md = re.sub(r"(?:^|\s)(?:\d{1,2}\s+)?(§\s*\d+[A-Za-z\-]*\.)", r"\n\n#### \1", md)
    # 5. Promote Nevada NRS 603A section headings ("NRS 603A.010 Definitions.")
    md = re.sub(r"(?m)^(?:\*\*)?(NRS\s+603A\.\d+[A-Za-z]?)\b\s*([^\n]+)$", r"#### \1 \2", md)
    # 6. Promote Australia AI Action Plan numbered focus areas / actions and NYC DCWP § 5-300 rules
    md = re.sub(r"(?m)^(§\s*5-30\d\.\s+[^\n]+)$", r"### \1", md)
    md = re.sub(r"(?m)^(Focus\s+Area\s+\d+:\s+[^\n]+)$", r"## \1", md, flags=re.I)

    md = normalize_statute_markdown(md, doc_title, "regulation/force")
    lines = md.splitlines()
    out: list[str] = []
    in_toc = False
    for idx, line in enumerate(lines):
        s = line.strip()
        if not s:
            out.append("")
            continue
        s_clean = re.sub(r"^\*\*(.+?)\*\*$", r"\1", s).strip()
        # Detect TOC start
        if re.match(r"^(?:#+\s*)?(?:TABLE\s+OF\s+CONTENTS|Contents|Inhaltsübersicht|Índice|Sumario)$", s_clean, re.I):
            in_toc = True
            out.append(s_clean)
            continue
        if in_toc:
            if idx > 120 or re.match(r"^(?:CHAPTER\s+[I1]\b|PART\s+[I1]\b|TITLE\s+[I1]\b|Art\.\s*1[º°]?\b|Artículo\s+1\b|Article\s+1\b|SECTION\s+1\b|SEC\.\s*1\b|第一条\b|第\s*1\s*條\b|1-модда\b)", s_clean, re.I):
                in_toc = False
            else:
                out.append(re.sub(r"^#+\s*", "", line))
                continue
        if s.startswith("#"):
            out.append(line)
            continue
        # Promote CJK chapters and articles
        if re.match(r"^第\s*[一二三四五六七八九十百千0-9０-９]+\s*[章篇编部編]\b", s_clean) and len(s_clean) < 120:
            out.append(f"## {s_clean}")
        elif re.match(r"^第\s*[一二三四五六七八九十百千0-9０-９]+\s*[节節]\b", s_clean) and len(s_clean) < 120:
            out.append(f"### {s_clean}")
        elif m_cjk_art := re.match(r"^(第\s*[一二三四五六七八九十百千0-9０-９]+(?:\s*[-之の]\s*[一二三四五六七八九十0-9０-９]+)*\s*[条條](?:\s*[のノ之\-]\s*[一二三四五六七八九十百千0-9０-９]+)*)(?:[\s　]+(.+))?$", s_clean):
            art_id = re.sub(r"\s+", "", m_cjk_art.group(1))
            rest = (m_cjk_art.group(2) or "").strip()
            out.append(f"### {art_id}")
            if rest:
                out.append("")
                out.append(rest)
        # Promote Brazilian / Spanish / French / Italian / EU / German / Uzbek / Kazakh articles
        elif m_br_art := re.match(r"^(Art\.\s*\d+(?:-[A-Z])?[º°]?\.?)\s+(.+)$", s_clean):
            art_id = m_br_art.group(1).rstrip(".")
            rest = m_br_art.group(2).strip()
            out.append(f"#### {art_id}")
            out.append("")
            out.append(rest)
        elif re.match(r"^(?:TÍTULO|CAPÍTULO|Capítulo|CHAPITRE|Chapitre|TITRE|Titre|PARTE|Parte)\s+(?:[IVXLCDM]+(?:er)?|\d+)\b", s_clean) and len(s_clean) < 160:
            out.append(f"## {s_clean}")
        elif re.match(r"^(?:Seção|SEÇÃO|Subseção|Section|SECTION|Abschnitt)\s+(?:[IVXLCDM]+(?:er)?|\d+)\b", s_clean) and len(s_clean) < 160:
            out.append(f"### {s_clean}")
        elif re.match(r"^(?:Artículo|ARTÍCULO|Article|ARTICLE|Artikel|Articolo)\s+(?:[LRD]\.?\s*)?\d+(?:er|[A-Za-z])?(?:[\.\-]\d+[A-Za-z]*)*\.?(?:\s|$)", s_clean) and len(s_clean) < 200:
            out.append(f"#### {s_clean}")
        elif re.match(r"^\d+-(?:модда|modda|бап)\b", s_clean, re.I) and len(s_clean) < 220:
            out.append(f"#### {s_clean}")
        elif re.match(r"^(?:[IVXLCDM]+|\d+)-(?:боб|бўлим|тарау|bob)\b", s_clean, re.I) and len(s_clean) < 200:
            out.append(f"## {s_clean}")
        # US / State statutes (e.g. RCW 19.373.010, 87-1101, § 12D-101, Sec. 503.001, 13-61-101)
        elif re.match(r"^(?:RCW\s+\d+\.\d+\.\d+|§+\s*\d+[\dA-Za-z\.\-]*|Sec\.\s*\d+[\dA-Za-z\.\-]*|\d{1,3}-[0-9A-Za-z]{1,5}-\d{1,5}[A-Za-z]?)\b", s_clean) and len(s_clean) < 200:
            out.append(f"#### {s_clean}")
        else:
            out.append(line)
    res = "\n".join(out)
    if not res.lstrip().startswith("# "):
        res = f"# {doc_title}\n\n{res.lstrip()}"
    return res.strip() + "\n"


def expand_regulation_candidates(rel_slug: str, orig_url: str) -> list[str]:
    """Expand a regulation's registry URL into prioritized full-text download candidates."""
    cands: list[str] = []
    if rel_slug in REGULATION_URL_OVERRIDES:
        cands.extend(REGULATION_URL_OVERRIDES[rel_slug])

    # 1. UK legislation.gov.uk -> /data.xml
    if "legislation.gov.uk/" in orig_url:
        base_uk = re.sub(r"/(?:contents(?:/made)?|enacted|made)/?$", "", orig_url.rstrip("/"))
        cands.append(f"{base_uk}/data.xml")

    # 2. Germany gesetze-im-internet.de -> /xml.zip
    if "gesetze-im-internet.de/" in orig_url:
        base_de = orig_url.rstrip("/")
        if not base_de.endswith(".zip"):
            cands.append(f"{base_de}/xml.zip")

    # 3. EU EUR-Lex -> HTML and Cellar (both CELEX: and /eli/{reg|dir}/{YYYY}/{N}/oj URLs)
    m_celex = re.search(r"CELEX[:%3A]+([0-9A-Z]+)", orig_url, re.I)
    if m_celex:
        celex = m_celex.group(1).upper()
        cands.append(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}")
        cands.append(f"https://publications.europa.eu/resource/celex/{celex}")
    m_eli = re.search(r"eur-lex\.europa\.eu/eli/(reg|dir)/(\d{4})/(\d+)/oj", orig_url, re.I)
    if m_eli:
        kind_char = "R" if m_eli.group(1).lower() == "reg" else "L"
        celex = f"3{m_eli.group(2)}{kind_char}{int(m_eli.group(3)):04d}"
        cands.append(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}")
        cands.append(f"https://publications.europa.eu/resource/celex/{celex}")

    # 3b. Utah Legislature static bill shell -> Enrolled XML & Introduced XML
    m_ut = re.search(r"le\.utah\.gov/~(\d{4})/bills/static/([A-Z]+\d+)\.html", orig_url, re.I)
    if m_ut:
        uy, ub = m_ut.group(1), m_ut.group(2).upper()
        cands.append(f"https://le.utah.gov/Session/{uy}/bills/enrolled/{ub}.xml")
        cands.append(f"https://le.utah.gov/~{uy}/bills/xmlEnrolled/{ub}.xml")
        cands.append(f"https://le.utah.gov/Session/{uy}/bills/introduced/{ub}.xml")

    # 4. California leginfo -> billTextClient.xhtml
    if "leginfo.legislature.ca.gov/faces/billNavClient.xhtml" in orig_url:
        cands.append(orig_url.replace("billNavClient.xhtml", "billTextClient.xhtml"))

    # 5. Australia legislation.gov.au -> /latest/downloads
    m_au = re.search(r"legislation\.gov\.au/([A-Z]\d+[A-Z]\d+)", orig_url)
    if m_au:
        cands.append(f"https://www.legislation.gov.au/{m_au.group(1)}/latest/downloads")

    # 6. Ireland irishstatutebook.ie -> /print
    if "irishstatutebook.ie/" in orig_url and not orig_url.rstrip("/").endswith("/print"):
        cands.append(re.sub(r"/html/?$", "/print", orig_url.rstrip("/")))

    # 7. Brazil planalto.gov.br -> Wayback CDX clean capture (since direct planalto returns 814-byte Acesso Negado)
    if "planalto.gov.br/" in orig_url:
        wb_clean = find_wayback_clean_url(orig_url, min_compressed_bytes=3000)
        if wb_clean:
            cands.append(wb_clean)

    # 8. Original URL (unless it is only a bare domain homepage)
    parsed = urllib.parse.urlparse(orig_url)
    if parsed.path.strip("/") or parsed.query:
        cands.append(orig_url)
        wb = find_wayback_clean_url(orig_url, min_compressed_bytes=3000)
        if wb and wb not in cands:
            cands.append(wb)

    return cands


def clean_existing_regulations() -> None:
    """Clean and re-extract the existing regulation directories in dataset-public/regulation/."""
    print("=== Step 1: Cleaning & Re-extracting Existing Regulations ===")

    # 1. Canada Bill C-27 (parl.ca/aida) from Parliament of Canada XML
    aida_dir = PUB_REG_DIR / "parl.ca/aida"
    if aida_dir.exists():
        xml_data, final_u = fetch_url_bytes("https://www.parl.ca/Content/Bills/441/Government/C-27/C-27_1/C-27_E.xml")
        if xml_data and b"<Bill" in xml_data[:2000]:
            (aida_dir / "aida.xml").write_bytes(xml_data)
            doc_title = "Bill C-27: Digital Charter Implementation Act, 2022 (CPPA, PIDPTA, and Artificial Intelligence and Data Act — AIDA)"
            subprocess.run(
                [sys.executable, str(PARSE_CANADA_XML), str(aida_dir), "--out-stem", "aida", "--title", doc_title],
                check=True,
            )
            n_sec = len(json.loads((aida_dir / "aida-sections.json").read_text(encoding="utf-8")))
            mp = aida_dir / "aida-metadata.json"
            if mp.exists():
                m = json.loads(mp.read_text(encoding="utf-8"))
                m["links"]["textUsed"] = final_u
                m["current_extraction"] = {
                    "date": "2026-11-10",
                    "tool": "tools-resources/utils/parse_canada_justice_xml.py",
                    "s3_archive_path": "",
                    "notes": f"Parsed {n_sec} sections from Parliament of Canada Bill C-27 XML (CPPA, PIDPTA, and AIDA).",
                }
                mp.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"[CANADA XML] parl.ca/aida -> {n_sec} sections")

    # 2. Japan e-Gov XML statutes already in dataset-public/regulation/
    for rel_slug in [
        "cao.go.jp/economic-security-promotion",
        "cas.go.jp/specified-secret-protection",
        "soumu.go.jp/telecommunications-business-act",
    ]:
        law_id, title = JAPAN_EGOV_LAW_IDS[rel_slug]
        doc_dir = PUB_REG_DIR / rel_slug
        if not doc_dir.exists():
            continue
        stem = doc_dir.name
        md_text = egov_xml_to_md(law_id, title)
        if len(md_text) > 1000:
            (doc_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")
            n_sec, n_id = run_parse_sections(doc_dir, stem)
            # Remove older *-overview-sections.{json,csv} if canonical <stem>-sections.{json,csv} now exists
            for old_f in doc_dir.glob("*-overview-sections.*"):
                old_f.unlink(missing_ok=True)
            print(f"[JP EGOV XML] {rel_slug} -> {n_sec} sections ({n_id} IDs)")

    # 3. Clean California existing markdown files (caloppa, sb-1001-bot-disclosure, physicians-make-decisions-act)
    caloppa_dir = PUB_REG_DIR / "ca.gov/caloppa"
    if caloppa_dir.exists():
        data, final_u = fetch_url_bytes(REGULATION_URL_OVERRIDES["ca.gov/caloppa"][0])
        if data:
            md = html_to_clean_markdown(
                _decode_html_bytes(data),
                final_u,
                "California Online Privacy Protection Act (CalOPPA — Business and Professions Code §§ 22575–22579)",
            )
            md = promote_multilingual_statute_headings(
                md,
                "California Online Privacy Protection Act (CalOPPA — Business and Professions Code §§ 22575–22579)",
            )
            (caloppa_dir / "caloppa.md").write_text(md, encoding="utf-8")
            n_sec, n_id = run_parse_sections(caloppa_dir, "caloppa")
            print(f"[CA LEGINFO] ca.gov/caloppa -> {n_sec} sections ({n_id} IDs)")

    for rel_slug, stem, doc_title in [
        (
            "ca.gov/sb-1001-bot-disclosure",
            "sb-1001-bot-disclosure",
            "California SB-1001: Bots Disclosure Act (Business and Professions Code §§ 17940–17943)",
        ),
        (
            "ca.gov/physicians-make-decisions-act",
            "physicians-make-decisions-act",
            "California SB-1120: Physicians Make Decisions Act (Health & Safety Code § 1367.01; Insurance Code § 10123.135)",
        ),
    ]:
        doc_dir = PUB_REG_DIR / rel_slug
        md_path = doc_dir / f"{stem}.md"
        if md_path.exists():
            txt = md_path.read_text(encoding="utf-8")
            if "## Bill Text" in txt:
                txt = f"# {doc_title}\n\n## Bill Text" + txt.split("## Bill Text", 1)[1]
            elif "# SB-" in txt:
                idx_sb = txt.find("# SB-")
                txt = txt[idx_sb:]
            txt = promote_multilingual_statute_headings(txt, doc_title)
            md_path.write_text(txt, encoding="utf-8")
            n_sec, n_id = run_parse_sections(doc_dir, stem)
            print(f"[CA CLEAN] {rel_slug} -> {n_sec} sections ({n_id} IDs)")

    # 4. Clean Delaware DPDPA, Florida 501.171, Iowa ICDPA, Montana MCDPA
    del_dir = PUB_REG_DIR / "delaware.gov/dpdpa"
    if del_dir.exists():
        txt = (del_dir / "dpdpa.md").read_text(encoding="utf-8")
        if "### TITLE 6" in txt:
            txt = "# Delaware Personal Data Privacy Act (6 Del. C. Chapter 12D)\n\n### TITLE 6" + txt.split("### TITLE 6", 1)[1]
        txt = re.sub(r"(?m)^(?:#+\s*)?(§\s*12D-\d+\..+)$", r"#### \1", txt)
        (del_dir / "dpdpa.md").write_text(txt, encoding="utf-8")
        n_sec, n_id = run_parse_sections(del_dir, "dpdpa")
        print(f"[DE CLEAN] delaware.gov/dpdpa -> {n_sec} sections ({n_id} IDs)")

    fl_dir = PUB_REG_DIR / "florida.gov/biometric-privacy-laws"
    if fl_dir.exists():
        txt = (fl_dir / "biometric-privacy-laws.md").read_text(encoding="utf-8")
        if "#### SECTION 171" in txt:
            txt = "# Florida Information Protection Act (Fla. Stat. § 501.171)\n\n#### SECTION 171" + txt.split("#### SECTION 171", 1)[1]
        txt = re.sub(r"(?m)^\((\d{1,2})\)\s+([A-Z][A-Z\s,\-—]{2,60}\.—)", r"#### Section (\1) \2", txt)
        (fl_dir / "biometric-privacy-laws.md").write_text(txt, encoding="utf-8")
        n_sec, n_id = run_parse_sections(fl_dir, "biometric-privacy-laws")
        print(f"[FL CLEAN] florida.gov/biometric-privacy-laws -> {n_sec} sections ({n_id} IDs)")

    ia_dir = PUB_REG_DIR / "iowa.gov/icdpa"
    if ia_dir.exists():
        txt = (ia_dir / "icdpa.md").read_text(encoding="utf-8")
        txt = re.sub(r"(?m)^```\s*$", "", txt)
        # Strip the 2-column TOC lines ("### 715D.1      Definitions.      715D.6 ...")
        lines = [
            l for l in txt.splitlines()
            if not re.match(r"^###\s+715D\.[1-5]\s{3,}", l.strip())
        ]
        (ia_dir / "icdpa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        n_sec, n_id = run_parse_sections(ia_dir, "icdpa")
        print(f"[IA CLEAN] iowa.gov/icdpa -> {n_sec} sections ({n_id} IDs)")

    mt_dir = PUB_REG_DIR / "mt.gov/mcdpa"
    if mt_dir.exists():
        txt = (mt_dir / "mcdpa.md").read_text(encoding="utf-8")
        lines = []
        seen_part = False
        for l in txt.splitlines():
            s = l.strip()
            if s.startswith(("# Montana Code Annotated", "####  TITLE 30", "###  CHAPTER 14")):
                continue
            if s.startswith("##  Part 28"):
                if seen_part:
                    continue
                seen_part = True
            if re.match(r"^#\s+[A-Z]", s) and not s.startswith("# Montana Consumer"):
                continue
            if re.match(r"^30-14-28\d{2}\.\s+", s):
                lines.append(f"### {s}")
            else:
                lines.append(l)
        (mt_dir / "mcdpa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        n_sec, n_id = run_parse_sections(mt_dir, "mcdpa")
        print(f"[MT CLEAN] mt.gov/mcdpa -> {n_sec} sections ({n_id} IDs)")

    ma_dir = PUB_REG_DIR / "mass.gov/ai-bills"
    if ma_dir.exists():
        txt = (ma_dir / "ai-bills.md").read_text(encoding="utf-8")
        if "## Search Results Table" in txt:
            body_part = txt.split("## Search Results Table", 1)[1]
            if "## Site Information & Links" in body_part:
                body_part = body_part.split("## Site Information & Links", 1)[0]
            body_part = re.sub(
                r"(?m)^\|\s*\[\s*((?:H|S|HD|SD)\.\d+(?:\s+[A-Z])?)\s*\]\(([^)]+)\)\s*\|\s*(.+)$",
                lambda m: f"\n### {m.group(1).replace(' ', '-')}: Sponsor / Committee — {m.group(3).strip()}\n",
                body_part,
            )
            clean_ma = "# Massachusetts AI Legislation Tracker (194th General Court)\n\n" + body_part.strip() + "\n"
            (ma_dir / "ai-bills.md").write_text(clean_ma, encoding="utf-8")
            n_sec, n_id = run_parse_sections(ma_dir, "ai-bills")
            print(f"[MA CLEAN] mass.gov/ai-bills -> {n_sec} sections ({n_id} IDs)")

    # 5. Re-extract existing directories that had landing pages instead of full text
    for rel_slug, stem, doc_title in [
        ("oaic.gov.au/privacy-act", "privacy-act", "Privacy Act 1988 (No. 119, 1988 — Australia)"),
        ("industry.gov.au/ai-action-plan", "ai-action-plan", "Australia's AI Action Plan (June 2021)"),
        ("oregon.gov/ocpa", "ocpa", "Oregon Consumer Privacy Act (SB 619, 2023)"),
        ("wa.gov/my-health-my-data-act", "my-health-my-data-act", "Washington My Health My Data Act (Chapter 19.373 RCW)"),
        ("ny.gov/shield-act", "shield-act", "New York Stop Hacks and Improve Electronic Data Security (SHIELD) Act (S5575B / GBL §§ 899-aa, 899-bb)"),
        ("ny.gov/nybcl", "nybcl", "New York Biometric Privacy Act (Assembly Bill A27 / General Business Law Article 32-A)"),
        ("ny.gov/local-law-144-ai-hiring", "local-law-144-ai-hiring", "New York City Local Law 144 of 2021 — Automated Employment Decision Tools (DCWP Final Rule, 6 RCNY §§ 5-300 to 5-304)"),
        ("in.gov/incdpa", "incdpa", "Indiana Consumer Data Protection Act (HEA/SEA 5 — Indiana Code Title 24, Article 15)"),
        ("nv.gov/privacy-amendments", "privacy-amendments", "Nevada Revised Statutes Chapter 603A — Security and Privacy of Personal Information"),
        ("texas.gov/cubi-biometric-privacy", "cubi-biometric-privacy", "Texas Capture or Use of Biometric Identifier Act (Bus. & Com. Code § 503.001 / HB 3186)"),
    ]:
        doc_dir = PUB_REG_DIR / rel_slug
        if not doc_dir.exists():
            continue
        md_text, used_url, tool_str = fetch_and_convert_regulation(rel_slug, REGULATION_URL_OVERRIDES[rel_slug][0], doc_title)
        if len(md_text) > 800:
            (doc_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")
            n_sec, n_id = run_parse_sections(doc_dir, stem)
            print(f"[RE-EXTRACTED] {rel_slug} -> {n_sec} sections ({n_id} IDs) from {used_url[:65]}")


def fetch_and_convert_regulation(rel_slug: str, orig_url: str, doc_title: str) -> tuple[str, str, str]:
    """Fetch a regulation from its candidate URLs and convert to structured Markdown."""
    # Check Japan e-Gov XML first
    if rel_slug in JAPAN_EGOV_LAW_IDS:
        law_id, jp_title = JAPAN_EGOV_LAW_IDS[rel_slug]
        try:
            md = egov_xml_to_md(law_id, jp_title)
            if len(md) > 800:
                return (
                    md,
                    f"https://laws.e-gov.go.jp/api/1/lawdata/{law_id}",
                    "e-gov-law-xml + tools-resources/utils/parse_regulatory_sections.py",
                )
        except Exception:
            pass

    candidates = expand_regulation_candidates(rel_slug, orig_url)
    for cand_url in candidates:
        data, final_url = fetch_url_bytes(cand_url, timeout=30)
        if not data:
            continue

        # 1. Australia legislation.gov.au /latest/downloads page -> extract /text/original/pdf link
        if "legislation.gov.au/" in final_url and b"/text/" in data:
            s_html = data.decode("utf-8", errors="ignore")
            au_pdfs = sorted(
                set(re.findall(r"https://www\.legislation\.gov\.au/[^\"'\s\\]+/text/(?:original|1)/pdf", s_html))
            )
            for pdf_u in au_pdfs:
                pdata, pfinal = fetch_url_bytes(pdf_u, timeout=35)
                if pdata and (pdata[:5] == b"%PDF-" or b"%PDF-1." in pdata[:1024]):
                    data, final_url = pdata, pfinal
                    break

        # 2. Germany gesetze-im-internet.de xml.zip
        if data[:4] == b"PK\x03\x04" and "gesetze-im-internet.de" in final_url:
            try:
                md = parse_german_xml_zip(data, doc_title)
                if len(md) > 800:
                    return (
                        md,
                        final_url,
                        "gesetze-im-internet-xml + tools-resources/utils/parse_regulatory_sections.py",
                    )
            except Exception:
                pass

        # 3. UK legislation.gov.uk CLML /data.xml
        if b"http://www.legislation.gov.uk/namespaces/legislation" in data[:2500]:
            try:
                md = parse_uk_clml_xml(data, doc_title)
                if len(md) > 800:
                    return (
                        md,
                        final_url,
                        "uk-clml-xml + tools-resources/utils/parse_regulatory_sections.py",
                    )
            except Exception:
                pass

        # 3b. Utah Legislature <leg> bill XML
        if b"<leg " in data[:1200] and "le.utah.gov" in final_url:
            try:
                md = parse_utah_bill_xml(data, doc_title)
                if len(md) > 600:
                    return (
                        md,
                        final_url,
                        "utah-leg-xml + tools-resources/utils/parse_regulatory_sections.py",
                    )
            except Exception:
                pass

        # 4. PDF document
        is_pdf = data[:5] == b"%PDF-" or b"%PDF-1." in data[:1024]
        if is_pdf:
            idx_p = data.find(b"%PDF-")
            if idx_p > 0:
                data = data[idx_p:]
            try:
                md, pages = pdf_bytes_to_markdown(data, doc_title)
                if len(md) < 600:
                    md, pages = fallback_pdf_text_to_markdown(data, doc_title)
                if len(md) >= 600:
                    md = promote_multilingual_statute_headings(md, doc_title)
                    md = ensure_hierarchical_headings(md, doc_title, "")
                    return (
                        md,
                        final_url,
                        "pymupdf + tools-resources/utils/parse_regulatory_sections.py",
                    )
            except Exception:
                pass
            continue

        # 5. HTML / XHTML document
        if b"Acesso Negado!" in data[:1000] or b"data-beasties-container" in data[:1000]:
            continue
        html_str = _decode_html_bytes(data)
        # Check for embedded PDF links on publication landing pages (e.g., gov.uk/government/publications/...)
        if any(
            sub in final_url
            for sub in ("/government/publications/", "meity.gov.in/", "coe.int/", "au.int/", "adgm.com/", "difc.com/")
        ):
            soup = BeautifulSoup(html_str, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if ".pdf" in href.lower():
                    pdf_u = urllib.parse.urljoin(final_url, href)
                    pdata, pfinal = fetch_url_bytes(pdf_u, timeout=30)
                    if pdata and (pdata[:5] == b"%PDF-" or b"%PDF-1." in pdata[:1024]):
                        idx_p = pdata.find(b"%PDF-")
                        if idx_p > 0:
                            pdata = pdata[idx_p:]
                        try:
                            md, _ = pdf_bytes_to_markdown(pdata, doc_title)
                            if len(md) >= 800:
                                md = promote_multilingual_statute_headings(md, doc_title)
                                md = ensure_hierarchical_headings(md, doc_title, "")
                                return (
                                    md,
                                    pfinal,
                                    "pymupdf + tools-resources/utils/parse_regulatory_sections.py",
                                )
                        except Exception:
                            pass

        try:
            md = html_to_clean_markdown(html_str, final_url, doc_title)
            if len(md) >= 1200 and "Search OpenLegislation Statutes" not in md and "We use cookies on this site" not in md[:400]:
                md = promote_multilingual_statute_headings(md, doc_title)
                md = ensure_hierarchical_headings(md, doc_title, "")
                return (
                    md,
                    final_url,
                    "requests + markdownify + tools-resources/utils/parse_regulatory_sections.py",
                )
        except Exception:
            pass

    return "", "", ""


def derive_verified_published_date(*texts: str) -> str:
    """Extract a verified 4-digit year (1970..2029) or YYYY-MM-DD date from name/url/title/description, or return empty string."""
    for t in texts:
        if not t:
            continue
        m_iso = re.search(r"\b(19[7-9]\d|20[0-2]\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b", t)
        if m_iso:
            return m_iso.group(0)
        m_yr = re.search(r"(?:^|[^0-9])(19[7-9]\d|20[0-2]\d)(?:[^0-9]|$)", t)
        if m_yr:
            return f"{m_yr.group(1)}-01-01"
    return ""


def collect_unextracted_regulations() -> list[dict]:
    """Collect all match_nodes in SecID/registry/regulation/ not yet extracted in dataset-public/regulation/."""
    existing_dirs = {
        str(p.parent.relative_to(PUB_REG_DIR))
        for p in PUB_REG_DIR.rglob("*.json")
        if p.name != "README.json"
    }
    items: list[dict] = []
    for p in sorted(SECID_REG_DIR.rglob("*.json")):
        tld = p.relative_to(SECID_REG_DIR).parts[0]
        reg_data = json.loads(p.read_text(encoding="utf-8"))
        ns = reg_data.get("namespace", "")
        issuer = (
            reg_data.get("official_name")
            or reg_data.get("full_name")
            or reg_data.get("common_name")
            or reg_data.get("short_name")
            or ns
        )
        for node in reg_data.get("match_nodes", []):
            pats = node.get("patterns") or []
            if not pats:
                continue
            name = re.sub(r"^(?:\(\?i\))?\^|\$$", "", pats[0])
            if not name or re.search(r"[\\\[\]\(\)\?\+\*\{\}]", name) or name.startswith("_"):
                continue
            rel_slug = f"{ns}/{name}"
            if rel_slug in existing_dirs:
                continue
            if rel_slug in EXISTING_SLUG_ALIASES and EXISTING_SLUG_ALIASES[rel_slug] in existing_dirs:
                continue
            nd = node.get("data") or {}
            title = nd.get("official_name") or nd.get("common_name") or node.get("description") or name
            desc = nd.get("description") or node.get("description") or title
            acronym = nd.get("common_name") if (nd.get("common_name") and len(nd.get("common_name", "")) <= 18) else ""
            urls = [u.get("url") for u in (nd.get("urls") or []) if isinstance(u, dict) and u.get("url")]
            url = nd.get("url") or (urls[0] if urls else "")
            subtype = nd.get("subtype") or ["statute"]
            if isinstance(subtype, str):
                subtype = [subtype]
            items.append({
                "tld": tld,
                "namespace": ns,
                "issuer": issuer,
                "name": name,
                "rel_slug": rel_slug,
                "rel_dir": f"regulation/{rel_slug}",
                "stem": name,
                "secid": f"secid:regulation/{rel_slug}",
                "full_name": title,
                "acronym": acronym,
                "subtype": subtype,
                "description": desc,
                "url": url,
                "published": derive_verified_published_date(name, url, title, desc),
            })
    return items


def extract_unextracted_regulations() -> None:
    """Extract all remaining unextracted regulations in SecID/registry/regulation/."""
    items = collect_unextracted_regulations()
    print(f"=== Step 2: Processing {len(items)} Unextracted Regulations ===")
    extracted_cnt = 0
    meta_only_cnt = 0

    for idx, item in enumerate(items, start=1):
        rel_slug = item["rel_slug"]
        doc_dir = REPO_ROOT / item["rel_dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)
        stem = item["stem"]
        md_text, used_url, tool_str = fetch_and_convert_regulation(rel_slug, item["url"], item["full_name"])
        lic_obj = license_for_tld(item["tld"], item["namespace"], md_text=md_text, secid=item["secid"])

        if md_text:
            (doc_dir / f"{stem}.md").write_text(md_text, encoding="utf-8")
            n_sec, n_id = run_parse_sections(doc_dir, stem)
            if n_sec >= 1:
                write_metadata(
                    doc_dir,
                    stem,
                    secid=item["secid"],
                    name=item["full_name"],
                    acronym=item["acronym"],
                    version="",
                    owner=item["issuer"],
                    doc_type="Regulation",
                    subtype=item["subtype"],
                    description=item["description"],
                    cloud_rel=(
                        f"Establishes statutory or regulatory compliance obligations issued by {item['issuer']} "
                        f"({item['namespace']}) applicable to cloud service providers, data controllers, and digital operators."
                    ),
                    ai_rel=(
                        f"Governs data protection, automated decision-making, cybersecurity, or AI system compliance "
                        f"within {item['issuer']} ({item['namespace']})."
                    ),
                    license_obj=lic_obj,
                    source_url=item["url"],
                    text_used_url=used_url,
                    published=item["published"],
                    active=True,
                    retired_date=None,
                    supersedes=None,
                    superseded_by=None,
                    tool_str=tool_str,
                    extraction_notes=f"Extracted official regulation ({used_url}) to Markdown ({len(md_text):,} chars). Parsed {n_sec} sections ({n_id} with explicit section identifiers).",
                    end_state="extracted",
                    end_reason="regulation-doc",
                )
                extracted_cnt += 1
                print(
                    f"[{idx:>3}/{len(items)}] [EXTRACTED] {rel_slug:<52} | {len(md_text):>8,} chars | {n_sec:>3} secs ({n_id} ID)"
                )
                sys.stdout.flush()
                continue

        # Fallback: record honest metadata-only state when primary full text is not directly downloadable
        (doc_dir / f"{stem}.md").unlink(missing_ok=True)
        (doc_dir / f"{stem}-sections.json").unlink(missing_ok=True)
        (doc_dir / f"{stem}-sections.csv").unlink(missing_ok=True)
        write_metadata(
            doc_dir,
            stem,
            secid=item["secid"],
            name=item["full_name"],
            acronym=item["acronym"],
            version="",
            owner=item["issuer"],
            doc_type="Regulation",
            subtype=item["subtype"],
            description=item["description"],
            cloud_rel=(
                f"Establishes statutory or regulatory compliance obligations issued by {item['issuer']} "
                f"({item['namespace']}) applicable to cloud service providers, data controllers, and digital operators."
            ),
            ai_rel=(
                f"Governs data protection, automated decision-making, cybersecurity, or AI system compliance "
                f"within {item['issuer']} ({item['namespace']})."
            ),
            license_obj=lic_obj,
            source_url=item["url"],
            text_used_url="",
            published=item["published"],
            active=True,
            retired_date=None,
            supersedes=None,
            superseded_by=None,
            tool_str="",
            extraction_notes=(
                f"Official primary full-text document for {item['secid']} ({item['url']}) is not directly "
                f"downloadable (upstream portal root URL only, SPA/WAF barrier, or pending publication); "
                f"recorded as metadata-only."
            ),
            end_state="metadata-only",
            end_reason="pending-acquisition",
        )
        meta_only_cnt += 1
        print(f"[{idx:>3}/{len(items)}] [META-ONLY] {rel_slug:<52} | url={item['url'][:55]}")
        sys.stdout.flush()

    print(f"\n=== Regulation Extraction Summary: extracted={extracted_cnt}, metadata-only={meta_only_cnt} ===")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--step", choices=["clean", "extract", "all"], default="all")
    args = ap.parse_args()
    if args.step in ("clean", "all"):
        clean_existing_regulations()
    if args.step in ("extract", "all"):
        extract_unextracted_regulations()


if __name__ == "__main__":
    main()
