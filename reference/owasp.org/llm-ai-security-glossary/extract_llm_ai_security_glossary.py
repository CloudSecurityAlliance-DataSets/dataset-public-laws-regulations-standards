#!/usr/bin/env python3
"""Extract the OWASP LLM & Generative AI Security Glossary.

Source: https://genai.owasp.org/glossary/
Each term is a <p><strong>[emoji] Term:</strong>&nbsp;definition...<a>source</a></p>
inside <main>. Some definitions span multiple <p> blocks; we group adjacent
paragraphs that do not begin with a new <strong> term as continuations.

Status markers in OWASP doc:
  - "✅" = Approved
  - "🔷" = Standard / proposed
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent
DIRNAME = "llm-ai-security-glossary"
SOURCE_URL = "https://genai.owasp.org/glossary/"

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"
RAW_HTML = HERE / "_source.html"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

STATUS_MAP = {
    "✅": "approved",
    "🔷": "standard",
}


def fetch_html() -> str:
    """Fetch the OWASP glossary HTML, preferring a local cache.

    OWASP's site occasionally rate-limits scripted requests; if _source.html
    is already present we read it directly. Otherwise we fetch and cache it.
    """
    if RAW_HTML.exists():
        return RAW_HTML.read_text(encoding="utf-8")
    resp = requests.get(SOURCE_URL, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    return resp.text


def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def parse_term_paragraph(p) -> tuple[str | None, str, str]:
    """Return (term, status, first-paragraph-body) or (None,'','') if not a term paragraph."""
    strong = p.find("strong", recursive=False)
    if not strong:
        # nested strong inside the first child
        strong = p.find("strong")
    if not strong:
        return None, "", ""
    strong_text = strong.get_text(strip=True)
    # Detect status marker
    status = ""
    for marker, name in STATUS_MAP.items():
        if strong_text.startswith(marker):
            status = name
            strong_text = strong_text[len(marker):].strip()
            break
    if not strong_text:
        # the strong was just the emoji — not a term header line
        return None, "", ""
    # Term = strong_text up to optional trailing colon
    term = strong_text.rstrip(":").strip()
    # Body = paragraph text after the strong element
    # Build by extracting all text after strong within p
    parts: list[str] = []
    found_strong = False
    for el in p.children:
        if not found_strong:
            if el is strong:
                found_strong = True
            continue
        if isinstance(el, NavigableString):
            parts.append(str(el))
        else:
            parts.append(el.get_text(" ", strip=False))
    body = " ".join(parts)
    body = re.sub(r"^[:\s\xa0]+", "", body)
    body = " ".join(body.split())
    return term, status, body


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup
    rows: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is not None:
            current["definition"] = " ".join(current["definition"].split()).strip()
            rows.append(current)
            current = None

    for p in main.find_all("p"):
        term, status, body = parse_term_paragraph(p)
        if term is not None:
            # Filter out non-term boilerplate strongs (status legend etc.)
            # Real entries have a non-empty body OR look like a clear glossary header.
            if not body and term.lower() in {"approved", "standard"}:
                continue
            flush()
            note_parts = []
            if status:
                note_parts.append(f"status: {status}")
            current = {
                "term": term,
                "definition": body,
                "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
                "notes": "; ".join(note_parts),
            }
        else:
            # continuation
            if current is not None:
                extra = p.get_text(" ", strip=True)
                if extra:
                    current["definition"] += " " + extra
    flush()

    # Drop obvious non-terms (header, footer)
    filtered = []
    for r in rows:
        t = r["term"].lower()
        if t in {"approved", "standard"}:
            continue
        # Drop very short entries with empty bodies
        if not r["definition"]:
            continue
        filtered.append(r)
    return filtered


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
        fh.write("# OWASP LLM & Generative AI Security Glossary\n\n")
        fh.write(f"Source: {SOURCE_URL}\n\n")
        fh.write(f"Total terms: {len(rows)}\n\n")
        for r in rows:
            fh.write(f"## {r['term']}\n\n")
            if r["definition"]:
                fh.write(f"{r['definition']}\n\n")
            if r["notes"]:
                fh.write(f"*{r['notes']}*\n\n")

    print(f"Wrote {len(rows)} rows.")


if __name__ == "__main__":
    main()
