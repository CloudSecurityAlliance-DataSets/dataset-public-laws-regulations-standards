#!/usr/bin/env python3
"""Parse the CPE 2.3 Naming Specification's Well-Formed Name (WFN) attributes
into a structured CSV/JSON.

CPE 2.3 defines 11 attributes for the Well-Formed Name (WFN) data model.
Each attribute has a per-attribute restriction section (Section 5.3.3.N).
Four attributes (sw_edition, target_sw, target_hw, other) are marked
"extended attributes" — newly introduced in version 2.3.

Output: cpe-2.3-attributes.{csv,json} — 11 rows.

Columns:
  order              1-11 (attribute position in the canonical CPE 2.3 URI
                     binding: cpe:2.3:part:vendor:product:version:update:
                     edition:language:sw_edition:target_sw:target_hw:other)
  attribute_name     part / vendor / product / ...
  is_extended        true for sw_edition / target_sw / target_hw / other
  is_deprecated      true for edition (deprecated since 2.3, kept for 2.2 compat)
  description        prose definition from Section 5.3.3.N
  allowed_values     for `part`: "a" (application) / "o" (operating system)
                     / "h" (hardware); empty for free-string attributes
"""
import csv
import json
import re
from pathlib import Path


# Canonical attribute order per the CPE 2.3 URI binding string format
# cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
ATTRIBUTES = [
    "part",
    "vendor",
    "product",
    "version",
    "update",
    "edition",
    "language",
    "sw_edition",
    "target_sw",
    "target_hw",
    "other",
]

EXTENDED = {"sw_edition", "target_sw", "target_hw", "other"}

# Section number 5.3.3.N corresponds to attribute N — but spec section ordering
# is slightly different from URI ordering (edition is 5.3.3.6 not URI position 7;
# language is 5.3.3.10 not URI position 7). Map section -> attribute name.
SECTION_TO_ATTR = {
    "5.3.3.1": "part",
    "5.3.3.2": "vendor",
    "5.3.3.3": "product",
    "5.3.3.4": "version",
    "5.3.3.5": "update",
    "5.3.3.6": "edition",
    "5.3.3.7": "sw_edition",
    "5.3.3.8": "target_sw",
    "5.3.3.9": "target_hw",
    "5.3.3.10": "language",
    "5.3.3.11": "other",
}


def extract_description(md: str, section: str, next_section: str) -> str:
    """Pull the text body between `section` heading and the next heading."""
    # Section names in the markdown have underscores escaped (\\_) and are
    # title-cased. Match flexibly.
    section_pat = re.compile(
        rf"^#+\s*\*?\*?{re.escape(section)}\b[^\n]*\*?\*?\s*$",
        re.MULTILINE,
    )
    next_pat = re.compile(
        rf"^#+\s*\*?\*?{re.escape(next_section)}\b",
        re.MULTILINE,
    )
    m_start = section_pat.search(md)
    if not m_start:
        return ""
    m_next = next_pat.search(md, m_start.end())
    end = m_next.start() if m_next else m_start.end() + 3000
    body = md[m_start.end():end].strip()
    # Drop section anchors / page markers
    body = re.sub(r"\{\d+\}-+", "", body)
    body = re.sub(r"<span[^>]*>.*?</span>", "", body)
    # Collapse whitespace
    body = re.sub(r"\s+", " ", body)
    # Strip our own markdown link escapes
    body = re.sub(r"\\(.)", r"\1", body)
    return body.strip()


def part_allowed_values(description: str) -> str:
    """Pull the 3 allowed values for `part` from its description text."""
    m = re.findall(r'value\s+"([aoh])"', description)
    if m:
        return ",".join(m)
    return ""


def is_deprecated(description: str) -> bool:
    return "deprecated" in description.lower()


def main():
    here = Path(__file__).parent
    md = (here / "cpe.md").read_text(encoding="utf-8")

    sections = list(SECTION_TO_ATTR.items())
    rows = []
    for i, (sec, attr) in enumerate(sections):
        # Determine the next section to bound the body. After the last one
        # (5.3.3.11), use "5.4" as the boundary.
        next_sec = sections[i + 1][0] if i + 1 < len(sections) else "5.4"
        description = extract_description(md, sec, next_sec)

        rows.append({
            "order": ATTRIBUTES.index(attr) + 1,
            "attribute_name": attr,
            "is_extended": "true" if attr in EXTENDED else "false",
            "is_deprecated": "true" if is_deprecated(description) else "false",
            "description": description,
            "allowed_values": part_allowed_values(description) if attr == "part" else "",
        })

    # Sort by canonical URI order
    rows.sort(key=lambda r: r["order"])

    csv_path = here / "cpe-2.3-attributes.csv"
    json_path = here / "cpe-2.3-attributes.json"
    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_ext = sum(1 for r in rows if r["is_extended"] == "true")
    n_dep = sum(1 for r in rows if r["is_deprecated"] == "true")
    print(f"Attributes: {len(rows)}  ({n_ext} extended, {n_dep} deprecated)")
    for r in rows:
        marker = "★" if r["is_extended"] == "true" else " "
        print(f"  {r['order']:2}. {marker} {r['attribute_name']:12} {'(deprecated)' if r['is_deprecated']=='true' else ''}")


if __name__ == "__main__":
    main()
