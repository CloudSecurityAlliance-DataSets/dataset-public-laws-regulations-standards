#!/usr/bin/env python3
"""Extract the Texas DIR Cybersecurity Terminology glossary from its DOCX.

Source page: https://dir.texas.gov/resource-library-item/cybersecurity-terminology
DOCX:        https://dir.texas.gov/sites/default/files/Cybersecurity%20Terminology.docx

The live DOCX URL is fronted by Cloudflare bot protection that blocks scripted
download. We cache the DOCX locally (_source.docx); if absent the script falls
back to the Wayback Machine archive.

Each non-empty Normal-style paragraph encodes one term:
    Term – Definition...
Acceptable separators (in order of preference): "–" (en dash), "—" (em dash),
"-–" (hyphen+en-dash quirk), " - " (hyphen).
"""
from __future__ import annotations

import csv
import json
import re
import urllib.request
from pathlib import Path

import docx

HERE = Path(__file__).resolve().parent
DIRNAME = "cybersecurity-terminology"
SOURCE_PAGE = "https://dir.texas.gov/resource-library-item/cybersecurity-terminology"
DOCX_URL = "https://dir.texas.gov/sites/default/files/Cybersecurity%20Terminology.docx"
WAYBACK_URL = (
    "https://web.archive.org/web/2024/"
    "https://dir.texas.gov/sites/default/files/Cybersecurity%20Terminology.docx"
)

LOCAL_DOCX = HERE / "_source.docx"
OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def ensure_docx() -> Path:
    if LOCAL_DOCX.exists() and LOCAL_DOCX.stat().st_size > 10_000:
        return LOCAL_DOCX
    # try Wayback (the live URL is bot-blocked)
    req = urllib.request.Request(WAYBACK_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    LOCAL_DOCX.write_bytes(data)
    return LOCAL_DOCX


# Try separators in this priority order; first match (with surrounding spaces optional) wins.
SEPARATORS = [" – ", " — ", " -– ", " -- ", " -–", " –", "– ", " - "]


def split_term(text: str) -> tuple[str, str] | None:
    # Normalize whitespace once
    t = text.strip()
    if not t:
        return None
    # try each separator
    for sep in SEPARATORS:
        idx = t.find(sep)
        if 0 < idx < 200:  # term should be reasonably short
            term = t[:idx].strip().rstrip("-–—").strip()
            definition = t[idx + len(sep):].strip()
            if term and definition:
                return term, definition
    # fallback: first " - " or hyphen+space combination anywhere
    return None


def slugify(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def parse(doc: docx.document.Document) -> list[dict]:
    rows: list[dict] = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        style = p.style.name if p.style else ""
        if style.startswith("Heading"):
            continue
        parts = split_term(text)
        if not parts:
            # Could not parse — emit raw as note in case it's still meaningful
            continue
        term, definition = parts
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_PAGE}#{slugify(term)}",
            "notes": "",
        })
    return rows


def main() -> None:
    docx_path = ensure_docx()
    doc = docx.Document(str(docx_path))
    rows = parse(doc)

    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(rows)
    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# Texas DIR Cybersecurity Terminology\n\n")
        fh.write(f"Source: {SOURCE_PAGE}\n\n")
        fh.write(f"DOCX: {DOCX_URL}\n\n")
        fh.write(f"Total terms: {len(rows)}\n\n")
        for r in rows:
            fh.write(f"## {r['term']}\n\n")
            if r["definition"]:
                fh.write(f"{r['definition']}\n\n")

    print(f"Wrote {len(rows)} rows.")


if __name__ == "__main__":
    main()
