#!/usr/bin/env python3
"""Parse FIPS 199 (Standards for Security Categorization) into structured CSV/JSON.

FIPS 199 defines a 3 x 3 security-categorization matrix:

  Security objectives  : Confidentiality, Integrity, Availability
  Potential impact     : LOW, MODERATE, HIGH

Each (objective, level) cell is described by Table 1 in the document. The source
markdown's rendering of Table 1 has heavy PDF-layout artifacts (cells broken
across many sub-rows), so we synthesize the matrix from the more-reliable prose
sections that define each objective and each impact level separately.

The output captures the 9-cell matrix plus the underlying objective definitions
and level qualifiers so downstream consumers can reason about either axis.

Outputs (alongside fips-199.md):
  fips-199-criteria.csv / .json  — one row per (objective, level) pair, 9 rows
"""
import csv
import json
import re
from pathlib import Path


def main():
    here = Path(__file__).parent
    md_path = here / "fips-199.md"
    csv_path = here / "fips-199-criteria.csv"
    json_path = here / "fips-199-criteria.json"

    md = md_path.read_text(encoding="utf-8")

    # The three security objectives are defined in headed sections in the
    # markdown:
    #   #### **CONFIDENTIALITY**
    #   "<definition>" [44 U.S.C., Sec. 3542]
    #   A loss of *confidentiality* is the <loss_meaning>.
    def grab_objective(name):
        # Find the heading; then scan forward for the quoted definition and the
        # "A loss of *...* is ..." sentence. Tolerate smart quotes, HR rules,
        # and intervening blank lines.
        heading = re.search(rf"####\s+\*\*{name}\*\*", md, re.IGNORECASE)
        if not heading:
            raise SystemExit(f"Could not find heading: {name}")
        tail = md[heading.end():heading.end() + 1500]
        def_m = re.search(r'["“]([^"”]+)["”…]', tail)
        loss_m = re.search(r"A loss of \*[a-z]+\* is\s+([^.\n]+)\.", tail, re.IGNORECASE)
        if not def_m or not loss_m:
            raise SystemExit(f"Could not extract def/loss for: {name}")
        definition = re.sub(r"\s+", " ", def_m.group(1)).strip()
        definition = re.sub(r"[.…]+$", "", definition) + "."
        loss_meaning = re.sub(r"\s+", " ", loss_m.group(1)).strip() + "."
        return definition, loss_meaning

    objectives = {}
    for name in ("CONFIDENTIALITY", "INTEGRITY", "AVAILABILITY"):
        d, lm = grab_objective(name)
        objectives[name.title()] = {"definition": d, "loss_meaning": lm}

    # The three impact levels are defined in nearby prose with the pattern:
    #   #### The *potential impact* is **LOW** if—
    #   - The loss of confidentiality, integrity, or availability could be
    #     expected to have a **limited** adverse effect on...
    #   AMPLIFICATION: <amplification>
    level_re = re.compile(
        r"is \*\*(LOW|MODERATE|HIGH)\*\* if.*?"
        r"could be expected to have a \*\*([^*]+)\*\* adverse effect.*?"
        r"AMPLIFICATION:\s+([^\n]+(?:\n[^\n]+)?)",
        re.DOTALL | re.IGNORECASE,
    )
    levels = {}
    for m in level_re.finditer(md):
        name = m.group(1)
        qualifier = re.sub(r"\s+", " ", m.group(2)).strip()
        amplification = re.sub(r"\s+", " ", m.group(3)).strip()
        levels[name] = {"qualifier": qualifier, "amplification": amplification}

    missing = {"LOW", "MODERATE", "HIGH"} - set(levels)
    if missing:
        raise SystemExit(f"Could not extract level definitions: {missing}")

    # Build the 9-cell matrix.
    objective_loss = {
        "Confidentiality": "unauthorized disclosure of information",
        "Integrity": "unauthorized modification or destruction of information",
        "Availability": "disruption of access to or use of information or an information system",
    }
    rows = []
    for objective in ("Confidentiality", "Integrity", "Availability"):
        for level in ("LOW", "MODERATE", "HIGH"):
            qual = levels[level]["qualifier"]
            loss_phrase = objective_loss[objective]
            impact = (
                f"The {loss_phrase} could be expected to have a {qual} adverse effect on "
                f"organizational operations, organizational assets, or individuals."
            )
            rows.append({
                "objective": objective,
                "objective_definition": objectives[objective]["definition"],
                "objective_loss_meaning": objectives[objective]["loss_meaning"],
                "level": level,
                "level_qualifier": qual,
                "level_amplification": levels[level]["amplification"],
                "impact_description": impact,
            })

    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)

    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    print(f"Objectives: {list(objectives)}")
    print(f"Levels: {list(levels)}")
    print(f"Rows: {len(rows)}")
    print(f"Wrote {csv_path.name} and {json_path.name}")


if __name__ == "__main__":
    main()
