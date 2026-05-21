#!/usr/bin/env python3
"""Extract the Virginia VITA Commonwealth of Virginia IT Glossary.

Source: https://www.vita.virginia.gov/policy--governance/governance/cov-it-glossary/
The index page lists 27 alphabetic subpages (123 + A through Z). Each subpage
contains a list of <li class="usa-collection__item"> blocks, each holding:
  - <h2>Term</h2>
  - <p><strong>(Context: ...</strong>)</p>     (optional)
  - <h5>Definition</h5>
  - <p>...</p>  (one or more definition paragraphs)
  - additional <p> blocks with source links (skipped in definition)
"""
from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
DIRNAME = "cov-it-glossary"

BASE = "https://www.vita.virginia.gov"
INDEX_URL = f"{BASE}/policy--governance/governance/cov-it-glossary/"
LETTERS = ["123"] + [chr(c) for c in range(ord("a"), ord("z") + 1)]

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"
CACHE_DIR = HERE / "_source_pages"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_letter(letter: str) -> str:
    CACHE_DIR.mkdir(exist_ok=True)
    cache = CACHE_DIR / f"{letter}.html"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    url = f"{INDEX_URL}{letter}/"
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    cache.write_text(resp.text, encoding="utf-8")
    return resp.text


def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


DETAIL_CACHE = HERE / "_source_pages" / "_detail"


def fetch_detail(href: str) -> str:
    """Fetch and cache a single per-term detail page used by the O letter."""
    DETAIL_CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9]+", "_", href).strip("_")
    cache = DETAIL_CACHE / f"{key}.html"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    url = href if href.startswith("http") else f"{BASE}{href}"
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    cache.write_text(resp.text, encoding="utf-8")
    time.sleep(0.4)
    return resp.text


def parse_letter(html: str, letter: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict] = []
    for item in soup.select("li.usa-collection__item"):
        h2 = item.find("h2")
        # Some letter pages (e.g., O) ship stub <h4 class="usa-collection__heading">
        # items that link to a per-term detail page; fetch the detail when needed.
        if not h2:
            stub_h = item.find("h4", class_="usa-collection__heading")
            stub_a = stub_h.find("a") if stub_h else None
            if not stub_a or not stub_a.get("href"):
                continue
            detail_html = fetch_detail(stub_a["href"])
            detail_soup = BeautifulSoup(detail_html, "html.parser")
            d_main = detail_soup.find("main") or detail_soup
            # Inject a synthetic wrapper to reuse parsing logic below
            # Build a "fake item" from detail page main: term h2 + p Context + h5 Definition + p
            fake = BeautifulSoup("<li></li>", "html.parser").li
            for tag in d_main.find_all(["h2", "h4", "h5", "p"]):
                fake.append(tag)
            item = fake
            h2 = item.find("h2")
            if not h2:
                continue
        term = " ".join(h2.get_text(" ", strip=True).split())
        if not term:
            continue
        # find Context line: a <p><strong>(Context: ...</strong>)</p>
        context = ""
        for p in item.find_all("p"):
            txt = p.get_text(" ", strip=True)
            if txt.lower().startswith("(context:"):
                # strip outer parens and label
                inside = txt.strip()
                inside = re.sub(r"^\(context:\s*", "", inside, flags=re.I)
                inside = inside.rstrip(")").strip()
                context = inside
                break
        # find Definition: locate h5 "Definition" and collect following <p>s until
        # we hit something that looks like a source link block (anchor-only paragraphs at the end).
        definition_parts: list[str] = []
        defin_header = item.find(lambda t: t.name in ("h5", "h4") and "definition" in t.get_text(strip=True).lower())
        if defin_header:
            # walk siblings until next h-tag
            for sib in defin_header.next_siblings:
                name = getattr(sib, "name", None)
                if name and re.match(r"h\d", name):
                    break
                if name == "p":
                    # treat as definition unless it is just one anchor (source link)
                    text = sib.get_text(" ", strip=True)
                    # check whether the whole paragraph is just one link
                    only_links = (
                        len(sib.find_all("a")) >= 1
                        and " ".join(a.get_text(" ", strip=True) for a in sib.find_all("a")).strip()
                        == text.strip()
                    )
                    if only_links and len(text) < 250:
                        # most likely a "source" link paragraph - skip
                        continue
                    if text:
                        definition_parts.append(text)
        definition = " ".join(definition_parts)
        definition = " ".join(definition.split()).strip()

        anchor_id = item.get("data-content-id") or slugify(term)
        anchor = f"{INDEX_URL}{letter}/#{anchor_id}"

        notes = f"context: {context}" if context else ""
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": anchor,
            "notes": notes,
        })
    return rows


def main() -> None:
    all_rows: list[dict] = []
    for letter in LETTERS:
        html = fetch_letter(letter)
        rows = parse_letter(html, letter)
        all_rows.extend(rows)
        # be polite
        time.sleep(0.5)
        print(f"  {letter}: {len(rows)} terms")

    OUT_JSON.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(all_rows)
    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# Commonwealth of Virginia IT Glossary (COV IT Glossary)\n\n")
        fh.write(f"Source: {INDEX_URL}\n\n")
        fh.write(f"Total terms: {len(all_rows)}\n\n")
        for r in all_rows:
            fh.write(f"## {r['term']}\n\n")
            if r["definition"]:
                fh.write(f"{r['definition']}\n\n")
            if r["notes"]:
                fh.write(f"*{r['notes']}*\n\n")

    print(f"Wrote {len(all_rows)} rows total.")


if __name__ == "__main__":
    main()
