#!/usr/bin/env python3
"""Extract the Barracuda Networks glossary (https://www.barracuda.com/support/glossary)
into the canonical glossary schema ({term, definition, source_anchor, notes}) as
glossary-terms.csv / .json.

Page architecture: the /support/glossary index is an AEM page whose term list is
client-rendered, so the individual term pages are enumerated from the site
sitemap.xml (the /support/glossary/<slug> URLs). Each term page is
server-rendered with a clean <h1> (the term) and a schema.org Article
`description` (a one-sentence definition, identical to the meta description) —
the "meta-description tier" also used for the Forescout glossary. A minority of
pages have an empty Article description and only marketing-promo body text; for
those, when ANTHROPIC_API_KEY is set, the definition is distilled from the page
body prose via Claude (BARRACUDA_AI_MODEL) as a last resort — otherwise the page
is skipped.

Usage: python3 extract_barracuda_glossary.py
Requires network access (fetches the sitemap + one request per term page);
the AI fallback additionally requires ANTHROPIC_API_KEY.
"""
import csv
import gzip
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.request
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "glossary"
SITEMAP = "https://www.barracuda.com/sitemap.xml"
TERM_RE = re.compile(r"https://www\.barracuda\.com/support/glossary/[a-z0-9][a-z0-9-]+")
UA = "Mozilla/5.0 (compatible; CSA-internal-research)"

# Most term pages carry a curated schema.org Article description (used verbatim).
# A minority have an empty description and only marketing-promo body text; for
# those, when ANTHROPIC_API_KEY is set, the real definition is distilled from the
# page's body prose via Claude (it ignores the nav/promo noise). Model overridable.
AI_MODEL = os.environ.get("BARRACUDA_AI_MODEL", "claude-sonnet-4-6")
_DISTILL_SYSTEM = (
    "You extract a concise, neutral, dictionary-style definition of a TERM from "
    "the raw body text of a vendor web page. The page text includes navigation, "
    "marketing promos, and calls to action — ignore all of that and use only the "
    "sentences that actually define or explain the term. Return 1-3 plain "
    "sentences defining the term: no marketing, no product/company names "
    "(Barracuda, BarracudaONE, etc.), no calls to action. If the page contains no "
    "real definition of the term, return exactly NONE. Return ONLY the definition "
    "text (or NONE), no preamble, no quotes, no markdown."
)


def fetch(url: str) -> str:
    # Barracuda's CDN gzips responses regardless of Accept-Encoding, and urllib
    # does not auto-decompress — so decode by Content-Encoding explicitly.
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        enc = (r.headers.get("Content-Encoding") or "").lower()
    if enc == "gzip":
        raw = gzip.decompress(raw)
    elif enc == "deflate":
        raw = zlib.decompress(raw)
    return raw.decode("utf-8", "replace")


def term_urls() -> list[str]:
    sm = fetch(SITEMAP)
    urls = sorted(set(TERM_RE.findall(sm)))
    # drop the index page itself if present
    return [u for u in urls if not u.rstrip("/").endswith("/glossary")]


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", s))).strip()


_LEAD = re.compile(r"^(what\s+(?:is|are)\s+(?:(?:a|an|the)\s+)?|what's\s+(?:(?:a|an|the)\s+)?)", re.I)


def clean_term(h1_html: str) -> str:
    """Reduce an SEO-article <h1> to a bare glossary term.

    Most term pages already have a clean <h1> ('Account Takeover'); a few use
    article titles ('What is cloud WAF: Use case and benefits', 'EDR vs. XDR:
    Understand the Key Differences'). Strip a leading 'What is/are ...', a
    trailing '?', and any ': subtitle' tail — leaving 'Cloud WAF', 'EDR vs. XDR'.
    """
    t = strip_tags(h1_html)
    t = _LEAD.sub("", t).strip()
    t = t.split(": ", 1)[0].strip()      # drop ': subtitle' tail
    t = re.sub(r"\?+\s*$", "", t).strip()
    return t


def body_paragraphs(page: str) -> str:
    """Concatenate the page's substantial <p> text (definition prose + promo noise)."""
    ps = [strip_tags(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", page, re.S)]
    return " ".join(p for p in ps if len(p) > 60)


def make_ai_client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set — curated-description tier only.", file=sys.stderr)
        return None
    try:
        import anthropic
    except ImportError:
        print("anthropic SDK not installed — curated-description tier only.", file=sys.stderr)
        return None
    return anthropic.Anthropic()


def distill(client, term: str, body: str) -> str | None:
    try:
        resp = client.messages.create(
            model=AI_MODEL,
            max_tokens=400,
            system=_DISTILL_SYSTEM,
            messages=[{"role": "user", "content": f"TERM: {term}\n\nPAGE TEXT:\n{body[:8000]}"}],
        )
        out = re.sub(r"\s+", " ", "".join(b.text for b in resp.content if b.type == "text")).strip()
        return None if not out or out.upper() == "NONE" else out
    except Exception as e:
        print(f"  AI distill failed for {term!r}: {e}", file=sys.stderr)
        return None


def parse_term(url: str, page: str, client=None) -> dict | None:
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    term = clean_term(h1.group(1)) if h1 else ""
    definition, src = "", ""
    for block in re.findall(r'type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S):
        try:
            d = json.loads(block)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") == "Article" and d.get("description"):
            definition = htmllib.unescape(d["description"]).strip()
            src = "schema.org Article description (curated meta-description tier)"
            break
    if not definition:  # fall back to meta description
        m = re.search(r'<meta name="description" content="([^"]*)"', page)
        if m and m.group(1).strip():
            definition = htmllib.unescape(m.group(1)).strip()
            src = "meta description"
    if not definition and term and client:  # last resort: AI-distil from body prose
        d = distill(client, term, body_paragraphs(page))
        if d:
            definition, src = d, f"ai_distilled_from_body ({AI_MODEL})"
    if not term or not definition:
        return None
    return {
        "term": term,
        "definition": definition,
        "source_anchor": url,
        "notes": f"definition from {src}",
    }


def main() -> None:
    client = make_ai_client()
    urls = term_urls()
    print(f"{len(urls)} glossary term URLs from sitemap", file=sys.stderr)
    rows, misses = [], []
    for i, u in enumerate(urls, 1):
        try:
            row = parse_term(u, fetch(u), client)
        except Exception as e:
            row = None
            print(f"  [{i}] ERROR {u}: {e}", file=sys.stderr)
        if row:
            rows.append(row)
        else:
            misses.append(u)
        time.sleep(0.4)  # be polite
        if i % 25 == 0:
            print(f"  {i}/{len(urls)} ...", file=sys.stderr)
    rows.sort(key=lambda r: r["term"].lower())
    (HERE / f"{PREFIX}-terms.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (HERE / f"{PREFIX}-terms.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} terms to {PREFIX}-terms.json / .csv ({len(misses)} skipped)", file=sys.stderr)
    if misses:
        print("skipped:", ", ".join(u.rsplit('/', 1)[-1] for u in misses), file=sys.stderr)


if __name__ == "__main__":
    main()
