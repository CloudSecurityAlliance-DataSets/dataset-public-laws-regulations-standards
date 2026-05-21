#!/usr/bin/env python3
"""Extract glossary terms from the AWS Well-Architected Security Pillar glossary page.

Source: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/glossary.html

NOTE ON SOURCE STATE (verified 2026-05):
    As of the date of this extraction the Security Pillar glossary page itself
    contains no inline term entries. Its sole content is a redirect notice:

        "For the latest AWS terminology, see the AWS glossary in the AWS
         Glossary Reference."

    (Target: https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html)

    Historically AWS guides shipped a `<dl class="termset"><dt>Term</dt>
    <dd>Definition</dd></dl>` block on this page. That content has been
    moved to the central AWS Glossary Reference and is no longer duplicated
    here. This script still parses the page (so re-running it will pick up
    terms if AWS ever restores them in-place) and emits the standard output
    artifacts even when zero terms are found.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/glossary.html"
SCRIPT_DIR = Path(__file__).resolve().parent

OUT_MD = SCRIPT_DIR / "wellarchitected-security-glossary.md"
OUT_CSV = SCRIPT_DIR / "wellarchitected-security-glossary-terms.csv"
OUT_JSON = SCRIPT_DIR / "wellarchitected-security-glossary-terms.json"


def fetch(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def parse_terms(html: str) -> List[Dict[str, str]]:
    """Pull <dt>/<dd> pairs out of the page.

    AWS docs historically used `<dl class="termset">` or plain `<dl>` blocks.
    We scan every `<dl>` on the page so the parser remains robust if AWS
    re-introduces terms with slightly different markup.
    """
    soup = BeautifulSoup(html, "html.parser")
    terms: List[Dict[str, str]] = []

    # Restrict to the main content area when present, otherwise the whole doc.
    root = soup.find(id="main-col-body") or soup

    for dl in root.find_all("dl"):
        # Walk children in document order; pair each <dt> with the following <dd>(s).
        current_term = None
        current_anchor = ""
        for child in dl.find_all(["dt", "dd"], recursive=True):
            if child.name == "dt":
                current_term = child.get_text(" ", strip=True)
                # Try to capture an anchor for source-linking.
                anchor_el = child.find("a", attrs={"id": True}) or child.find(
                    "a", attrs={"name": True}
                )
                if anchor_el:
                    current_anchor = anchor_el.get("id") or anchor_el.get("name") or ""
                else:
                    current_anchor = child.get("id", "") or ""
            elif child.name == "dd" and current_term is not None:
                definition = child.get_text(" ", strip=True)
                terms.append(
                    {
                        "term": current_term,
                        "definition": definition,
                        "source_anchor": current_anchor,
                        "notes": "",
                    }
                )
                # Allow multi-dd per dt (rare); reset only when next <dt> arrives.
    return terms


def write_outputs(terms: List[Dict[str, str]], redirect_note: str) -> None:
    # JSON
    OUT_JSON.write_text(json.dumps(terms, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # CSV
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        writer.writeheader()
        for t in terms:
            writer.writerow(t)

    # Markdown
    lines: List[str] = []
    lines.append("# AWS Well-Architected Security Pillar Glossary")
    lines.append("")
    lines.append(f"Source: <{SOURCE_URL}>")
    lines.append("")
    if redirect_note:
        lines.append("## Note")
        lines.append("")
        lines.append(redirect_note)
        lines.append("")
    if terms:
        lines.append(f"## Terms ({len(terms)})")
        lines.append("")
        for t in terms:
            lines.append(f"### {t['term']}")
            lines.append("")
            lines.append(t["definition"])
            lines.append("")
    else:
        lines.append("## Terms")
        lines.append("")
        lines.append(
            "_No inline glossary terms were present on the source page at extraction time._"
        )
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch(SOURCE_URL)
    terms = parse_terms(html)

    # Detect the redirect-only state: the page references the central AWS glossary
    # without providing inline terms.
    redirect_note = ""
    soup = BeautifulSoup(html, "html.parser")
    body_text = " ".join(
        (soup.find(id="main-col-body") or soup).get_text(" ", strip=True).split()
    )
    if (
        not terms
        and "AWS Glossary Reference" in body_text
        and "/glossary/latest/reference/glos-chap.html" in html
    ):
        redirect_note = (
            "The AWS Well-Architected Security Pillar glossary page no longer "
            "hosts inline terms. AWS now directs readers to the central "
            "[AWS Glossary Reference]"
            "(https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html) "
            "for the latest terminology. This extraction therefore contains zero "
            "terms; re-run the script if AWS restores in-page definitions."
        )

    write_outputs(terms, redirect_note)
    print(f"Extracted {len(terms)} term(s) from {SOURCE_URL}")
    if redirect_note:
        print("NOTE: Source page is a redirect-only stub; see markdown output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
