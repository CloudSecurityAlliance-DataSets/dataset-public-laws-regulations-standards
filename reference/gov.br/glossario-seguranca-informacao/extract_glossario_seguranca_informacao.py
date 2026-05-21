#!/usr/bin/env python3
"""Extract the Brazilian GSI/PR Glossário de Segurança da Informação.

Source: https://www.gov.br/gsi/pt-br/seguranca-da-informacao-e-cibernetica/glossario-de-seguranca-da-informacao-1
License: CC-BY-ND-3.0 (no-derivatives — content stored verbatim).

The portal renders an A-Z tab interface where each letter's content is loaded
from a sibling URL (`.../glossario-de-seguranca-da-informacao-1/{letter}`).
Within each letter page, terms are rendered as `<p class="dou-paragraph">`
nodes containing one `<strong>` (or `<em><strong>`) with the term, followed
by a hyphen and the verbatim Portuguese definition.

Outputs (written next to this script):
  - glossario-seguranca-informacao.md
  - glossario-seguranca-informacao-terms.csv  (term, definition, source_anchor, notes)
  - glossario-seguranca-informacao-terms.json
"""

from __future__ import annotations

import csv
import json
import re
import string
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_URL = (
    "https://www.gov.br/gsi/pt-br/seguranca-da-informacao-e-cibernetica/"
    "glossario-de-seguranca-da-informacao-1"
)

# Letters offered by the tab UI (A-Z plus a "2" group seen in the page header).
LETTERS = list(string.ascii_uppercase) + ["2"]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

HERE = Path(__file__).resolve().parent


def fetch(url: str, retries: int = 3, sleep: float = 2.0) -> str:
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.5"}
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if attempt < retries:
                time.sleep(sleep * attempt)
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


# Match the term/definition boundary. The first <strong> in the paragraph
# carries the term; the textual hyphen that follows separates term from gloss.
# Some entries use a regular hyphen "-", some an en-dash, em-dash, or a NBSP.
SEPARATORS = re.compile(r"\s*[‐-―\-]\s*")


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).replace("\xa0", " ").strip()


def split_term_definition(p: Tag) -> tuple[str, str] | None:
    """Return (term, definition) for a glossary <p>, or None if not parseable.

    Strategy: the term is the visible text of the leading <strong>/<em><strong>.
    Whatever follows in the paragraph is the definition. We strip a leading
    separator (hyphen + spaces) from the definition because the visual format
    is uniformly "TERM - definition".
    """
    # First non-empty inline node should be a <strong> (possibly inside <em>).
    head = None
    for child in p.children:
        if isinstance(child, NavigableString):
            if collapse_ws(str(child)):
                # Leading text before any <strong> — not a normal entry.
                return None
            continue
        if isinstance(child, Tag):
            head = child
            break
    if head is None:
        return None

    # Drill into <em><strong>...</strong></em> if needed.
    strong = head if head.name == "strong" else head.find("strong")
    if strong is None:
        return None

    term = collapse_ws(strong.get_text(" ", strip=True))
    if not term:
        return None

    # Definition = the paragraph text minus the leading <strong>/<em>-<strong> wrapper.
    # Easiest: clone the paragraph, remove the head element, take remaining text.
    p_copy = BeautifulSoup(str(p), "html.parser").p
    if p_copy is None:
        return None
    # remove first inline tag (the term wrapper)
    first_tag = None
    for ch in p_copy.children:
        if isinstance(ch, Tag):
            first_tag = ch
            break
    if first_tag is not None:
        first_tag.decompose()
    definition = collapse_ws(p_copy.get_text(" ", strip=True))
    # Strip a single leading separator (hyphen with surrounding whitespace).
    definition = SEPARATORS.sub("", definition, count=1) if SEPARATORS.match(definition) else definition
    # Many entries end with a semicolon (DOU style) — keep it verbatim per CC-BY-ND.
    return term, definition


def parse_letter(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(id="parent-fieldname-text") or soup
    out: list[tuple[str, str]] = []
    for p in container.find_all("p", class_="dou-paragraph"):
        pair = split_term_definition(p)
        if pair is None:
            continue
        term, definition = pair
        if not term or not definition:
            continue
        # The header line is "PORTARIA GSI/PR ..." inside an <h3>, so it won't be a <p>.
        out.append((term, definition))
    return out


def main() -> int:
    all_entries: list[dict] = []
    per_letter_md: dict[str, list[tuple[str, str]]] = {}

    for letter in LETTERS:
        url = f"{BASE_URL}/{letter.lower()}"
        try:
            html = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] {letter}: {exc}", file=sys.stderr)
            continue
        entries = parse_letter(html)
        if not entries:
            # Some letters legitimately have no terms (K, W, X, Y, Z, 2 may be empty).
            print(f"[info] {letter}: 0 entries", file=sys.stderr)
            per_letter_md[letter] = []
            continue
        per_letter_md[letter] = entries
        for term, definition in entries:
            all_entries.append(
                {
                    "term": term,
                    "definition": definition,
                    "source_anchor": url,
                    "notes": "",
                }
            )
        print(f"[info] {letter}: {len(entries)} entries", file=sys.stderr)

    # Write CSV
    csv_path = HERE / "glossario-seguranca-informacao-terms.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        writer.writeheader()
        writer.writerows(all_entries)

    # Write JSON
    json_path = HERE / "glossario-seguranca-informacao-terms.json"
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(all_entries, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    # Write Markdown (verbatim definitions, grouped by letter)
    md_path = HERE / "glossario-seguranca-informacao.md"
    with md_path.open("w", encoding="utf-8") as fh:
        fh.write("# Glossário de Segurança da Informação\n\n")
        fh.write(
            "Fonte: Gabinete de Segurança Institucional da Presidência da República "
            "(GSI/PR), Portaria GSI/PR nº 93, de 18 de outubro de 2021, e atualizações "
            "posteriores publicadas em "
            f"<{BASE_URL}>.\n\n"
        )
        fh.write(
            "Licença: CC-BY-ND-3.0. Definições reproduzidas verbatim; nenhuma alteração "
            "editorial foi aplicada.\n\n"
        )
        fh.write(f"Total de termos: {len(all_entries)}.\n\n")
        for letter in LETTERS:
            entries = per_letter_md.get(letter, [])
            if not entries:
                continue
            fh.write(f"## {letter}\n\n")
            for term, definition in entries:
                fh.write(f"**{term}** — {definition}\n\n")

    print(f"[done] {len(all_entries)} terms")
    print(f"[done] wrote {csv_path}")
    print(f"[done] wrote {json_path}")
    print(f"[done] wrote {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
