#!/usr/bin/env python3
"""Extract the Washington State AG Office Glossary of Data Breach Terms.

Source: https://www.atg.wa.gov/glossary-data-breach-terms
Each term is in <div class="termWrapper" id="..."> with a termHeader
(term) and termDescription (definition) child div.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
DIRNAME = "data-breach-glossary"
SOURCE_URL = "https://www.atg.wa.gov/glossary-data-breach-terms"

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"
RAW_HTML = HERE / "_source.html"


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_html() -> str:
    resp = requests.get(SOURCE_URL, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    return resp.text


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict] = []
    for wrapper in soup.select("div.termWrapper"):
        header = wrapper.select_one("div.termHeader")
        desc = wrapper.select_one("div.termDescription")
        if not header:
            continue
        term = " ".join(header.get_text(" ", strip=True).split())
        if not term:
            continue
        definition = (
            " ".join(desc.get_text(" ", strip=True).split()) if desc else ""
        )
        anchor_id = wrapper.get("id", "")
        anchor = f"{SOURCE_URL}#{anchor_id}" if anchor_id else SOURCE_URL
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": anchor,
            "notes": "",
        })
    return rows


def main() -> None:
    html = fetch_html()
    RAW_HTML.write_text(html, encoding="utf-8")
    rows = parse(html)

    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(rows)

    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# Washington State AG — Glossary of Data Breach Terms\n\n")
        fh.write(f"Source: {SOURCE_URL}\n\n")
        fh.write(f"Total terms: {len(rows)}\n\n")
        for r in rows:
            fh.write(f"## {r['term']}\n\n")
            if r["definition"]:
                fh.write(f"{r['definition']}\n\n")

    print(f"Wrote {len(rows)} rows.")


if __name__ == "__main__":
    main()
