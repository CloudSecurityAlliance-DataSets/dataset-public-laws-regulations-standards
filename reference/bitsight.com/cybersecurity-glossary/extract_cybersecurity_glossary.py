#!/usr/bin/env python3
"""Extract the Bitsight Cybersecurity Glossary into CSV/JSON.

Source:  https://www.bitsight.com/glossary
License: LicenseRef-Vendor-Copyright (Bitsight Technologies, Inc.; internal CSA use only).

Page architecture: the index page is JS-hydrated; after hydration the DOM holds
~119 .definition-block elements, each only containing the term title and a
deep-link to its per-term page. Definitions live on the per-term pages, which
are plain server-rendered HTML accessible to plain HTTP (no JS / no anti-bot).

Fetch strategy:
  1. The index page's hydrated DOM is captured separately via
     tools-resources/utils/playwright_fetch.py and committed as
     .source-cache.html alongside this script.
  2. This extractor parses the index to harvest term URLs.
  3. For each term URL, it does a polite HTTP fetch (1.5s delay) and parses
     the per-term page's h1 (term) + first article <p> (definition).

To re-capture the index:
  python3 tools-resources/utils/playwright_fetch.py \\
    https://www.bitsight.com/glossary \\
    reference/bitsight.com/cybersecurity-glossary/.source-cache.html \\
    --auto --dwell 8

Produces:
  cybersecurity-glossary.md
  cybersecurity-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  cybersecurity-glossary-terms.json
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.bitsight.com/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "cybersecurity-glossary"
CACHE_PATH = OUT_DIR / ".source-cache.html"
PER_TERM_DELAY_S = 1.5
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


def squish(s):
    return re.sub(r"\s+", " ", s).strip()


def harvest_term_urls(index_html):
    """Walk the hydrated index DOM and return [(term_text, url), ...]."""
    soup = BeautifulSoup(index_html, "html.parser")
    out = []
    for block in soup.select(".definition-block"):
        a = block.find("a", href=True)
        if not a:
            continue
        url = a["href"].strip()
        if not url.startswith("http"):
            continue
        # The term is in the <strong> inside the anchor.
        strong = a.find("strong")
        term = squish((strong or a).get_text(" ", strip=True))
        if not term:
            continue
        out.append((term, url))
    # Dedupe by URL preserving order.
    seen = set()
    deduped = []
    for term, url in out:
        if url in seen:
            continue
        seen.add(url)
        deduped.append((term, url))
    return deduped


def fetch_term_definition(url, session):
    """Fetch a per-term page, return the introductory definition section (paragraphs and lists before the first h2)."""
    r = session.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    article = soup.find("article")
    if not article:
        return None
    parts = []
    for el in article.find_all(["h2", "h3", "p", "li"]):
        if el.name in ("h2", "h3") and parts:
            break
        if el.name == "p" and el.find_parent("li") is not None:
            continue
        text = squish(el.get_text(" ", strip=True))
        if not text:
            continue
        if el.name == "p" and (len(text) >= 40 or parts):
            parts.append(text)
        elif el.name == "li" and parts:
            parts.append(f"- {text}")
    return " ".join(parts) if parts else None


def parse():
    if not CACHE_PATH.exists():
        raise SystemExit(
            f"Missing {CACHE_PATH}. Run tools-resources/utils/playwright_fetch.py "
            f"to capture the JS-hydrated index page first."
        )
    index_html = CACHE_PATH.read_text()
    candidates = harvest_term_urls(index_html)
    print(f"harvested {len(candidates)} term URLs from index", file=sys.stderr)

    session = requests.Session()
    session.headers.update(
        {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    )

    terms = []
    for i, (term, url) in enumerate(candidates, start=1):
        try:
            definition = fetch_term_definition(url, session)
        except Exception as e:
            print(f"  [{i}/{len(candidates)}] FAIL {term}: {e}", file=sys.stderr)
            time.sleep(PER_TERM_DELAY_S)
            continue
        if not definition:
            print(f"  [{i}/{len(candidates)}] EMPTY {term} (no article p)", file=sys.stderr)
            time.sleep(PER_TERM_DELAY_S)
            continue
        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": url,
                "notes": "",
            }
        )
        if i % 25 == 0:
            print(f"  [{i}/{len(candidates)}] {term}", file=sys.stderr)
        time.sleep(PER_TERM_DELAY_S)

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
        f.write("# Bitsight Cybersecurity Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Bitsight Technologies, Inc.; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
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
    terms = parse()
    write_md(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Extracted {len(terms)} terms")


if __name__ == "__main__":
    main()
