#!/usr/bin/env python3
"""Parse NIST IR 8477 (Mapping Relationships Between Documentary Standards,
Regulations, Frameworks, and Guidelines) into structured CSV/JSON.

IR 8477 defines five mapping styles for relating concepts between documents.
Each style has its own definition; three of them also define a set of
relationship types and (for STRM) rationale dimensions.

Output:
  ir-8477-mapping-styles.{csv,json}      — 5 rows, one per mapping style
  ir-8477-relationship-types.{csv,json}  — one row per (style, type), ~12 rows

Pulls each style's Definition paragraph from the markdown so the script is
reproducible against the source rather than hardcoding text.
"""
import csv
import json
import re
from pathlib import Path

# Five mapping styles defined in IR 8477 with their canonical relationship
# types (and STRM rationale dimensions). The style metadata is derived from
# the markdown; the type listings are canonical to the spec.
STYLES = [
    {
        "style_id": "crosswalk",
        "style_name": "Concept Crosswalk",
        "section": "4.1",
        "section_heading": "## 4.1. Concept Crosswalk",
        "relationship_types": [],  # no types — just "relationship exists"
    },
    {
        "style_id": "supportive",
        "style_name": "Supportive Relationship Mapping",
        "section": "4.2",
        "section_heading": "## 4.2. Supportive Relationship Mapping",
        "relationship_types": [
            ("supports", "Supports",
             "Concept A supports concept B when A can be applied alone or in combination with one or more other concepts to achieve B in whole or in part."),
            ("is-supported-by", "Is supported by",
             "Concept A is supported by concept B when B can be applied alone or in combination with one or more other concepts to achieve A in whole or in part."),
            ("identical", "Identical",
             "Concept A and concept B are identical. They use exactly the same wording."),
            ("equivalent", "Equivalent",
             "Concept A and concept B are equivalent. They have the same meaning but different wording."),
            ("contrary", "Contrary",
             "Concept A and concept B each have one or more elements that contradict one or more elements of the other concept."),
            ("no-relationship", "No relationship",
             "Concept A and concept B are not related or are not sufficiently related to merit another supportive relationship type."),
        ],
    },
    {
        "style_id": "strm",
        "style_name": "Set Theory Relationship Mapping",
        "section": "4.3",
        "section_heading": "#### 4.3. Set Theory Relationship Mapping",
        "rationales": [
            ("syntactic", "How similar is the wording that expresses the two concepts? Word-for-word analysis."),
            ("semantic", "How similar are the meanings of the two concepts? Involves interpretation of language."),
            ("functional", "How similar are the results of executing the two concepts?"),
        ],
        "relationship_types": [
            ("subset-of", "Subset of",
             "Concept A is a subset of concept B. Concept B contains everything that concept A does and more."),
            ("intersects-with", "Intersects with",
             "Concept A and concept B have some overlap, but each includes content that the other does not."),
            ("equal", "Equal",
             "Concept A and concept B are the same, although not necessarily identical."),
            ("superset-of", "Superset of",
             "Concept A is a superset of concept B. Concept A contains everything that concept B does and more."),
            ("no-relationship", "No relationship",
             "Concept A and concept B are unrelated; their content does not overlap."),
        ],
    },
    {
        "style_id": "structural",
        "style_name": "Structural Relationship Mapping",
        "section": "4.4",
        "section_heading": "## 4.4. Structural Relationship Mapping",
        "relationship_types": [
            ("parent-child", "Parent-child",
             "The child concept is part of the parent concept. Does not specify whether the child concept is required or optional to achieve the parent concept."),
        ],
    },
    {
        "style_id": "custom",
        "style_name": "Custom",
        "section": "4.5",
        "section_heading": "## 4.5. Custom",
        "relationship_types": [],  # user-defined
    },
]


def extract_definition(md: str, section_heading: str) -> str:
    """Find the section heading and extract the Definition: paragraph."""
    idx = md.find(section_heading)
    if idx < 0:
        # Some markdown headings have inconsistent ## vs #### levels — fall back
        # to a relaxed match on the section number.
        section_num = section_heading.split("#")[-1].strip().split(".")[0:2]
        section_num = ".".join(section_num)
        loose = re.search(rf"^#+\s+{re.escape(section_num)}\.\s+", md, re.MULTILINE)
        if not loose:
            return ""
        idx = loose.start()
    # Body starts after the heading; pick the line that begins with "Definition:"
    body = md[idx:idx + 3000]
    m = re.search(r"^\s*Definition:\s*(.+?)(?:\n\s*\n|^\s*Primary Uses:)",
                  body, re.MULTILINE | re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    return ""


def main():
    here = Path(__file__).parent
    md = (here / "ir-8477.md").read_text(encoding="utf-8")

    style_rows = []
    type_rows = []

    for s in STYLES:
        definition = extract_definition(md, s["section_heading"])
        style_rows.append({
            "style_id": s["style_id"],
            "style_name": s["style_name"],
            "section": s["section"],
            "definition": definition,
            "n_relationship_types": len(s["relationship_types"]),
        })
        for tid, tname, tdef in s["relationship_types"]:
            type_rows.append({
                "style_id": s["style_id"],
                "style_name": s["style_name"],
                "type_id": tid,
                "type_name": tname,
                "definition": tdef,
            })

    # STRM has rationale dimensions; emit a third file for those
    strm = next(s for s in STYLES if s["style_id"] == "strm")
    rationale_rows = [
        {"style_id": "strm", "rationale_id": rid, "definition": rdef}
        for rid, rdef in strm["rationales"]
    ]

    # Write outputs
    style_csv = here / "ir-8477-mapping-styles.csv"
    style_json = here / "ir-8477-mapping-styles.json"
    with style_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(style_rows[0].keys()),
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(style_rows)
    style_json.write_text(json.dumps(style_rows, indent=2, ensure_ascii=False))

    type_csv = here / "ir-8477-relationship-types.csv"
    type_json = here / "ir-8477-relationship-types.json"
    with type_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(type_rows[0].keys()),
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(type_rows)
    type_json.write_text(json.dumps(type_rows, indent=2, ensure_ascii=False))

    rationale_csv = here / "ir-8477-strm-rationales.csv"
    rationale_json = here / "ir-8477-strm-rationales.json"
    with rationale_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rationale_rows[0].keys()),
                           quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rationale_rows)
    rationale_json.write_text(json.dumps(rationale_rows, indent=2, ensure_ascii=False))

    print(f"Mapping styles:      {len(style_rows)}")
    print(f"Relationship types:  {len(type_rows)}")
    print(f"STRM rationales:     {len(rationale_rows)}")
    print(f"Wrote: ir-8477-mapping-styles, ir-8477-relationship-types, ir-8477-strm-rationales (.csv + .json each)")


if __name__ == "__main__":
    main()
