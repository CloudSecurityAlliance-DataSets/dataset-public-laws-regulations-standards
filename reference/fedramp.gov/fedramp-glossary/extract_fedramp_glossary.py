#!/usr/bin/env python3
"""Extract the FedRAMP Terminology Glossary into structured form.

Source: https://help.fedramp.gov/hc/en-us/articles/28857981903003-Terminology-Glossary
(retrieved via the Internet Archive snapshot dated 2025-10-02 because the
live help center is gated behind a Cloudflare interactive challenge that
non-browser clients cannot solve).

The glossary is a single Zendesk article whose body is a two-column
<table> with rows of (Term, Meaning). Some meanings are placeholders that
just point readers at the NIST Glossary (csrc.nist.gov/glossary); we
preserve those as a notes flag rather than as a real definition.

Outputs (written next to this script):
  - fedramp-glossary.md            human-readable markdown rendering
  - fedramp-glossary-terms.csv     term,definition,source_anchor,notes
  - fedramp-glossary-terms.json    list of dicts (same fields)
"""
from __future__ import annotations

import csv
import json
import re
import sys
import urllib.request
from html import unescape
from pathlib import Path

ARCHIVE_URL = (
    "http://web.archive.org/web/20251002031416/"
    "https://help.fedramp.gov/hc/en-us/articles/28857981903003-Terminology-Glossary"
)
LIVE_URL = (
    "https://help.fedramp.gov/hc/en-us/articles/28857981903003-Terminology-Glossary"
)

HERE = Path(__file__).resolve().parent
HTML_CACHE = HERE / ".source-cache.html"

NIST_GLOSSARY_REFERRAL_RE = re.compile(
    r"please\s+see\s+nist\s+glossary\s+definition", re.IGNORECASE
)
WAYBACK_PREFIX_RE = re.compile(r"https?://web\.archive\.org/web/\d+/")


def fetch_source(force: bool = False) -> str:
    if HTML_CACHE.exists() and not force:
        return HTML_CACHE.read_text(encoding="utf-8")
    req = urllib.request.Request(
        ARCHIVE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8", errors="replace")
    HTML_CACHE.write_text(body, encoding="utf-8")
    return body


def isolate_article_body(html: str) -> str:
    m = re.search(r'<article[^>]*class="article"[^>]*>(.*?)</article>', html, re.S)
    if not m:
        raise RuntimeError("article container not found in source HTML")
    body = m.group(1)
    m2 = re.search(r'class="article-body"[^>]*>(.*)', body, re.S)
    if m2:
        body = m2.group(1)
    return body


def strip_tags(fragment: str) -> str:
    """Convert an HTML fragment to plain text, preserving paragraph breaks."""
    # Drop wayback rewriter wrappers around hrefs
    fragment = WAYBACK_PREFIX_RE.sub("", fragment)
    # Replace block-level closers with newlines so paragraphs survive collapse.
    fragment = re.sub(r"</(p|div|li|br|tr)\s*>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    # Drop all remaining tags.
    fragment = re.sub(r"<[^>]+>", "", fragment)
    text = unescape(fragment)
    text = text.replace("\xa0", " ")
    # Collapse runs of whitespace within a line, but keep paragraph breaks.
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    cleaned = "\n".join(ln for ln in lines if ln)
    return cleaned.strip()


def slugify(term: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    return slug or "term"


def extract_rows(article_body: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for row_match in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", article_body, re.S | re.I):
        cells = re.findall(
            r"<td\b[^>]*>(.*?)</td>", row_match.group(1), re.S | re.I
        )
        if len(cells) < 2:
            continue
        term = strip_tags(cells[0])
        meaning = strip_tags(cells[1])
        rows.append((term, meaning))
    return rows


def classify(term: str, meaning: str) -> tuple[str, str]:
    """Return (definition, notes).

    For rows where the meaning is a referral to the NIST Glossary, we keep
    `definition` empty and record the referral in `notes`.
    """
    if not meaning:
        return "", "empty meaning cell in source"
    if NIST_GLOSSARY_REFERRAL_RE.search(meaning.replace("\n", " ")):
        return "", "see NIST Glossary (https://csrc.nist.gov/glossary)"
    return meaning, ""


def is_header_row(term: str, meaning: str) -> bool:
    t = term.strip().lower()
    m = meaning.strip().lower()
    return t == "term" and m == "meaning"


def is_blank_row(term: str, meaning: str) -> bool:
    return not term.strip() and not meaning.strip()


def build_records(rows: list[tuple[str, str]]) -> list[dict]:
    records: list[dict] = []
    seen_slugs: dict[str, int] = {}
    for term, meaning in rows:
        if is_header_row(term, meaning) or is_blank_row(term, meaning):
            continue
        if not term.strip():
            # Orphaned meaning with no term — skip but keep visible in logs.
            print(f"WARN: skipping row with empty term, meaning={meaning!r}",
                  file=sys.stderr)
            continue
        definition, notes = classify(term, meaning)
        base = slugify(term)
        n = seen_slugs.get(base, 0) + 1
        seen_slugs[base] = n
        anchor = base if n == 1 else f"{base}-{n}"
        records.append(
            {
                "term": term.strip(),
                "definition": definition,
                "source_anchor": anchor,
                "notes": notes,
            }
        )
    return records


def write_csv(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        w.writeheader()
        for r in records:
            w.writerow(r)


def write_json(records: list[dict], path: Path) -> None:
    path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_markdown(records: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# FedRAMP Terminology Glossary")
    lines.append("")
    lines.append(f"Source: {LIVE_URL}")
    lines.append(
        f"Extraction source (Cloudflare-gated live page; archived snapshot used): "
        f"{ARCHIVE_URL}"
    )
    lines.append("")
    lines.append(
        "Some terms in the source table do not carry their own FedRAMP "
        "definition and instead defer to the [NIST Glossary]"
        "(https://csrc.nist.gov/glossary). Those rows are preserved here "
        "with an empty definition and a note."
    )
    lines.append("")
    lines.append(f"Total terms: **{len(records)}**")
    lines.append("")
    lines.append("| Term | Definition | Notes |")
    lines.append("|------|------------|-------|")
    for r in records:
        term_cell = r["term"].replace("|", "\\|")
        # Markdown tables can't contain newlines inside cells — flatten.
        defn_cell = r["definition"].replace("|", "\\|").replace("\n", " ")
        notes_cell = r["notes"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {term_cell} | {defn_cell} | {notes_cell} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch_source()
    body = isolate_article_body(html)
    rows = extract_rows(body)
    records = build_records(rows)

    write_markdown(records, HERE / "fedramp-glossary.md")
    write_csv(records, HERE / "fedramp-glossary-terms.csv")
    write_json(records, HERE / "fedramp-glossary-terms.json")

    print(f"extracted {len(records)} terms")
    referral = sum(1 for r in records if r["notes"].startswith("see NIST"))
    print(f"  with own FedRAMP definition: {len(records) - referral}")
    print(f"  deferring to NIST Glossary:  {referral}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
