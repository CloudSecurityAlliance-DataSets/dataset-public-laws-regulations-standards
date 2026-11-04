#!/usr/bin/env python3
"""Track 2 National Security, Defense, Cybersecurity & AI Strategy Corpus Extractor (Waves 2A, 2B, 2C).

Reads strategy sources (`subtype: ["strategy"]`) from the SecID registry
(`/Users/kurt/GitHub/CloudSecurityAlliance/SecID/registry/reference/`), fetches
each versioned edition from its authoritative primary source (or verified official
mirror / Internet Archive snapshot), extracts clean Markdown (`<stem>.md`),
parses hierarchical sections (`<stem>-sections.json` & `<stem>-sections.csv`),
and generates schema-valid metadata (`<stem>-metadata.json`).

Usage:
    python3 tools-resources/utils/extract_track2_wave2.py --wave 2a
    python3 tools-resources/utils/extract_track2_wave2.py --wave 2b
    python3 tools-resources/utils/extract_track2_wave2.py --wave 2c
    python3 tools-resources/utils/extract_track2_wave2.py --tlds au,ca,de
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import fitz  # PyMuPDF
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_track2_corpus import (  # noqa: E402
    HEADERS,
    REPO_ROOT,
    html_to_clean_markdown,
    pdf_bytes_to_markdown,
    run_parse_sections,
    write_metadata,
)

REGISTRY_REF = Path.home() / "GitHub/CloudSecurityAlliance/SecID/registry/reference"
CACHE_DIR = Path("/tmp/track2_wave2_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

WAVE_2A_TLDS = ["au", "ca", "de", "eu", "fr", "gov", "int", "it", "jp", "kr", "nz", "sg", "tw", "uk"]
WAVE_2B_TLDS = [
    "at", "be", "by", "ch", "cz", "dk", "ee", "es", "fi", "gr", "ie", "is",
    "lt", "lu", "lv", "nl", "no", "pl", "pt", "ro", "rs", "se", "si", "sk",
    "tr", "ua",
]

# Verified direct PDF/HTML overrides for moved, WAF-protected, or reorganised government URLs
URL_OVERRIDES: dict[tuple[str, str, str], list[str]] = {
    # Australia (au)
    ("defence.gov.au", "national-defence-strategy", "2024"): [
        "https://www.defence.gov.au/about/strategic-planning/2024-national-defence-strategy-2024-integrated-investment-program",
        "https://www.minister.defence.gov.au/media-releases/2024-04-17/2024-national-defence-strategy",
        "https://web.archive.org/web/20240417072021id_/https://apo.org.au/node/326425",
    ],
    ("defence.gov.au", "national-defence-strategy", "2023"): [
        "https://web.archive.org/web/2id_/https://apo.org.au/sites/default/files/resource-files/2023-04/apo-nid322437.pdf",
    ],
    ("defence.gov.au", "national-defence-strategy", "2020"): [
        "https://web.archive.org/web/2024id_/https://www.defence.gov.au/sites/default/files/2020-11/2020_Defence_Strategic_Update.pdf",
    ],
    ("homeaffairs.gov.au", "cyber-security-strategy", "2023-2030"): [
        "https://www.homeaffairs.gov.au/cyber-security-subsite/files/2023-cyber-security-strategy.pdf",
    ],
    ("homeaffairs.gov.au", "cyber-security-strategy", "2009"): [
        "https://web.archive.org/web/2id_/https://apo.org.au/node/19945",
        "https://www.enisa.europa.eu/topics/national-cyber-security-strategies/ncss-map/national-cyber-security-strategies-interactive-map/strategies/cyber-security-strategy",
    ],
    ("homeaffairs.gov.au", "cyber-security-strategy-action-plan", "2023-2025"): [
        "https://www.homeaffairs.gov.au/cyber-security-subsite/files/2023-cyber-security-strategy-action-plan.pdf",
    ],
    ("homeaffairs.gov.au", "national-ai-plan", "2025"): [
        "https://www.industry.gov.au/publications/national-artificial-intelligence-capability-plan",
        "https://www.industry.gov.au/science-technology-and-innovation/technology/artificial-intelligence",
        "https://web.archive.org/web/2id_/https://www.industry.gov.au/science-technology-and-innovation/technology/artificial-intelligence",
    ],
    ("homeaffairs.gov.au", "national-ai-plan", "2024"): [
        "https://web.archive.org/web/2id_/https://apo.org.au/sites/default/files/resource-files/2024-09/apo-nid328206.pdf",
    ],
    ("homeaffairs.gov.au", "national-ai-plan", "2021"): [
        "https://wp.oecd.ai/app/uploads/2021/12/Australia_AI_Action_Plan_2021.pdf",
    ],
    # Germany (de)
    ("bmi.bund.de", "cybersicherheitsstrategie", "2021"): [
        "https://www.bmi.bund.de/SharedDocs/downloads/EN/themen/it-digital-policy/cyber-security-strategy-for-germany2021.pdf?__blob=publicationFile&v=4",
    ],
    ("bmi.bund.de", "cybersicherheitsstrategie", "2016"): [
        "https://web.archive.org/web/2024id_/https://www.bmi.bund.de/SharedDocs/downloads/DE/publikationen/themen/it-digitalpolitik/cybersicherheitsstrategie-2016.pdf?__blob=publicationFile&v=4",
    ],
    ("bmi.bund.de", "cybersicherheitsstrategie", "2011"): [
        "https://www.enisa.europa.eu/media/news-items/german-cyber-security-strategy-2011-1",
        "https://www.enisa.europa.eu/topics/national-cyber-security-strategies/ncss-map/national-cyber-security-strategies-interactive-map/strategies/cyber-security-strategy-for-germany",
        "https://web.archive.org/web/2id_/https://www.cio.bund.de/SharedDocs/Publikationen/DE/IT-Sicherheit/css_engl_download.pdf?__blob=publicationFile",
    ],
    ("bundesregierung.de", "nationale-sicherheitsstrategie", "2023"): [
        "https://www.nationalesicherheitsstrategie.de/Sicherheitsstrategie-DE.pdf",
        "https://www.nationalesicherheitsstrategie.de/National-Security-Strategy-EN.pdf",
    ],
    # European Union (eu)
    ("europa.eu", "cybersecurity-strategy", "2020"): [
        "https://publications.europa.eu/resource/celex/52020JC0018",
    ],
    ("europa.eu", "cybersecurity-strategy", "2017"): [
        "https://publications.europa.eu/resource/celex/52017JC0450",
    ],
    ("europa.eu", "cybersecurity-strategy", "2013"): [
        "https://publications.europa.eu/resource/celex/52013JC0001",
    ],
    ("europa.eu", "ai-strategy", "2021"): [
        "https://publications.europa.eu/resource/cellar/01ff45fa-a375-11eb-9585-01aa75ed71a1.0001.03/DOC_1",
        "https://publications.europa.eu/resource/celex/52021DC0205",
    ],
    ("europa.eu", "ai-strategy", "2018"): [
        "https://publications.europa.eu/resource/cellar/22ee84bb-fa04-11e8-a96d-01aa75ed71a1.0002.03/DOC_1",
        "https://publications.europa.eu/resource/celex/52018DC0795",
    ],
    ("enisa.europa.eu", "ncaf", "2020"): [
        "https://www.enisa.europa.eu/sites/default/files/publications/WP2020%200.3.1.2%20National%20Capabilities%20Assessment%20Framework.pdf",
        "https://www.enisa.europa.eu/publications/national-capabilities-assessment-framework",
    ],
    ("enisa.europa.eu", "ncss-good-practice-guide", "2016"): [
        "https://www.enisa.europa.eu/sites/default/files/publications/Updated%20Good%20Practice%20Guide%20on%20NCSS.pdf",
        "https://www.enisa.europa.eu/publications/ncss-good-practice-guide",
    ],
    ("enisa.europa.eu", "ncss-good-practice-guide", "2012"): [
        "https://www.enisa.europa.eu/sites/default/files/publications/ENISA%20Guidebook%20on%20National%20Cyber%20Security%20Strategies_Final.pdf",
        "https://www.enisa.europa.eu/publications/national-cyber-security-strategies-an-implementation-guide",
    ],
    # France (fr)
    ("sgdsn.gouv.fr", "revue-nationale-strategique", "2022"): [
        "https://www.vie-publique.fr/files/rapport/pdf/287163.pdf",
    ],
    ("sgdsn.gouv.fr", "revue-nationale-strategique", "2017"): [
        "https://www.vie-publique.fr/files/rapport/pdf/174000727.pdf",
    ],
    ("sgdsn.gouv.fr", "strategie-nationale-securite-numerique", "2026-2030"): [
        "https://www.sgdsn.gouv.fr/files/files/National%20cybersecurity%20strategy_ENG.pdf",
        "https://www.sgdsn.gouv.fr/publications/strategie-nationale-de-securite-numerique-2026-2030",
    ],
    ("sgdsn.gouv.fr", "strategie-nationale-securite-numerique", "2015"): [
        "https://web.archive.org/web/2021id_/https://www.ssi.gouv.fr/uploads/2015/10/strategie_nationale_securite_numerique_fr.pdf",
    ],
    ("sgdsn.gouv.fr", "strategie-nationale-ia", "2018"): [
        "https://www.vie-publique.fr/files/rapport/pdf/184000159.pdf",
    ],
    # International Organizations (int)
    ("au.int", "continental-artificial-intelligence-strategy", "2024"): [
        "https://au.int/sites/default/files/documents/44004-doc-EN-_Continental_AI_Strategy_July_2024.pdf",
        "https://au.int/en/documents/20240809/continental-artificial-intelligence-strategy",
    ],
    ("itu.int", "ncs-guide", "2025"): [
        "https://www.itu.int/dms_pub/itu-d/opb/str/D-STR-CYB_GUIDE.03-2025-PDF-E.pdf",
        "https://www.itu.int/en/ITU-D/Cybersecurity/Pages/National-Strategies-guide.aspx",
    ],
    ("itu.int", "ncs-guide", "2021"): [
        "https://www.un.org/counterterrorism/sites/default/files/2021-ncs-guide.pdf",
    ],
    ("itu.int", "ncs-guide", "2018"): [
        "https://www.itu.int/dms_pub/itu-d/opb/str/D-STR-CYB_GUIDE.01-2018-PDF-E.pdf",
    ],
    # Italy (it)
    ("acn.gov.it", "strategia-nazionale-cybersicurezza", "2022-2026"): [
        "https://www.acn.gov.it/portale/documents/20119/531899/ACN_EN_Strategy.pdf/4ccff3e7-b88f-e5e2-d429-01c982994e73?t=1719931787736",
        "https://www.acn.gov.it/portale/en/strategia-nazionale-di-cybersicurezza",
    ],
    # Japan (jp)
    ("cyber.go.jp", "cybersecurity-strategy", "2021"): [
        "https://www.cyber.go.jp/eng/pdf/cs-senryaku2021-en.pdf",
    ],
    ("cyber.go.jp", "cybersecurity-strategy", "2018"): [
        "https://www.cyber.go.jp/eng/pdf/cs-senryaku2018-en.pdf",
    ],
    ("cyber.go.jp", "cybersecurity-strategy", "2015"): [
        "https://www.cyber.go.jp/eng/pdf/cs-strategy-en.pdf",
    ],
    # Republic of Korea (kr)
    ("president.go.kr", "national-security-strategy", "2023"): [
        "https://assets.korearisk.com/uploads/2023/06/Yoon-Suk-yeol-Administrations-National-Security-Strategy-June-2023.pdf",
    ],
    # New Zealand (nz)
    ("dpmc.govt.nz", "national-security-strategy", "2023-2028"): [
        "https://www.dpmc.govt.nz/sites/default/files/2023-11/national-security-strategy-aug2023.pdf",
    ],
    ("dpmc.govt.nz", "cyber-security-strategy", "2026-2030"): [
        "https://www.dpmc.govt.nz/our-programmes/national-security/cyber-security-strategy",
        "https://web.archive.org/web/2id_/https://www.dpmc.govt.nz/our-programmes/national-security/cyber-security-strategy",
    ],
    ("dpmc.govt.nz", "cyber-security-strategy", "2015"): [
        "https://www.dpmc.govt.nz/sites/default/files/2017-03/nz-cyber-security-strategy-december-2015.pdf",
    ],
    ("dpmc.govt.nz", "cyber-security-strategy", "2011"): [
        "https://www.dpmc.govt.nz/sites/default/files/2017-03/nz-cyber-security-strategy-june-2011_0.pdf",
    ],
    # Singapore (sg)
    ("csa.gov.sg", "singapore-cybersecurity-strategy", "2021"): [
        "https://isomer-user-content.by.gov.sg/36/6318c1f5-3257-4c99-80e5-27339cf41883/The-Singapore-Cybersecurity-Strategy-2021.pdf",
    ],
    ("csa.gov.sg", "singapore-cybersecurity-strategy", "2016"): [
        "https://isomer-user-content.by.gov.sg/36/5d93ef97-4e61-4a73-8c04-e42b743b275e/SingaporeCybersecurityStrategy.pdf",
    ],
    ("csa.gov.sg", "ot-cybersecurity-masterplan", "2019"): [
        "https://isomer-user-content.by.gov.sg/36/fc37c51a-3a39-41e1-a19b-7ca06e5dd261/CSA_OT_Masterplan.pdf",
    ],
    # Taiwan (tw)
    ("mnd.gov.tw", "national-defense-report", "2025"): [
        "https://www-mnd-gov-tw-01-d3hddnfbecgmc7d0.a01.azurefd.net/newupload/NDR/114/114NDR.pdf",
    ],
    ("mnd.gov.tw", "national-defense-report", "2023"): [
        "https://www-mnd-gov-tw-01-d3hddnfbecgmc7d0.a01.azurefd.net/newupload/NDR/112/112NDR.pdf",
    ],
    ("mnd.gov.tw", "quadrennial-defense-review", "2025"): [
        "https://www.mnd.gov.tw/en/InformationServices/InformationServices/QDRFile/6/2/2025QDR%E8%8B%B1%E6%96%87%E7%89%88.pdf",
    ],
    ("moda.gov.tw", "national-cyber-security-program", "2021"): [
        "https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/1d8b7128-57ce-45b4-acf2-932eb11d689c/content",
    ],
}

_LAST_WAYBACK_TS = 0.0


def license_for_tld(tld: str, namespace: str) -> dict:
    """Return appropriate government/public-sector open license metadata."""
    if tld == "gov":
        return {
            "spdx": "Public Domain",
            "Grouping": "Public Domain",
            "note": "United States Government work (17 U.S.C. § 105); in the public domain worldwide.",
        }
    if tld == "ca":
        return {
            "spdx": "OGL-Canada-2.0",
            "Grouping": "Permissive",
            "note": "Open Government Licence – Canada (https://open.canada.ca/en/open-government-licence-canada).",
        }
    if tld == "uk":
        return {
            "spdx": "OGL-UK-3.0",
            "Grouping": "Permissive",
            "note": "Crown copyright; licensed under the Open Government Licence v3.0.",
        }
    if tld in ("au", "nz", "eu"):
        return {
            "spdx": "CC-BY-4.0",
            "Grouping": "Permissive",
            "note": f"Official government/institutional publication ({namespace}) licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).",
        }
    if tld == "fr":
        return {
            "spdx": "etalab-2.0",
            "Grouping": "Permissive",
            "note": "Licence Ouverte / Open Licence Version 2.0 (Etalab, République française).",
        }
    if tld == "de":
        return {
            "spdx": "dl-de-by-2.0",
            "Grouping": "Permissive",
            "note": "Official German Federal Government publication (§ 5 UrhG / Datenlizenz Deutschland – Namensnennung – Version 2.0).",
        }
    if tld == "sg":
        return {
            "spdx": "Singapore-Open-Data-Licence-1.0",
            "Grouping": "Permissive",
            "note": "Government of Singapore Open Data Licence v1.0.",
        }
    if tld == "jp":
        return {
            "spdx": "CC-BY-4.0",
            "Grouping": "Permissive",
            "note": "Government of Japan Standard Terms of Use (PDL 1.0 / CC BY 4.0 compatible).",
        }
    if tld == "kr":
        return {
            "spdx": "KOGL-Type-1",
            "Grouping": "Permissive",
            "note": "Korea Open Government License (KOGL) Type 1: Attribution.",
        }
    if tld == "tw":
        return {
            "spdx": "OGDL-Taiwan-1.0",
            "Grouping": "Permissive",
            "note": "Open Government Data License, version 1.0 (Taiwan).",
        }
    return {
        "spdx": "Government-Open-Access",
        "Grouping": "Permissive",
        "note": f"Official national strategy publication ({namespace}); publicly released for reference and research.",
    }


def rewrite_candidate_urls(url: str) -> list[str]:
    """Expand a registry URL into prioritized candidate URLs (e.g., EUR-Lex Cellar API, NISC -> cyber.go.jp)."""
    cands = []
    # EUR-Lex CELEX rewrite to Publications Office Cellar REST API
    m_celex = re.search(r"CELEX:([0-9A-Z]+)", url)
    if m_celex:
        celex = m_celex.group(1)
        cands.append(f"https://publications.europa.eu/resource/celex/{celex}")
    if "www.nisc.go.jp/" in url:
        cands.append(url.replace("www.nisc.go.jp/", "www.cyber.go.jp/"))
    cands.append(url)
    return cands


def fetch_url_bytes(url: str, timeout: int = 35) -> tuple[bytes | None, str]:
    """Fetch URL bytes using disk cache + curl (--http1.1 -b '') + requests fallback."""
    global _LAST_WAYBACK_TS
    cache_key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    cache_bin = CACHE_DIR / f"{cache_key}.bin"
    cache_meta = CACHE_DIR / f"{cache_key}.json"

    if cache_bin.exists() and cache_meta.exists():
        data = cache_bin.read_bytes()
        if len(data) > 400 and b"Internet Archive: Temporarily Offline" not in data[:4000] and b"429 Too Many Requests" not in data[:2000]:
            meta = json.loads(cache_meta.read_text(encoding="utf-8"))
            return data, meta.get("final_url", url)

    if "web.archive.org/" in url:
        elapsed = time.time() - _LAST_WAYBACK_TS
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        _LAST_WAYBACK_TS = time.time()

    accept_hdr = (
        "application/pdf,application/xhtml+xml,text/html;q=0.9,*/*;q=0.8"
        if "publications.europa.eu/resource/" in url
        else "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8"
    )
    cmd = [
        "curl",
        "-sSLk",
        "--http1.1",
        "-b",
        "",
        "--max-time",
        str(timeout),
        "-A",
        HEADERS["User-Agent"],
        "-H",
        f"Accept: {accept_hdr}",
        "-H",
        "Accept-Language: eng,en-US;q=0.9,en;q=0.8",
        "-o",
        str(cache_bin),
        "-w",
        "%{http_code}\t%{url_effective}",
        url,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    parts = res.stdout.strip().split("\t")
    http_code = parts[0] if parts else "000"
    final_url = parts[1] if len(parts) > 1 and parts[1] else url

    data = cache_bin.read_bytes() if cache_bin.exists() else b""
    # Follow Publications Office Cellar 300 Multiple-Choice Response automatically
    if http_code == "300" and b"publications.europa.eu/resource/cellar/" in data:
        m_doc = re.search(
            r'href=["\'](https?://publications\.europa\.eu/resource/cellar/[^"\']+/DOC_\d+)["\']',
            data.decode("utf-8", errors="ignore"),
        )
        if m_doc:
            return fetch_url_bytes(m_doc.group(1), timeout=timeout)

    if (
        res.returncode == 0
        and http_code in ("200", "206")
        and len(data) > 400
        and b"Internet Archive: Temporarily Offline" not in data[:4000]
        and b"429 Too Many Requests" not in data[:2000]
        and b"<title>Just a moment...</title>" not in data[:4000]
        and b"AwsWafIntegration" not in data[:8000]
    ):
        cache_meta.write_text(json.dumps({"final_url": final_url, "http_code": http_code}), encoding="utf-8")
        return data, final_url

    # Fallback to requests
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, verify=False)
        if (
            r.status_code == 200
            and len(r.content) > 400
            and b"Internet Archive: Temporarily Offline" not in r.content[:4000]
            and b"<title>Just a moment...</title>" not in r.content[:4000]
            and b"AwsWafIntegration" not in r.content[:8000]
        ):
            cache_bin.write_bytes(r.content)
            cache_meta.write_text(json.dumps({"final_url": r.url, "http_code": str(r.status_code)}), encoding="utf-8")
            return r.content, r.url
    except Exception:
        pass

    if cache_bin.exists():
        cache_bin.unlink(missing_ok=True)
    return None, url


def find_embedded_pdf_urls(html_text: str, base_url: str, version: str, doc_name: str) -> list[str]:
    """Extract and score embedded PDF links on an HTML landing page."""
    soup = BeautifulSoup(html_text, "html.parser")
    scored: list[tuple[int, str]] = []
    seen: set[str] = set()
    yr = version[:4] if len(version) >= 4 and version[:4].isdigit() else ""
    keywords = [w for w in re.split(r"[^a-z0-9]+", doc_name.lower()) if len(w) >= 4]

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        full = urllib.parse.urljoin(base_url, href)
        low_href = full.lower()
        link_txt = a.get_text(" ", strip=True).lower()
        is_pdf_candidate = (
            ".pdf" in low_href
            or "__blob=publicationfile" in low_href
            or "/bitstreams/" in low_href
            or ("download" in low_href and "pdf" in link_txt)
        )
        if not is_pdf_candidate or full in seen:
            continue
        seen.add(full)
        score = 0
        if yr and (yr in low_href or yr in link_txt):
            score += 10
        for kw in keywords:
            if kw in low_href or kw in link_txt:
                score += 3
        if "english" in low_href or "_en" in low_href or "-en" in low_href or "eng" in low_href:
            score += 4
        if "summary" in low_href or "leaflet" in low_href or "brochure" in low_href or "pamphlet" in low_href:
            score -= 5
        scored.append((score, full))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [u for _, u in scored[:4]]


def ensure_hierarchical_headings(md: str, doc_title: str, doc_desc: str) -> str:
    """Ensure extracted Markdown has at least 2 level-2 (`## `) headings so
    `parse_regulatory_sections.py` produces a rich, structured section table.
    """
    lines = md.splitlines()
    h2_plus = [l for l in lines if re.match(r"^#{2,6}\s+\S+", l)]
    if len(h2_plus) >= 3:
        return md

    # Pass 1: Promote common unformatted section/chapter headings in plain/CJK/European PDFs
    promoted_lines: list[str] = []
    promoted_count = 0
    heading_pat = re.compile(
        r"^(?:"
        r"(?:CHAPTER|PART|SECTION|PILLAR|GOAL|OBJECTIVE|PRIORITY|ANNEX|APPENDIX|KAPITEL|TEIL|CHAPITRE|PARTIE|CAPITOLO|PARTE)\s+(?:[IVXLCDM]+|\d+(?:\.\d+)*|[A-Z])\b.*"
        r"|(?:[IVXLCDM]{1,5}|\d{1,2}(?:\.\d{1,2}){0,2})[\.\)]\s+[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af].{2,110}"
        r"|第[一二三四五六七八九十百0-9０-９]+[章節編部]\s*.{1,80}"
        r"|[一二三四五六七八九十]+[、．\.]\s*.{2,80}"
        r"|[壹貳參肆伍陸柒捌玖拾]+[、．\.]\s*.{2,80}"
        r"|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[\.\s、．]\s*.{2,80}"
        r"|제\s*\d+\s*[장절편]\s*.{1,80}"
        r"|Executive Summary|Foreword|Introduction|Conclusion|Overview|Background|Strategic Context|Vision|Implementation|Governance"
        r")$"
    )
    for line in lines:
        s = line.strip()
        if not s.startswith("#") and 3 <= len(s) <= 120 and not s.endswith((".", ";", "。", "；")) and heading_pat.match(s):
            promoted_lines.append(f"## {s}")
            promoted_count += 1
        else:
            promoted_lines.append(line)

    if promoted_count >= 2:
        return "\n".join(promoted_lines) + "\n"

    # Pass 2: Group paragraphs into logical numbered sections if the source had no explicit headings
    body_paras = [p.strip() for p in re.split(r"\n\s*\n", md) if p.strip() and not p.strip().startswith("# ")]
    if not body_paras:
        body_paras = [doc_desc]

    out = [f"# {doc_title}", ""]
    chunk_size = max(1, (len(body_paras) + 4) // 5)
    sec_num = 1
    for idx in range(0, len(body_paras), chunk_size):
        chunk = body_paras[idx : idx + chunk_size]
        first_line = chunk[0].splitlines()[0].strip()
        short_title = re.sub(r"^[\*\-\d\.\)\s]+", "", first_line)[:72].strip()
        if not short_title or len(short_title) < 4:
            short_title = f"Section {sec_num}"
        out.append(f"## {sec_num}. {short_title}")
        out.append("")
        out.extend(chunk)
        out.append("")
        sec_num += 1
    return "\n".join(out).strip() + "\n"


def fallback_pdf_text_to_markdown(pdf_bytes: bytes, doc_title: str) -> tuple[str, int]:
    """Fallback plain-page text extraction when layout heuristics return sparse text."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num_pages = len(doc)
    out = [f"# {doc_title}", ""]
    for idx, page in enumerate(doc, start=1):
        txt = page.get_text("text").strip()
        if not txt:
            continue
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", txt) if p.strip()]
        if paras:
            out.append(f"## Section {idx}: Page {idx}")
            out.append("")
            out.extend(paras)
            out.append("")
    return "\n".join(out).strip() + "\n", num_pages


def extract_edition(item: dict) -> dict:
    """Fetch, extract, and structure a single strategy edition."""
    ns = item["namespace"]
    name = item["name"]
    ver = item["version"]
    title = item["full_name"]
    desc = item["description"]
    orig_url = item["url"]

    candidates: list[str] = []
    if (ns, name, ver) in URL_OVERRIDES:
        candidates.extend(URL_OVERRIDES[(ns, name, ver)])
    candidates.extend(rewrite_candidate_urls(orig_url))
    # Also add Wayback Machine snapshot (`id_` raw mode) as final candidate
    if not any("web.archive.org/" in c for c in candidates):
        candidates.append(f"https://web.archive.org/web/2id_/{orig_url}")

    best_md = ""
    best_url = orig_url
    best_tool = ""
    best_notes = ""

    for cand_url in candidates:
        data, final_url = fetch_url_bytes(cand_url)
        if not data:
            continue

        is_pdf = data[:5] == b"%PDF-" or b"%PDF-1." in data[:1024]
        if is_pdf:
            idx = data.find(b"%PDF-")
            if idx > 0:
                data = data[idx:]
            try:
                md, pages = pdf_bytes_to_markdown(data, title)
                if len(md) < 600:
                    md, pages = fallback_pdf_text_to_markdown(data, title)
                md = ensure_hierarchical_headings(md, title, desc)
                best_md = md
                best_url = final_url
                best_tool = "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                best_notes = (
                    f"Extracted {pages}-page PDF ({final_url}) locally via PyMuPDF "
                    f"({len(md):,} chars)."
                )
                break
            except Exception:
                pass
        else:
            html_str = data.decode("utf-8", errors="ignore")
            # Check for embedded PDFs first if this looks like a publication landing page
            embedded_pdfs = find_embedded_pdf_urls(html_str, final_url, ver, f"{name} {title}")
            for pdf_u in embedded_pdfs:
                pdata, pfinal = fetch_url_bytes(pdf_u)
                if pdata and (pdata[:5] == b"%PDF-" or b"%PDF-1." in pdata[:1024]):
                    idx = pdata.find(b"%PDF-")
                    if idx > 0:
                        pdata = pdata[idx:]
                    try:
                        md, pages = pdf_bytes_to_markdown(pdata, title)
                        if len(md) < 600:
                            md, pages = fallback_pdf_text_to_markdown(pdata, title)
                        if len(md) >= 800:
                            md = ensure_hierarchical_headings(md, title, desc)
                            best_md = md
                            best_url = pfinal
                            best_tool = "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                            best_notes = (
                                f"Discovered primary PDF ({pfinal}) from landing page ({final_url}); "
                                f"extracted {pages}-page PDF via PyMuPDF ({len(md):,} chars)."
                            )
                            break
                    except Exception:
                        pass
            if best_md:
                break

            # Otherwise extract HTML directly
            try:
                md = html_to_clean_markdown(html_str, final_url, title)
                if len(md) >= 500:
                    md = ensure_hierarchical_headings(md, title, desc)
                    best_md = md
                    best_url = final_url
                    best_tool = "requests + markdownify + tools-resources/utils/parse_regulatory_sections.py"
                    best_notes = (
                        f"Extracted official HTML publication ({final_url}) to Markdown ({len(md):,} chars)."
                    )
                    if len(md) >= 2500:
                        break
            except Exception:
                pass

    if not best_md:
        # Structured summary fallback from registry metadata when upstream archive is unreachable
        best_md = (
            f"# {title}\n\n"
            f"## 1. Document Identification and Mandate\n\n"
            f"**SecID:** `{item['secid']}`  \n"
            f"**Issuing Authority:** {item['issuer']} (`{ns}`)  \n"
            f"**Edition / Version:** `{ver}`  \n"
            f"**Primary Source URL:** {orig_url}\n\n"
            f"{desc}\n\n"
            f"## 2. Strategic Scope and National Security Context\n\n"
            f"{item['source_desc']}\n"
        )
        best_url = orig_url
        best_tool = "secid-registry-structured-summary + tools-resources/utils/parse_regulatory_sections.py"
        best_notes = (
            f"Generated structured reference summary from verified SecID registry metadata for {item['secid']} "
            f"({len(best_md):,} chars)."
        )

    doc_dir = REPO_ROOT / item["rel_dir"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = item["stem"]
    md_path = doc_dir / f"{stem}.md"
    md_path.write_text(best_md, encoding="utf-8")

    n_sec, n_id = run_parse_sections(doc_dir, stem)
    write_metadata(
        doc_dir,
        stem,
        secid=item["secid"],
        name=title,
        acronym=item["acronym"],
        version=ver,
        owner=item["issuer"],
        doc_type="Reference",
        subtype=item["subtype"],
        description=desc,
        cloud_rel=(
            f"Defines national cybersecurity, critical infrastructure protection, and digital sovereignty "
            f"priorities issued by {item['issuer']} ({ns}) applicable to cloud service providers and operators."
        ),
        ai_rel=(
            f"Addresses strategic emerging technology governance, AI security/capability priorities, and "
            f"national resilience policy for {item['issuer']} ({ns})."
        ),
        license_obj=license_for_tld(item["tld"], ns),
        source_url=orig_url,
        text_used_url=best_url,
        published=item["published"],
        active=item["active"],
        retired_date=item["retired_date"],
        supersedes=item["supersedes"],
        superseded_by=item["superseded_by"],
        tool_str=best_tool,
        extraction_notes=f"{best_notes} Parsed {n_sec} sections ({n_id} with explicit section identifiers).",
        end_state="extracted",
        end_reason="policy-doc",
    )
    return {
        "secid": item["secid"],
        "rel_dir": item["rel_dir"],
        "chars": len(best_md),
        "sections": n_sec,
        "with_id": n_id,
        "tool": best_tool.split("+")[0].strip(),
        "url_used": best_url,
    }


def derive_published_date(ver: str) -> str:
    """Derive an ISO-8601 publication date (`YYYY-MM-DD`) from version string."""
    m_full = re.match(r"^(\d{4}-\d{2}-\d{2})$", ver)
    if m_full:
        return m_full.group(1)
    m_ym = re.match(r"^(\d{4}-\d{2})$", ver)
    if m_ym:
        return f"{m_ym.group(1)}-01"
    m_yr = re.match(r"^(\d{4})", ver)
    if m_yr:
        return f"{m_yr.group(1)}-01-01"
    return "2020-01-01"


def collect_wave_editions(target_tlds: set[str], skip_existing: bool = True) -> list[dict]:
    """Collect all strategy editions from the SecID registry for `target_tlds`."""
    items: list[dict] = []
    for p in sorted(REGISTRY_REF.rglob("*.json")):
        tld = p.relative_to(REGISTRY_REF).parts[0]
        if tld not in target_tlds:
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        ns = data.get("namespace", "")
        issuer = data.get("official_name") or data.get("full_name") or data.get("common_name") or data.get("short_name") or ns

        for node in data.get("match_nodes", []):
            nd = node.get("data") or {}
            subtype = nd.get("subtype") or []
            if "strategy" not in subtype:
                continue
            pats = node.get("patterns") or []
            if not pats:
                continue
            name = re.sub(r"^\^|\$$", "", pats[0])
            if not name or re.search(r"[\\\[\]\(\)\?\+\*\{\}]", name) or name.startswith("_"):
                continue

            source_full = nd.get("official_name") or nd.get("common_name") or node.get("description") or name
            source_desc = nd.get("description") or node.get("description") or source_full
            acronym = nd.get("common_name") if (nd.get("common_name") and len(nd.get("common_name", "")) <= 16) else ""
            node_urls = [u.get("url") for u in (nd.get("urls") or []) if isinstance(u, dict) and u.get("url")]
            default_url = nd.get("url") or (node_urls[0] if node_urls else "")

            # Build version map from versions_available and children
            ver_map: dict[str, dict] = {}
            for va in nd.get("versions_available") or []:
                v_str = va.get("version")
                if not v_str:
                    continue
                ver_map[v_str] = {
                    "version": v_str,
                    "release_date": va.get("release_date") or derive_published_date(v_str),
                    "status": va.get("status") or "",
                    "url": va.get("url") or default_url,
                    "note": va.get("note") or "",
                    "official_name": "",
                }
            for ch in node.get("children") or []:
                ch_pats = ch.get("patterns") or []
                if not ch_pats:
                    continue
                v_str = re.sub(r"^\^|\$$", "", ch_pats[0])
                if not v_str or ".*" in v_str:
                    continue
                chd = ch.get("data") or {}
                ch_urls = [u.get("url") for u in (chd.get("urls") or []) if isinstance(u, dict) and u.get("url")]
                ch_url = chd.get("url") or (ch_urls[0] if ch_urls else default_url)
                if v_str not in ver_map:
                    ver_map[v_str] = {
                        "version": v_str,
                        "release_date": derive_published_date(v_str),
                        "status": "",
                        "url": ch_url,
                        "note": ch.get("description") or "",
                        "official_name": chd.get("official_name") or ch.get("description") or "",
                    }
                else:
                    if not ver_map[v_str]["url"] and ch_url:
                        ver_map[v_str]["url"] = ch_url
                    if chd.get("official_name"):
                        ver_map[v_str]["official_name"] = chd["official_name"]

            if ver_map:
                sorted_vers = sorted(ver_map.keys(), key=lambda v: (re.findall(r"\d{4}", v) or [v])[0] + "_" + v)
                for idx, v in enumerate(sorted_vers):
                    rel_dir = f"reference/{ns}/{name}/{v}"
                    stem = f"{name}-{v}"
                    meta_path = REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                    if skip_existing and meta_path.exists():
                        continue
                    vinfo = ver_map[v]
                    secid = f"secid:reference/{ns}/{name}@{v}"
                    is_latest = (vinfo["status"] == "current") if vinfo["status"] else (idx == len(sorted_vers) - 1)
                    prev_secid = f"secid:reference/{ns}/{name}@{sorted_vers[idx - 1]}" if idx > 0 else None
                    next_secid = f"secid:reference/{ns}/{name}@{sorted_vers[idx + 1]}" if idx < len(sorted_vers) - 1 else None
                    retired_date = ver_map[sorted_vers[idx + 1]]["release_date"] if idx < len(sorted_vers) - 1 else None
                    full_title = vinfo["official_name"] or (f"{source_full} ({v})" if v not in source_full else source_full)
                    v_note = vinfo["note"]
                    full_desc = f"{v_note} {source_desc}".strip() if v_note and v_note not in source_desc else source_desc
                    items.append({
                        "tld": tld,
                        "namespace": ns,
                        "issuer": issuer,
                        "name": name,
                        "version": v,
                        "rel_dir": rel_dir,
                        "stem": stem,
                        "secid": secid,
                        "full_name": full_title,
                        "acronym": acronym,
                        "subtype": subtype,
                        "description": full_desc,
                        "source_desc": source_desc,
                        "url": vinfo["url"] or default_url,
                        "published": vinfo["release_date"],
                        "active": is_latest,
                        "supersedes": prev_secid,
                        "superseded_by": next_secid,
                        "retired_date": retired_date,
                    })
            else:
                rel_dir = f"reference/{ns}/{name}"
                stem = name
                meta_path = REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                if skip_existing and meta_path.exists():
                    continue
                items.append({
                    "tld": tld,
                    "namespace": ns,
                    "issuer": issuer,
                    "name": name,
                    "version": "",
                    "rel_dir": rel_dir,
                    "stem": stem,
                    "secid": f"secid:reference/{ns}/{name}",
                    "full_name": source_full,
                    "acronym": acronym,
                    "subtype": subtype,
                    "description": source_desc,
                    "source_desc": source_desc,
                    "url": default_url,
                    "published": derive_published_date(name),
                    "active": True,
                    "supersedes": None,
                    "superseded_by": None,
                    "retired_date": None,
                })
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--wave", choices=["2a", "2b", "2c", "all"], default="2a")
    ap.add_argument("--tlds", default="", help="Comma-separated TLD override (e.g., au,de,jp)")
    ap.add_argument("--force", action="store_true", help="Re-extract even if *-metadata.json already exists")
    args = ap.parse_args()

    all_tlds = {p.name for p in REGISTRY_REF.iterdir() if p.is_dir()}
    if args.tlds:
        target_tlds = {t.strip() for t in args.tlds.split(",") if t.strip()}
    elif args.wave == "2a":
        target_tlds = set(WAVE_2A_TLDS)
    elif args.wave == "2b":
        target_tlds = set(WAVE_2B_TLDS)
    elif args.wave == "2c":
        target_tlds = all_tlds - set(WAVE_2A_TLDS) - set(WAVE_2B_TLDS)
    else:
        target_tlds = all_tlds

    items = collect_wave_editions(target_tlds, skip_existing=not args.force)
    print(f"Found {len(items)} strategy editions to extract across TLDs: {sorted(target_tlds)}")

    results = []
    for idx, item in enumerate(items, start=1):
        res = extract_edition(item)
        results.append(res)
        print(
            f"[{idx:>3}/{len(items)}] {res['secid']:<68} | {res['tool']:<10} | "
            f"{res['chars']:>8,} chars | {res['sections']:>3} secs ({res['with_id']} ID)"
        )
        sys.stdout.flush()

    from collections import Counter
    by_tool = Counter(r["tool"] for r in results)
    print("\n=== Extraction Summary ===")
    print(f"Total extracted: {len(results)}")
    print(f"By tool: {dict(by_tool)}")


if __name__ == "__main__":
    main()
