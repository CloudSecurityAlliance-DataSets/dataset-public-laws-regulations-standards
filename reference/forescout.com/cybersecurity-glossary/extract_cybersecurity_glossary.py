#!/usr/bin/env python3
"""Extract the Forescout Cybersecurity Glossary into CSV/JSON/MD.

Source:  https://www.forescout.com/glossary/
License: LicenseRef-Vendor-Copyright (Forescout Technologies, Inc.; internal CSA use only — not redistributable).

Page architecture: the /glossary/ index is a JS-hydrated WordPress page whose
static HTML is only a shell and contains no terms (so there is no useful
.source-cache.html to commit here). The entries are a WordPress custom post
type ("glossary", rest_base "glossary") served by the site's public REST API.
This extractor pulls them straight from the API — no browser / JS rendering:

    GET https://www.forescout.com/wp-json/wp/v2/glossary?per_page=100

Each entry is a full SEO article, not a dictionary definition. When
ANTHROPIC_API_KEY is set, the fuller `content.rendered` article body (present on
~41 of 50 entries) is distilled into a clean, neutral dictionary-style
definition via Claude (model from FORESCOUT_AI_MODEL). The ~9 entries with no
article body — and any run without a key — fall back to the Yoast SEO meta
description (`yoast_head_json.description`), then the `excerpt`. `notes` records
which tier each definition came from, for provenance.

Produces:
  cybersecurity-glossary.md
  cybersecurity-glossary-terms.csv    (header: term,definition,source_anchor,notes)
  cybersecurity-glossary-terms.json

Re-running only needs network access to the REST API above; the extractor is
deterministic given the live API contents.
"""

import csv
import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.forescout.com/glossary/"
API_URL = "https://www.forescout.com/wp-json/wp/v2/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "cybersecurity-glossary"

# When ANTHROPIC_API_KEY is set, the fuller `content.rendered` article body
# (present on ~41 of 50 entries) is distilled into a clean dictionary-style
# definition via Claude. Entries with no substantial body — and any run without
# a key — fall back to the Yoast meta description. Model is overridable.
AI_MODEL = os.environ.get("FORESCOUT_AI_MODEL", "claude-sonnet-4-6")
_DISTILL_SYSTEM = (
    "You rewrite vendor cybersecurity-glossary articles into concise, neutral, "
    "dictionary-style definitions. Given a TERM and the SEO article written about "
    "it, return 1-3 plain sentences defining the term. Rules: define the term "
    "itself, not the vendor; no marketing, no calls to action, no product or "
    "company names (Forescout, etc.); no 'CYBERSECURITY A-Z' or section labels; "
    "start with the concept, not 'This article'. Return ONLY the definition text, "
    "no preamble, no quotes, no markdown."
)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)

# Leading interrogative phrasing to strip from SEO titles → the bare term.
_LEAD = re.compile(r"^(what\s+(?:is|are)\s+(?:(?:a|an|the)\s+)?|what's\s+(?:(?:a|an|the)\s+)?)", re.I)


def squish(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def html_text(html: str) -> str:
    return squish(BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True))


def clean_term(title_html: str) -> str:
    term = html_text(title_html)
    term = _LEAD.sub("", term).strip()
    term = re.sub(r"\?+\s*$", "", term).strip()  # drop trailing question marks
    return term


def clean_excerpt(excerpt_html: str) -> str:
    """Excerpt fallback: drop the leading 'CYBERSECURITY A-Z' section label."""
    text = html_text(excerpt_html)
    text = re.sub(r"^CYBERSECURITY\s+A-Z\s*", "", text, flags=re.I).strip()
    return text


def make_ai_client():
    """Return an Anthropic client if a key is configured, else None."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set — using Yoast meta descriptions only.", file=sys.stderr)
        return None
    try:
        import anthropic
    except ImportError:
        print("anthropic SDK not installed — using Yoast meta descriptions only.", file=sys.stderr)
        return None
    return anthropic.Anthropic()


def distill(client, term: str, article_text: str) -> str | None:
    """Distill a clean definition from the article body via Claude; None on failure."""
    body = article_text[:6000]
    try:
        resp = client.messages.create(
            model=AI_MODEL,
            max_tokens=400,
            system=_DISTILL_SYSTEM,
            messages=[{"role": "user", "content": f"TERM: {term}\n\nARTICLE:\n{body}"}],
        )
        out = squish("".join(b.text for b in resp.content if b.type == "text"))
        return out or None
    except Exception as e:  # network / API hiccup — caller falls back to Yoast
        print(f"  AI distill failed for {term!r}: {e}", file=sys.stderr)
        return None


def fetch_items(session: requests.Session) -> list[dict]:
    """Page through the glossary REST endpoint until exhausted."""
    items, page = [], 1
    while True:
        r = session.get(API_URL, params={"per_page": 100, "page": page}, timeout=30)
        if r.status_code == 400:  # WP returns 400 past the last page
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", "1"))
        if page >= total_pages:
            break
        page += 1
    return items


def parse(session: requests.Session, client=None) -> list[dict]:
    items = fetch_items(session)
    print(f"fetched {len(items)} glossary entries from REST API", file=sys.stderr)

    terms = []
    for it in items:
        term = clean_term(it.get("title", {}).get("rendered", ""))
        if not term:
            continue
        body = html_text(it.get("content", {}).get("rendered", ""))
        yoast = squish((it.get("yoast_head_json") or {}).get("description", ""))
        excerpt = clean_excerpt(it.get("excerpt", {}).get("rendered", ""))

        # Prefer a clean AI-distilled definition from the article body; fall
        # back to the Yoast meta description, then the excerpt.
        definition, src = None, None
        if client and len(body) > 200:
            d = distill(client, term, body)
            if d:
                definition, src = d, f"ai_distilled_from_content ({AI_MODEL})"
        if not definition and yoast:
            definition, src = yoast, "yoast_meta_description"
        if not definition and excerpt:
            definition, src = excerpt, "excerpt"
        if not definition:
            print(f"  SKIP (no definition): {term}", file=sys.stderr)
            continue
        terms.append({
            "term": term,
            "definition": definition,
            "source_anchor": it.get("link", SOURCE_URL),
            "notes": f"definition from {src}",
        })

    # Dedupe by term (keep the longer definition), then sort case-insensitively.
    by_term = {}
    for t in terms:
        key = t["term"].lower()
        cur = by_term.get(key)
        if cur is None or len(t["definition"]) > len(cur["definition"]):
            by_term[key] = t
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms: list[dict]) -> Path:
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Forescout Cybersecurity Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Forescout Technologies, Inc.; "
                "internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            f.write(f"Source: <{t['source_anchor']}>\n\n")
    return path


def write_csv(terms: list[dict]) -> Path:
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(terms)
    return path


def write_json(terms: list[dict]) -> Path:
    path = OUT_DIR / f"{PREFIX}-terms.json"
    with open(path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
    return path


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    client = make_ai_client()
    terms = parse(session, client)
    write_md(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Extracted {len(terms)} terms")


if __name__ == "__main__":
    main()
