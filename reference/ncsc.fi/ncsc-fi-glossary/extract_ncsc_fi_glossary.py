#!/usr/bin/env python3
"""Parse the NCSC-FI Glossary of Central Cyber Security Terms into per-term rows.

Source: https://www.traficom.fi/en/everyday-information-security/glossary-central-cyber-security-terms

Markdown structure (after HTML→markdown conversion):

    ## Term Name

    Definition paragraph 1.

    Optional definition paragraph 2.

    ## Next Term
    ...

Site chrome H2s ("On this page", "Footer", language-switcher placeholders)
are filtered out by a denylist.

Output: ncsc-fi-glossary-terms.{csv,json} — schema:
    term            human-readable term name
    definition      prose definition (whitespace-normalized)
    source_anchor   absolute URL to the page (no per-term anchors on source)
    notes           empty
"""
import csv
import json
import re
from pathlib import Path


SOURCE_URL = "https://www.traficom.fi/en/everyday-information-security/glossary-central-cyber-security-terms"
HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "ncsc-fi-glossary.md"

# H2s that are site chrome, not glossary terms.
CHROME_HEADINGS = {
    "on this page", "footer",
    "the national cyber security centre finland at the finnish transport and",
}


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    lines = md.splitlines()
    # Find all `## ` headings and slice
    rows = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("## "):
            heading = lines[i][3:].strip()
            # Multi-line H2 (heading wrapped across lines): join with next non-blank
            # if it's non-heading prose
            j = i + 1
            while (j < len(lines) and lines[j].strip()
                   and not lines[j].startswith("#")
                   and not lines[j].lstrip().startswith("*")
                   and len(lines[j].split()) < 10
                   and j == i + 1):
                # Conservative: only join one continuation line
                heading = heading + " " + lines[j].strip()
                j += 1
                break
            # Skip site chrome
            if heading.lower().strip() in CHROME_HEADINGS:
                i = j
                continue
            # Collect definition until next `## ` or end
            defn_lines = []
            k = j
            while k < len(lines):
                if lines[k].startswith("## "):
                    break
                defn_lines.append(lines[k])
                k += 1
            definition = "\n".join(defn_lines).strip()
            # Collapse runs of whitespace
            definition = re.sub(r"\s+", " ", definition).strip()
            if definition:
                rows.append({
                    "term": heading,
                    "definition": definition,
                    "source_anchor": SOURCE_URL,
                    "notes": "",
                })
            i = k
        else:
            i += 1

    stem = HERE.name
    csv_path = HERE / f"{stem}-terms.csv"
    json_path = HERE / f"{stem}-terms.json"
    fields = ["term", "definition", "source_anchor", "notes"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    print(f"Terms: {len(rows)}")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
