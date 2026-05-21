#!/usr/bin/env python3
"""Extract the Slovak NBU Krátky slovník hybridných hrozieb into structured CSV/JSON.

Source: https://www.nbu.gov.sk/kratky-slovnik-hybridnych-hrozieb/
License: Slovak government work — no proprietary copyright notice; Slovak
public-authority output is generally redistributable as state-authored content.

The page is JS-rendered (curl returns only the skeleton), so this script reads
from a `_rendered-terms.json` snapshot captured via chrome-devtools-mcp. To
refresh:

  1. Open the URL in chrome-devtools-mcp / Playwright / Chrome.
  2. Run in the console:

       const results = [];
       document.querySelectorAll('strong, b').forEach(s => {
         const term = s.textContent.trim();
         if (!term || !/^[A-Z]/.test(term)) return;
         const parent = s.closest('p') || s.parentElement;
         if (!parent) return;
         const fullText = parent.textContent.trim();
         const idx = fullText.indexOf(term);
         if (idx < 0) return;
         let def = fullText.slice(idx + term.length).trim().replace(/^[\\s:\\-–—.,]+/, '');
         const m = def.match(/^\\(anglický ekvivalent:\\s*([^)]+)\\)\\s*/i);
         let englishEquivalent = '';
         if (m) { englishEquivalent = m[1].trim(); def = def.slice(m[0].length).trim(); }
         if (def.length < 10) return;
         results.push({term, englishEquivalent, definition: def});
       });
       JSON.stringify(results);

  3. Save the array as `_rendered-terms.json` in this directory.
  4. Re-run this script.

The terms are Slovak with English equivalents recorded in the notes field.

Produces:
  slovnik-hybridnych-hrozieb.md
  slovnik-hybridnych-hrozieb-terms.csv  (term,definition,source_anchor,notes)
  slovnik-hybridnych-hrozieb-terms.json
"""

import csv
import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "slovnik-hybridnych-hrozieb"
RENDERED = OUT_DIR / "_rendered-terms.json"
SOURCE_URL = "https://www.nbu.gov.sk/kratky-slovnik-hybridnych-hrozieb/"


def slugify(term):
    # Slovak diacritics get folded for the anchor
    folded = re.sub(r"[^a-zA-Z0-9]+", "-", term.lower().encode("ascii", "ignore").decode()).strip("-")
    return folded


def load_terms():
    if not RENDERED.exists():
        raise SystemExit(
            f"Missing {RENDERED}. The NBU page is JS-rendered; recapture via "
            "chrome-devtools-mcp (see this file's docstring)."
        )
    with open(RENDERED) as f:
        data = json.load(f)
    out = []
    for d in data:
        term = d.get("term", "").strip()
        definition = d.get("definition", "").strip()
        english = d.get("englishEquivalent", "").strip()
        if not term or not definition:
            continue
        notes = f"english equivalent: {english}" if english else ""
        out.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
            "notes": notes,
        })
    return out


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Krátky slovník hybridných hrozieb (Slovak NBU)\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: Slovak government work (state-authored content, generally redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["notes"]:
                f.write(f"*{t['notes']}*\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(terms)
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    with open(path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
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
