#!/usr/bin/env python3
"""Extract the VulnCheck Exploit Intelligence 101 glossary into CSV/JSON.

Source:  https://docs.vulncheck.com/kb
License: LicenseRef-Vendor-Copyright (VulnCheck Inc.; internal CSA use only).

Page structure: GitBook-style knowledge base page. Term entries are h3 elements
followed by a <p> with the definition. ~42 entries in a flat list.

Produces:
  vulncheck-glossary.md
  vulncheck-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  vulncheck-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://docs.vulncheck.com/kb"
OUT_DIR = Path(__file__).parent
PREFIX = "vulncheck-glossary"
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
    # Anchor on h3 elements; collect <p> elements within this h3 section before the next heading.
    for h3 in soup.select("h3"):
        term = re.sub(r"\s+blog/\S+$", "", squish(h3.get_text(" ", strip=True)))
        if not term or len(term) > 200:
            continue
        ps = []
        for el in h3.next_elements:
            if el is h3 or el in h3.descendants:
                continue
            if getattr(el, "name", None) in ("h1", "h2", "h3", "h4"):
                break
            if getattr(el, "name", None) == "p":
                txt = squish(el.get_text(" ", strip=True))
                if txt:
                    ps.append(txt)
        if not ps:
            continue
        definition = " ".join(ps)
        if not definition or len(definition) < 30:
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
        f.write("# VulnCheck Exploit Intelligence Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (VulnCheck Inc.; internal CSA use only — not redistributable).\n\n")
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
