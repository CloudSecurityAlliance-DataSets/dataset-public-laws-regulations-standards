#!/usr/bin/env python3
"""Extract the Apple Platform Security Glossary into CSV/JSON.

Source:  https://support.apple.com/guide/security/glossary-sec93292bfa6/web
License: LicenseRef-Vendor-Copyright (Apple Inc.; internal CSA use only).

Page structure: a single <dl> with 60 <dt>/<dd> pairs. Same template shape as
the AWS glossary.

Produces:
  platform-security-glossary.md
  platform-security-glossary-terms.csv  (header: term,definition,source_anchor,notes)
  platform-security-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://support.apple.com/guide/security/glossary-sec93292bfa6/web"
OUT_DIR = Path(__file__).parent
PREFIX = "platform-security-glossary"
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


def squish(s):
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for dl in soup.select("dl"):
        # Iterate dt/dd siblings inside dl.
        for dt in dl.find_all("dt"):
            term = squish(dt.get_text(" ", strip=True))
            if not term:
                continue
            dd = dt.find_next_sibling("dd")
            if not dd:
                continue
            definition = squish(dd.get_text(" ", strip=True))
            if not definition:
                continue
            anchor = f"{SOURCE_URL}#{slug(term)}"
            terms.append(
                {
                    "term": term,
                    "definition": definition,
                    "source_anchor": anchor,
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
        f.write("# Apple Platform Security Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Apple Inc.; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
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
    html = fetch()
    terms = parse(html)
    write_md(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Extracted {len(terms)} terms")


if __name__ == "__main__":
    main()
