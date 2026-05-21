#!/usr/bin/env python3
"""Extract the NCSC UK Glossary into structured CSV/JSON.

Source: https://www.ncsc.gov.uk/section/advice-guidance/glossary
License: UK Crown Copyright — Open Government Licence v3.0

The live NCSC site is heavily JS-rendered (the term list is an accordion-style
component populated client-side, with no usable inline term/definition pairs
in the initial HTML). This script reads a pre-rendered terms dump
(`_rendered-terms.json`) captured by browser automation. To refresh:

  1. Open https://www.ncsc.gov.uk/section/advice-guidance/glossary in a
     headless browser (Playwright/Puppeteer) and wait for the accordion to
     render.
  2. Run the following in the page console (or via page.evaluate):

        const buttons = document.querySelectorAll('button h3');
        const results = [];
        for (const h3 of buttons) {
          const button = h3.closest('button');
          if (!button) continue;
          const term = h3.textContent.trim();
          if (term === 'Popular Searches') continue;
          const panel = button.nextElementSibling;
          if (!panel) continue;
          // ...parse paragraphs, "Also known as", "See also"...
          results.push({term, definition, source_anchor, notes});
        }
        return JSON.stringify(results);

  3. Save the JSON to `_rendered-terms.json` in this directory.
  4. Re-run this script.

Produces:
  ncsc-glossary.md           — rendered markdown
  ncsc-glossary-terms.csv    — header: term,definition,source_anchor,notes
  ncsc-glossary-terms.json   — list of {term,definition,source_anchor,notes}
"""

import csv
import json
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "ncsc-glossary"
RENDERED = OUT_DIR / "_rendered-terms.json"


def load_terms():
    if not RENDERED.exists():
        raise SystemExit(
            "Missing _rendered-terms.json. The NCSC site is JS-rendered; "
            "re-capture the terms via headless browser (see this file's docstring)."
        )
    raw = RENDERED.read_text().strip()
    # The captured file may be a JSON-encoded string (i.e. the page.evaluate
    # result wrapped in quotes) or a bare JSON array. Handle both.
    if raw.startswith('"'):
        raw = json.loads(raw)
    if isinstance(raw, str):
        terms = json.loads(raw)
    else:
        terms = raw
    return terms


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# NCSC UK Glossary\n\n")
        f.write("Source: https://www.ncsc.gov.uk/section/advice-guidance/glossary\n\n")
        f.write("License: UK Crown Copyright — Open Government Licence v3.0\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t.get("notes"):
                f.write(f"*{t['notes']}*\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        w.writeheader()
        for t in terms:
            w.writerow({k: t.get(k, "") for k in ["term", "definition", "source_anchor", "notes"]})
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    out = [{k: t.get(k, "") for k in ["term", "definition", "source_anchor", "notes"]} for t in terms]
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return path


def main():
    terms = load_terms()
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
