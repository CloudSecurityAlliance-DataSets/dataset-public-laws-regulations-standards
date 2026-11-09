#!/usr/bin/env python3
"""Extract the Microsoft Security Response Center (MSRC) Glossary into CSV/JSON.

Source:  https://www.microsoft.com/en-us/msrc/glossary
License: LicenseRef-Vendor-Copyright (Microsoft Corporation; internal CSA use only).

Page structure: AEM-rendered single page. Inside <main>, the glossary body is a
flat sequence of <h4>Term Name</h4><p>Definition</p> pairs grouped under
single-letter <h2>A</h2><h2>B</h2>… section markers. The page also contains some
synthetic h4 elements outside the term body (UI chrome); we anchor on h4 whose
following sibling is a <p> with non-trivial text to filter those out.

Produces:
  msrc-glossary.md
  msrc-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  msrc-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.microsoft.com/en-us/msrc/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "msrc-glossary"
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
    main = soup.find("main") or soup
    terms = []
    for h4 in main.select("h4"):
        term = squish(h4.get_text(" ", strip=True))
        if not term or len(term) > 200:
            continue
        parts = []
        for el in h4.next_elements:
            if el is h4 or el in h4.descendants:
                continue
            if getattr(el, "name", None) in ("h1", "h2", "h3", "h4"):
                break
            if getattr(el, "name", None) in ("p", "li"):
                if el.name == "p" and el.find_parent("li") is not None:
                    continue
                txt = squish(el.get_text(" ", strip=True))
                if txt:
                    parts.append(f"- {txt}" if el.name == "li" else txt)
        if not parts:
            continue
        definition = " ".join(parts)
        if not definition or len(definition) < 20:
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
        f.write("# Microsoft Security Response Center (MSRC) Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Microsoft Corporation; internal CSA use only — not redistributable).\n\n")
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
