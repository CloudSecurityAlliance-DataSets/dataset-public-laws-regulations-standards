#!/usr/bin/env python3
"""Extract the Wikimedia Security Team / Definitions glossary.

Source: https://www.mediawiki.org/wiki/Wikimedia_Security_Team/Definitions
Fetched via the MediaWiki ?action=raw endpoint to get clean wikitext.

Wikitext uses MediaWiki definition-list syntax: lines starting with `;` mark
a term, with `:` separating term and definition (or definition on following
lines starting with `:`).
"""
from __future__ import annotations

import csv
import json
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRNAME = "security-team-definitions"

SOURCE_URL = (
    "https://www.mediawiki.org/w/index.php"
    "?title=Wikimedia_Security_Team/Definitions&action=raw"
)
PAGE_URL = "https://www.mediawiki.org/wiki/Wikimedia_Security_Team/Definitions"

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"
RAW_WIKITEXT = HERE / "_source.wikitext"


def strip_wikitext(s: str) -> str:
    """Remove basic wikitext markup, leaving plain text."""
    # [[link|display]] -> display, [[link]] -> link
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    # [http://url display] -> display
    s = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", s)
    # [http://url] -> (link)
    s = re.sub(r"\[(https?://\S+)\]", r"\1", s)
    # '''bold''' / ''italic'' -> text
    s = re.sub(r"'''([^']+)'''", r"\1", s)
    s = re.sub(r"''([^']+)''", r"\1", s)
    # category/template noise
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    return " ".join(s.split()).strip()


def fetch_wikitext() -> str:
    req = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": (
                "CSA-DataSets-Bot/0.1 "
                "(contact: systemautomation@cloudsecurityalliance.org)"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_definitions(wikitext: str) -> list[dict]:
    rows: list[dict] = []
    current_section: list[str] = []
    pending_term: str | None = None
    pending_def_parts: list[str] = []

    def flush() -> None:
        nonlocal pending_term, pending_def_parts
        if pending_term:
            definition = " ".join(strip_wikitext(p) for p in pending_def_parts).strip()
            anchor = (
                PAGE_URL + "#" + re.sub(r"[^A-Za-z0-9]+", "_", pending_term).strip("_")
            )
            note = ""
            if current_section:
                note = " > ".join(current_section)
            rows.append({
                "term": pending_term,
                "definition": definition,
                "source_anchor": anchor,
                "notes": f"section: {note}" if note else "",
            })
        pending_term = None
        pending_def_parts = []

    for line in wikitext.splitlines():
        line_rstrip = line.rstrip()

        # heading
        m = re.match(r"^(=+)\s*(.*?)\s*\1\s*$", line_rstrip)
        if m:
            flush()
            level = len(m.group(1))
            title = m.group(2).strip()
            # = level 1 (page title), == level 2 main section, === level 3 sub
            depth = level - 2  # convert so 0 = top section
            if depth < 0:
                continue
            current_section = current_section[:depth] + [title]
            continue

        # definition-list term: `;Term: definition` or `;Term`
        m = re.match(r"^;\s*(.*?)\s*$", line_rstrip)
        if m:
            flush()
            body = m.group(1)
            # split on first colon NOT inside [[ ]]
            # use a state machine
            depth = 0
            split_at: int | None = None
            for i, ch in enumerate(body):
                if ch == "[" and i + 1 < len(body) and body[i + 1] == "[":
                    depth += 1
                elif ch == "]" and i + 1 < len(body) and body[i + 1] == "]":
                    depth -= 1
                elif ch == ":" and depth == 0:
                    split_at = i
                    break
            if split_at is not None:
                term_part = body[:split_at].strip()
                def_part = body[split_at + 1:].strip()
                pending_term = strip_wikitext(term_part)
                if def_part:
                    pending_def_parts.append(def_part)
            else:
                pending_term = strip_wikitext(body)
            continue

        # continuation of a definition `:more text` (only when we have pending_term)
        m = re.match(r"^:\s*(.*?)\s*$", line_rstrip)
        if m and pending_term is not None:
            pending_def_parts.append(m.group(1))
            continue

        # blank line ends a definition
        if not line_rstrip.strip():
            flush()
            continue

        # other text within a definition (numbered list under "Examples", etc.) ignored
        if pending_term is None:
            continue
        # otherwise treat as continuation if line is indented or part of multi-line def
        pending_def_parts.append(line_rstrip.strip())

    flush()
    # Drop duplicate terms (same term + same definition)
    seen = set()
    deduped = []
    for r in rows:
        key = (r["term"].lower(), r["definition"].lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)
    return deduped


def main() -> None:
    wikitext = fetch_wikitext()
    RAW_WIKITEXT.write_text(wikitext, encoding="utf-8")
    rows = parse_definitions(wikitext)

    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(rows)

    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# Wikimedia Security Team — Definitions\n\n")
        fh.write(f"Source: {PAGE_URL}\n\n")
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
