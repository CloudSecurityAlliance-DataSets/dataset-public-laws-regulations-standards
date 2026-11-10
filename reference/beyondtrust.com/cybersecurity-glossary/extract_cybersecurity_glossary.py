#!/usr/bin/env python3
"""Extract the BeyondTrust Cybersecurity Glossary into CSV/JSON.

Source:  https://www.beyondtrust.com/resources/glossary  (anti-bot 403's curl)
License: LicenseRef-Vendor-Copyright (BeyondTrust Corporation; internal CSA use only).

Fetch strategy: SingleFile HTML capture committed alongside the script as
.source-cache.html (per the FedRAMP-template pattern from PROCESSING-GLOSSARIES.md).
The live page is Cloudflare/anti-bot-gated, so we rely on the human-captured
snapshot for reproducibility. Re-capture by saving the live page with the
SingleFile browser extension and overwriting .source-cache.html.

Page structure: AlpineJS-rendered glossary list captured post-hydration.
~54 .glossary-section elements (the first is the Alpine template; rest are real).
Each real section has:
  h2.glossary-title          -> term name (rendered text, not the x-text placeholder)
  p[x-text="entry.glossaryTermSummary"]  -> definition body
  a[href*="/resources/glossary/"]  -> deep link to the per-term page

Produces:
  cybersecurity-glossary.md
  cybersecurity-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  cybersecurity-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

SOURCE_URL = "https://www.beyondtrust.com/resources/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "cybersecurity-glossary"
CACHE_PATH = OUT_DIR / ".source-cache.html"


def squish(s):
    return re.sub(r"\s+", " ", s).strip().lstrip("​").strip()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for section in soup.select(".glossary-section"):
        title_el = section.select_one(".glossary-title")
        if not title_el:
            continue
        term = squish(title_el.get_text(" ", strip=True))
        # The Alpine template section's title is empty; skip it.
        if not term:
            continue

        # Definition is the p with x-text="entry.glossaryTermSummary".
        body_p = section.select_one('p[x-text="entry.glossaryTermSummary"]')
        if body_p is None:
            body_p = section.find("p")
        if not body_p:
            continue
        definition = squish(body_p.get_text(" ", strip=True))
        if not definition:
            continue

        # Deep link: the first <a> with a glossary/ path
        anchor_a = section.find("a", href=re.compile(r"/resources/glossary/"))
        if anchor_a and anchor_a.get("href"):
            source_anchor = anchor_a["href"]
        else:
            source_anchor = SOURCE_URL

        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": source_anchor,
                "notes": "",
            }
        )

    by_term = {}
    for t in terms:
        key = t["term"].lower()
        existing = by_term.get(key)
        if existing is None or len(t["definition"]) > len(existing["definition"]):
            by_term[key] = t
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# BeyondTrust Cybersecurity Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (BeyondTrust Corporation; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["source_anchor"] != SOURCE_URL:
                f.write(f"Source: <{t['source_anchor']}>\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(terms)
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    with open(path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
    return path


def main():
    if not CACHE_PATH.exists():
        raise SystemExit(
            f"Missing {CACHE_PATH}. The live page is anti-bot-gated; "
            f"capture {SOURCE_URL} with the SingleFile browser extension "
            f"and save as .source-cache.html here."
        )
    html = CACHE_PATH.read_text()
    terms = parse(html)
    write_md(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Extracted {len(terms)} terms from {CACHE_PATH}")


if __name__ == "__main__":
    main()
