#!/usr/bin/env python3
"""Parse PCI DSS v3.2.1 marker JSON output into structured CSV/JSON.

Input:  pci-dss-v3.2.1.json  (marker output, --output_format json)
Output: pci-dss-v3.2.1-requirements.csv
        pci-dss-v3.2.1-requirements.json

PCI DSS v3.2.1 uses a simpler 3-column requirement table than v4.x:
  "PCI DSS Requirements" | "Testing Procedures" | "Guidance"

No Defined/Customized Approach distinction (introduced in v4.0). Each
table may contain MANY requirements (one per data row); v4.x has one
table per requirement. Each row is one logical requirement.

Output fields per requirement:
  - requirement_id           (e.g., "1.1.1")
  - top_level_requirement    (1-12, plus 'A1', 'A2', 'A3' for appendices)
  - section_id               (e.g., "1.1")
  - requirement_text         (the "PCI DSS Requirements" column)
  - testing_procedures       (the "Testing Procedures" column, contains
                               1.1.1.a, 1.1.1.b, etc.)
  - guidance                 (the "Guidance" column)
"""
import csv
import json
import re

from bs4 import BeautifulSoup


def walk_blocks(node):
    yield node
    for c in node.get("children", []) or []:
        yield from walk_blocks(c)


REQ_HEADER_RE = re.compile(r"(?:PCI DSS|A[123]) Requirements")


def collect_requirement_tables(doc):
    """Find tables that look like PCI DSS v3.2.1 requirement tables.

    Body section tables use "PCI DSS Requirements"; Appendix A1/A2/A3
    tables use "A1 Requirements" / "A2 Requirements" / "A3 Requirements"
    as the left-column header. Headers may render with <br> between
    words, so normalize first.
    """
    out = []
    for n in walk_blocks(doc):
        if n.get("block_type") != "Table":
            continue
        html = n.get("html") or ""
        normalized = re.sub(r"<br[^>]*>", " ", html)
        if REQ_HEADER_RE.search(normalized) and "Testing Procedures" in normalized:
            out.append(n)
    return out


def normalize_text(s):
    """Clean marker's <br>-derived newlines into flowing text."""
    if not s:
        return ""
    s = re.sub(r"\n\s*•\s*\n", " • ", s)
    s = re.sub(r"\s*•\s*", " • ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = "\n".join(re.sub(r" +", " ", line.strip()) for line in s.splitlines())
    # Join wrapped lines
    lines = s.split("\n")
    joined = []
    for line in lines:
        if (joined and joined[-1] and not joined[-1].endswith((".", ":", "•", "?", "!", ")", ";"))
                and line and line[0].islower()):
            joined[-1] = joined[-1] + " " + line
        else:
            joined.append(line)
    return "\n".join(joined).strip()


# PCI DSS v3.2.1 has 12 numeric main requirements + Appendix A1/A2/A3
ID_RE = re.compile(r"^(A?\d{1,2}(?:\.\d+)+)\b")


def extract_requirement_id(text):
    """Find the requirement ID at the start of a column-1 cell.

    v3.2.1 IDs: 1.1, 1.1.1, 1.1.1.1, A1.1, A3.2.1, etc.
    The ID typically appears as the first token after some intro text
    (due to marker's <br> handling, sometimes mid-cell).
    """
    if not text:
        return None
    # Try first: a standalone ID at the start or on its own line
    for line in text.split("\n"):
        line = line.strip()
        m = ID_RE.match(line)
        if m:
            return m.group(1)
    # Fallback: any X.Y or X.Y.Z token
    m = re.search(r"\b(A?\d{1,2}(?:\.\d+){1,3})\b", text)
    return m.group(1) if m else None


def strip_embedded_id(text, req_id):
    """Remove standalone occurrences of the requirement's own ID from
    cleaned content (marker positions it mid-text based on the source PDF
    visual layout, where it sat between two content lines)."""
    if not text or not req_id:
        return text
    text = re.sub(rf"(?:^|\n)\s*{re.escape(req_id)}\s*(?=\n|$)", "\n", text)
    text = re.sub(rf"^\s*{re.escape(req_id)}\s+", "", text)
    return text


def parse_tables(tables):
    """Walk every Table; emit one record per data row.

    Each table has a header row (PCI DSS Requirements | Testing Procedures
    | Guidance) followed by data rows where col 1 contains the requirement
    ID + text.
    """
    rows = []
    for t in tables:
        soup = BeautifulSoup(t.get("html", ""), "html.parser")
        trs = soup.find_all("tr")
        if not trs:
            continue
        # Skip header row(s)
        data_rows = []
        for tr in trs:
            cells = tr.find_all(["th", "td"])
            # Header rows have <th>; data rows are all <td>
            if any(c.name == "th" for c in cells):
                continue
            data_rows.append(cells)

        # Each data row → potentially one requirement
        for cells in data_rows:
            texts = [c.get_text("\n", strip=True) for c in cells]
            if len(texts) < 1 or not any(texts):
                continue
            col1 = texts[0] if len(texts) > 0 else ""
            col2 = texts[1] if len(texts) > 1 else ""
            col3 = texts[2] if len(texts) > 2 else ""
            req_id = extract_requirement_id(col1)
            if not req_id:
                continue
            rows.append({
                "_raw_col1": col1,
                "_raw_col2": col2,
                "_raw_col3": col3,
                "requirement_id": req_id,
            })
    return rows


def main():
    doc = json.loads(open("pci-dss-v3.2.1.json").read())
    tables = collect_requirement_tables(doc)
    print(f"Requirement tables: {len(tables)}")

    raw = parse_tables(tables)
    print(f"Raw rows: {len(raw)}")

    # Merge rows with the same requirement_id (multi-row continuation in source)
    by_id = {}
    for r in raw:
        rid = r["requirement_id"]
        existing = by_id.setdefault(rid, {
            "requirement_id": rid,
            "_col1": [], "_col2": [], "_col3": [],
        })
        for k, src in [("_col1", "_raw_col1"), ("_col2", "_raw_col2"), ("_col3", "_raw_col3")]:
            if r[src] and r[src] not in existing[k]:
                existing[k].append(r[src])

    # Build final records
    out = []
    for rid, agg in by_id.items():
        col1 = strip_embedded_id("\n".join(agg["_col1"]), rid)
        col2 = "\n".join(agg["_col2"])  # don't strip id from testing (has sub-IDs)
        col3 = "\n".join(agg["_col3"])
        parts = rid.split(".")
        section_id = ".".join(parts[:2])
        top = parts[0]
        out.append({
            "requirement_id": rid,
            "top_level_requirement": top,
            "section_id": section_id,
            "requirement_text": normalize_text(col1),
            "testing_procedures": normalize_text(col2),
            "guidance": normalize_text(col3),
        })

    # Natural-sort by requirement ID
    def sort_key(r):
        rid = r["requirement_id"]
        # Handle A1.1.1, A2.x.x, A3.x.x — sort appendix after numeric
        if rid.startswith("A"):
            top_int = 100 + int(rid[1])
            rest = rid[2:].split(".")[1:] if "." in rid else []
        else:
            top_int = int(rid.split(".")[0])
            rest = rid.split(".")[1:]
        return (top_int,) + tuple(int(p) if p.isdigit() else 0 for p in rest)

    sorted_rows = sorted(out, key=sort_key)

    fields = ["requirement_id", "top_level_requirement", "section_id",
              "requirement_text", "testing_procedures", "guidance"]

    with open("pci-dss-v3.2.1-requirements.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(sorted_rows)

    with open("pci-dss-v3.2.1-requirements.json", "w", encoding="utf-8") as f:
        json.dump(sorted_rows, f, indent=2, ensure_ascii=False)

    print(f"\nUnique requirements: {len(sorted_rows)}")
    from collections import Counter
    top = Counter(r["top_level_requirement"] for r in sorted_rows)
    for k in sorted(top, key=lambda x: (x.startswith("A"), x)):
        print(f"  {k}: {top[k]}")
    print("\nFirst 3:")
    for r in sorted_rows[:3]:
        print(f"  {r['requirement_id']}: {r['requirement_text'][:70]}")


if __name__ == "__main__":
    main()
