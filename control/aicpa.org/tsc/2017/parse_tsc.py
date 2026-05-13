#!/usr/bin/env python3
"""Parse AICPA TSC 2017 (with Revised Points of Focus 2022) marker JSON
into structured CSV/JSON.

Input:  tsc-2017.json  (marker output, --output_format json)
Output: tsc-2017-criteria.csv
        tsc-2017-criteria.json

TSC criteria use these ID formats:
  CC1.x - CC9.x : Common Criteria (security, mandatory in every SOC 2)
  A1.x         : Availability (optional category)
  C1.x         : Confidentiality (optional category)
  PI1.x        : Processing Integrity (optional category)
  P1.x - P8.x  : Privacy (optional category)

Each criterion table has:
  - Header row: "TSP Ref. #" | "TRUST SERVICES CRITERIA AND POINTS OF FOCUS"
  - Optional section row: blank | section title (e.g., "CONTROL ENVIRONMENT")
  - Criterion row: <ID> | <criterion statement>
  - Points-of-focus rows: blank | <bullet or descriptive text>

One row per criterion in the output.
"""
import csv
import json
import re

from bs4 import BeautifulSoup


def walk(node):
    yield node
    for c in node.get("children", []) or []:
        yield from walk(c)


# TSC criterion IDs: CC1.1, CC6.7, A1.1, C1.2, PI1.3, P3.1, etc.
ID_RE = re.compile(r"^((?:CC|A|C|PI|P)\d+\.\d+)$")


def is_id(text):
    """Return the parsed criterion ID if text is an ID cell."""
    if not text:
        return None
    m = ID_RE.match(text.strip())
    return m.group(1) if m else None


def parse_tables(doc):
    """Walk all tables; collect criterion records."""
    records = []
    for n in walk(doc):
        if n.get("block_type") != "Table":
            continue
        html = n.get("html") or ""
        if not re.search(r"(?:CC|A|C|PI|P)\d+\.\d+", html):
            continue

        soup = BeautifulSoup(html, "html.parser")
        trs = soup.find_all("tr")

        current_section = ""
        current_id = None
        current_text = ""
        current_focus = []

        def flush():
            nonlocal current_id, current_text, current_focus
            if current_id:
                # Determine category from ID prefix
                if current_id.startswith("CC"):
                    category = "Common Criteria"
                elif current_id.startswith("A"):
                    category = "Availability"
                elif current_id.startswith("PI"):
                    category = "Processing Integrity"
                elif current_id.startswith("C"):
                    category = "Confidentiality"
                elif current_id.startswith("P"):
                    category = "Privacy"
                else:
                    category = ""
                records.append({
                    "criterion_id": current_id,
                    "category": category,
                    "section": current_section,
                    "criterion_text": current_text.strip(),
                    "points_of_focus": "\n".join(current_focus).strip(),
                })
            current_id = None
            current_text = ""
            current_focus = []

        for tr in trs:
            cells = tr.find_all(["th", "td"])
            if not cells:
                continue
            # Get the two columns
            c1 = cells[0].get_text(" ", strip=True) if len(cells) >= 1 else ""
            c2 = cells[1].get_text(" ", strip=True) if len(cells) >= 2 else ""

            # Header row: skip
            if cells[0].name == "th" and "TSP" in c1:
                continue
            # Section header row: blank col 1, all-caps text in col 2
            if not c1 and c2 and c2.isupper():
                current_section = c2.strip()
                continue
            # Criterion row: col 1 is an ID
            new_id = is_id(c1)
            if new_id:
                flush()
                current_id = new_id
                current_text = c2
                continue
            # Continuation row: blank col 1, content in col 2 = points of focus
            if not c1 and c2 and current_id:
                current_focus.append(c2)
                continue

        flush()

    return records


def load_recovered_patch():
    """Load canonical text for criteria that marker dropped at page breaks.

    Returns {criterion_id: record} or {} if the patch file is absent. Only
    fills gaps — never overwrites successfully-parsed entries.
    """
    try:
        with open("tsc-2017-recovered-criteria.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    out = {}
    for r in data.get("criteria", []):
        rec = dict(r)
        rec["extraction_source"] = data.get("_extraction_source", "manual_patch")
        out[rec["criterion_id"]] = rec
    return out


def main():
    doc = json.loads(open("tsc-2017.json").read())
    records = parse_tables(doc)

    # Dedupe by ID (some criteria may appear in multiple tables; keep richest)
    by_id = {}
    for r in records:
        r.setdefault("extraction_source", "marker")
        existing = by_id.get(r["criterion_id"])
        if not existing or len(r["points_of_focus"]) > len(existing["points_of_focus"]):
            by_id[r["criterion_id"]] = r

    # Fill gaps from the recovered-criteria patch file. We only add IDs that
    # marker missed entirely; we never overwrite extracted text.
    patch = load_recovered_patch()
    patched_added = []
    for cid, rec in patch.items():
        if cid not in by_id:
            by_id[cid] = rec
            patched_added.append(cid)

    # Sort criteria
    def sort_key(r):
        rid = r["criterion_id"]
        # CC1.1 -> ('CC', 1, 1)
        m = re.match(r"([A-Z]+)(\d+)\.(\d+)", rid)
        prefix, n, sub = m.group(1), int(m.group(2)), int(m.group(3))
        # Order: CC < A < C < PI < P
        order = {"CC": 0, "A": 1, "C": 2, "PI": 3, "P": 4}.get(prefix, 9)
        return (order, n, sub)

    sorted_records = sorted(by_id.values(), key=sort_key)

    fields = ["criterion_id", "category", "section", "criterion_text",
              "points_of_focus", "extraction_source"]
    with open("tsc-2017-criteria.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(sorted_records)

    with open("tsc-2017-criteria.json", "w", encoding="utf-8") as f:
        json.dump(sorted_records, f, indent=2, ensure_ascii=False)

    print(f"Criteria: {len(sorted_records)}")
    from collections import Counter
    cats = Counter(r["category"] for r in sorted_records)
    for c in ["Common Criteria", "Availability", "Confidentiality", "Processing Integrity", "Privacy"]:
        print(f"  {c}: {cats[c]}")
    if patched_added:
        print(f"\nRecovered from patch file ({len(patched_added)}): {', '.join(patched_added)}")
    print("\nFirst 3:")
    for r in sorted_records[:3]:
        print(f"  {r['criterion_id']}: {r['criterion_text'][:70]}")


if __name__ == "__main__":
    main()
