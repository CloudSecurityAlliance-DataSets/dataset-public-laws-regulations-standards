#!/usr/bin/env python3
"""Extract the CCDCOE Cyber Law Toolkit Glossary into structured CSV/JSON.

Source: https://cyberlaw.ccdcoe.org/wiki/Glossary
License: CC-BY-SA-4.0 (per the MediaWiki footer on the source page)

The CCDCOE site sits behind anti-bot protection that blocks plain WebFetch.
We capture the rendered DOM via chrome-devtools-mcp (an evaluate_script that
walks the MediaWiki dl/dt/dd structure) and save the term/definition pairs as
`_rendered-terms.json`. This script reads that cached file so subsequent runs
do not need a headless browser. To refresh the snapshot:

  1. Open https://cyberlaw.ccdcoe.org/wiki/Glossary in a real browser
     (chrome-devtools-mcp, Playwright, or manual).
  2. Run in the console:

       const out = [];
       document.querySelectorAll('dl dt').forEach(dt => {
         const term = dt.textContent.trim();
         const dd = dt.nextElementSibling;
         if (dd && dd.tagName === 'DD') out.push({term, def: dd.textContent.trim()});
       });
       JSON.stringify(out)

  3. Save the output array to `_rendered-terms.json` in this directory.
  4. Re-run this script.

Produces:
  glossary.md
  glossary-terms.csv  (term,definition,source_anchor,notes)
  glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "glossary"
RENDERED = OUT_DIR / "_rendered-terms.json"
SOURCE_URL = "https://cyberlaw.ccdcoe.org/wiki/Glossary"


def slugify(term):
    return re.sub(r"[^a-zA-Z0-9]+", "_", term).strip("_")


def load_terms():
    if not RENDERED.exists():
        raise SystemExit(
            f"Missing {RENDERED}. The CCDCOE site is JS-rendered behind anti-bot; "
            "re-capture the term list via headless browser (see this file's docstring)."
        )
    with open(RENDERED) as f:
        data = json.load(f)
    # The captured dump uses {term, def} keys; normalize to the standard schema.
    out = []
    for d in data:
        term = d.get("term", "").strip()
        definition = d.get("def", d.get("definition", "")).strip()
        if not term or not definition:
            continue
        out.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
            "notes": "",
        })
    return out


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# CCDCOE Cyber Law Toolkit Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: CC-BY-SA-4.0.\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
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
