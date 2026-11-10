#!/usr/bin/env python3
"""Extract Palo Alto Networks Cyberpedia glossary into structured CSV/JSON.

Source:  https://www.paloaltonetworks.com/cyberpedia/glossary
License: LicenseRef-Vendor-Copyright (Palo Alto Networks copyright; internal CSA use only).

Page structure: ~99 div.glossary-card elements carrying a div.glossary-title hold
the term + primary definition. ~198 sibling .glossary-card elements without a title
hold supplementary content ("What I need to know about X", "Five FAQs about X") and
are not used here (the row-per-term schema doesn't model them; they remain available
in the cached HTML if needed later).

Per-term shape inside a titled card:
  h4.glossary-title.h7         -> term name (may carry trailing ':')
  div.glossary-subtitle        -> definition body
  div.glossary-badges a[href]  -> deep-link to per-term article (relative path)

Produces in the script's directory:
  cyberpedia-glossary.md
  cyberpedia-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  cyberpedia-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.paloaltonetworks.com/cyberpedia/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "cyberpedia-glossary"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


def fetch():
    r = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    r.raise_for_status()
    return r.text


def clean_term(raw):
    return re.sub(r"\s+", " ", raw).strip().rstrip(":").strip()


def clean_definition(raw):
    # The subtitle may include trailing "Related Content"-ish noise from nested
    # markup; trim repeated whitespace and any trailing "Related Content" marker.
    text = re.sub(r"\s+", " ", raw).strip()
    text = re.sub(r"\s*Related Content\s*$", "", text, flags=re.IGNORECASE)
    return text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for card in soup.select(".glossary-card"):
        title_el = card.select_one(".glossary-title")
        if not title_el:
            continue  # supplementary FAQ/expansion card, no primary term

        subtitle_el = card.select_one(".glossary-subtitle")
        if not subtitle_el:
            continue  # term card without a definition body; skip rather than guess

        term = clean_term(title_el.get_text(" ", strip=True))
        definition = clean_definition(subtitle_el.get_text(" ", strip=True))
        if not term or not definition:
            continue

        link_el = card.select_one(".glossary-badges a[href]")
        if link_el and link_el.get("href"):
            source_anchor = urljoin(SOURCE_URL, link_el["href"].split("?")[0])
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

    # Dedupe by case-insensitive term, keep the longest definition.
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
        f.write("# Palo Alto Networks Cyberpedia Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Palo Alto Networks copyright; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["source_anchor"] != SOURCE_URL:
                f.write(f"Related: <{t['source_anchor']}>\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        w.writeheader()
        w.writerows(terms)
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    with open(path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
    return path


def main():
    html = fetch()
    terms = parse(html)
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
