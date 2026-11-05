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
    ("president.go.kr", "national-ai-strategy", "2024"): [
        "https://www.msit.go.kr/ssm/file/fileDown.do?atchFileNo=47317&fileOrd=1&fileBtn=A",
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


def license_for_tld(tld: str, namespace: str, md_text: str = "", secid: str = "") -> dict:
    """Return complete schema-aligned government/public-sector license metadata verified against document text."""
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
            or namespace == "defence.gov.au"
            or secid.endswith("@2009")
        ):
            return _make_license(
                "LicenseRef-Government-Work",
                "Government-Work",
                "Government publication; Commonwealth of Australia copyright retained. Publicly released for free download, policy reference, and study under the Copyright Act 1968; prior written permission required for commercial reproduction or derivative works.",
                "https://www.defence.gov.au/copyright",
                redistribution="permitted_for_reference",
                derivatives="prohibited",
                publicly_redistributable=True,
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
                "Copyright Government of Singapore (MDDI / Smart Nation). Document explicitly permits reproduction without modification for non-commercial use only.",
                "https://www.smartnation.gov.sg/terms-of-use/",
                redistribution="permitted_non_commercial_verbatim",
                derivatives="prohibited",
                publicly_redistributable=True,
            )
        return _make_license(
            "LicenseRef-Government-Work",
            "Government-Work",
            "Government publication; Copyright Government of Singapore (Cyber Security Agency of Singapore / Smart Nation and Digital Government Office) retained. Publicly released for free download, policy reference, and citation; consult Singapore Government Terms of Use before commercial redistribution or derivative works.",
            "https://www.csa.gov.sg/terms-of-use",
            redistribution="permitted_for_reference",
            derivatives="prohibited",
            publicly_redistributable=True,
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
                publicly_redistributable=True,
            )
        if "reprints without permission will be prosecuted" in md_text.lower() or namespace == "mnd.gov.tw":
            return _make_license(
                "LicenseRef-Government-Work",
                "Government-Work",
                "Government publication; Copyright Ministry of National Defense, R.O.C. (Taiwan) retained. Publicly released for free download, policy reference, and study; commercial reprints or derivative works without permission are prohibited.",
                "https://www.mnd.gov.tw/",
                redistribution="permitted_for_reference",
                derivatives="prohibited",
                publicly_redistributable=True,
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
                    publicly_redistributable=True,
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
                "LicenseRef-Government-Work",
                "Government-Work",
                "Intergovernmental organization publication; African Union Commission copyright retained. Publicly released for free download, policy reference, and study.",
                "https://au.int/en/legal-disclaimer",
                redistribution="permitted_for_reference",
                derivatives="varies_by_jurisdiction",
                publicly_redistributable=True,
            )
        return _make_license(
            "CC-BY-3.0-IGO",
            "Permissive",
            f"International intergovernmental organization publication ({namespace}); open access for public policy and research reference.",
            "http://creativecommons.org/licenses/by/3.0/igo",
            redistribution="permitted_with_attribution",
            derivatives="permitted_with_attribution",
            publicly_redistributable=True,
        )
    return _make_license(
        "LicenseRef-Government-Work",
        "Government-Work",
        f"Official national strategy publication ({namespace}); publicly released for free download, policy reference, and research.",
        None,
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
        if dl_url not in seen and (not namespace or _is_trusted_pdf_target(base_url, dl_url, namespace)):
            seen.add(dl_url)
            scored.append((25, dl_url))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [u for _, u in scored[:4]]


def ensure_hierarchical_headings(md: str, doc_title: str, doc_desc: str, is_annex: bool = False) -> str:
    """Promote legitimate unformatted section/chapter headings in plain/CJK/European PDFs and XHTML
    without inventing arbitrary artificial chunk headings.
    """
    md = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]+", " ", md)
    raw_lines = md.splitlines()
    # Pre-pass: join standalone section number lines (e.g. `1.` or `2.2.`) with the immediately following title line
    lines: list[str] = []
    idx = 0
    while idx < len(raw_lines):
        cur = raw_lines[idx].strip()
        if re.match(r"^\d{1,2}(?:\.\d{1,2})*\.$", cur) and idx + 1 < len(raw_lines):
            nxt = raw_lines[idx + 1].strip()
            if nxt and not nxt.startswith(("#", "[")) and 3 <= len(nxt) <= 220 and re.match(r"^[A-ZÄÖÜÉÈÊÀÁÍÓÚÑ]", nxt):
                lines.append(f"{cur} {nxt}")
                idx += 2
                continue
        lines.append(raw_lines[idx])
        idx += 1

    # Detect Table of Contents block (e.g. `Contents` followed by lines that repeat when body starts)
    toc_skip_indices: set[int] = set()
    for i, l in enumerate(lines[:50]):
        if l.strip().lower() in ("contents", "table of contents"):
            first_entry = ""
            first_idx = -1
            for j in range(i + 1, min(i + 15, len(lines))):
                cand_e = lines[j].strip()
                if len(cand_e) >= 10 and not cand_e.startswith("["):
                    first_entry = cand_e
                    first_idx = j
                    break
            if first_entry:
                for k in range(first_idx + 2, min(first_idx + 160, len(lines))):
                    if lines[k].strip() == first_entry:
                        toc_skip_indices.update(range(i, k))
                        break
            break

    h2_plus = [l for l in lines if re.match(r"^#{2,6}\s+\S+", l)]
    numbered_h2 = [
        l
        for l in h2_plus
        if re.match(
            r"^#{2,6}\s+(?:(?:CHAPTER|PART|SECTION|PILLAR|GOAL|OBJECTIVE|PRIORITY|ANNEX|APPENDIX|제\s*\d+\s*[장절편]|第[一二三四五六七八九十百0-9０-９]+[章節編部])\b|(?:\d{1,2}(?:\.\d{1,2})*|[IVXLCDM]{1,5}|[A-H])[\.\)\s]|[一二三四五六七八九十壹貳參肆伍陸柒捌玖拾ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[、．\.])",
            l,
            re.IGNORECASE,
        )
    ]
    if (len(h2_plus) >= 6 or len(numbered_h2) >= 2) and not is_annex:
        return "\n".join(lines) + "\n"

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
        r"(?i:CHAPTER|PART|SECTION|PILLAR|GOAL|OBJECTIVE|PRIORITY|ANNEX|APPENDIX|KAPITEL|TEIL|CHAPITRE|PARTIE|CAPITOLO|PARTE)\s+(?:[IVXLCDM]+|\d+(?:\.\d+)*|[A-Z])\b.*"
        r"|(?:[IVXLCDM]{1,5}|\d{1,2}(?:\.\d{1,2}){0,2})[\.\)]\s*[A-Za-zÄÖÜÉÈÊÀÁÍÓÚÑ\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af].{2,220}"
        r"|[A-H]\.\s*[A-Z][A-Za-z0-9\s,\-–—'’\(\)/:;\.]{2,220}"
        r"|[IVX]{1,4}\s+[A-Z][A-Za-z0-9\s,\-–—'’\(\)/]{2,90}"
        r"|第[一二三四五六七八九十百0-9０-９]+[章節編部]\s*.{1,80}"
        r"|[一二三四五六七八九十]+[、．\.]\s*.{2,80}"
        r"|[壹貳參肆伍陸柒捌玖拾]+[、．\.]\s*.{2,80}"
        r"|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+[\.\s、．]\s*.{2,80}"
        r"|제\s*\d+\s*[장절편]\s*.{1,80}"
        r"|Executive Summary|Foreword|Preface|Introduction|Conclusion|Conclusions:?|Overview|Background|Strategic Context|Vision|Implementation|Governance|Abbreviations|Definitions"
        r"|Introduction:\s+.{5,140}"
        r"|IT threat assessment|Framework conditions|Basic principles.*|Strategic objectives and measures|Sustainable implementation"
        r")$"
    )
    explicit_sec_prefix_re = re.compile(
        r"^(?:[A-H]\.\s*[A-Z]|(?i:CHAPTER|PART|SECTION|ANNEX|APPENDIX)\s+(?:[IVXLCDM]+|\d+))\b"
    )
    for idx_l, line in enumerate(lines):
        if idx_l in toc_skip_indices:
            promoted_lines.append(line)
            continue
        s = line.strip()
        # Normalize missing space after Appendix/Annex/Chapter/Part/Section number (e.g. `Appendix 2Analysis...` -> `Appendix 2: Analysis...`)
        s = re.sub(
            r"^((?i:Appendix|Annex|Chapter|Part|Section)\s+(?:[IVXLCDM]+|\d+))([A-ZÄÖÜÉÈÊÀÁÍÓÚÑ])",
            r"\1: \2",
            s,
        )
        allow_trailing_dot = bool(explicit_sec_prefix_re.match(s))
        if (
            not s.startswith("#")
            and 3 <= len(s) <= 230
            and not s.endswith((";", "。", "；"))
            and (allow_trailing_dot or not s.endswith("."))
            and not re.search(r"\b2\.\s*\S+.*\b3\.", s)
            and heading_pat.match(s)
        ):
            # Ensure a space after leading number/Roman/letter dot (e.g., `1.Introduction` -> `1. Introduction`)
            s_norm = re.sub(
                r"^((?:\d{1,2}(?:\.\d{1,2})*|[IVXLCDM]{1,5}|[A-H])\.)([A-Za-zÄÖÜÉÈÊÀÁÍÓÚÑ\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af])",
                r"\1 \2",
                s,
            )
            if allow_trailing_dot and s_norm.endswith("."):
                s_norm = s_norm.rstrip(".")
            if re.match(r"^Appendix\s+\d+\b", s_norm, re.IGNORECASE):
                in_appendix = True
            m_sub = re.match(r"^(\d{1,2}(?:\.\d{1,2})+)\.", s_norm)
            m_single_num = re.match(r"^(\d{1,2})\.\s+(.+)$", s_norm)
            if is_annex:
                if m_single_num and in_appendix:
                    # Inside an Appendix of an Annex, emit unnumbered subsection heading to avoid colliding with main doc section numbers
                    promoted_lines.append(f"#### {m_single_num.group(2)}")
                elif m_single_num and has_roman_parts:
                    promoted_lines.append(f"#### Chapter {m_single_num.group(1)}: {m_single_num.group(2)}")
                elif m_sub:
                    promoted_lines.append(f"#### {s_norm}")
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
    r"|E\d{6,}\b"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$"
    r"|\d{4}$"
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


def postprocess_markdown_structure(md: str, doc_title: str) -> str:
    """Clean up PDF/XHTML heading artifacts so every heading represents a genuine section with body prose
    or child sections, without colophon headings, split sentences, or reversed banner titles.
    """
    from parse_regulatory_sections import parse_heading

    md = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]+", " ", md)
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    blocks: list[str] = []
    for b in raw_blocks:
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
        blocks[i] = f"{hashes} {txt}"
        sec_id, _, _ = parse_heading(txt)
        if _COLOPHON_HEADING_RE.search(txt) or re.match(r"^(?:Table\s+of\s+Contents|Contents)\s*$", txt, re.I):
            blocks[i] = txt
            continue
        if not sec_id and (len(txt) > 140 or txt.endswith((",", ";"))):
            blocks[i] = txt
            continue
        if not sec_id and txt.endswith(".") and not re.search(r"\b(?:U\.S|U\.K|E\.U|Inc|Ltd|Co|Dr|Mr|Ms|St|etc)\.$", txt):
            blocks[i] = txt
            continue
        if not sec_id and re.search(r"[a-z]\.\s+[A-Z][a-z]+\s+[a-z]+", txt):
            blocks[i] = txt

    # Pass 2: Merge split headings (dangling prepositions) and demote unnumbered headings followed by lowercase continuation
    merged: list[str] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        m = re.match(r"^(#{2,6})\s+(.+?)\s*$", b)
        if m and i + 1 < len(blocks):
            hashes, txt = m.group(1), m.group(2).strip()
            nxt = blocks[i + 1].strip()
            sec_id, _, _ = parse_heading(txt)
            # Unnumbered heading followed immediately by a plain block starting with a lowercase letter -> sentence wrap!
            if not sec_id and not nxt.startswith("#") and re.match(r"^(?:[a-z]|\d+(?:\.\d+)?\s+[a-z])", nxt):
                merged.append(f"{txt} {nxt}")
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
                    id1, _, kind1 = parse_heading(h1_txt)
                    id2, _, kind2 = parse_heading(h2_txt)
                    if kind1 == "standalone_id" or _BARE_CONTAINER_HEADING_RE.match(h1_txt):
                        clean_h1 = h1_txt.rstrip(" -–—:.")
                        new_blocks.append(f"{h1_hashes} {clean_h1}: {h2_txt}")
                        i += 2
                        changed = True
                        continue
                    if id1 and not id2 and (len(h1_hashes) == len(h2_hashes) or _DANGLING_PREP_RE.search(h1_txt)):
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
                        if (
                            kind1 in ("pillar", "part", "chapter", "roman", "annex", "section_word")
                            and kind2 != kind1
                            and len(h1_hashes) == len(h2_hashes)
                            and len(h2_hashes) < 6
                        ):
                            blocks[i + 1] = "#" + blocks[i + 1]
                            changed = True
                        else:
                            blocks[i] = h1_txt
                            changed = True
            new_blocks.append(blocks[i])
            i += 1
        blocks = new_blocks

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

    return "\n\n".join(blocks) + "\n"


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
)


def is_valid_html_strategy_doc(md: str, final_url: str, item: dict) -> bool:
    """Return True only when an HTML extraction is a genuine full-text strategy document,
    rejecting generic homepages, catalog records, and short landing pages.
    """
    low_url = final_url.lower()
    if any(b in low_url for b in _BLOCKED_HTML_SUBSTRINGS):
        return False
    # Official EUR-Lex / Publications Office Cellar XHTML documents are authoritative full texts
    if "publications.europa.eu/resource/cellar/" in low_url or "eur-lex.europa.eu/" in low_url:
        return len(md) >= 5000
    # Require substantial prose and multiple real headings for general HTML strategy pages
    h2_count = sum(1 for l in md.splitlines() if re.match(r"^#{2,4}\s+\S+", l))
    return len(md) >= 4500 and h2_count >= 3


def fallback_pdf_text_to_markdown(pdf_bytes: bytes, doc_title: str) -> tuple[str, int]:
    """Fallback text + Tesseract OCR extraction when layout heuristics return sparse text."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num_pages = len(doc)
    out = [f"# {doc_title}", ""]
    for page in doc:
        txt = page.get_text("text").strip()
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
            if clean_l and not re.match(r"^\d{1,3}$", clean_l):
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
                if len(md) >= 800:
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

    doc_dir = REPO_ROOT / item["rel_dir"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    stem = item["stem"]
    md_path = doc_dir / f"{stem}.md"
    sec_json_path = doc_dir / f"{stem}-sections.json"
    sec_csv_path = doc_dir / f"{stem}-sections.csv"
    meta_path = doc_dir / f"{stem}-metadata.json"

    # If live/Wayback fetch failed transiently, preserve an already-extracted document on disk
    # unless its previous textUsed URL is now in `_BLOCKED_HTML_SUBSTRINGS`.
    if not best_md and md_path.exists() and meta_path.exists():
        try:
            prev_meta = json.loads(meta_path.read_text(encoding="utf-8"))
            prev_url = (prev_meta.get("links") or {}).get("textUsed") or ""
            prev_tool = (prev_meta.get("current_extraction") or {}).get("tool") or ""
            prev_notes = (prev_meta.get("current_extraction") or {}).get("notes") or ""
            if prev_url and not any(b in prev_url.lower() for b in _BLOCKED_HTML_SUBSTRINGS):
                best_md = md_path.read_text(encoding="utf-8")
                best_url = prev_url
                best_tool = prev_tool or "pymupdf + tools-resources/utils/parse_regulatory_sections.py"
                best_notes = re.sub(r"\s*Parsed\s+\d+\s+sections.*$", "", prev_notes).strip()
        except Exception:
            pass

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
            license_obj=license_for_tld(item["tld"], ns, md_text="", secid=item["secid"]),
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
            end_reason="source-unavailable",
        )
        return {
            "secid": item["secid"],
            "rel_dir": item["rel_dir"],
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
        license_obj=license_for_tld(item["tld"], ns, md_text=best_md, secid=item["secid"]),
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
                    if rel_dir in _WAVE1_REL_DIRS:
                        continue
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
                    v_note = (vinfo["note"] or "").strip()
                    if is_latest:
                        full_desc = f"{v_note} {source_desc}".strip() if v_note and v_note not in source_desc else source_desc
                    elif v_note:
                        if len(v_note) >= 40:
                            full_desc = v_note if v_note.endswith(".") else f"{v_note}."
                        else:
                            full_desc = f"{v_note.rstrip('.')} — {v} edition of {source_full}, published by {issuer} ({ns})."
                    else:
                        full_desc = f"Official {v} edition of {source_full} ({full_title}), published by {issuer} ({ns})."
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
                if rel_dir in _WAVE1_REL_DIRS:
                    continue
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
