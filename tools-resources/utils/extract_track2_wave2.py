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
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import pymupdf as fitz  # PyMuPDF
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_track2_corpus import (  # noqa: E402
    GOV_UK_DOCS,
    HEADERS,
    PUBLIC_SAFETY_DOCS,
    REPO_ROOT,
    WHITEHOUSE_DOCS,
    html_to_clean_markdown,
    pdf_bytes_to_markdown,
    run_parse_sections,
    write_metadata,
)

PRIVATE_REPO_ROOT = REPO_ROOT.parent / "dataset-private-laws-regulations-standards"

_WAVE1_REL_DIRS = (
    {s["rel_dir"] for s in PUBLIC_SAFETY_DOCS + WHITEHOUSE_DOCS + GOV_UK_DOCS}
    | {
        "reference/canada.ca/national-security-policy/2004",
        "reference/canada.ca/national-security-policy-progress-report/2005",
        "reference/canada.ca/our-north-strong-and-free/2024",
        "reference/canada.ca/national-security-transparency-commitment",
        "reference/canada.ca/enterprise-cyber-security-strategy/2024",
    }
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
        "https://web.archive.org/web/2023id_/https://apo.org.au/sites/default/files/resource-files/2009-12/apo-nid19945.pdf",
    ],
    ("homeaffairs.gov.au", "cyber-security-strategy-action-plan", "2023-2025"): [
        "https://www.homeaffairs.gov.au/cyber-security-subsite/files/2023-cyber-security-strategy-action-plan.pdf",
    ],
    ("homeaffairs.gov.au", "national-ai-plan", "2025"): [
        "https://www.industry.gov.au/sites/default/files/2025-12/national-ai-plan.pdf",
        "https://www.industry.gov.au/publications/national-ai-plan",
        "https://web.archive.org/web/2id_/https://www.industry.gov.au/sites/default/files/2025-12/national-ai-plan.pdf",
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
    ("europa.eu", "ai-strategy", "2025"): [
        "https://publications.europa.eu/resource/cellar/8707360e-15f6-11f0-b1a3-01aa75ed71a1.0001.02/DOC_1",
        "https://publications.europa.eu/resource/celex/52025DC0165",
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
        "https://web.archive.org/web/2id_/https://www.diplomatie.gouv.fr/IMG/pdf/2017-revue_strategique_dsn_cle4b3beb.pdf",
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
    ("president.go.kr", "national-ai-strategy", "2019"): [
        "https://wp.oecd.ai/app/uploads/2021/12/Korea_National_Strategy_for_Artificial_Intelligence_2019.pdf",
    ],
    # New Zealand (nz)
    ("dpmc.govt.nz", "national-security-strategy", "2023-2028"): [
        "https://www.dpmc.govt.nz/sites/default/files/2023-11/national-security-strategy-aug2023.pdf",
    ],
    ("dpmc.govt.nz", "cyber-security-strategy", "2026-2030"): [
        "https://www.dpmc.govt.nz/sites/default/files/2026-02/nz-cyber-security-strategy-2026-30.pdf",
        "https://web.archive.org/web/2id_/https://www.dpmc.govt.nz/sites/default/files/2026-02/nz-cyber-security-strategy-2026-30.pdf",
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
        "https://www.mnd.gov.tw/en/InformationServices/QDRFile/6/2/2025QDR%E8%8B%B1%E6%96%87%E7%89%88.pdf",
    ],
    ("mnd.gov.tw", "quadrennial-defense-review", "2021"): [
        "https://www.mnd.gov.tw/en/InformationServices/QDRFile/5/2/110%20QDR(%E8%8B%B1%E6%96%87%E6%AD%A3%E5%BC%8F%E7%89%88).pdf",
    ],
    ("moda.gov.tw", "national-cyber-security-program", "2021"): [
        "https://openresearch-repository.anu.edu.au/server/api/core/bitstreams/1d8b7128-57ce-45b4-acf2-932eb11d689c/content",
    ],
    # United Kingdom (uk)
    ("gov.uk", "national-ai-strategy", "2021"): [
        "https://assets.publishing.service.gov.uk/media/614db4d1e90e077a2cbdf3c4/National_AI_Strategy_-_PDF_version.pdf",
    ],
    # Wave 2B: Wider Europe
    ("pravo.by", "national-security-concept-of-belarus", "2024"): [
        "https://pravo.by/upload/docs/op/P924v0005_1714078800.pdf",
    ],
    ("nukib.gov.cz", "security-strategy-czech-republic", "2023"): [
        "https://mzv.gov.cz/file/5161068/Security_Strategy_of_the_Czech_Republic_2023.pdf",
    ],
    ("nukib.gov.cz", "national-cyber-security-strategy", "2021"): [
        "https://nukib.gov.cz/download/publications_en/strategy_action_plan/NSCS_2021_2025_ENG.pdf",
    ],
    ("nukib.gov.cz", "national-cyber-security-strategy", "2025"): [
        "https://nukib.gov.cz/download/publications_en/strategy_action_plan/National-Cyber-Security-Strategy-Czechia-2026.pdf",
    ],
    ("valitsus.ee", "national-security-concept", "2026"): [
        "https://riigikantselei.ee/sites/default/files/documents/2026-06/2026_06_10%20Estonian_National_Security_Concept_EN.pdf",
    ],
    ("kam.lrv.lt", "lithuanian-artificial-intelligence-strategy", "2019"): [
        "https://wp.oecd.ai/app/uploads/2021/12/Lithuania_Artificial_Intelligence_Strategy_2019.pdf",
    ],
    ("hcpn.gouvernement.lu", "national-cybersecurity-strategy", "2021"): [
        "https://hcpn.gouvernement.lu/dam-assets/fr/publications/brochure-livre/strategie-nationale-cybersecurite-4/National-Cybersecurity-Strategy-IV.pdf",
    ],
    ("ncsc.nl", "nederlandse-cybersecuritystrategie", "2022-2028"): [
        "https://www.nctv.nl/site/binaries/site-content/collections/documents/2022/10/10/nederlandse-cybersecuritystrategie-2022-2028/Nederlandse+Cybersecuritystrategie+2022-2028.pdf",
    ],
    ("rijksoverheid.nl", "nederlandse-cybersecuritystrategie", "2022-2028"): [
        "https://www.nctv.nl/site/binaries/site-content/collections/documents/2022/10/10/nederlandse-cybersecuritystrategie-2022-2028/Nederlandse+Cybersecuritystrategie+2022-2028.pdf",
    ],
    ("regjeringen.no", "national-strategy-for-artificial-intelligence", "2020"): [
        "https://wp.oecd.ai/app/uploads/2021/12/Norway_National_Strategy_for_Artificial_Intelligence_2020.pdf",
    ],
    ("gov.pl", "cybersecurity-strategy-of-poland", "2019"): [
        "https://www.gov.pl/attachment/6a4aafc6-e339-4cd5-a8e6-cd47257f02d8",
    ],
    ("regeringen.se", "nationell-strategi-cybersakerhet", "2017"): [
        "https://www.regeringen.se/contentassets/3f89e3c77ad74163909c092b1beae15e/nationell-strategi-for-samhallets-informations--och-cybersakerhet-skr.-201617213",
    ],
    ("gov.si", "cyber-security-strategy-of-slovenia", "2016"): [
        "https://www.gov.si/assets/ministrstva/MNZJU/MDP/DDD/DID/Cyber_Security_Strategy_Slovenia.pdf",
    ],
    ("uab.gov.tr", "national-artificial-intelligence-strategy", "2021"): [
        "https://wp.oecd.ai/app/uploads/2021/12/Turkey_National_Artificial_Intelligence_Strategy_2021-2025.pdf",
    ],
    ("dsn.gob.es", "estrategia-nacional-ciberseguridad", "2019"): [
        "https://www.dsn.gob.es/sites/default/files/2025-04/Estrategia%20Nacional%20de%20Ciberseguridad%202019%20-%20%20Interactivo_0%20%281%29_0.pdf",
    ],
    # Wave 2C: Rest of World
    ("cac.gov.cn", "national-cyberspace-security-strategy", "2016"): [
        "https://www.cac.gov.cn/2016-12/27/c_1120195926.htm",
    ],
    ("cac.gov.cn", "14th-five-year-plan-national-informatization", "2021-2025"): [
        "https://www.cac.gov.cn/rootimages/uploadimg/1642205314564505/1642205314564505.pdf",
    ],
}

# Editions whose registry URL is a generic portal root that serves an unrelated PDF, a different year's
# edition, or an unextractable image-only scan without body text; force honest metadata-only records.
_FORCE_METADATA_ONLY_SECIDS: set[str] = {
    "secid:reference/gob.cl/politica-nacional-ia@2024",
    "secid:reference/micitt.go.cr/estrategia-nacional-ciberseguridad@2017-2021",
    "secid:reference/cncs.gob.do/estrategia-nacional-ciberseguridad@2018-2021",
    "secid:reference/csa.gov.gh/ghana-national-artificial-intelligence-strategy@2023",
    "secid:reference/bssn.go.id/buku-putih-pertahanan-indonesia@2015",
    "secid:reference/ict.go.ke/kenya-national-artificial-intelligence-strategy@2025",
    "secid:reference/cert.gov.lk/national-information-and-cyber-security-strategy@2019",
    "secid:reference/cert.gov.lk/national-information-and-cyber-security-strategy@2025",
    "secid:reference/dgssi.gov.ma/maroc-digital-2030@2024",
    "secid:reference/nitda.gov.ng/nigeria-national-artificial-intelligence-strategy@2024",
    "secid:reference/treasury.govmu.org/mauritius-national-cyber-security-strategy@2014",
    "secid:reference/treasury.govmu.org/mauritius-national-cyber-security-strategy@2023",
    "secid:reference/treasury.govmu.org/mauritius-artificial-intelligence-strategy@2018",
    "secid:reference/mitic.gov.py/estrategia-nacional-ciberseguridad@2025-2028",
    "secid:reference/pravo.gov.ru/national-strategy-for-the-development-of-ai-until-2030@2019",
    "secid:reference/sdaia.gov.sa/nsdai@2020",
    "secid:reference/ncsa.or.th/national-security-policy-and-plan@2023",
}

_LAST_WAYBACK_TS = 0.0

_TRUSTED_PDF_HOSTS = (
    "azurefd.net",
    "by.gov.sg",
    "publishing.service.gov.uk",
    "europa.eu",
    "vie-publique.fr",
    "apo.org.au",
    "oecd.ai",
    "un.org",
    "itu.int",
    "anu.edu.au",
    "korearisk.com",
)


def _make_license(
    spdx: str,
    grouping: str,
    note: str,
    url: str | None = None,
    redistribution: str = "yes",
    derivatives: str = "yes",
    publicly_redistributable: bool = True,
) -> dict:
    return {
        "spdx": spdx,
        "Grouping": grouping,
        "redistribution": redistribution,
        "derivatives": derivatives,
        "publicly_redistributable": publicly_redistributable,
        "license_text_url": url,
        "note": note,
        "notes": note,
    }


_TLD_STATUTORY_LICENSES: dict[str, tuple[str, str, str, str]] = {
    "at": (
        "LicenseRef-AT-UrhG-Sec7",
        "Government-Work",
        "Austrian Copyright Act (UrhG) § 7 (Freie Werke — official works produced primarily for official use) and Open Data Österreich (CC BY 4.0).",
        "https://www.ris.bka.gv.at/NormDokument.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10001848&Paragraf=7",
    ),
    "be": (
        "LicenseRef-BE-CDE-ArtXI172",
        "Government-Work",
        "Belgian Code of Economic Law (Code de droit économique) Art. XI.172 (official acts of authority excluded from copyright) and federal open data reuse framework.",
        "https://data.gov.be/en/legal-framework",
    ),
    "by": (
        "LicenseRef-BY-Law262Z-Art7-1",
        "Public Domain",
        "Law of the Republic of Belarus No. 262-Z of May 17, 2011 on Copyright and Related Rights Art. 7(1) (official documents—laws, court decisions, and other texts of a legislative, administrative, and judicial character—are not objects of copyright).",
        "https://www.wipo.int/wipolex/ru/legislation/details/22302",
    ),
    "ch": (
        "LicenseRef-CH-URG-Art5",
        "Public Domain",
        "Swiss Federal Act on Copyright and Related Rights (URG / LDA, SR 231.1) Art. 5 (laws, decrees, administrative decisions, and official reports excluded from copyright protection).",
        "https://www.fedlex.admin.ch/eli/cc/1993/1798_1798_1798/en",
    ),
    "cz": (
        "LicenseRef-CZ-Copyright-Sec3a",
        "Public Domain",
        "Czech Copyright Act (Act No. 121/2000 Sb.) Section 3(a) (official works, including government policies, strategies, and public registers, excluded from copyright protection).",
        "https://www.zakonyprolidi.cz/cs/2000-121#p3",
    ),
    "dk": (
        "LicenseRef-DK-Ophavsretsloven-Sec9",
        "Public Domain",
        "Danish Consolidated Act on Copyright (Ophavsretsloven) § 9 (acts, administrative orders, proposals, and official public reports/documents excluded from copyright).",
        "https://www.retsinformation.dk/eli/lta/2014/1144",
    ),
    "ee": (
        "LicenseRef-EE-Autorioiguse-Sec5",
        "Public Domain",
        "Estonian Copyright Act (Autoriõiguse seadus) § 5 (legislation, administrative documents, and official state policies/concepts not subject to copyright).",
        "https://www.riigiteataja.ee/en/eli/504042021003/consolide",
    ),
    "es": (
        "LicenseRef-ES-TRLPI-Art13",
        "Government-Work",
        "Spanish Consolidated Intellectual Property Law (Real Decreto Legislativo 1/1996, TRLPI) Art. 13 (official legal/regulatory dispositions, royal decrees, ministerial orders in BOE, and official state acts) and Ley 37/2007 on Reuse of Public Sector Information.",
        "https://www.boe.es/buscar/act.php?id=BOE-A-1996-8930#a13",
    ),
    "fi": (
        "LicenseRef-FI-Tekijanoikeuslaki-Sec9",
        "Public Domain",
        "Finnish Copyright Act (Tekijänoikeuslaki 404/1961) § 9 (laws, decrees, and decisions/statements of public authorities carry no copyright) and Finnish Open Government Data Licence (CC BY 4.0).",
        "https://www.finlex.fi/fi/laki/ajantasa/1961/19610404#P9",
    ),
    "gr": (
        "LicenseRef-GR-Law2121-Art2",
        "Government-Work",
        "Greek Copyright Law 2121/1993 Art. 2(5) (official texts expressive of authority excluded from copyright) and Law 4727/2020 (Digital Governance and Open Data / PSI reuse).",
        "https://www.wipo.int/wipolex/en/legislation/details/8757",
    ),
    "ie": (
        "CC-BY-4.0",
        "Permissive",
        "Government of Ireland Public Sector Information (PSI) Open Data Licence (CC BY 4.0) / European Union (Open Data and Re-use of Public Sector Information) Regulations 2021 (S.I. No. 376/2021).",
        "https://data.gov.ie/pages/opendatalicence",
    ),
    "is": (
        "LicenseRef-IS-Hofundalog-Art9",
        "Public Domain",
        "Icelandic Copyright Act (Höfundalög nr. 73/1972) Art. 9 (acts, regulations, administrative directives, and official public reports excluded from copyright).",
        "https://www.althingi.is/lagas/nuna/1972073.html",
    ),
    "lt": (
        "LicenseRef-LT-Copyright-Art5",
        "Public Domain",
        "Republic of Lithuania Law on Copyright and Related Rights (No. VIII-1185) Art. 5 (official state and municipal legal acts and administrative documents not objects of copyright).",
        "https://e-seimas.lrs.lt/portal/legalAct/lt/TAD/TAIS.81676/asr",
    ),
    "lu": (
        "LicenseRef-LU-SIP-Prior-Agreement",
        "Proprietary / All Rights Reserved",
        "Grand Duchy of Luxembourg Government / HCPN General Legal Notice (permits viewing, downloading, and printing; prior agreement from the Government Information and Press Service (SIP) is required for public redistribution or derivative works — stored in private internal repository, not publicly redistributed).",
        "https://hcpn.gouvernement.lu/en/support/aspects-legaux.html",
    ),
    "lv": (
        "LicenseRef-LV-Autortiesibu-Sec6",
        "Public Domain",
        "Latvian Copyright Law (Autortiesību likums) Section 6(1) (regulatory enactments, administrative acts, and official state conceptual documents not protected by copyright).",
        "https://likumi.lv/ta/en/en/id/5138",
    ),
    "nl": (
        "CC0-1.0",
        "Public Domain",
        "Dutch Copyright Act (Auteurswet) Art. 11 & Art. 15b (no copyright in laws, decrees, or public works made generally available by public authorities without an explicit reservation of copyright; Rijksoverheid CC0 1.0).",
        "https://wetten.overheid.nl/BWBR0001886/",
    ),
    "no": (
        "NLOD-2.0",
        "Permissive",
        "Norwegian Copyright Act (Åndsverkloven, LOV-2018-06-15-40) § 14 (statutes, regulations, and official reports/documents issued by public authorities excluded from copyright) and Norwegian Licence for Open Government Data (NLOD 2.0).",
        "https://data.norge.no/nlod/en/2.0",
    ),
    "pl": (
        "LicenseRef-PL-Copyright-Art4",
        "Public Domain",
        "Polish Act of 4 February 1994 on Copyright and Related Rights Art. 4 (normative acts, resolutions of the Council of Ministers published in Monitor Polski, and official documents/materials are not subject to copyright).",
        "https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19940240083",
    ),
    "pt": (
        "LicenseRef-PT-CDADC-Art8-1",
        "Government-Work",
        "Portuguese Code of Copyright and Related Rights (CDADC, Decreto-Lei n.º 63/85) Art. 8.º(1) read with Art. 3.º(1)(c) (compiled or annotated official public texts and public speeches/reports not protected by copyright beyond the compiler's annotations).",
        "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/1985-34475475",
    ),
    "ro": (
        "LicenseRef-RO-Law8-1996-Art9",
        "Public Domain",
        "Romanian Law No. 8/1996 on Copyright and Related Rights Art. 9(b) (official texts of a political, legislative, administrative, or judicial nature are excluded from copyright).",
        "https://legislatie.just.ro/Public/DetaliiDocument/7816",
    ),
    "rs": (
        "LicenseRef-RS-Copyright-Art6",
        "Public Domain",
        "Republic of Serbia Law on Copyright and Related Rights (Official Gazette RS, No. 104/2009) Art. 6 (official materials of state bodies, laws, decrees, and strategies published in the Official Gazette are not protected by copyright).",
        "https://www.wipo.int/wipolex/en/legislation/details/6838",
    ),
    "se": (
        "LicenseRef-SE-Upphovsratt-Sec9",
        "Public Domain",
        "Swedish Act on Copyright in Literary and Artistic Works (Upphovsrättslagen 1960:729) § 9 (laws, ordinances, decisions, and official reports/strategies issued by Swedish public authorities are free from copyright).",
        "https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-1960729-om-upphovsratt-till-litterara-och_sfs-1960-729/",
    ),
    "si": (
        "LicenseRef-SI-ZASP-Art9",
        "Public Domain",
        "Slovenian Copyright and Related Rights Act (ZASP) Art. 9 (official legislative, administrative, and judicial texts, including Parliamentary Resolutions and government strategies, are not protected by copyright).",
        "https://pisrs.si/pregledPredpisa?id=ZAKO403",
    ),
    "sk": (
        "LicenseRef-SK-Law185-2015-Sec5",
        "Public Domain",
        "Slovak Copyright Act No. 185/2015 Z.z. § 5(b) (official works, government strategies, and public conceptual materials are excluded from copyright protection).",
        "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2015/185/",
    ),
    "tr": (
        "LicenseRef-TR-Law5846-Art31",
        "Public Domain",
        "Republic of Türkiye Law No. 5846 on Intellectual and Artistic Works Art. 31 (laws, regulations, Presidential decrees/circulars, and official publications may be freely reproduced and disseminated).",
        "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=5846&MevzuatTur=1&MevzuatTertip=3",
    ),
    "ua": (
        "LicenseRef-UA-Law2811-Art8",
        "Public Domain",
        "Law of Ukraine on Copyright and Related Rights (No. 2811-IX) Art. 8(1)(3) (acts of state authorities, Presidential Decrees enacting NSDC decisions, and official documents are not objects of copyright).",
        "https://zakon.rada.gov.ua/laws/show/2811-20",
    ),
    # Wave 2C: Rest of World (54 active strategy TLDs)
    "ae": (
        "LicenseRef-AE-TDRA-Terms",
        "Proprietary / All Rights Reserved",
        "UAE Telecommunications and Digital Government Regulatory Authority (TDRA) and UAE Government portal Terms and Conditions (copyright and intellectual property rights in ministerial strategy publications are reserved unless explicitly stated otherwise).",
        "https://tdra.gov.ae/en/terms-and-conditions",
    ),
    "ar": (
        "CC-BY-4.0",
        "Permissive",
        "República Argentina official government publication (Argentina.gob.ar / InfoLEG Terms and Conditions: licensed under Creative Commons Attribution 4.0 International — CC BY 4.0).",
        "https://www.argentina.gob.ar/terminos-y-condiciones",
    ),
    "az": (
        "LicenseRef-AZ-Law115IQ-Art7",
        "Public Domain",
        "Law of the Republic of Azerbaijan on Copyright and Related Rights (No. 115-IQ) Art. 7(a) (official documents — laws, court decisions, Presidential orders, and other texts of a legislative, administrative or judicial character — and their official translations are not objects of copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/AZ",
    ),
    "bd": (
        "LicenseRef-BD-Copyright-Sec72",
        "Government-Work",
        "Bangladesh Copyright Act, 2023 (Act No. 34 of 2023, replacing Copyright Act 2000) Sec. 72(1)(q)-(r) (official acts, Gazette publications, and government reports).",
        "https://www.wipo.int/wipolex/en/members/profile/BD",
    ),
    "bh": (
        "LicenseRef-BH-Law22-2006-Art4",
        "Public Domain",
        "Kingdom of Bahrain Law No. 22 of 2006 relating to the Protection of Copyright and Neighbouring Rights Art. 4(a) (official documents such as laws, decrees, regulations, decisions, and administrative decisions are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/BH",
    ),
    "br": (
        "LicenseRef-BR-Law9610-Art8-IV",
        "Public Domain",
        "Brazilian Copyright Law (Lei nº 9.610, de 19 de fevereiro de 1998) Art. 8º(IV) (texts of treaties, laws, decrees, regulations, judicial decisions, and other official acts are not objects of copyright protection) and Federal Open Data Policy (Decreto nº 8.777/2016).",
        "https://www.planalto.gov.br/ccivil_03/leis/l9610.htm",
    ),
    "bz": (
        "LicenseRef-BZ-Copyright-Cap252",
        "Proprietary / All Rights Reserved",
        "Belize Copyright Act (Chapter 252, Part IX Government copyright); no general statutory public-domain exemption for ministerial or regulatory strategy reports without explicit open licensing.",
        "https://www.wipo.int/wipolex/en/members/profile/BZ",
    ),
    "cl": (
        "LicenseRef-CL-Law17336-Official",
        "Government-Work",
        "Republic of Chile Law No. 17,336 on Intellectual Property and Diario Oficial / MinCiencia open government publication terms (official supreme decrees and open-licensed national policy documents).",
        "https://www.wipo.int/wipolex/en/members/profile/CL",
    ),
    "cn": (
        "LicenseRef-CN-Copyright-Art5-1",
        "Public Domain",
        "Copyright Law of the People's Republic of China Art. 5(1) (laws, regulations, resolutions, decisions and orders of state organs, and other documents of a legislative, administrative or judicial nature and their official translations are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/CN",
    ),
    "co": (
        "LicenseRef-CO-Law23-1982-Art41",
        "Public Domain",
        "Republic of Colombia Law 23 of 1982 on Copyright Art. 41 (permitted reproduction of the Constitution, laws, decrees, ordinances, regulations, and other administrative acts, including CONPES policy documents, conforming to the official edition) and Law 1712 of 2014 (Transparency and Open Data).",
        "https://www.wipo.int/wipolex/en/members/profile/CO",
    ),
    "cr": (
        "LicenseRef-CR-Law6683-Ministerial-Copyright",
        "Proprietary / All Rights Reserved",
        "Republic of Costa Rica Law No. 6683 on Copyright and Related Rights (ISBN-registered MICITT ministerial publications without an explicit open-redistribution license).",
        "https://www.wipo.int/wipolex/en/members/profile/CR",
    ),
    "do": (
        "LicenseRef-DO-Law65-00-Art4-3",
        "Public Domain",
        "Dominican Republic Law No. 65-00 on Copyright Art. 4(3) (official texts of a legislative, administrative or judicial nature, and their official translations, are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/DO",
    ),
    "eg": (
        "LicenseRef-EG-Law82-2002-Art141",
        "Public Domain",
        "Arab Republic of Egypt Law No. 82 of 2002 on the Protection of Intellectual Property Rights Art. 141(1) (official documents such as laws, regulations, and administrative decisions are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/EG",
    ),
    "et": (
        "LicenseRef-ET-Proc410-2004-Art5",
        "Public Domain",
        "Federal Democratic Republic of Ethiopia Copyright and Neighboring Rights Protection Proclamation No. 410/2004 Art. 5(b) (official texts of a legislative, administrative or legal nature and their official translations are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/ET",
    ),
    "fj": (
        "LicenseRef-FJ-Copyright-1999-Sec26",
        "Government-Work",
        "Fiji Copyright Act 1999 (Act No. 11 of 1999) Sec. 26 and Part X (State copyright and official legislative/inquiry exclusions).",
        "https://www.wipo.int/wipolex/en/members/profile/FJ",
    ),
    "gh": (
        "LicenseRef-GH-Act690-Sec2",
        "Government-Work",
        "Republic of Ghana Copyright Act, 2005 (Act 690) Sec. 2(b) (exclusion of enactments and official Government commission/agency reports published by the Government).",
        "https://www.wipo.int/wipolex/en/members/profile/GH",
    ),
    "id": (
        "LicenseRef-ID-Law28-2014-Art42",
        "Public Domain",
        "Republic of Indonesia Law No. 28 of 2014 on Copyright Art. 42(b) (no copyright subsists in laws, Government Regulations, Presidential Regulations/Decrees, regional regulations, and decisions of state bodies).",
        "https://www.wipo.int/wipolex/en/members/profile/ID",
    ),
    "il": (
        "LicenseRef-IL-Copyright-2007-State",
        "Proprietary / All Rights Reserved",
        "State of Israel Copyright Act, 2007 (5768-2007) Chapter 6 Secs. 36, 42 (State copyright in non-legislative ministerial and INCD strategy publications) and gov.il Terms of Use.",
        "https://www.wipo.int/wipolex/en/members/profile/IL",
    ),
    "in": (
        "LicenseRef-IN-Copyright-1957-Sec17d",
        "Proprietary / All Rights Reserved",
        "Indian Copyright Act, 1957 (Act No. 14 of 1957) Sec. 17(d) (Government copyright in ministerial and NITI Aayog strategy publications unless explicitly released under GODL-India).",
        "https://www.wipo.int/wipolex/en/members/profile/IN",
    ),
    "jm": (
        "LicenseRef-JM-Copyright-1993-Crown",
        "Proprietary / All Rights Reserved",
        "Jamaica Copyright Act, 1993 (Part XII Crown/Government copyright); ministerial strategy publications remain subject to Government copyright unless openly licensed.",
        "https://www.wipo.int/wipolex/en/members/profile/JM",
    ),
    "jo": (
        "LicenseRef-JO-Law22-1992-Art7",
        "Public Domain",
        "Hashemite Kingdom of Jordan Law on the Protection of Copyright and Related Rights No. 22 of 1992 Art. 7(a) (laws, regulations, administrative decisions, and all official documents and official translations thereof are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/JO",
    ),
    "ke": (
        "LicenseRef-KE-Cap130-Sec25",
        "Government-Work",
        "Republic of Kenya Copyright Act (Cap. 130, Act No. 12 of 2001) Sec. 2 & Sec. 25 (exclusion of written laws and Government copyright in commissioned publications).",
        "https://www.wipo.int/wipolex/en/members/profile/KE",
    ),
    "kw": (
        "LicenseRef-KW-Law75-2019-Art4",
        "Public Domain",
        "State of Kuwait Law No. 75 of 2019 on Copyright and Related Rights Art. 4(1) (official documents such as laws, regulations, and administrative decisions are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/KW",
    ),
    "kz": (
        "LicenseRef-KZ-Law6I-Art8-1",
        "Public Domain",
        "Law of the Republic of Kazakhstan No. 6-I of June 10, 1996 on Copyright and Related Rights Art. 8(1) (official documents — laws, resolutions, and other texts of a legislative, administrative, judicial or diplomatic character — and their official translations are not objects of copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/KZ",
    ),
    "lk": (
        "LicenseRef-LK-Act36-2003-Sec8",
        "Public Domain",
        "Democratic Socialist Republic of Sri Lanka Intellectual Property Act, No. 36 of 2003 Sec. 8(a) (no copyright protection extends to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/LK",
    ),
    "ma": (
        "LicenseRef-MA-Law2-00-Art8",
        "Public Domain",
        "Kingdom of Morocco Law No. 2-00 on Copyright and Related Rights Art. 8(a) (protection does not extend to official texts of a legislative, administrative or judicial nature, nor to their official translations).",
        "https://www.wipo.int/wipolex/en/members/profile/MA",
    ),
    "mn": (
        "LicenseRef-MN-Copyright-2021-Art8",
        "Public Domain",
        "Law of Mongolia on Copyright (2021) Art. 8.1.1 (laws, legislative acts, State Great Khural resolutions, and other official documents of a legislative, administrative, or judicial nature and their official translations are not protected by copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/MN",
    ),
    "mx": (
        "LicenseRef-MX-LFDA-Art14-VIII",
        "Public Domain",
        "United Mexican States Federal Copyright Law (Ley Federal del Derecho de Autor) Art. 14(VIII) (legislative, regulatory, administrative or judicial texts and their official translations are not subject to copyright protection) and Libre Uso MX (datos.gob.mx).",
        "https://www.wipo.int/wipolex/en/members/profile/MX",
    ),
    "my": (
        "LicenseRef-MY-Act332-Sec11-GovCopyright",
        "Proprietary / All Rights Reserved",
        "Malaysian Copyright Act 1987 (Act 332) Sec. 11 & Sec. 26 (Government copyright in works made under Government direction) and NACSA copyright reservation.",
        "https://www.wipo.int/wipolex/en/members/profile/MY",
    ),
    "ng": (
        "LicenseRef-NG-Copyright-2022-Sec28",
        "Government-Work",
        "Federal Republic of Nigeria Copyright Act, 2022 (Act No. 8 of 2023) Sec. 28 (Government copyright in works made under the direction or control of the Government or a state authority).",
        "https://www.wipo.int/wipolex/en/members/profile/NG",
    ),
    "np": (
        "LicenseRef-NP-Copyright-2059-Sec4",
        "Public Domain",
        "Nepal Copyright Act, 2059 (2002) Sec. 4(a) (no copyright protection extends to any constitution, law, rule, order, judicial decision, or official administrative text).",
        "https://www.wipo.int/wipolex/en/members/profile/NP",
    ),
    "om": (
        "LicenseRef-OM-RD65-2008-Art4",
        "Public Domain",
        "Sultanate of Oman Royal Decree No. 65/2008 promulgating the Law on Copyright and Related Rights Art. 4(a) (official documents of a legislative, administrative or judicial nature and their official translations are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/OM",
    ),
    "org": (
        "LicenseRef-MU-Copyright-2014-Sec7",
        "Public Domain",
        "Republic of Mauritius Copyright Act 2014 (Act No. 2 of 2014) Sec. 7(1)(b) (no copyright protection extends to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/MU",
    ),
    "pa": (
        "LicenseRef-PA-Law64-2012-Art9",
        "Public Domain",
        "Republic of Panama Law No. 64 of October 10, 2012 on Copyright and Neighboring Rights Art. 9(2) (official texts of a legislative, administrative or judicial nature, and their official translations, are not protected by copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/PA",
    ),
    "pe": (
        "LicenseRef-PE-DL822-Art9",
        "Public Domain",
        "Republic of Peru Legislative Decree No. 822 (Law on Copyright) Art. 9(b) (official texts of a legislative, administrative or judicial nature, and their official translations, are not objects of copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/PE",
    ),
    "pg": (
        "LicenseRef-PG-Copyright-2000-Sec5",
        "Public Domain",
        "Independent State of Papua New Guinea Copyright and Neighbouring Rights Act 2000 Sec. 5(b) (protection does not extend to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/PG",
    ),
    "ph": (
        "LicenseRef-PH-RA8293-Sec176",
        "Public Domain",
        "Intellectual Property Code of the Philippines (Republic Act No. 8293) Sec. 176.1 (no copyright shall subsist in any work of the Government of the Philippines).",
        "https://www.wipo.int/wipolex/en/members/profile/PH",
    ),
    "pk": (
        "LicenseRef-PK-Ordinance1962-Sec57",
        "Government-Work",
        "Pakistan Copyright Ordinance, 1962 (Ordinance No. XXXIV of 1962) Sec. 57(1)(q) (permitted reproduction of official acts, Gazette publications, and government reports unless prohibited by the Government).",
        "https://www.wipo.int/wipolex/en/members/profile/PK",
    ),
    "py": (
        "LicenseRef-PY-Law1328-Art8",
        "Public Domain",
        "Republic of Paraguay Law No. 1328/1998 on Copyright and Related Rights Art. 8(2) (official texts of a legislative, administrative or judicial nature, and their official translations, are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/PY",
    ),
    "qa": (
        "LicenseRef-QA-MCIT-QCRI-Terms",
        "Proprietary / All Rights Reserved",
        "State of Qatar Law No. 7 of 2002 on the Protection of Copyright and Neighboring Rights and MCIT / Qatar Computing Research Institute (HBKU) publication terms.",
        "https://www.wipo.int/wipolex/en/members/profile/QA",
    ),
    "ru": (
        "LicenseRef-RU-CivilCode-Art1259",
        "Public Domain",
        "Civil Code of the Russian Federation (Part Four) Art. 1259(6)(1) (official documents of state authorities, including laws, Presidential decrees, and other materials of a legislative, administrative or judicial nature and their official translations are not objects of copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/RU",
    ),
    "rw": (
        "LicenseRef-RW-Law055-2024-Art244",
        "Public Domain",
        "Republic of Rwanda Law No. 055/2024 of 20/06/2024 on Protection of Intellectual Property Art. 244(2) (official texts of a legislative, administrative or judicial nature, as well as their official translations, are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/RW",
    ),
    "sa": (
        "LicenseRef-SA-RD-M41-Art4",
        "Government-Work",
        "Kingdom of Saudi Arabia Copyright Law (Royal Decree No. M/41 of 2 Rajab 1424H) Art. 4(1) (laws, regulations, decisions of administrative commissions, and official documents and official translations thereof are excluded from protection).",
        "https://www.wipo.int/wipolex/en/members/profile/SA",
    ),
    "sn": (
        "LicenseRef-SN-Law2008-09-Art7",
        "Public Domain",
        "Republic of Senegal Law No. 2008-09 of January 25, 2008 on Copyright and Neighboring Rights Art. 7(a) (official texts of a legislative, administrative or judicial nature and their official translations are excluded from copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/SN",
    ),
    "th": (
        "LicenseRef-TH-Copyright-BE2537-Sec7",
        "Public Domain",
        "Kingdom of Thailand Copyright Act B.E. 2537 (1994) Sec. 7(2)-(3) (constitutions, legislation, regulations, notifications, orders, explanations and official correspondence of Ministries, Departments, or state agencies are not deemed copyright works).",
        "https://www.wipo.int/wipolex/en/members/profile/TH",
    ),
    "to": (
        "LicenseRef-TO-Copyright-Cap38-12-Sec5",
        "Public Domain",
        "Kingdom of Tonga Copyright Act (Cap. 38.12 / Act 20 of 2002) Sec. 5(b) (no copyright protection extends to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/TO",
    ),
    "tt": (
        "LicenseRef-TT-Chap82-80-Sec7",
        "Public Domain",
        "Republic of Trinidad and Tobago Copyright Act (Chap. 82:80, Act No. 8 of 1997) Sec. 7(1)(b) (no copyright protection extends to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/TT",
    ),
    "uy": (
        "CC-BY-4.0",
        "Permissive",
        "Oriental Republic of Uruguay official government publication (gub.uy Portal Unificado del Estado Uruguayo Terms of Use / Decree No. 54/017: licensed under Creative Commons Attribution 4.0 International — CC BY 4.0).",
        "https://www.gub.uy/terminos-uso",
    ),
    "uz": (
        "LicenseRef-UZ-LawZRU42-Art8",
        "Public Domain",
        "Law of the Republic of Uzbekistan No. ZRU-42 of July 20, 2006 on Copyright and Related Rights Art. 8(1) (official documents — laws, Presidential decrees/resolutions, and decisions, as well as their official translations — are not objects of copyright).",
        "https://www.wipo.int/wipolex/en/members/profile/UZ",
    ),
    "vn": (
        "LicenseRef-VN-IP-Law-Art15-2",
        "Public Domain",
        "Socialist Republic of Vietnam Law on Intellectual Property (No. 50/2005/QH11, as amended) Art. 15(2) (documents of state agencies, political organizations, and armed forces units in the domain of state management — including administrative documents and Prime Ministerial Decisions — and their official translations are not covered by copyright protection).",
        "https://www.wipo.int/wipolex/en/members/profile/VN",
    ),
    "vu": (
        "LicenseRef-VU-Cap331-Sec5",
        "Public Domain",
        "Republic of Vanuatu Copyright and Related Rights Act No. 42 of 2000 (Cap. 331) Sec. 5(1)(b) (copyright protection does not extend to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/VU",
    ),
    "ws": (
        "LicenseRef-WS-Copyright-1998-Sec5",
        "Public Domain",
        "Independent State of Samoa Copyright Act 1998 (No. 25 of 1998) Sec. 5(b) (no copyright protection extends to any official text of a legislative, administrative or legal nature, or any official translation thereof).",
        "https://www.wipo.int/wipolex/en/members/profile/WS",
    ),
    "za": (
        "LicenseRef-ZA-Act98-1978-Sec12-8",
        "Public Domain",
        "Republic of South Africa Copyright Act 98 of 1978 Sec. 12(8)(a) (no copyright shall subsist in official texts of a legislative, administrative or legal nature, or in official translations of such texts).",
        "https://www.wipo.int/wipolex/en/members/profile/ZA",
    ),
    "zm": (
        "LicenseRef-ZM-Cap406-Sec9",
        "Government-Work",
        "Republic of Zambia Copyright and Performance Rights Act, 1994 (Chapter 406) Sec. 9(a) & Sec. 30 (legislative exclusions and State copyright in Government works).",
        "https://www.wipo.int/wipolex/en/members/profile/ZM",
    ),
}


def license_for_tld(tld: str, namespace: str, md_text: str = "", secid: str = "") -> dict:
    """Return complete schema-aligned government/public-sector license metadata verified against document text."""
    low_md = (md_text or "").lower()
    # First check explicit copyright/redistribution restrictions in the extracted document text
    if low_md and any(
        kw in low_md
        for kw in (
            "by-nc",
            "non-commercial use only",
            "for non-commercial purposes only",
            "not for commercial use",
        )
    ):
        if tld == "sg":
            return _make_license(
                "LicenseRef-SG-Government-NonCommercial-NoDerivatives",
                "Non-Commercial-No-Derivatives",
                "Copyright Government of Singapore (MDDI / Smart Nation). Document permits reproduction without modification for non-commercial use only; routed to private dataset repository.",
                "https://www.smartnation.gov.sg/terms-of-use/",
                redistribution="permitted_non_commercial_verbatim",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        if tld == "int" and namespace == "itu.int":
            return _make_license(
                "CC-BY-NC-3.0-IGO",
                "Non-Commercial",
                "Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO (CC BY-NC-SA 3.0 IGO / CC BY-NC 3.0 IGO) as stated in the publication copyright notice.",
                "https://creativecommons.org/licenses/by-nc/3.0/igo/deed.en",
                redistribution="permitted_with_attribution_non_commercial",
                derivatives="permitted_with_attribution_non_commercial",
                publicly_redistributable=False,
            )
        if namespace == "oas.org":
            return _make_license(
                "CC-BY-NC-ND-3.0-IGO",
                "Non-Commercial-No-Derivatives",
                "Licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 IGO (CC BY-NC-ND 3.0 IGO) as stated in the GS/OAS publication copyright notice; stored in private internal repository, not publicly redistributed.",
                "https://creativecommons.org/licenses/by-nc-nd/3.0/igo/",
                redistribution="permitted_with_attribution_non_commercial_verbatim",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "LicenseRef-NonCommercial",
            "Non-Commercial",
            f"Official publication ({namespace}) with explicit non-commercial reuse restriction in document copyright notice.",
            None,
            redistribution="permitted_non_commercial",
            derivatives="prohibited",
            publicly_redistributable=False,
        )
    if (
        secid == "secid:reference/gov.br/pbia@2024-2028"
        or "é permitida a reprodução parcial ou total desta obra" in low_md
    ):
        return _make_license(
            "LicenseRef-BR-MCTI-CGEE-Attribution",
            "Permissive",
            "Federative Republic of Brazil (MCTI / CGEE) official publication; explicit open-attribution notice on page 4 ('É permitida a reprodução parcial ou total desta obra, desde que citada a fonte') and Brazilian Copyright Law (Lei nº 9.610/1998) Art. 8º(IV).",
            "https://www.planalto.gov.br/ccivil_03/leis/l9610.htm",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if low_md and any(
        kw in low_md
        for kw in (
            "all rights reserved",
            "all right reserved",
            "copyright retained",
            "redistribution subject to",
            "subject to separate terms",
            "without prior written permission",
            "without prior permission in writing",
            "without the prior permission",
            "tous droits réservés",
            "alle rechte vorbehalten",
            "todos los derechos reservados",
            "todos os direitos reservados",
            "sin permiso previo, expreso y por escrito",
        )
    ):
        if tld == "au":
            return _make_license(
                "LicenseRef-All-Rights-Reserved",
                "Proprietary / All Rights Reserved",
                "Commonwealth of Australia copyright retained; document explicitly prohibits reproduction, storage, or transmission without prior written permission.",
                "https://www.defence.gov.au/copyright",
                redistribution="prohibited",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "LicenseRef-All-Rights-Reserved",
            "Proprietary / All Rights Reserved",
            f"Official publication ({namespace}) with explicit copyright reservation ('All rights reserved' or prior permission requirement) in document text.",
            None,
            redistribution="prohibited",
            derivatives="prohibited",
            publicly_redistributable=False,
        )
    # If no full text has been acquired yet (`md_text` is empty), do not assert `publicly_redistributable: true`
    # until the primary document is acquired and inspected for imprint/third-party restrictions (except US 17 U.S.C. § 105 / OGL-Canada / OGL-UK).
    if not low_md.strip() and tld not in ("gov", "ca", "uk"):
        if namespace == "oas.org":
            return _make_license(
                "LicenseRef-OAS-Terms",
                "Proprietary / All Rights Reserved",
                "Metadata-only record (full text pending acquisition; redistribution rights not asserted until primary document is acquired and verified). Underlying General Secretariat of the Organization of American States (GS/OAS) publication is governed by OAS Terms and Conditions (copyright retained by GS/OAS).",
                "https://www.oas.org/en/terms_conditions.asp",
                redistribution="pending_verification",
                derivatives="pending_verification",
                publicly_redistributable=False,
            )
        stat = _TLD_STATUTORY_LICENSES.get(tld)
        if stat:
            spdx_id, grp, basis_note, stat_url = stat
            return _make_license(
                spdx_id,
                grp,
                f"Metadata-only record (full text pending acquisition; redistribution rights not asserted until primary document is acquired and verified). Underlying official publication ({namespace}) is governed by {basis_note}",
                stat_url,
                redistribution="pending_verification",
                derivatives="pending_verification",
                publicly_redistributable=False,
            )
        return _make_license(
            "LicenseRef-Government-Work",
            "Government-Work",
            f"Metadata-only record (full text pending acquisition; redistribution rights not asserted until primary document for {namespace} is acquired and verified against jurisdiction copyright terms).",
            f"https://{namespace}/" if namespace else None,
            redistribution="pending_verification",
            derivatives="pending_verification",
            publicly_redistributable=False,
        )
    if tld == "gov":
        return _make_license(
            "CC0-1.0",
            "Public Domain",
            "United States Government work (17 U.S.C. § 105); in the public domain worldwide.",
            "https://www.usa.gov/government-works",
        )
    if tld == "ca":
        return _make_license(
            "OGL-Canada-2.0",
            "Permissive",
            "Open Government Licence – Canada (https://open.canada.ca/en/open-government-licence-canada).",
            "https://open.canada.ca/en/open-government-licence-canada",
        )
    if tld == "uk":
        return _make_license(
            "OGL-UK-3.0",
            "Permissive",
            "Crown copyright; licensed under the Open Government Licence v3.0.",
            "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        )
    if tld == "au":
        if (
            "without prior written permission" in md_text.lower()
            or "without prior permission in writing" in md_text.lower()
            or namespace == "defence.gov.au"
            or secid.endswith("@2009")
        ):
            return _make_license(
                "LicenseRef-All-Rights-Reserved",
                "Proprietary / All Rights Reserved",
                "Commonwealth of Australia copyright retained; document explicitly prohibits reproduction, storage, or transmission without prior written permission.",
                "https://www.defence.gov.au/copyright",
                redistribution="prohibited",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "CC-BY-4.0",
            "Permissive",
            f"Commonwealth of Australia copyright ({namespace}); licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).",
            "https://creativecommons.org/licenses/by/4.0/",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "nz":
        return _make_license(
            "CC-BY-4.0",
            "Permissive",
            f"Crown copyright New Zealand ({namespace}); licensed under Creative Commons Attribution 4.0 International (NZGOAL / CC BY 4.0).",
            "https://creativecommons.org/licenses/by/4.0/",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "eu":
        return _make_license(
            "LicenseRef-EU-Reuse-Decision-2011-833",
            "Permissive",
            f"European Union official publication ({namespace}); reuse authorized with attribution under Commission Decision 2011/833/EU.",
            "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011D0833",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "fr":
        return _make_license(
            "etalab-2.0",
            "Permissive",
            "Licence Ouverte / Open Licence Version 2.0 (Etalab, République française).",
            "https://www.etalab.gouv.fr/licence-ouverte-open-licence/",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "de":
        return _make_license(
            "LicenseRef-Government-Work",
            "Government-Work",
            f"Official German Federal Government publication ({namespace}; § 5 UrhG public official work). Publicly released for free download, reference, and citation.",
            "https://www.gesetze-im-internet.de/urhg/__5.html",
            redistribution="permitted_for_reference",
            derivatives="varies_by_jurisdiction",
            publicly_redistributable=True,
        )
    if tld == "it":
        return _make_license(
            "CC-BY-4.0",
            "Permissive",
            f"Italian Government open publication ({namespace}); licensed under CC BY 4.0 (CAD Art. 52 / IODL 2.0).",
            "https://creativecommons.org/licenses/by/4.0/",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "sg":
        if (
            "reproduce this document without modification, but only for non-commercial use" in md_text.lower()
            or secid == "secid:reference/smartnation.gov.sg/national-ai-strategy@2023"
        ):
            return _make_license(
                "LicenseRef-SG-Government-NonCommercial-NoDerivatives",
                "Non-Commercial-No-Derivatives",
                "Copyright Government of Singapore (MDDI / Smart Nation). Document permits reproduction without modification for non-commercial use only; routed to private dataset repository.",
                "https://www.smartnation.gov.sg/terms-of-use/",
                redistribution="permitted_non_commercial_verbatim",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "LicenseRef-All-Rights-Reserved",
            "Proprietary / All Rights Reserved",
            "Copyright Government of Singapore retained (all rights reserved under Singapore Government Terms of Use; prior written permission required for reproduction or redistribution).",
            "https://www.csa.gov.sg/terms-of-use",
            redistribution="prohibited",
            derivatives="prohibited",
            publicly_redistributable=False,
        )
    if tld == "jp":
        return _make_license(
            "LicenseRef-Japan-Government-Notification-Likely-Excluded",
            "Government-Work",
            "Japanese Copyright Act Article 13 excludes laws, regulations, and government notifications from copyright; Cabinet-level strategy/guideline status is slightly nuanced (likely excluded as an official government directive, or covered under the Government of Japan Standard Terms of Use / Public Data License 1.0).",
            "https://www.digital.go.jp/resources/open_data/public_data_license_v1.0",
            redistribution="likely_permitted",
            derivatives="likely_permitted",
            publicly_redistributable=True,
        )
    if tld == "kr":
        return _make_license(
            "KOGL-1.0",
            "Permissive",
            "Republic of Korea official government publication (Korea Open Government License Type 1: Source Indication / Copyright Act Article 24-2).",
            "https://www.kogl.or.kr/info/licenseType.do",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "tw":
        if (
            "不得為商業目的之使用，亦不得修改該著作" in md_text
            or ("mnd.gov.tw/national-defense-report" in secid and secid.endswith(("@2023", "@2025")))
        ):
            return _make_license(
                "LicenseRef-TW-MND-NonCommercial-NoDerivatives",
                "Non-Commercial-No-Derivatives",
                "Copyright Ministry of National Defense, R.O.C. (Taiwan). Explicit copyright notice permits verbatim reproduction with attribution for non-commercial use only; commercial use and modifications are prohibited.",
                "https://www.mnd.gov.tw/",
                redistribution="permitted_non_commercial_verbatim_with_attribution",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        if "reprints without permission will be prosecuted" in md_text.lower() or namespace == "mnd.gov.tw":
            return _make_license(
                "LicenseRef-All-Rights-Reserved",
                "Proprietary / All Rights Reserved",
                "Copyright Ministry of National Defense, R.O.C. (Taiwan) retained; reprints or redistribution without permission are prohibited.",
                "https://www.mnd.gov.tw/",
                redistribution="prohibited",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "OGDL-Taiwan-1.0",
            "Permissive",
            "Open Government Data License, version 1.0 (Taiwan).",
            "https://data.gov.tw/license",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if tld == "int":
        if namespace == "itu.int":
            if "by-nc 3.0 igo" in md_text.lower() or secid.endswith(("@2021", "@2025")):
                return _make_license(
                    "CC-BY-NC-3.0-IGO",
                    "Non-Commercial",
                    "Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO (CC BY-NC-SA 3.0 IGO / CC BY-NC 3.0 IGO) as stated in the publication copyright notice.",
                    "https://creativecommons.org/licenses/by-nc/3.0/igo/deed.en",
                    redistribution="permitted_with_attribution_non_commercial",
                    derivatives="permitted_with_attribution_non_commercial",
                    publicly_redistributable=False,
                )
            return _make_license(
                "CC-BY-3.0-IGO",
                "Permissive",
                "Licensed under Creative Commons Attribution 3.0 IGO (CC BY 3.0 IGO) as stated in the publication copyright notice.",
                "http://creativecommons.org/licenses/by/3.0/igo",
                redistribution="permitted_with_attribution",
                derivatives="permitted_with_attribution",
                publicly_redistributable=True,
            )
        if namespace == "au.int":
            return _make_license(
                "LicenseRef-All-Rights-Reserved",
                "Proprietary / All Rights Reserved",
                "African Union Commission copyright retained; prior permission required for commercial redistribution or derivative works.",
                "https://au.int/en/legal-disclaimer",
                redistribution="prohibited",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            "LicenseRef-All-Rights-Reserved",
            "Proprietary / All Rights Reserved",
            f"International intergovernmental organization publication ({namespace}); copyright retained by issuing organization.",
            None,
            redistribution="prohibited",
            derivatives="prohibited",
            publicly_redistributable=False,
        )
    if namespace == "oas.org":
        return _make_license(
            "CC-BY-NC-ND-3.0-IGO",
            "Non-Commercial-No-Derivatives",
            "Licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 3.0 IGO (CC BY-NC-ND 3.0 IGO) as stated in the GS/OAS publication copyright notice; stored in private internal repository, not publicly redistributed.",
            "https://creativecommons.org/licenses/by-nc-nd/3.0/igo/",
            redistribution="permitted_with_attribution_non_commercial_verbatim",
            derivatives="prohibited",
            publicly_redistributable=False,
        )
    if secid == "secid:reference/gob.cl/politica-nacional-ciberseguridad@2017-2022" or "atribución-compartirigual 4.0" in low_md:
        return _make_license(
            "CC-BY-SA-4.0",
            "Share-Alike",
            "Government of Chile official publication (gob.cl); explicitly licensed in the document imprint under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
            "https://creativecommons.org/licenses/by-sa/4.0/",
            redistribution="permitted_with_attribution_share_alike",
            derivatives="permitted_with_attribution_share_alike",
            publicly_redistributable=True,
        )
    if secid == "secid:reference/moitt.gov.pk/national-security-policy-of-pakistan@2022":
        return _make_license(
            "LicenseRef-PK-NSD-Attribution",
            "Permissive",
            "Government of Pakistan (National Security Division, Prime Minister's Office) explicit open publication license ('This publication may be reproduced and transmitted by any means for non-commercial or commercial Reference with due attribution to the Government of Pakistan') and Pakistan Copyright Ordinance 1962 Sec. 57(1)(q).",
            "https://www.wipo.int/wipolex/en/members/profile/PK",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    if secid == "secid:reference/nca.gov.sa/national-cybersecurity-strategy@2020":
        return _make_license(
            "LicenseRef-SA-NCA-Open-TLP-White",
            "Government-Work",
            "Kingdom of Saudi Arabia National Cybersecurity Authority (NCA) official publication ('Sharing Notice: White | Document Classification: Open' — unrestricted public sharing) and Saudi Copyright Law (Royal Decree No. M/41) Art. 4(1).",
            "https://www.wipo.int/wipolex/en/members/profile/SA",
            redistribution="permitted",
            derivatives="permitted",
            publicly_redistributable=True,
        )
    stat = _TLD_STATUTORY_LICENSES.get(tld)
    if stat:
        spdx_id, grp, basis_note, stat_url = stat
        if grp in ("Proprietary / All Rights Reserved", "Non-Commercial", "Non-Commercial-No-Derivatives"):
            return _make_license(
                spdx_id,
                grp,
                f"Official publication ({namespace}); {basis_note} Full-text extraction stored in private internal repository, not publicly redistributed.",
                stat_url,
                redistribution="prohibited" if "Proprietary" in grp else "permitted_non_commercial",
                derivatives="prohibited",
                publicly_redistributable=False,
            )
        return _make_license(
            spdx_id,
            grp,
            f"Official publication ({namespace}); {basis_note}",
            stat_url,
            redistribution="permitted",
            derivatives="permitted",
            publicly_redistributable=True,
        )
    return _make_license(
        "LicenseRef-Government-Work",
        "Government-Work",
        f"Official national strategy publication ({namespace}); publicly released for free download, policy reference, and research.",
        f"https://{namespace}/" if namespace else None,
        redistribution="permitted_for_reference",
        derivatives="varies_by_jurisdiction",
        publicly_redistributable=True,
    )


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


def _decompress_and_validate_bytes(data: bytes) -> bytes:
    """Auto-decompress gzip payloads (e.g. Wayback `id_` responses) and reject corrupt non-PDF NUL bytes."""
    if not data:
        return b""
    if data[:2] == b"\x1f\x8b":
        try:
            data = gzip.decompress(data)
        except Exception:
            return b""
    is_pdf = data[:5] == b"%PDF-" or b"%PDF-1." in data[:1024]
    if not is_pdf and b"\x00" in data:
        return b""
    return data


def fetch_url_bytes(url: str, timeout: int = 35) -> tuple[bytes | None, str]:
    """Fetch URL bytes using disk cache + curl (--http1.1 --compressed -b '') + requests fallback."""
    global _LAST_WAYBACK_TS
    cache_key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    cache_bin = CACHE_DIR / f"{cache_key}.bin"
    cache_meta = CACHE_DIR / f"{cache_key}.json"

    if cache_bin.exists() and cache_meta.exists():
        raw = cache_bin.read_bytes()
        data = _decompress_and_validate_bytes(raw)
        if data and data != raw:
            cache_bin.write_bytes(data)
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
        "--compressed",
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

    raw_data = cache_bin.read_bytes() if cache_bin.exists() else b""
    data = _decompress_and_validate_bytes(raw_data)
    if data and data != raw_data:
        cache_bin.write_bytes(data)

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
        req_data = _decompress_and_validate_bytes(r.content)
        if (
            r.status_code == 200
            and len(req_data) > 400
            and b"Internet Archive: Temporarily Offline" not in req_data[:4000]
            and b"<title>Just a moment...</title>" not in req_data[:4000]
            and b"AwsWafIntegration" not in req_data[:8000]
        ):
            cache_bin.write_bytes(req_data)
            cache_meta.write_text(json.dumps({"final_url": r.url, "http_code": str(r.status_code)}), encoding="utf-8")
            return req_data, r.url
    except Exception:
        pass

    if cache_bin.exists():
        cache_bin.unlink(missing_ok=True)
    return None, url


def _unwrap_wayback_host(url: str) -> str:
    m = re.search(r"web\.archive\.org/web/[^/]+/(https?://.+)", url)
    if m:
        url = m.group(1)
    return (urllib.parse.urlparse(url).hostname or "").lower()


def _is_trusted_pdf_target(base_url: str, pdf_url: str, namespace: str) -> bool:
    """Ensure embedded PDF links stay on the official namespace/domain or a trusted government CDN."""
    pdf_host = _unwrap_wayback_host(pdf_url)
    base_host = _unwrap_wayback_host(base_url)
    ns_host = namespace.lower()
    if not pdf_host:
        return False
    if pdf_host == base_host or pdf_host.endswith("." + ns_host) or pdf_host == ns_host:
        return True
    base_parts = [p for p in ns_host.split(".") if p]
    pdf_parts = [p for p in pdf_host.split(".") if p]
    if len(base_parts) >= 2 and len(pdf_parts) >= 2 and base_parts[-2:] == pdf_parts[-2:]:
        return True
    return any(pdf_host == h or pdf_host.endswith("." + h) for h in _TRUSTED_PDF_HOSTS)


def find_embedded_pdf_urls(
    html_text: str,
    base_url: str,
    version: str,
    doc_name: str,
    namespace: str = "",
) -> list[str]:
    """Extract and score embedded PDF links on an HTML landing page, respecting <base href> and domain trust."""
    soup = BeautifulSoup(html_text, "html.parser")
    effective_base = base_url
    base_tag = soup.find("base", href=True)
    if base_tag and base_tag["href"].strip():
        effective_base = urllib.parse.urljoin(base_url, base_tag["href"].strip())

    scored: list[tuple[int, str]] = []
    seen: set[str] = set()
    yr = version[:4] if len(version) >= 4 and version[:4].isdigit() else ""
    target_years = set(re.findall(r"(?:199\d|20[0-3]\d)", version))
    keywords = [
        w
        for w in re.split(r"[^a-z0-9]+", doc_name.lower())
        if len(w) >= 2 and w not in ("the", "and", "for", "of", "in", "to", "on", "strategy", "national", "policy", "report", "plan", "program")
    ]

    wayback_prefix_m = re.match(r"^(https?://web\.archive\.org/web/[^/]+/https?://[^/]+)", effective_base)
    wayback_origin_prefix = wayback_prefix_m.group(1) if wayback_prefix_m else ""

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        if wayback_origin_prefix and href.startswith("/") and not href.startswith("//") and not href.startswith("/web/"):
            full = wayback_origin_prefix + href
        else:
            full = urllib.parse.urljoin(effective_base, href)
        low_href = full.lower()
        link_txt = a.get_text(" ", strip=True).lower()
        is_pdf_candidate = (
            ".pdf" in low_href
            or "__blob=publicationfile" in low_href
            or "/bitstreams/" in low_href
            or "qdrfile/" in low_href
            or ("download" in low_href and "pdf" in link_txt)
        )
        if not is_pdf_candidate or full in seen:
            continue
        if any(b in low_href for b in _BLOCKED_HTML_SUBSTRINGS):
            continue
        if "cyber" in low_href and not any(k in doc_name.lower() for k in ("cyber", "ciber", "kyber", "siber")):
            continue
        if namespace and not _is_trusted_pdf_target(base_url, full, namespace):
            continue
        cand_tail = urllib.parse.unquote(low_href.rsplit("/", 1)[-1])
        cand_years = set(re.findall(r"(?:199\d|20[0-3]\d)", f"{cand_tail} {link_txt}"))
        if target_years and cand_years and target_years.isdisjoint(cand_years):
            continue
        seen.add(full)
        score = 0
        if yr and (yr in low_href or yr in link_txt):
            score += 10
        kw_matches = 0
        for kw in keywords:
            if kw in low_href or kw in link_txt:
                score += 4
                kw_matches += 1
        if "strategy" in low_href or "strategy" in link_txt or "qdr" in low_href:
            score += 3
        if "english" in low_href or "_en" in low_href or "-en" in low_href or "eng" in low_href:
            score += 4
        if "summary" in low_href or "leaflet" in low_href or "brochure" in low_href or "pamphlet" in low_href:
            score -= 5
        if score >= 6 and (
            kw_matches >= 1
            or "strategy" in low_href
            or "strategy" in link_txt
            or "qdr" in low_href
            or "apo-nid" in low_href
        ):
            scored.append((score, full))

    # Also detect Korean government eGovFrame PDF attachment links: fn_download('atchFileNo', 'fileOrd', 'pdf')
    for m_fn in re.finditer(
        r"fn_download\(\s*['\"](\d+)['\"]\s*,\s*['\"](\d+)['\"]\s*,\s*['\"]pdf['\"]\s*\)",
        html_text,
        re.IGNORECASE,
    ):
        dl_url = urllib.parse.urljoin(
            effective_base,
            f"/ssm/file/fileDown.do?atchFileNo={m_fn.group(1)}&fileOrd={m_fn.group(2)}&fileBtn=A",
        )
        if "atchfileno=47317" in dl_url.lower():
            continue
        if dl_url not in seen and (not namespace or _is_trusted_pdf_target(base_url, dl_url, namespace)):
            seen.add(dl_url)
            scored.append((25, dl_url))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [u for _, u in scored[:4]]


def ensure_hierarchical_headings(md: str, doc_title: str, doc_desc: str, is_annex: bool = False) -> str:
    """Promote legitimate unformatted section/chapter headings in plain/CJK/European PDFs and XHTML
    without inventing arbitrary artificial chunk headings.
    """
    md = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\xad]+", " ", md)
    # Restore raster chapter and pillar divider headings in Costa Rica's 2023-2027 National Cybersecurity Strategy from Page 7 Table of Contents
    if "Estrategia Nacional de Ciberseguridad de Costa Rica" in doc_title or "PARTICIPACIÓN SOCIAL Y CIUDADANA 7." in md:
        _cr_replacements = [
            (
                "L\n\na pandemia de COVID-19 y la postpandemia han generado",
                "## 1. CONTEXTO ACTUAL DE CIBERSEGURIDAD\n\nLa pandemia de COVID-19 y la postpandemia han generado",
            ),
            (
                "L a pandemia de COVID-19 y la postpandemia han generado",
                "## 1. CONTEXTO ACTUAL DE CIBERSEGURIDAD\n\nLa pandemia de COVID-19 y la postpandemia han generado",
            ),
            (
                "osta Rica cuenta con un marco jurídico y reglamentario para proteger a la sociedad contra la ciberdelincuencia y promover un entorno cibernético seguro, de conformidad con los principios de inclusión y de entorno de confianza. C",
                "## 2. MARCO NORMATIVO\n\nCosta Rica cuenta con un marco jurídico y reglamentario para proteger a la sociedad contra la ciberdelincuencia y promover un entorno cibernético seguro, de conformidad con los principios de inclusión y de entorno de confianza.",
            ),
            (
                "osta Rica ha vivido una profunda transformación digital durante la última década. Según la Superintendencia de Telecomunicaciones (SUTEL), Internet se ha convertido en un servicio esencial para los consumidores tanto a través de redes fijas como móviles. El aumento ha sido significativo tanto en la cantidad de usuarios como en las velocidades y el volumen de tráfico de la información (SUTEL, 2023). C",
                "## 3. DIAGNÓSTICO\n\nCosta Rica ha vivido una profunda transformación digital durante la última década. Según la Superintendencia de Telecomunicaciones (SUTEL), Internet se ha convertido en un servicio esencial para los consumidores tanto a través de redes fijas como móviles. El aumento ha sido significativo tanto en la cantidad de usuarios como en las velocidades y el volumen de tráfico de la información (SUTEL, 2023).",
            ),
            (
                "L\n\na Estrategia Nacional de Ciberseguridad 2023-202715 proporciona una visión cohesiva",
                "## 4. MARCO ESTRATÉGICO\n\nLa Estrategia Nacional de Ciberseguridad 2023-202715 proporciona una visión cohesiva",
            ),
            (
                "L a Estrategia Nacional de Ciberseguridad 2023-202715 proporciona una visión cohesiva",
                "## 4. MARCO ESTRATÉGICO\n\nLa Estrategia Nacional de Ciberseguridad 2023-202715 proporciona una visión cohesiva",
            ),
            (
                "Costa Rica establecerá un marco de gobernanza que defina roles,",
                "#### Pilar 1. Reforzar la gobernanza de ciberseguridad\n\nCosta Rica establecerá un marco de gobernanza que defina roles,",
            ),
            (
                "Costa Rica desarrollará legislación y regulación cibernética junto con un marco normativo",
                "#### Pilar 2. Adecuar el marco jurídico cibernético\n\nCosta Rica desarrollará legislación y regulación cibernética junto con un marco normativo",
            ),
            (
                "Costa Rica establecerá un marco de gestión integral de riesgos de ciberseguridad que permita",
                "#### Pilar 3. Fortalecer la protección de infraestructuras y la ciber resiliencia nacional\n\nCosta Rica establecerá un marco de gestión integral de riesgos de ciberseguridad que permita",
            ),
            (
                "Costa Rica desarrollará una fuerza laboral capacitada en ciberseguridad a través de programas",
                "#### Pilar 4. Reforzar las capacidades del ecosistema de ciberseguridad\n\nCosta Rica desarrollará una fuerza laboral capacitada en ciberseguridad a través de programas",
            ),
            (
                "Costa Rica impulsará la cooperación nacional e internacional, la colaboración y el intercambio",
                "#### Pilar 5. Cooperar en el entorno digital\n\nCosta Rica impulsará la cooperación nacional e internacional, la colaboración y el intercambio",
            ),
            (
                "C\n\nosta Rica continuará avanzando en su desarrollo y empleará las oportunidades de optimización",
                "## 5. INTERVENCIONES PÚBLICAS\n\nCosta Rica continuará avanzando en su desarrollo y empleará las oportunidades de optimización",
            ),
            (
                "C osta Rica continuará avanzando en su desarrollo y empleará las oportunidades de optimización",
                "## 5. INTERVENCIONES PÚBLICAS\n\nCosta Rica continuará avanzando en su desarrollo y empleará las oportunidades de optimización",
            ),
            (
                "E\n\nl seguimiento a la ejecución física y presupuestal",
                "El seguimiento a la ejecución física y presupuestal",
            ),
            (
                "E l seguimiento a la ejecución física y presupuestal",
                "El seguimiento a la ejecución física y presupuestal",
            ),
            (
                "## PARTICIPACIÓN SOCIAL Y CIUDADANA 7.",
                "## 7. PARTICIPACIÓN SOCIAL Y CIUDADANA",
            ),
            (
                "PARTICIPACIÓN SOCIAL Y CIUDADANA 7.",
                "## 7. PARTICIPACIÓN SOCIAL Y CIUDADANA",
            ),
            (
                "L\n\na construcción de la Estrategia Nacional de Ciberseguridad 2023-2027",
                "La construcción de la Estrategia Nacional de Ciberseguridad 2023-2027",
            ),
            (
                "L a construcción de la Estrategia Nacional de Ciberseguridad 2023-2027",
                "La construcción de la Estrategia Nacional de Ciberseguridad 2023-2027",
            ),
            (
                "## DIVULGACIÓN 8.",
                "## 8. DIVULGACIÓN",
            ),
            (
                "DIVULGACIÓN 8.",
                "## 8. DIVULGACIÓN",
            ),
            (
                "E\n\nn línea con lo dispuesto en el Plan Nacional de Desarrollo",
                "En línea con lo dispuesto en el Plan Nacional de Desarrollo",
            ),
            (
                "E n línea con lo dispuesto en el Plan Nacional de Desarrollo",
                "En línea con lo dispuesto en el Plan Nacional de Desarrollo",
            ),
            (
                "## GLOSARIO 9.",
                "## 9. GLOSARIO",
            ),
            (
                "GLOSARIO 9.",
                "## 9. GLOSARIO",
            ),
            (
                "## REFERENCIAS BIBLIOGRÁFICAS 10.",
                "## 10. REFERENCIAS BIBLIOGRÁFICAS",
            ),
            (
                "REFERENCIAS BIBLIOGRÁFICAS 10.",
                "## 10. REFERENCIAS BIBLIOGRÁFICAS",
            ),
        ]
        for old_s, new_s in _cr_replacements:
            md = md.replace(old_s, new_s, 1)
    # Split inline concatenated Turkish `Eylem N.M_` table cells onto their own lines
    md = re.sub(r"([^\n#])\s+(Eylem\s+\d+\.\d+[_\s:])", r"\1\n\n\2", md)
    raw_lines = md.splitlines()
    # Pre-pass: join standalone section number lines (e.g. `1.`, `2.2.`, `### 5.2.1`) with the immediately following title line
    lines: list[str] = []
    idx = 0
    while idx < len(raw_lines):
        cur = raw_lines[idx].strip()
        if idx > 0 and cur == "#":
            idx += 1
            continue
        if cur.startswith(("[Главная](https://pravo.by/)", "[Карточка документа](https://pravo.by/")):
            idx += 1
            continue
        m_cyr = re.match(
            r"^(#{2,6}\s+)?((?:РАЗДЕЛ|Раздел|РОЗДІЛ|Розділ|ГЛАВА|Глава|ЧАСТЬ|Часть|ЧАСТИНА|Частина|CAP[ÍI]TULO|Cap[íi]tulo)\s+(?:[IVXLCDM]+|\d+))\.?$",
            cur,
        )
        if m_cyr:
            j = idx + 1
            while j < len(raw_lines) and not raw_lines[j].strip():
                j += 1
            if j < len(raw_lines) and j <= idx + 4:
                nxt = raw_lines[j].strip()
                if nxt and not nxt.startswith(("#", "[", "|")) and 3 <= len(nxt) <= 220 and not re.search(r"\.{4,}\s*\d+$", nxt):
                    kw_tok = m_cyr.group(2)
                    lvl = "###" if kw_tok.upper().startswith(("ГЛАВА", "CAP")) else "##"
                    # Check if an uppercase continuation line immediately follows `nxt`
                    k = j + 1
                    while k < len(raw_lines) and not raw_lines[k].strip():
                        k += 1
                    if (
                        k < len(raw_lines)
                        and k <= j + 2
                        and re.match(r"^[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f\s,\-–—\(\)]{3,120}$", raw_lines[k].strip())
                        and not re.match(r"^(?:РАЗДЕЛ|РОЗДІЛ|ГЛАВА|ЧАСТЬ|ЧАСТИНА|CAP[ÍI]TULO)\b", raw_lines[k].strip(), re.I)
                    ):
                        nxt = f"{nxt} {raw_lines[k].strip()}"
                        j = k
                    lines.append(f"{lvl} {kw_tok} — {nxt.rstrip('.')}")
                    idx = j + 1
                    continue
        m_bare = re.match(r"^(#{2,6}\s+)?(\d{1,2}(?:\.\d{1,2})+\.?|\d{1,2}\.|[IVX]{1,4}\.|[A-H]\.)$", cur)
        if m_bare:
            j = idx + 1
            while j < len(raw_lines) and not raw_lines[j].strip():
                j += 1
            if j < len(raw_lines) and j <= idx + 4:
                nxt = raw_lines[j].strip()
                h_pref = (m_bare.group(1) or "").strip()
                num_tok = m_bare.group(2)
                m_nh = re.match(r"^(#{2,6})\s+(.+)$", nxt)
                if m_nh and not re.match(r"^(?:\d|[IVX]+\.)", m_nh.group(2).strip()):
                    eff_h = h_pref or m_nh.group(1)
                    lines.append(f"{eff_h} {num_tok} {m_nh.group(2).strip()}")
                    idx = j + 1
                    continue
                if nxt.startswith("Identifying the Lead Project Authority In line with "):
                    eff_h = h_pref or "###"
                    lines.append(f"{eff_h} {num_tok} Identifying the Lead Project Authority")
                    lines.append("")
                    lines.append(nxt[len("Identifying the Lead Project Authority ") :].strip())
                    idx = j + 1
                    continue
                if nxt.startswith("Handlungsfelder und Massnahmen Bei der Umsetzung "):
                    eff_h = h_pref or "###"
                    lines.append(f"{eff_h} {num_tok} Handlungsfelder und Massnahmen")
                    lines.append("")
                    lines.append(nxt[len("Handlungsfelder und Massnahmen ") :].strip())
                    idx = j + 1
                    continue
                if (
                    nxt
                    and not nxt.startswith(("#", "["))
                    and 3 <= len(nxt) <= 220
                    and (not nxt.endswith(".") or (re.match(r"^\d{1,2}(?:\.\d{1,2})+\.?$", num_tok) and len(nxt) <= 120))
                    and re.match(r"^:?[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f\u0590-\u05ff\u4e00-\u9fff]", nxt)
                ):
                    clean_nxt = nxt.rstrip(".") if nxt.endswith(".") else nxt
                    norm_num_tok = num_tok if num_tok.endswith(".") else f"{num_tok}."
                    if h_pref:
                        lines.append(f"{h_pref} {norm_num_tok} {clean_nxt}")
                    else:
                        lines.append(f"{norm_num_tok} {clean_nxt}")
                    idx = j + 1
                    continue
        lines.append(raw_lines[idx])
        idx += 1

    # Detect Table of Contents block (e.g. `Contents`, `Table of contents`, `Índice`, `Sumario`)
    def _norm_toc_line(s: str) -> str:
        s = re.sub(r"^#+\s*", "", s.strip())
        s = re.sub(r"[\.\s]+\d{1,3}$", "", s).strip()
        return s.lower()

    toc_skip_indices: set[int] = set()
    for i, l in enumerate(lines[:95]):
        low_tok = re.sub(r"^#+\s*", "", l.strip()).lower().rstrip(":")
        if low_tok in (
            "contents",
            "table of contents",
            "tabla de contenido",
            "tabla de contenidos",
            "índice",
            "indice",
            "sumario",
            "summay",
            "inhalt",
            "inhaltsverzeichnis",
            "sommaire",
            "table des matières",
            "目录",
        ):
            first_entry = ""
            first_idx = -1
            for j in range(i + 1, min(i + 18, len(lines))):
                cand_e = _norm_toc_line(lines[j])
                if len(cand_e) >= 4 and not cand_e.startswith("[") and not cand_e.isdigit():
                    first_entry = cand_e.split(" capítulo ")[0].strip()
                    first_idx = j
                    break
            if first_entry:
                for k in range(first_idx + 2, min(first_idx + 180, len(lines))):
                    cand_k = _norm_toc_line(lines[k])
                    if cand_k == first_entry or (len(first_entry) >= 12 and cand_k.startswith(first_entry[:24])):
                        toc_skip_indices.update(range(i, k))
                        for idx_t in range(i, k):
                            if lines[idx_t].lstrip().startswith("#"):
                                lines[idx_t] = re.sub(r"^#+\s*", "", lines[idx_t].strip())
                        break
            break

    has_part_or_chapter_structure = any(
        re.match(r"^(?:#{2,6}\s+)?(?:РАЗДЕЛ|Раздел|РОЗДІЛ|Розділ|ГЛАВА|Глава|CAP[ÍI]TULO|Capítulo)\s+(?:[IVXLCDM]+|\d+)\b", l.strip())
        for idx_l, l in enumerate(lines)
        if idx_l not in toc_skip_indices
    )

    h2_plus = [l for l in lines if re.match(r"^#{2,6}\s+\S+", l)]
    numbered_h2 = [
        l
        for l in h2_plus
        if re.match(
            r"^#{2,6}\s+(?:(?:CHAPTER|PART|SECTION|PILLAR|GOAL|OBJECTIVE|PRIORITY|ANNEX|APPENDIX|BAHAGIAN|제\s*\d+\s*[장절편]|第[一二三四五六七八九十百0-9０-９]+[章节篇编部節編])\b|(?:\d{1,2}(?:\.\d{1,2})*|[IVXLCDM]{1,5}|[A-H])[\.\)\s-]|[一二三四五六七八九十壹貳參肆伍陸柒捌玖拾ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[、．\.]|[（\(][一二三四五六七八九十0-9]+[）\)])",
            l,
            re.IGNORECASE,
        )
    ]
    if (len(h2_plus) >= 6 or len(numbered_h2) >= 2) and not is_annex:
        # Even when headings exist, promote unformatted all-caps major headings (`II. THINKING...`, `1. INTRODUCTION`),
        # explicit part/chapter headers (`РАЗДЕЛ I ...`, `ГЛАВА 1 ...`, `CAPÍTULO 1`), and explicit multi-dot subheadings (`1.1. Context`).
        patched_lines: list[str] = []
        for idx_l, l in enumerate(lines):
            s = re.sub(r"^\*\*(.+?)\*\*$", r"\1", l.strip()).strip()
            s = re.sub(r"^(Eylem\s+\d+\.\d+)_+\s*", r"\1: ", s)
            if idx_l not in toc_skip_indices and not s.startswith("#"):
                if re.match(r"^Eylem\s+\d+\.\d+:\s+\S", s):
                    patched_lines.append(f"### {s.rstrip('.')}")
                    continue
                if re.match(r"^[一二三四五六七八九十]+[、．\.]\s*[^。；\n]{2,50}$", s):
                    patched_lines.append(f"## {s}")
                    continue
                if re.match(r"^[（\(][一二三四五六七八九十0-9]+[）\)]\s*[^；\n]{2,50}。?$", s):
                    patched_lines.append(f"### {s.rstrip('。')}")
                    continue
                if re.match(r"^(?:\d+\s*-\s*)?ИЛОВА$", s):
                    patched_lines.append(f"## {s}")
                    continue
                if re.match(r"^(?:[IVXLCDM]+|\d+)\s*-\s*(?i:боб|бўлим|параграф|bob|bo['ʻ’]lim)\.?\s+\S.{1,160}$", s):
                    patched_lines.append(f"### {s.rstrip('.')}")
                    continue
                if not has_part_or_chapter_structure and re.match(
                    r"^(?:[IVX]{1,4}|\d{1,2})\.\s+[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f]{2,}[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f0-9\s,\-–—'’\(\)/]{2,180}$",
                    s,
                ):
                    patched_lines.append(f"## {s}")
                    continue
                if re.match(
                    r"^(?:РАЗДЕЛ|Раздел|РОЗДІЛ|Розділ|ЧАСТЬ|Часть|ЧАСТИНА|Частина|PART|PARTIE|PARTE|TEIL)\s+(?:[IVXLCDM]+|\d+)\b.{0,180}$",
                    s,
                ):
                    patched_lines.append(f"## {s.rstrip('.')}")
                    continue
                if re.match(
                    r"^(?:ГЛАВА|Глава|CAP[ÍI]TULO|CAPITOLO|CHAPTER|CHAPITRE|KAPITEL)\s+(?:[IVXLCDM]+|\d+)\b.{0,180}$",
                    s,
                ):
                    patched_lines.append(f"### {s.rstrip('.')}")
                    continue
                if re.match(r"^(?:Strategic\s+)?Priority\s+\d+\b.{0,140}$", s):
                    patched_lines.append(f"## {s.rstrip('.')}")
                    continue
                if re.match(r"^(?:Strategic\s+)?Objective\s+\d+\.\d+\.?\s+[A-Z].{2,160}$", s):
                    patched_lines.append(f"### {s.rstrip('.')}")
                    continue
                if re.match(r"^\d{1,2}\.\d{1,2}(?:\.\d{1,2})*\.?\s+:?[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f\u0590-\u05ff\u4e00-\u9fff][^\n\.]{2,140}$", s):
                    patched_lines.append(f"### {s}")
                    continue
            patched_lines.append(l)
        return "\n".join(patched_lines) + "\n"

    promoted_lines: list[str] = []
    promoted_count = 0
    in_appendix = False
    has_roman_parts = any(
        re.match(r"^[IVX]{1,4}\.\s*[A-Za-z]", l.strip())
        for idx_l, l in enumerate(lines)
        if idx_l not in toc_skip_indices
    )
    heading_pat = re.compile(
        r"^(?:"
        r"(?i:CHAPTER|PART|SECTION|PILLAR|GOAL|OBJECTIVE|PRIORITY|ANNEX|APPENDIX|KAPITEL|TEIL|CHAPITRE|PARTIE|CAPITOLO|CAP[ÍI]TULO|PARTE|BAHAGIAN|ART[ÍI]CULO|ĐIỀU|L[ÍI]NEA\s+ESTRAT[ÉE]GICA|РАЗДЕЛ|РОЗДІЛ|ГЛАВА|ЧАСТЬ|ЧАСТИНА)\s+(?:[IVXLCDM]+|\d+(?:\.\d+)*|[A-Z])\b.*"
        r"|(?:[IVXLCDM]+|\d+)\s*-\s*(?i:боб|бўлим|параграф|ИЛОВА|bob|bo['ʻ’]lim)\.?\s*.{0,180}"
        r"|ИЛОВА|PHỤ\s+LỤC"
        r"|Eylem\s+\d+\.\d+[_\s:].*"
        r"|(?:[IVXLCDM]{1,5}|\d{1,2}(?:\.\d{1,2}){0,2})[\.\)]\s*:?[A-Za-zÄÖÜÉÈÊÀÁÍÓÚÑ\u0400-\u04ff\u0590-\u05ff\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af].{2,220}"
        r"|[A-H]\.\s*[A-Z][A-Za-z0-9\s,\-–—'’\(\)/:;\.]{2,220}"
        r"|[IVX]{1,4}\s+[A-Z][A-Za-z0-9\s,\-–—'’\(\)/]{2,90}"
        r"|第[一二三四五六七八九十百0-9０-９]+[章节篇编部節編]\s*.{1,80}"
        r"|[一二三四五六七八九十]+[、．\.]\s*.{2,80}"
        r"|[（\(][一二三四五六七八九十0-9]+[）\)]\s*.{2,80}"
        r"|[壹貳參肆伍陸柒捌玖拾]+[、．\.]\s*.{2,80}"
        r"|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[\.\s、．]\s*.{2,80}"
        r"|제\s*\d+\s*[장절편]\s*.{1,80}"
        r"|前言|目录|结束语|结语|Global AI Governance Initiative"
        r"|Executive Summary|Foreword|Preface|Introduction|Conclusion|Conclusions:?|Overview|Background|Strategic Context|Vision|Implementation|Governance|Abbreviations|Definitions"
        r"|Introduction:\s+.{5,140}"
        r"|IT threat assessment|Framework conditions|Basic principles.*|Strategic objectives and measures|Sustainable implementation"
        r")$"
    )
    explicit_sec_prefix_re = re.compile(
        r"^(?:[A-H]\.\s*[A-Z]|Eylem\s+\d+\.\d+|(?:[IVXLCDM]+|\d+)\s*-\s*(?i:боб|бўлим|параграф|ИЛОВА|bob|bo['ʻ’]lim)|(?i:CHAPTER|PART|SECTION|ANNEX|APPENDIX|CAP[ÍI]TULO|BAHAGIAN|ART[ÍI]CULO|L[ÍI]NEA\s+ESTRAT[ÉE]GICA|РАЗДЕЛ|РОЗДІЛ|ГЛАВА)\s+(?:[IVXLCDM]+|\d+))\b"
    )
    for idx_l, line in enumerate(lines):
        if idx_l in toc_skip_indices:
            promoted_lines.append(line)
            continue
        s = re.sub(r"^\*\*(.+?)\*\*$", r"\1", line.strip()).strip()
        if re.match(r"^[（\(][一二三四五六七八九十0-9]+[）\)]\s*[^。；\n]{2,50}。$", s):
            s = s.rstrip("。")
        s = re.sub(r"^(Eylem\s+\d+\.\d+)_+\s*", r"\1: ", s)
        # Normalize missing space after Appendix/Annex/Chapter/Part/Section number (e.g. `Appendix 2Analysis...` -> `Appendix 2: Analysis...`)
        s = re.sub(
            r"^((?i:Appendix|Annex|Chapter|Part|Section)\s+(?:[IVXLCDM]+|\d+))([A-ZÄÖÜÉÈÊÀÁÍÓÚÑ])",
            r"\1: \2",
            s,
        )
        allow_trailing_dot = bool(explicit_sec_prefix_re.match(s))
        max_len = 360 if allow_trailing_dot else 230
        if has_part_or_chapter_structure and re.match(r"^\d{1,2}\.\s+", s):
            promoted_lines.append(line)
            continue
        if (
            not s.startswith("#")
            and 3 <= len(s) <= max_len
            and not s.endswith((";", "。", "；", "-"))
            and (not s.endswith(":") or re.match(r"^(?:Introduction|Conclusions?):", s, re.I))
            and (allow_trailing_dot or not s.endswith("."))
            and not re.search(r"\b2\.\s*\S+.*\b3\.", s)
            and heading_pat.match(s)
        ):
            # Ensure a space after leading number/Roman/letter dot (e.g., `1.Introduction` -> `1. Introduction`)
            s_norm = re.sub(
                r"^((?:\d{1,2}(?:\.\d{1,2})*|[IVXLCDM]{1,5}|[A-H])\.)([A-Za-zÄÖÜÉÈÊÀÁÍÓÚÑ\u0400-\u04ff\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af])",
                r"\1 \2",
                s,
            )
            if allow_trailing_dot and s_norm.endswith("."):
                s_norm = s_norm.rstrip(".")
            if re.match(r"^Appendix\s+\d+\b", s_norm, re.IGNORECASE):
                in_appendix = True
            m_sub = re.match(
                r"^(?:(\d{1,2}(?:\.\d{1,2})+)\.|(?i:ГЛАВА|Глава|CAP[ÍI]TULO)\s+\d+|Eylem\s+\d+\.\d+|[（\(][一二三四五六七八九十0-9]+[）\)]|第[一二三四五六七八九十百0-9０-９]+[节節]|\d+\s*-\s*(?i:боб|параграф|bob))",
                s_norm,
            )
            m_single_num = re.match(r"^(\d{1,2})\.\s+(.+)$", s_norm)
            if is_annex:
                if m_single_num and in_appendix:
                    # Inside an Appendix of an Annex, emit unnumbered subsection heading to avoid colliding with main doc section numbers
                    promoted_lines.append(f"#### {m_single_num.group(2)}")
                elif m_single_num and has_roman_parts:
                    promoted_lines.append(f"#### Chapter {m_single_num.group(1)}: {m_single_num.group(2)}")
                elif m_sub:
                    sub_hashes = "#####" if has_roman_parts else "####"
                    promoted_lines.append(f"{sub_hashes} {s_norm}")
                else:
                    promoted_lines.append(f"### {s_norm}")
            else:
                prefix = "###" if m_sub else "##"
                promoted_lines.append(f"{prefix} {s_norm}")
            promoted_count += 1
        else:
            promoted_lines.append(line)

    if promoted_count >= 1:
        return "\n".join(promoted_lines) + "\n"
    return "\n".join(lines) + "\n"


_COLOPHON_HEADING_RE = re.compile(
    r"^(?:"
    r"Published\s+(?:in|by)\b"
    r"|©"
    r"|Copyright\b"
    r"|ISBN\b"
    r"|ISSN\b"
    r"|Command\s+Paper\b"
    r"|CP\s+\d+"
    r"|Presented\s+to\s+Parliament\b"
    r"|by\s+Command\s+of\b"
    r"|by\s+the\s+Secretary\s+of\s+State\b"
    r"|This\s+publication\s+is\s+(?:licensed|available)\b"
    r"|Where\s+we\s+have\s+identified\b"
    r"|Any\s+enquiries\s+regarding\b"
    r"|Printed\s+(?:in|on|by)\b"
    r"|\(?(?:Provisional|Tentative)\s+translation\)?"
    r"|Status:\s+"
    r"|E\d{6,}\b"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$"
    r"|\d{1,4}$"
    r"|\d{1,3}\s+(?:QUADRILLION|TRILLION|BILLION|MILLION|THOUSAND|PERCENT)\b"
    r"|¡¡\s+|US\$\d+|0?\d+%\s+OF\s+THE|ICT/BPO\s+OPERATIONS|50\s+INTERNET\s+HAS|BILLION\s+CONNECTIONS|BY\s+2020$|INCREASE\s+TO$|IT\s+IS\s+PREDICTED\s+TO\s+INCREASE\s+TO$|CYBERCRIMES[’']\s+ESTIMATED\s+COST"
    r"|1\.\s+SOCIEDAD\s+Y\s+CIENCIAS\s+SOCIALES"
    r"|A\s+sustainable\s+framework\s+to\s+ensure\s+the\s+availability\s+of\s+human\s+capital"
    r"|\d{1,2}\.\s+We\s+(?:want|will)\b"
    r"|[•●▪▸]\s+"
    r"|https?://"
    r"|\|\s*\S+"
    r"|붙임\s+"
    r"|[“\"«»'‘]"
    r")",
    re.IGNORECASE,
)

_DANGLING_PREP_RE = re.compile(
    r"\b(?:an|a|the|of|for|to|in|on|by|with|and|or|from|into|at|as|through|between|under|over|towards|toward"
    r"|de|du|des|la|le|les|et|en|dans|pour|sur|par|au|aux"
    r"|und|der|die|das|für|von|mit|im|in|zu|zur|zum)$",
    re.IGNORECASE,
)

_BARE_CONTAINER_HEADING_RE = re.compile(
    r"^(?:"
    r"(?:Handlungsfeld|Chapitre|Partie|Objectif\s+stratégique\s+n°|Action|SYSTEM|Pillar|Part|Chapter|Section|Annex|Appendix|Goal|Priority|Principle|Objective)\s+(?:[IVXLCDM]+|\d+[a-z]?|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\s*[\-–—:\.]?"
    r"|#\d+"
    r")$",
    re.IGNORECASE,
)

_LETTERSPACED_HEADING_MAP: dict[str, str] = {
    "NATIONALCYBERSECURITYSTRATEGYIV": "NATIONAL CYBERSECURITY STRATEGY IV",
    "TABLEOFCONTENTS": "TABLE OF CONTENTS",
    "INTRODUCTION": "INTRODUCTION",
    "II.NATIONALCYBERSECURITYSTRATEGYIV(2021-2025)": "II. NATIONAL CYBERSECURITY STRATEGY IV (2021-2025)",
    "1.OBJECTIVESANDPRIORITIESOFTHENCSSIV": "1. OBJECTIVES AND PRIORITIES OF THE NCSS IV",
    "STRATEGICOBJECTIVES:": "STRATEGIC OBJECTIVES:",
    "1.1OBJECTIVEI:BUILDINGTRUSTINTHEDIGITALWORLDANDPROTECTIONOFHUMANRIGHTSONLINE": "1.1 OBJECTIVE I: BUILDING TRUST IN THE DIGITAL WORLD AND PROTECTION OF HUMAN RIGHTS ONLINE",
    "1.2OBJECTIVEII:STRENGTHENINGTHESECURITYANDRESILIENCEOFDIGITALINFRASTRUCTURESINLUXEMBOURG": "1.2 OBJECTIVE II: STRENGTHENING THE SECURITY AND RESILIENCE OF DIGITAL INFRASTRUCTURES IN LUXEMBOURG",
    "1.3OBJECTIVEIII:DEVELOPINGARELIABLE,SUSTAINABLEANDSECUREDITIGALECONOMY": "1.3 OBJECTIVE III: DEVELOPING A RELIABLE, SUSTAINABLE AND SECURE DIGITAL ECONOMY",
    "1.3OBJECTIVEIII:DEVELOPINGARELIABLE,SUSTAINABLEANDSECUREDIGITALECONOMY": "1.3 OBJECTIVE III: DEVELOPING A RELIABLE, SUSTAINABLE AND SECURE DIGITAL ECONOMY",
    "2.NATIONALCYBERSECURITYGOVERNANCEFRAMEWORK": "2. NATIONAL CYBERSECURITY GOVERNANCE FRAMEWORK",
    "3.PREPAREDNESS,RESPONSEANDRECOVERYMEASURES": "3. PREPAREDNESS, RESPONSE AND RECOVERY MEASURES",
    "4.EDUCATION,TRAININGANDAWARENESSPROGRAMMES": "4. EDUCATION, TRAINING AND AWARENESS PROGRAMMES",
    "5.RESEARCHANDDEVELOPMENTPLANS": "5. RESEARCH AND DEVELOPMENT PLANS",
    "5.1UNIVERSITYOFLUXEMBOURG:INTERDISCIPLINARYCENTREFORSECURITY,RELIABILITYANDTRUST(SNT)": "5.1 UNIVERSITY OF LUXEMBOURG: INTERDISCIPLINARY CENTRE FOR SECURITY, RELIABILITY AND TRUST (SNT)",
    "KEYFIGURES": "KEY FIGURES",
    "STRATEGICRESEARCHAREAS": "STRATEGIC RESEARCH AREAS",
    "PARTNERSHIPPROGRAMME": "PARTNERSHIP PROGRAMME",
    "RESEARCHGROUPS": "RESEARCH GROUPS",
    "5.2LUXEMBOURGINSTITUTEOFSCIENCEANDTECHNOLOGY(LIST)": "5.2 LUXEMBOURG INSTITUTE OF SCIENCE AND TECHNOLOGY (LIST)",
    "RESEARCHAREAS": "RESEARCH AREAS",
    "RESEARCHAREASDATASECURITYANDDATAPRIVACY": "RESEARCH AREAS: DATA SECURITY AND DATA PRIVACY",
    "DATASECURITYANDDATAPRIVACY": "DATA SECURITY AND DATA PRIVACY",
    "CYBERSYSTEMSECURITYANDRESILIENCE": "CYBER SYSTEM SECURITY AND RESILIENCE",
    "PROJECTSANDPARTNERS": "PROJECTS AND PARTNERS",
    "PROJECTS:": "PROJECTS:",
    "PARTNERS:": "PARTNERS:",
    "III.EVALUATIONANDEXPERIENCESOFTHENCSSIII": "III. EVALUATION AND EXPERIENCES OF THE NCSS III",
    "IV.ACTIONPLAN(NON-PUBLIC)": "IV. ACTION PLAN (NON-PUBLIC)",
    "GLOSSARY": "GLOSSARY",
}


def postprocess_markdown_structure(md: str, doc_title: str) -> str:
    """Clean up PDF/XHTML heading artifacts so every heading represents a genuine section with body prose
    or child sections, without colophon headings, split sentences, or reversed banner titles.
    """
    from parse_regulatory_sections import parse_heading

    md = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]+", " ", md)
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    blocks: list[str] = []
    has_titled_pijler = any(re.search(r"^#{2,6}\s+Pijler\s+[IVX]+:\s+\S", b, re.M) for b in raw_blocks)
    for b in raw_blocks:
        # Split Dutch strategy chapter headings where the chapter lead paragraph was concatenated onto the heading line
        m_nl_lead = re.match(
            r"^(#{2,6}\s+(?:1\.\s+Maatschappelijke opgave cybersecurity|2\.\s+Visie:\s+Digitale veiligheid voor iedereen een vanzelfsprekendheid|3\.\s+Doelen|Inleiding en context))\s+((?:Dit hoofdstuk|De visie|Om de visie|Met de Nederlandse)\b[\s\S]+)$",
            b,
        )
        if m_nl_lead:
            blocks.append(m_nl_lead.group(1).strip())
            blocks.append(m_nl_lead.group(2).strip())
            continue
        if has_titled_pijler and re.match(r"^#{2,6}\s+Pijler\s+[IVX]+\s*$", b):
            blocks.append(re.sub(r"^#{2,6}\s+", "", b))
            continue
        if has_titled_pijler and re.match(r"^##\s+Pijler\s+[IVX]+:\s+\S", b):
            blocks.append("#" + b)
            continue
        # Split any block that contains multiple lines where at least one line is a `#` heading
        if "\n" in b and any(l.strip().startswith("#") for l in b.splitlines()):
            cur_buf: list[str] = []
            for l in b.splitlines():
                if l.strip().startswith("#"):
                    if cur_buf:
                        blocks.append("\n".join(cur_buf))
                        cur_buf = []
                    blocks.append(l.strip())
                else:
                    cur_buf.append(l)
            if cur_buf:
                blocks.append("\n".join(cur_buf))
        else:
            blocks.append(b)

    # Strip trailing CMS "related links / social footer" sections
    for idx_b, b in enumerate(blocks):
        if re.match(
            r"^#{2,6}\s+(?:Aller plus loin|Ceci pourrait vous intéresser|Suivez-nous sur les réseaux sociaux|Related links|See also)\b",
            b,
            re.IGNORECASE,
        ):
            blocks = blocks[:idx_b]
            break

    # Pass 1: Normalize interior `# ` headings to `## ` and demote colophon/imprint/copyright/quote/date lines
    has_part_ii_container = any(
        "NATIONALCYBERSECURITYSTRATEGYIV(2021-2025)" in re.sub(r"\s+", "", blk)
        for blk in blocks
    )
    for i, b in enumerate(blocks):
        if i > 0 and re.match(r"^#\s+\S", b):
            b = "#" + b
            blocks[i] = b
        m = re.match(r"^(#{2,6})\s+(.+?)\s*$", b)
        if not m:
            continue
        hashes = m.group(1)
        txt = m.group(2).strip()
        txt = re.sub(r"\bS\s+E\s+C\s+T\s+I\s+O\s+N\s+(\d+)\b", r"Section \1", txt, flags=re.IGNORECASE)
        txt = re.sub(r"^I\s+N\s+T\s+E\s+L\s+L\s+I\s+G\s+E\s+N\s+C\s+E\s+S\s+T\s+R\s+A\s+T\s+E\s+G\s+Y\s*(?:[—–-]\s*)?", "", txt).strip()
        txt = re.sub(r"^(\d{1,3}(?:\.\d{1,3})*\.)([A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f])", r"\1 \2", txt)
        nospace_key = re.sub(r"\s+", "", txt)
        if nospace_key in _LETTERSPACED_HEADING_MAP:
            txt = _LETTERSPACED_HEADING_MAP[nospace_key]
        if txt in (
            "STRATEGIC OBJECTIVES:",
            "KEY FIGURES",
            "PROJECTS:",
            "PARTNERS:",
            "II. Consolidating the security and resilience of digital infrastructures in Luxembourg",
            "III. Developing of a reliable, sustainable and secure digital economy",
        ) or re.match(r"^(?:365\s+workforce|56\s+partners|43%\s+of\s+Doctoral)\b", txt, re.I):
            blocks[i] = txt
            continue
        if not txt or re.match(
            r"^(?:\d{1,3}\s+(?:National\s+(?:Cyber\s*security|Security|Defence|Defense|AI|Artificial\s+Intelligence)\s+Strategy|Estrategia\s+(?:Nacional|de\s+Seguridad))\b.*|Prime\s+Minister[’']s\s+OfficeIntroduction|DE\s+CIBERSEGURIDAD|NATIONAL\s+CYBERSECURITY\s+—\s+STRATEGY)$",
            txt,
            re.IGNORECASE,
        ):
            blocks[i] = ""
            continue
        # Deduplicate repeated `<Title> <Title>` after `Chapter N:` or `Capítulo N:`
        m_dup_ch = re.match(r"^((?:Cap[íi]tulo|Chapter)\s+\d+:\s+)(.+)$", txt, re.IGNORECASE)
        if m_dup_ch:
            ch_pref, ch_rest = m_dup_ch.group(1), re.sub(r"\s+—\s+", " ", m_dup_ch.group(2).strip())
            words_r = ch_rest.split()
            if len(words_r) >= 4 and len(words_r) % 2 == 0:
                half = len(words_r) // 2
                if " ".join(words_r[:half]).lower() == " ".join(words_r[half:]).lower():
                    txt = f"{ch_pref}{' '.join(words_r[:half])}"
            hashes = "##"
        elif re.match(r"^(?:Cap[íi]tulo|Chapter)\s+\d+\b", txt, re.IGNORECASE):
            hashes = "##"
        elif re.match(r"^(?:Objetivo\s+[IVX]+|Goal\s+[IVX]+|L[ÍI]NEA\s+DE\s+ACCI[ÓO]N\s+\d+|LINE\s+OF\s+ACTION\s+\d+)\b", txt, re.IGNORECASE):
            hashes = "###"
        elif txt in (
            "1. OBJECTIVES AND PRIORITIES OF THE NCSS IV",
            "2. NATIONAL CYBERSECURITY GOVERNANCE FRAMEWORK",
            "3. PREPAREDNESS, RESPONSE AND RECOVERY MEASURES",
            "4. EDUCATION, TRAINING AND AWARENESS PROGRAMMES",
            "5. RESEARCH AND DEVELOPMENT PLANS",
        ):
            hashes = "###"
        elif re.match(r"^[IVX]{1,3}\.\d{1,2}\s+[A-Z]{2,}", txt):
            hashes = "#####"
        elif txt in ("STRATEGIC RESEARCH AREAS", "PARTNERSHIP PROGRAMME", "RESEARCH GROUPS", "RESEARCH AREAS: DATA SECURITY AND DATA PRIVACY", "CYBER SYSTEM SECURITY AND RESILIENCE", "PROJECTS AND PARTNERS"):
            hashes = "#####"
        sec_id, _, _ = parse_heading(txt)
        if re.match(r"^\d{1,2}(?:\.\d{1,2})+\b", sec_id):
            min_dotted_depth = min(6, sec_id.count(".") + (3 if has_part_ii_container else 2))
            if len(hashes) < min_dotted_depth:
                hashes = "#" * min_dotted_depth
        blocks[i] = f"{hashes} {txt}"
        if _COLOPHON_HEADING_RE.search(txt) or re.match(r"^(?:Table\s+of\s+Contents|Contents)\s*$", txt, re.I):
            blocks[i] = txt
            continue
        if re.search(r"\s{2,}\d{1,3}$", txt) or re.match(r"^\d{1,2}\.\d{1,2}\s+[A-Z].+\s+\d{1,2}$", txt):
            blocks[i] = txt
            continue
        if not sec_id and re.match(r"^(?:This\s+chapter\s+|En\s+este\s+cap[íi]tulo\s+|Este\s+cap[íi]tulo\s+)", txt, re.I):
            blocks[i] = txt
            continue
        if not sec_id and txt[0].islower():
            blocks[i] = txt
            continue
        if not sec_id and re.match(r"^[A-ZÀ-ÖØ-ÞĀ-ŽА-ЯЁ]{1,4}\.?$", txt):
            blocks[i] = txt
            continue
        if not sec_id and (len(txt) > 140 or txt.endswith((",", ";"))):
            blocks[i] = txt
            continue
        if re.match(r"^\d{1,2}[\.\)]\s+", txt) and txt.endswith(":"):
            blocks[i] = txt
            continue
        if not sec_id and txt.endswith(".") and not re.search(r"\b(?:U\.S|U\.K|E\.U|Inc|Ltd|Co|Dr|Mr|Ms|St|etc)\.$", txt):
            blocks[i] = txt
            continue
        if not sec_id and re.search(r"[a-z]\.\s+[A-Z][a-z]+\s+[a-z]+", txt):
            blocks[i] = txt

    # Pass 2: Merge split headings (dangling prepositions) and demote unnumbered headings followed by lowercase continuation
    blocks = [b for b in blocks if b.strip()]
    merged: list[str] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.startswith("Capítulo 5: La ciberseguridad en el") and i + 1 < len(blocks) and "Sistema de Seguridad" in blocks[i + 1]:
            merged.append("## Capítulo 5: La ciberseguridad en el Sistema de Seguridad Nacional")
            i += 2
            continue
        if b == "LÍNEA DE ACCIÓN 2" and i + 1 < len(blocks) and blocks[i + 1].startswith("### Garantizar la seguridad"):
            merged.append("### LÍNEA DE ACCIÓN 2")
            blocks[i + 1] = re.sub(r"^#+\s*", "", blocks[i + 1]).strip()
            i += 1
            continue
        if re.match(r"^\d{1,2}(?:\.\d{1,2})+\.$", b) and i + 1 < len(blocks):
            nxt = blocks[i + 1].strip()
            if (
                "\n" not in nxt
                and not nxt.startswith(("#", "["))
                and 3 <= len(nxt) <= 120
                and re.match(r"^[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ]", nxt)
            ):
                lvl = min(6, b.rstrip(".").count(".") + 2)
                merged.append(f"{'#' * lvl} {b} {nxt.rstrip('.')}")
                i += 2
                continue
        m = re.match(r"^(#{2,6})\s+(.+?)\s*$", b)
        if m and i + 1 < len(blocks):
            hashes, txt = m.group(1), m.group(2).strip()
            nxt = blocks[i + 1].strip()
            sec_id, _, _ = parse_heading(txt)
            # Bare `## Capítulo N` / `## Chapter N` followed by a short plain-text chapter title block
            if (
                re.match(r"^(?:Cap[íi]tulo|Chapter)\s+\d+$", txt, re.IGNORECASE)
                and not nxt.startswith("#")
                and len(nxt) <= 120
                and not re.match(r"^(?:This\s+chapter\s+|En\s+este\s+cap[íi]tulo\s+|Este\s+cap[íi]tulo\s+)", nxt, re.I)
            ):
                clean_title = re.sub(r"\s+", " ", nxt).strip()
                merged.append(f"## {txt}: {clean_title}")
                if i + 2 < len(blocks):
                    m_dup_h = re.match(r"^#{2,6}\s+(.+?)\s*$", blocks[i + 2].strip())
                    if m_dup_h and m_dup_h.group(1).strip().lower() == clean_title.lower():
                        i += 3
                        continue
                i += 2
                continue
            # Bare dotted/Roman/letter section identifier heading followed by its title block -> merge title into heading
            if re.match(r"^(\d{1,2}(?:\.\d{1,2})+\.?|\d{1,2}\.|[IVX]{1,4}\.|[A-H]\.)$", txt) and not nxt.startswith("#"):
                if nxt.startswith("Identifying the Lead Project Authority In line with "):
                    merged.append(f"{hashes} {txt} Identifying the Lead Project Authority")
                    blocks[i + 1] = nxt[len("Identifying the Lead Project Authority ") :].strip()
                    i += 1
                    continue
                if nxt.startswith("Handlungsfelder und Massnahmen Bei der Umsetzung "):
                    merged.append(f"{hashes} {txt} Handlungsfelder und Massnahmen")
                    blocks[i + 1] = nxt[len("Handlungsfelder und Massnahmen ") :].strip()
                    i += 1
                    continue
                if (
                    "\n" not in nxt
                    and len(nxt) <= 220
                    and (not nxt.endswith(".") or (re.match(r"^\d{1,2}(?:\.\d{1,2})+\.?$", txt) and len(nxt) <= 120))
                    and re.match(r"^:?[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ\u0410-\u042f\u0590-\u05ff\u4e00-\u9fff]", nxt)
                ):
                    clean_nxt = nxt.rstrip(".") if nxt.endswith(".") else nxt
                    merged.append(f"{hashes} {txt} {clean_nxt}")
                    i += 2
                    continue
            if not sec_id and re.match(r"^[\d\s./:–—-]+$", txt):
                merged.append(txt)
                i += 1
                continue
            # Heading followed immediately by a multi-word plain block starting with a lowercase letter -> sentence/word wrap!
            if (
                not nxt.startswith("#")
                and re.match(r"^(?:[a-z]|\d+(?:\.\d+)?\s+[a-z])", nxt)
                and (not sec_id or (len(hashes) >= 3 and re.match(r"^\d{1,2}$", sec_id)))
            ):
                merged.append(f"{txt} {nxt}")
                i += 2
                continue
            # Numbered heading without terminal sentence punctuation followed by a short lowercase wrapped continuation line -> join into heading
            if (
                sec_id
                and not txt.endswith((":", ".", ";", "?", "!"))
                and "list of " not in txt.lower()
                and not nxt.startswith("#")
                and "\n" not in nxt
                and re.match(r"^[a-z]", nxt)
                and not re.match(r"^[a-h]\.\s", nxt)
                and not nxt.endswith(";")
                and len(nxt.split()) <= 10
            ):
                merged.append(f"{hashes} {txt} {nxt}")
                i += 2
                continue
            # Heading ending with a dangling preposition/article followed by a short title phrase -> join into heading
            if (
                _DANGLING_PREP_RE.search(txt)
                and not nxt.startswith("#")
                and "\n" not in nxt
                and len(nxt) <= 85
                and not nxt.endswith((".", ";", ":"))
                and re.match(r"^[A-Za-zÄÖÜÉÈÊÀÁÍÓÚÑ]", nxt)
            ):
                merged.append(f"{hashes} {txt} {nxt}")
                i += 2
                continue
            # Heading followed by a short <=5-word lowercase wrapped title tail immediately before another heading -> join into heading
            if (
                i + 2 < len(blocks)
                and re.match(r"^#{2,6}\s+", blocks[i + 2])
                and not nxt.startswith("#")
                and "\n" not in nxt
                and len(nxt.split()) <= 5
                and not nxt.endswith((".", ";", ":"))
                and re.match(r"^[a-z(]", nxt)
            ):
                merged.append(f"{hashes} {txt} {nxt}")
                i += 2
                continue
        merged.append(b)
        i += 1
    blocks = merged

    # Pass 3: Fix reversed `<Title>` + `## Section N` pairs (e.g., Taiwan QDR 2025)
    fixed_rev: list[str] = []
    i = 0
    has_reversed_sections = False
    while i < len(blocks):
        m1 = re.match(r"^(#{2,6})\s+(.+?)\s*$", blocks[i])
        if m1 and i + 1 < len(blocks):
            m2 = re.match(r"^(#{2,6})\s+(Section\s+\d+)\s*$", blocks[i + 1], re.IGNORECASE)
            if m2 and parse_heading(m1.group(2))[0] == "":
                fixed_rev.append(f"### {m2.group(2)}: {m1.group(2).strip()}")
                has_reversed_sections = True
                i += 2
                continue
        fixed_rev.append(blocks[i])
        i += 1
    if has_reversed_sections:
        # Shift child `### 1. ...` headings under `### Section N: ...` to `#### 1. ...`
        in_sec = False
        for idx_b, b in enumerate(fixed_rev):
            if re.match(r"^###\s+Section\s+\d+:", b, re.IGNORECASE):
                in_sec = True
            elif re.match(r"^##\s+", b):
                in_sec = False
            elif in_sec and re.match(r"^###\s+\d{1,2}\.\s+", b):
                fixed_rev[idx_b] = "#" + b
    blocks = fixed_rev

    # Pass 3b: Demote single-number headings inside a Figure diagram block (e.g. ITU NCS Guide 2025 Figure 4)
    in_figure_callout = False
    for idx_b, b in enumerate(blocks):
        if re.match(r"^Figure\s+\d+\s*[-–—:]", b, re.I):
            in_figure_callout = True
        elif in_figure_callout:
            if re.match(r"^#{2,6}\s+(?:\d{1,2}\.\d{1,2}|Section\s+\d+|Chapter\s+\d+|Part\s+\d+)\b", b, re.I) or "guardrail" in b.lower():
                in_figure_callout = False
            elif not b.startswith("#") and b.endswith(".") and len(b) >= 40:
                in_figure_callout = False
            elif re.match(r"^#{2,6}\s+\d{1,2}\.\s+", b):
                blocks[idx_b] = re.sub(r"^#{2,6}\s+", "", b)

    # Pass 3c: Promote `### Chapter N` / `### Part N` / `### Pillar N` / `### Section N` to `##` when no numbered `##` exists
    if not any(b.startswith("## ") and parse_heading(b[3:].strip())[0] != "" for b in blocks):
        if any(re.match(r"^###\s+(?:Chapter|Part|Pillar|Section)\s+(?:[IVXLCDM]+|\d+)\b", b, re.I) for b in blocks):
            for idx_b, b in enumerate(blocks):
                if re.match(r"^###\s+(?:Chapter|Part|Pillar|Section)\s+(?:[IVXLCDM]+|\d+)\b", b, re.I):
                    blocks[idx_b] = b[1:]  # `### Chapter N` -> `## Chapter N`

    # Pass 4: Merge or resolve consecutive headings that have NO intervening body prose
    changed = True
    while changed:
        changed = False
        new_blocks: list[str] = []
        i = 0
        while i < len(blocks):
            m1 = re.match(r"^(#{2,6})\s+(.+?)\s*$", blocks[i])
            if m1 and i + 1 < len(blocks):
                m2 = re.match(r"^(#{2,6})\s+(.+?)\s*$", blocks[i + 1])
                if m2:
                    h1_hashes, h1_txt = m1.group(1), m1.group(2).strip()
                    h2_hashes, h2_txt = m2.group(1), m2.group(2).strip()
                    id1, name1, kind1 = parse_heading(h1_txt)
                    id2, name2, kind2 = parse_heading(h2_txt)
                    if not id2 and ((id1 and (name1 == id1 or not name1)) or _BARE_CONTAINER_HEADING_RE.match(h1_txt)):
                        clean_h1 = h1_txt.rstrip(" -–—:.")
                        new_blocks.append(f"{h1_hashes} {clean_h1}: {h2_txt}")
                        i += 2
                        changed = True
                        continue
                    if (
                        id1
                        and not id2
                        and h2_txt.upper() not in ("GLOSSARY", "REFERENCES", "BIBLIOGRAPHY", "CONCLUSION", "CONCLUSIONS", "ABBREVIATIONS", "ACRONYMS")
                        and (len(h1_hashes) == len(h2_hashes) or _DANGLING_PREP_RE.search(h1_txt))
                    ):
                        new_blocks.append(f"{h1_hashes} {h1_txt} {h2_txt}")
                        i += 2
                        changed = True
                        continue
                    if not id1 and not id2 and len(h1_hashes) == len(h2_hashes):
                        if (
                            h1_txt.lower() == h2_txt.lower()
                            or h1_txt.lower() == doc_title.lower()
                            or h1_txt.lower() in doc_title.lower()
                        ):
                            i += 1
                            changed = True
                            continue
                        new_blocks.append(f"{h1_hashes} {h1_txt} — {h2_txt}")
                        i += 2
                        changed = True
                        continue
                    if not id1 and len(h1_hashes) >= len(h2_hashes):
                        blocks[i] = h1_txt
                        changed = True
                    elif id1 and id2 and len(h1_hashes) >= len(h2_hashes):
                        if id1.startswith("Eylem ") and len(h1_txt) > 30:
                            pass
                        elif (
                            (
                                kind1 in ("pillar", "part", "chapter", "roman", "annex", "section_word")
                                and kind2 != kind1
                                and len(h1_hashes) == len(h2_hashes)
                            )
                            or id2.startswith(id1 + ".")
                        ) and len(h2_hashes) < 6:
                            blocks[i + 1] = "#" + blocks[i + 1]
                            changed = True
                        else:
                            blocks[i] = h1_txt
                            changed = True
            new_blocks.append(blocks[i])
            i += 1
        blocks = new_blocks

    # Deduplicate any `<Title> <Title>` inside `## Capítulo N: ...` or `## Chapter N: ...` produced by Pass 4
    for idx_b, b in enumerate(blocks):
        m_ch_dup = re.match(r"^(#{2,6}\s+(?:Cap[íi]tulo|Chapter)\s+\d+:\s+)(.+)$", b, re.IGNORECASE)
        if m_ch_dup:
            pref_c, rest_c = m_ch_dup.group(1), re.sub(r"\s+—\s+", " ", m_ch_dup.group(2).strip())
            w_c = rest_c.split()
            if len(w_c) >= 4 and len(w_c) % 2 == 0:
                h_c = len(w_c) // 2
                if " ".join(w_c[:h_c]).lower() == " ".join(w_c[h_c:]).lower():
                    blocks[idx_b] = f"{pref_c}{' '.join(w_c[:h_c])}"

    # Pass 5: Normalize depth when Roman `### I.`, single-number `### 1.`, and multi-dot `### 1.1` share depth 3 with no numbered `##` parent
    has_numbered_h2 = any(b.startswith("## ") and parse_heading(b[3:].strip())[0] != "" for b in blocks)
    has_h3_roman = any(re.match(r"^###\s+[IVX]{1,4}(?:\.|\s)\s*[A-Z]", b) for b in blocks)
    has_h3_single = any(re.match(r"^###\s+\d{1,2}\.\s+\S", b) for b in blocks)
    has_h3_multi = any(re.match(r"^###\s+\d{1,2}\.\d{1,2}\b", b) for b in blocks)
    if not has_numbered_h2 and has_h3_roman and has_h3_single and has_h3_multi:
        for i, b in enumerate(blocks):
            m_rom = re.match(r"^###\s+([IVX]{1,4})\.?\s+([A-Z].*)$", b)
            if m_rom:
                blocks[i] = f"## {m_rom.group(1)}. {m_rom.group(2)}"
            elif re.match(r"^###\s+\d{1,2}\.\d{1,2}\b", b):
                blocks[i] = "#" + b  # `### 1.1` -> `#### 1.1`
    elif not has_numbered_h2 and has_h3_single and has_h3_multi:
        for i, b in enumerate(blocks):
            if re.match(r"^###\s+\d{1,2}\.\s+\S", b):
                blocks[i] = b[1:]  # `### 1.` -> `## 1.`

    # Pass 5b: Keep unnumbered subsections nested at `###` inside `## Chapter` / `## Part` / `## Pillar` containers

    in_h2_container = False
    for i, b in enumerate(blocks):
        m_h2 = re.match(r"^##\s+(.+?)\s*$", b)
        if not m_h2:
            continue
        h2_txt = m_h2.group(1).strip()
        h2_id, _, h2_kind = parse_heading(h2_txt)
        if h2_kind in ("chapter", "part", "pillar", "annex"):
            in_h2_container = True
        elif h2_id:
            in_h2_container = False
        elif in_h2_container:
            if re.match(r"^(?:Conclusion|Conclusions|Glossary|Abbreviations|Acknowledgements|References|Bibliography)\b", h2_txt, re.I):
                in_h2_container = False
            else:
                blocks[i] = "#" + b  # `## <unnumbered>` -> `### <unnumbered>` under active `## Chapter/Part/Pillar`

    # Pass 6: Demote any remaining leaf heading with empty body or trivial <=3-word page-number/date/bullet body
    changed_leaf = True
    while changed_leaf:
        changed_leaf = False
        heading_indices = [idx_b for idx_b, b in enumerate(blocks) if re.match(r"^#{1,6}\s+", b)]
        for pos, h_idx in enumerate(heading_indices):
            m_h = re.match(r"^(#{2,6})\s+(.+?)\s*$", blocks[h_idx])
            if not m_h:
                continue
            cur_depth = len(m_h.group(1))
            cur_txt = m_h.group(2).strip()
            cur_id, _, _ = parse_heading(cur_txt)
            next_h_idx = heading_indices[pos + 1] if pos + 1 < len(heading_indices) else len(blocks)
            next_depth = 0
            if next_h_idx < len(blocks):
                m_nh = re.match(r"^(#{1,6})\s+", blocks[next_h_idx])
                next_depth = len(m_nh.group(1)) if m_nh else 0
            has_child = next_depth > cur_depth
            body_blocks = blocks[h_idx + 1 : next_h_idx]
            body_str = "\n\n".join(body_blocks).strip()
            if not body_str and not has_child:
                if (cur_id.startswith("Eylem ") and len(cur_txt) > 30) or cur_txt == "IV. ACTION PLAN (NON-PUBLIC)":
                    continue
                blocks[h_idx] = cur_txt
                changed_leaf = True
                break
            if not cur_id and not has_child and body_str:
                cjk_chars = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", body_str)
                latin_words = re.findall(r"[A-Za-z0-9]+", body_str)
                is_trivial_body = (
                    (len(cjk_chars) == 0 and len(latin_words) <= 3)
                    or (len(cjk_chars) <= 3 and len(latin_words) == 0)
                    or bool(re.match(r"^(?:\d{1,3}\s*\|\s*.+|- \[SNS Share\].+)$", body_str))
                )
                if is_trivial_body:
                    blocks[h_idx] = cur_txt
                    changed_leaf = True
                    break

    # Pass 7: Strip letter-spaced TOC block before Foreword and reconnect column-wrapped paragraphs
    fw_idx = next((idx_b for idx_b, b in enumerate(blocks) if b.startswith("· F O R E W O R D O F X AV I E R")), -1)
    if fw_idx > 1:
        end_fw = fw_idx + 1
        if end_fw < len(blocks) and blocks[end_fw].endswith("M E D I A ·"):
            end_fw += 1
        blocks = [blocks[0], "## Foreword by Xavier Bettel, Prime Minister, Minister for Communications and Media"] + blocks[end_fw:]

    merged_blocks: list[str] = []
    idx_m = 0
    while idx_m < len(blocks):
        cur_b = blocks[idx_m].replace(
            "I n i t i a t i v e s /A s s o c i a t i o n s / N e t w o r k s",
            "Initiatives / Associations / Networks",
        )
        if cur_b == "· I N T R O D U C T I O N : M A I N T R E N D S A N D T H R E AT S ·":
            idx_m += 1
            continue
        if (
            idx_m + 1 < len(blocks)
            and not cur_b.startswith("#")
            and not blocks[idx_m + 1].startswith(("#", "•", "- "))
            and not cur_b.endswith((".", ":", ";", "!", "?", ")", '"', "'", "”", "’"))
            and (
                re.match(r"^[a-zà-öø-ÿ]", blocks[idx_m + 1])
                or re.search(r"\b(?:the|a|an|of|in|to|for|with|by|and|or|at|from|as)$", cur_b, re.I)
            )
            and not re.match(r"^[A-Z0-9\s,\-–—\(\)’':;/\.]{2,80}$", blocks[idx_m + 1])
        ):
            nxt_b = blocks[idx_m + 1]
            if re.search(r"[a-zA-Z]-$", cur_b):
                cur_b = cur_b[:-1] + nxt_b
            elif re.search(r"https?://\S*[/._-]$", cur_b):
                cur_b = cur_b + nxt_b
            else:
                cur_b = f"{cur_b} {nxt_b}"
            blocks[idx_m + 1] = cur_b
            idx_m += 1
            continue
        merged_blocks.append(cur_b)
        idx_m += 1

    return "\n\n".join(merged_blocks) + "\n"


def _append_eurlex_cellar_annexes(best_md: str, final_url: str, title: str, desc: str) -> str:
    """If `final_url` is an EUR-Lex Cellar `DOC_1` resource, probe `DOC_2` and `DOC_3` for companion Annexes."""
    m = re.match(r"^(https?://publications\.europa\.eu/resource/cellar/[^/]+)/DOC_1$", final_url)
    if not m:
        return best_md
    base_cellar = m.group(1)
    for doc_idx in (2, 3):
        annex_url = f"{base_cellar}/DOC_{doc_idx}"
        adata, afinal = fetch_url_bytes(annex_url)
        if not adata:
            continue
        is_pdf = adata[:5] == b"%PDF-" or b"%PDF-1." in adata[:1024]
        annex_md = ""
        if is_pdf:
            idx = adata.find(b"%PDF-")
            if idx > 0:
                adata = adata[idx:]
            try:
                amd, _ = pdf_bytes_to_markdown(adata, "Annex")
                # Strip top `# Annex` and repeated `### ANNEX` page headers
                alines = [
                    l
                    for l in amd.splitlines()
                    if not re.match(r"^#\s+Annex\s*$", l.strip(), re.I)
                    and not re.match(r"^#{2,4}\s+ANNEX\s*$", l.strip(), re.I)
                ]
                annex_md = ensure_hierarchical_headings("\n".join(alines), "Annex", desc, is_annex=True)
            except Exception:
                annex_md = ""
        else:
            ahtml = adata.decode("utf-8", errors="ignore")
            if "<html" in ahtml[:1000].lower() or "<?xml" in ahtml[:1000].lower():
                try:
                    amd = html_to_clean_markdown(ahtml, afinal, "Annex")
                    alines = [l for l in amd.splitlines() if not re.match(r"^#\s+Annex\s*$", l.strip(), re.I)]
                    annex_md = ensure_hierarchical_headings("\n".join(alines), "Annex", desc, is_annex=True)
                except Exception:
                    annex_md = ""
        if len(annex_md.strip()) >= 1500:
            best_md = best_md.rstrip() + f"\n\n## Annex I: Coordinated Plan / Action Plan Annex\n\n{annex_md.strip()}\n"
    return best_md


_BLOCKED_HTML_SUBSTRINGS = (
    "nsp.nanet.go.kr",
    "pa.go.kr/research/",
    "president.go.kr",
    "korea.kr/special/policycurationview",
    "msit.go.kr/",
    "nstc.gov.tw",
    "ised-isde.canada.ca/site/ised/en/pan-canadian-artificial-intelligence-strategy",
    "cybersecurity.gov.au/about-us/strategies-and-action-plans",
    "homeaffairs.gov.au",
    "industry.gov.au/science-technology-and-innovation/",
    "industry.gov.au/publications/national-ai-plan",
    "csa.gov.sg/resources/publications/",
    "moda.gov.tw/acs/press/",
    "dpmc.govt.nz/our-programmes/",
    "apo.org.au/node/",
    "ai.gov.gr/wp-content/uploads/2026/10/tn-gia-olous.pdf",
    "gov.si/en/policies/defence-civil-protection-and-public-order/national-security/",
    "samsik.dk",
    "riigikantselei.ee/en/supporting-government",
    "varam.gov.lv/en",
    "gov.pl/web/cyfryzacja/",
    "regeringen.se/rattsliga-dokument/",
    "thedigital.gov.ua",
)


def is_valid_html_strategy_doc(md: str, final_url: str, item: dict) -> bool:
    """Return True only when an HTML extraction is a genuine full-text strategy document,
    rejecting generic homepages, catalog records, and short landing pages.
    """
    low_url = final_url.lower()
    if any(b in low_url for b in _BLOCKED_HTML_SUBSTRINGS):
        return False
    parsed_u = urllib.parse.urlparse(low_url)
    if parsed_u.path.rstrip("/") in ("", "/en", "/fr", "/de", "/es", "/ru", "/uk", "/pl", "/ar", "/zh"):
        return False
    # Official EUR-Lex / Publications Office Cellar XHTML documents and official legal gazette decrees are authoritative full texts
    if any(
        k in low_url
        for k in (
            "publications.europa.eu/resource/cellar/",
            "eur-lex.europa.eu/",
            "pravo.by/document/",
            "zakon.rada.gov.ua/laws/show/",
            "boe.es/",
            "gov.cn/zhengce/",
            "cac.gov.cn/",
            "xinhuanet.com/politics/",
            "lex.uz/docs/",
        )
    ):
        return len(md) >= 2500
    # Require substantial prose and multiple real headings for general HTML strategy pages
    h2_count = sum(1 for l in md.splitlines() if re.match(r"^#{2,4}\s+\S+", l))
    return len(md) >= 25000 and h2_count >= 5


def _decode_html_bytes(data: bytes) -> str:
    """Decode HTML/XML bytes strictly as UTF-8 first, falling back to Windows-1252/ISO-8859-1 so accented Latin characters are preserved."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def fallback_pdf_text_to_markdown(pdf_bytes: bytes, doc_title: str, ocr_lang: str = "eng") -> tuple[str, int]:
    """Fallback text + Tesseract OCR extraction when layout heuristics return sparse text or scanned pages with digital signature overlays."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num_pages = len(doc)
    out = [f"# {doc_title}", ""]
    vn_heading_re = re.compile(
        r"^(?:Điều\s+\d+[\.\:]?\s+\S|[IVX]{1,4}\.\s+[A-ZĐÂĂÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴ]{2,}|\d{1,2}\.\s+[A-ZĐÂĂÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴ]\S+|PHỤ\s+LỤC\b)"
    )
    for page in doc:
        txt = page.get_text("text").strip()
        if (not txt or (ocr_lang == "vie" and len(txt) < 500)) and num_pages <= 120:
            try:
                pix = page.get_pixmap(dpi=300, annots=False)
                res = subprocess.run(
                    ["tesseract", "stdin", "stdout", "-l", ocr_lang, "--psm", "6"],
                    input=pix.tobytes("png"),
                    capture_output=True,
                    timeout=60,
                )
                if res.returncode == 0:
                    ocr_txt = res.stdout.decode("utf-8", errors="ignore").strip()
                    if len(ocr_txt) > len(txt):
                        txt = ocr_txt
            except Exception:
                pass
        if not txt and num_pages <= 120:
            try:
                tp = page.get_textpage_ocr(dpi=150, full=True)
                txt = page.get_text("text", textpage=tp).strip()
            except Exception:
                txt = ""
        if not txt:
            continue
        for raw_line in txt.splitlines():
            clean_l = re.sub(r"\s+", " ", raw_line).strip()
            if not clean_l or re.match(r"^\d{1,3}$", clean_l):
                continue
            if ocr_lang == "vie" and vn_heading_re.match(clean_l):
                out.append("")
                if re.match(r"^(?:Điều\s+\d+|[IVX]{1,4}\.\s+|PHỤ\s+LỤC\b)", clean_l):
                    out.append(f"## {clean_l.rstrip('.')}")
                else:
                    out.append(f"### {clean_l.rstrip('.')}")
                out.append("")
            else:
                out.append(clean_l)
        out.append("")
    return "\n".join(out).strip() + "\n", num_pages


def extract_edition(item: dict) -> dict:
    """Fetch, extract, and structure a single strategy edition, or record honest metadata-only state."""
    ns = item["namespace"]
    name = item["name"]
    ver = item["version"]
    title = item["full_name"]
    desc = item["description"]
    orig_url = item["url"]
    ocr_lang = "vie" if ns == "chinhphu.vn" else "eng"

    candidates: list[str] = []
    if item["secid"] not in _FORCE_METADATA_ONLY_SECIDS:
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
                used_ocr = False
                if len(md) < 600 or (ocr_lang == "vie" and len(md) < 5000):
                    md, pages = fallback_pdf_text_to_markdown(data, title, ocr_lang=ocr_lang)
                    used_ocr = True
                if len(md) >= 800:
                    md = ensure_hierarchical_headings(md, title, desc)
                    best_md = md
                    best_url = final_url
                    best_tool = (
                        f"pymupdf + tesseract-ocr ({ocr_lang}) + tools-resources/utils/parse_regulatory_sections.py"
                        if used_ocr
                        else "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                    )
                    best_notes = (
                        f"Extracted {pages}-page PDF ({final_url}) locally via PyMuPDF"
                        f"{f' + Tesseract OCR ({ocr_lang})' if used_ocr else ''} "
                        f"({len(md):,} chars)."
                    )
                    break
            except Exception:
                pass
        else:
            html_str = _decode_html_bytes(data)
            is_eurlex_xhtml = (
                "publications.europa.eu/resource/cellar/" in final_url.lower()
                or "eur-lex.europa.eu/" in final_url.lower()
            )
            # Check for embedded PDFs first unless this is already an authoritative EUR-Lex Cellar XHTML document
            if not is_eurlex_xhtml:
                embedded_pdfs = find_embedded_pdf_urls(
                    html_str, final_url, ver, f"{name} {title}", namespace=ns
                )
                for pdf_u in embedded_pdfs:
                    pdata, pfinal = fetch_url_bytes(pdf_u)
                    if pdata and (pdata[:5] == b"%PDF-" or b"%PDF-1." in pdata[:1024]):
                        idx = pdata.find(b"%PDF-")
                        if idx > 0:
                            pdata = pdata[idx:]
                        try:
                            md, pages = pdf_bytes_to_markdown(pdata, title)
                            used_ocr = False
                            if len(md) < 600 or (ocr_lang == "vie" and len(md) < 5000):
                                md, pages = fallback_pdf_text_to_markdown(pdata, title, ocr_lang=ocr_lang)
                                used_ocr = True
                            if len(md) >= 800:
                                md = ensure_hierarchical_headings(md, title, desc)
                                best_md = md
                                best_url = pfinal
                                best_tool = (
                                    f"pymupdf + tesseract-ocr ({ocr_lang}) + tools-resources/utils/parse_regulatory_sections.py"
                                    if used_ocr
                                    else "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                                )
                                best_notes = (
                                    f"Discovered primary PDF ({pfinal}) from landing page ({final_url}); "
                                    f"extracted {pages}-page PDF via PyMuPDF"
                                    f"{f' + Tesseract OCR ({ocr_lang})' if used_ocr else ''} ({len(md):,} chars)."
                                )
                                break
                        except Exception:
                            pass
            if best_md:
                break

            # Otherwise extract HTML directly if it passes full-text strategy validation
            try:
                md = html_to_clean_markdown(html_str, final_url, title)
                md = ensure_hierarchical_headings(md, title, desc)
                if is_valid_html_strategy_doc(md, final_url, item):
                    best_md = md
                    best_url = final_url
                    best_tool = "requests + markdownify + tools-resources/utils/parse_regulatory_sections.py"
                    best_notes = (
                        f"Extracted official HTML publication ({final_url}) to Markdown ({len(md):,} chars)."
                    )
                    break
            except Exception:
                pass

    stem = item["stem"]

    # If live/Wayback fetch failed transiently, preserve an already-extracted document on disk
    # (from either public or private repo) unless its previous textUsed URL is now in `_BLOCKED_HTML_SUBSTRINGS`
    # or the edition is in `_FORCE_METADATA_ONLY_SECIDS`.
    if not best_md and item["secid"] not in _FORCE_METADATA_ONLY_SECIDS:
        for cand_root in (REPO_ROOT, PRIVATE_REPO_ROOT):
            cand_dir = cand_root / item["rel_dir"]
            cand_md = cand_dir / f"{stem}.md"
            cand_meta = cand_dir / f"{stem}-metadata.json"
            if cand_md.exists() and cand_meta.exists():
                try:
                    prev_meta = json.loads(cand_meta.read_text(encoding="utf-8"))
                    prev_url = (prev_meta.get("links") or {}).get("textUsed") or ""
                    prev_tool = (prev_meta.get("current_extraction") or {}).get("tool") or ""
                    prev_notes = (prev_meta.get("current_extraction") or {}).get("notes") or ""
                    if prev_url and not any(b in prev_url.lower() for b in _BLOCKED_HTML_SUBSTRINGS):
                        best_md = ensure_hierarchical_headings(cand_md.read_text(encoding="utf-8"), title, desc)
                        best_url = prev_url
                        best_tool = prev_tool or "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                        best_notes = re.sub(r"\s*Parsed\s+\d+\s+sections.*$", "", prev_notes).strip()
                        break
                except Exception:
                    pass

    lic_obj = license_for_tld(item["tld"], ns, md_text=best_md, secid=item["secid"])
    # Metadata-only records belong in the public catalog repository only when their jurisdiction/source license is not Proprietary/Non-Commercial
    if (
        not best_md
        and item["tld"] not in ("sg", "lu")
        and lic_obj.get("Grouping") not in ("Proprietary / All Rights Reserved", "Non-Commercial", "Non-Commercial-No-Derivatives")
    ):
        is_public = True
    else:
        is_public = bool(lic_obj.get("publicly_redistributable", True))
    target_root = REPO_ROOT if is_public else PRIVATE_REPO_ROOT
    other_root = PRIVATE_REPO_ROOT if is_public else REPO_ROOT

    # Clean up any stale copy in the other repository so public/private separation is strictly enforced
    other_dir = other_root / item["rel_dir"]
    if other_dir.exists():
        shutil.rmtree(other_dir)
        parent_p = other_dir.parent
        while parent_p != other_root / "reference" and parent_p != other_root:
            try:
                parent_p.rmdir()
            except OSError:
                break
            parent_p = parent_p.parent

    doc_dir = target_root / item["rel_dir"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    md_path = doc_dir / f"{stem}.md"
    sec_json_path = doc_dir / f"{stem}-sections.json"
    sec_csv_path = doc_dir / f"{stem}-sections.csv"
    meta_path = doc_dir / f"{stem}-metadata.json"

    if not best_md:
        # Clean up any stale or synthetic extraction artifacts and record honest metadata-only state
        md_path.unlink(missing_ok=True)
        sec_json_path.unlink(missing_ok=True)
        sec_csv_path.unlink(missing_ok=True)
        unavail_note = (
            f"Official primary full-text document for {item['secid']} ({orig_url}) is not directly "
            f"downloadable (upstream portal landing page only, IP-restricted archive, or broken upstream link); "
            f"recorded as metadata-only."
        )
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
            license_obj=lic_obj,
            source_url=orig_url,
            text_used_url="",
            published=item["published"],
            active=item["active"],
            retired_date=item["retired_date"],
            supersedes=item["supersedes"],
            superseded_by=item["superseded_by"],
            tool_str="",
            extraction_notes=unavail_note,
            end_state="metadata-only",
            end_reason="pending-acquisition",
        )
        return {
            "secid": item["secid"],
            "rel_dir": item["rel_dir"],
            "repo": target_root.name,
            "chars": 0,
            "sections": 0,
            "with_id": 0,
            "tool": "metadata-only",
            "url_used": "",
        }

    best_md = _append_eurlex_cellar_annexes(best_md, best_url, title, desc)
    best_md = postprocess_markdown_structure(best_md, title)
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
        license_obj=lic_obj,
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
    if item["secid"] == "secid:reference/dsn.gob.es/estrategia-nacional-ciberseguridad@2019" and meta_path.exists():
        mdata = json.loads(meta_path.read_text(encoding="utf-8"))
        mdata["lifecycle"]["notes"] = (
            "Approved by the National Security Council on 2019-04-12; published in BOE on 2019-04-30 "
            "(Orden PCI/487/2019, BOE-A-2019-6347); bilingual booklet edition issued June 2019. "
            "Implemented and complemented (not superseded) by the 2022 Plan Nacional de Ciberseguridad."
        )
        meta_path.write_text(json.dumps(mdata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif item["secid"] == "secid:reference/gov.br/pbia@2024-2028" and meta_path.exists():
        mdata = json.loads(meta_path.read_text(encoding="utf-8"))
        mdata["lifecycle"]["notes"] = (
            "Presented to President Luiz Inácio Lula da Silva at the 5th National Conference on Science, "
            "Technology and Innovation on 2024-07-30; final consolidated MCTI/CGEE book edition published in 2025."
        )
        meta_path.write_text(json.dumps(mdata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "secid": item["secid"],
        "rel_dir": item["rel_dir"],
        "repo": target_root.name,
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
                    if rel_dir in _WAVE1_REL_DIRS:
                        continue
                    stem = f"{name}-{v}"
                    meta_path = REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                    priv_meta_path = PRIVATE_REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                    if skip_existing and (meta_path.exists() or priv_meta_path.exists()):
                        continue
                    vinfo = ver_map[v]
                    secid = f"secid:reference/{ns}/{name}@{v}"
                    is_latest = (vinfo["status"] == "current") if vinfo["status"] else (idx == len(sorted_vers) - 1)
                    prev_ver = sorted_vers[idx - 1] if idx > 0 else ""
                    prev_is_current = bool(prev_ver and ver_map[prev_ver].get("status") == "current")
                    prev_secid = f"secid:reference/{ns}/{name}@{prev_ver}" if (idx > 0 and not prev_is_current) else None
                    next_secid = f"secid:reference/{ns}/{name}@{sorted_vers[idx + 1]}" if (idx < len(sorted_vers) - 1 and not is_latest) else None
                    retired_date = ver_map[sorted_vers[idx + 1]]["release_date"] if (idx < len(sorted_vers) - 1 and not is_latest) else None
                    if secid == "secid:reference/dsn.gob.es/estrategia-nacional-ciberseguridad@2019":
                        pub_date = "2019-04-30"
                    elif secid == "secid:reference/gov.br/pbia@2024-2028":
                        pub_date = "2025-01-01"
                    else:
                        pub_date = vinfo["release_date"]
                    ed_issuer = (
                        "NITI Aayog (National Institution for Transforming India)"
                        if secid == "secid:reference/meity.gov.in/national-ai-strategy@2018"
                        else issuer
                    )
                    full_title = vinfo["official_name"] or (f"{source_full} ({v})" if v not in source_full else source_full)
                    v_note = (vinfo["note"] or "").strip()
                    if secid == "secid:reference/meity.gov.in/national-ai-strategy@2018":
                        full_desc = (
                            "National Strategy for Artificial Intelligence (#AIforAll, June 2018), published by "
                            "NITI Aayog (National Institution for Transforming India), defining India's foundational "
                            "AI research, adoption, and responsible deployment strategy across healthcare, agriculture, "
                            "education, smart cities, and smart mobility."
                        )
                    elif is_latest:
                        full_desc = f"{v_note} {source_desc}".strip() if v_note and v_note not in source_desc else source_desc
                    elif v_note:
                        if len(v_note) >= 40:
                            full_desc = v_note if v_note.endswith(".") else f"{v_note}."
                        else:
                            full_desc = f"{v_note.rstrip('.')} — {v} edition of {source_full}, published by {ed_issuer} ({ns})."
                    else:
                        full_desc = f"Official {v} edition of {source_full} ({full_title}), published by {ed_issuer} ({ns})."
                    items.append({
                        "tld": tld,
                        "namespace": ns,
                        "issuer": ed_issuer,
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
                        "published": pub_date,
                        "active": is_latest,
                        "supersedes": prev_secid,
                        "superseded_by": next_secid,
                        "retired_date": retired_date,
                    })
            else:
                rel_dir = f"reference/{ns}/{name}"
                if rel_dir in _WAVE1_REL_DIRS:
                    continue
                stem = name
                meta_path = REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                priv_meta_path = PRIVATE_REPO_ROOT / rel_dir / f"{stem}-metadata.json"
                if skip_existing and (meta_path.exists() or priv_meta_path.exists()):
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
