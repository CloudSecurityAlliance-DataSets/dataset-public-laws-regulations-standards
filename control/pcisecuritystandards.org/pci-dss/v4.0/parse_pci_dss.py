#!/usr/bin/env python3
"""Parse PCI DSS v4.0.1 marker JSON output into structured CSV/JSON.

Input:  pci-dss-v4.0.json  (marker output, --output_format json)
Output: pci-dss-v4.0-requirements.csv
        pci-dss-v4.0-requirements.json

Each output row represents one PCI DSS requirement (e.g., "1.1.1", "8.3.1"),
with these fields:
  - requirement_id           (e.g., "1.1.1")
  - top_level_requirement    (e.g., "1")
  - section_id               (e.g., "1.1")
  - section_title            (e.g., "Processes and mechanisms...")
  - requirement_text         (Defined Approach Requirements)
  - testing_procedures       (Defined Approach Testing Procedures, joined)
  - customized_approach_objective
  - applicability_notes
  - purpose
  - good_practice
  - examples
  - definitions
  - further_information

The parser walks marker's Document -> Page -> Table tree and uses each Table
block whose HTML contains "Defined Approach Requirements" as a single PCI DSS
requirement. Each such Table preserves the 3-column page layout
(Defined Approach Requirements / Defined Approach Testing Procedures / Purpose)
from the source PDF, with content flowing vertically across multiple visual
rows within each column.
"""
import csv
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


# Section markers that appear as inline headers within column content.
# Within column 1 (Defined Approach Requirements), the marker text introduces
# a new logical field.
COL1_MARKERS = ["Customized Approach Objective", "Applicability Notes"]

# Within column 3 (Guidance), these markers separate Purpose / Good Practice /
# Examples / Definitions / Further Information.
COL3_MARKERS = ["Good Practice", "Examples", "Definitions", "Further Information"]


def walk_blocks(node):
    """Yield every block in the marker tree."""
    yield node
    for c in node.get("children", []) or []:
        yield from walk_blocks(c)


_REQ_TABLE_HEADER_RE = re.compile(
    r"Defined Approach\s*(?:<br\s*/?>)?\s*Requirements", re.IGNORECASE
)


def collect_requirement_tables(doc):
    """Find all marker Table blocks that correspond to PCI DSS requirements.

    Marker sometimes renders the column header with an embedded <br> tag
    between "Approach" and "Requirements" (seen in v4.0; v4.0.1's output uses
    a plain space). Match both shapes.
    """
    out = []
    for n in walk_blocks(doc):
        if n.get("block_type") != "Table":
            continue
        html = n.get("html") or ""
        if _REQ_TABLE_HEADER_RE.search(html):
            out.append(n)
    return out


def split_on_markers(text, markers):
    """Split RAW text (with newlines preserved) on inline section markers.

    Each marker appears on its own line in the source PDF rendering. Returns
    {'_prefix': content_before_first_marker, marker_name: content_after_marker}.
    Splitting happens BEFORE text normalization so that bullet/newline cleanup
    doesn't hide the line-anchored markers.
    """
    if not text:
        return {"_prefix": ""}
    pattern = "(?:^|\n)\\s*(" + "|".join(re.escape(m) for m in markers) + ")\\s*(?:\n|$)"
    pieces = re.split(pattern, text)
    result = {"_prefix": pieces[0]}
    for i in range(1, len(pieces), 2):
        marker = pieces[i]
        content = pieces[i + 1] if i + 1 < len(pieces) else ""
        result[marker] = content
    return result


def normalize_text(s, strip_id=None):
    """Clean up marker's <br>-derived newlines into flowing text.

    If strip_id is given, remove standalone occurrences of that requirement ID
    (e.g., "1.1.1") that marker embedded mid-sentence based on visual layout.
    """
    if not s:
        return ""
    if strip_id:
        # Remove the ID only when it appears as a layout artifact: alone on its
        # own line, or at the very start of the text. Preserve legitimate
        # references like "Requirement 1.1.1 is about...".
        s = re.sub(rf"(?:^|\n)\s*{re.escape(strip_id)}\s*(?=\n|$)", "\n", s)
        s = re.sub(rf"^\s*{re.escape(strip_id)}\s+", "", s)
    # Bullet on its own line: attach to preceding line
    s = re.sub(r"\n\s*•\s*\n", " • ", s)
    s = re.sub(r"\s*•\s*", " • ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = "\n".join(re.sub(r" +", " ", line.strip()) for line in s.splitlines())
    # Join consecutive lines that look like a single wrapped sentence
    lines = s.split("\n")
    joined = []
    for line in lines:
        if (
            joined
            and joined[-1]
            and not joined[-1].endswith((".", ":", "•", "?", "!", ")", ":", ";"))
            and line
            and line[0].islower()
        ):
            joined[-1] = joined[-1] + " " + line
        else:
            joined.append(line)
    return "\n".join(joined).strip()


def extract_requirement_id(col1_text):
    """Pick the most-likely requirement ID from column 1 text.

    The requirement ID appears as a standalone token like '1.1.1', '8.3.1', or
    'A3.2.5.1' (Appendix A entries — DESV, multi-tenancy, additional PCI DSS
    requirements). Multiple IDs may appear in cross-references; we want the
    first one that looks like 'the requirement this table describes'
    (typically near the start of the cell).

    Appendix-A IDs take precedence when present so that A3.X.Y.Z isn't
    truncated to its trailing numeric portion (2.5.1).
    """
    if not col1_text:
        return None
    # Appendix-A IDs come first if present anywhere in the cell.
    appendix = re.findall(r"\b(A\d+(?:\.\d+){2,3})\b", col1_text)
    if appendix:
        return appendix[0]
    # Prefer IDs on their own line or after a newline.
    standalone = re.findall(r"(?:^|\n)\s*(\d{1,2}\.\d+\.\d+(?:\.\d+)?)\b", col1_text)
    if standalone:
        return standalone[0]
    # Fallback: any X.Y.Z token.
    inline = re.findall(r"\b(\d{1,2}\.\d+\.\d+(?:\.\d+)?)\b", col1_text)
    return inline[0] if inline else None


def parse_table(table_node):
    """Parse one requirement table into structured fields."""
    html = table_node.get("html", "")
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")

    # Capture the section header row: usually 2nd row with `colspan` containing
    # the section number + title, e.g., "1.1 Processes and mechanisms..."
    section_id = ""
    section_title = ""
    for r in rows[:3]:
        cells = r.find_all(["th", "td"])
        for c in cells:
            txt = c.get_text("\n", strip=True)
            m = re.match(r"^(\d{1,2}\.\d+)\s*\n?(.*)", txt, re.S)
            if m and not section_id:
                section_id = m.group(1)
                section_title = re.sub(r"\s+", " ", m.group(2)).strip()
                break

    # Locate the inner column-header row ("Defined Approach Requirements" ...).
    # Match on the row's combined cell text (with <br>/whitespace normalized)
    # so v4.0's <br>-broken header renders the same as v4.0.1's plain spacing.
    header_idx = None
    for i, r in enumerate(rows):
        row_text = " ".join(c.get_text(" ", strip=True) for c in r.find_all(["th", "td"]))
        if _REQ_TABLE_HEADER_RE.search(row_text):
            header_idx = i
            break
    if header_idx is None:
        return None

    # Aggregate the three columns across all data rows
    col1, col2, col3 = [], [], []
    for r in rows[header_idx + 1:]:
        cells = r.find_all(["th", "td"])
        texts = [c.get_text("\n", strip=True) for c in cells]
        if len(texts) >= 3:
            col1.append(texts[0])
            col2.append(texts[1])
            col3.append(texts[2])
        elif len(texts) == 2:
            col1.append(texts[0])
            col2.append("")
            col3.append(texts[1])
        elif len(texts) == 1:
            col1.append(texts[0])

    # Keep RAW text for marker splitting (newlines preserved)
    col1_raw = "\n".join(t for t in col1 if t)
    col2_raw = "\n".join(t for t in col2 if t)
    col3_raw = "\n".join(t for t in col3 if t)

    req_id = extract_requirement_id(col1_raw)
    if not req_id:
        return None

    # Split BEFORE normalizing so line-anchored markers still match
    col1_split = split_on_markers(col1_raw, COL1_MARKERS)
    col3_split = split_on_markers(col3_raw, COL3_MARKERS)

    # Normalize each field, stripping the table's own requirement ID where it
    # got embedded mid-text
    def norm(s):
        return normalize_text(s, strip_id=req_id)

    top = req_id.split(".")[0]

    return {
        "requirement_id": req_id,
        "top_level_requirement": top,
        "section_id": section_id or ".".join(req_id.split(".")[:2]),
        "section_title": section_title,
        "requirement_text": norm(col1_split.get("_prefix", "")),
        "testing_procedures": norm(col2_raw),
        "customized_approach_objective": norm(col1_split.get("Customized Approach Objective", "")),
        "applicability_notes": norm(col1_split.get("Applicability Notes", "")),
        "purpose": norm(col3_split.get("_prefix", "")),
        "good_practice": norm(col3_split.get("Good Practice", "")),
        "examples": norm(col3_split.get("Examples", "")),
        "definitions": norm(col3_split.get("Definitions", "")),
        "further_information": norm(col3_split.get("Further Information", "")),
    }


def main():
    here = Path(__file__).parent
    input_path = here / "pci-dss-v4.0.json"
    csv_path = here / "pci-dss-v4.0-requirements.csv"
    json_path = here / "pci-dss-v4.0-requirements.json"

    print(f"Loading {input_path.name} ...")
    doc = json.loads(input_path.read_text())

    tables = collect_requirement_tables(doc)
    print(f"Requirement tables found: {len(tables)}")

    rows = []
    skipped = 0
    for t in tables:
        parsed = parse_table(t)
        if parsed is None:
            skipped += 1
            continue
        rows.append(parsed)

    # Some requirements span multiple tables (continuation pages). Merge by ID.
    by_id = {}
    for r in rows:
        rid = r["requirement_id"]
        if rid in by_id:
            existing = by_id[rid]
            # Concatenate text fields where they differ
            for k in ("requirement_text", "testing_procedures", "customized_approach_objective",
                      "applicability_notes", "purpose", "good_practice", "examples",
                      "definitions", "further_information"):
                if r[k] and r[k] not in existing[k]:
                    existing[k] = (existing[k] + "\n" + r[k]).strip()
        else:
            by_id[rid] = r

    # Sort by requirement ID using natural ordering (1.1.1 before 1.1.10).
    # Appendix A IDs (A1.*, A2.*, A3.*) sort AFTER the main 1-12 requirements
    # by remapping "A<n>" to 100 + n.
    def sort_key(r):
        parts = r["requirement_id"].split(".")
        out = []
        for p in parts:
            if p.isdigit():
                out.append(int(p))
            elif re.match(r"^A\d+$", p):
                out.append(100 + int(p[1:]))
            else:
                out.append(0)
        return tuple(out)

    sorted_rows = sorted(by_id.values(), key=sort_key)

    fields = list(sorted_rows[0].keys())

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(sorted_rows)

    json_path.write_text(json.dumps(sorted_rows, indent=2, ensure_ascii=False))

    # Summary
    print(f"\nParsed: {len(sorted_rows)} unique requirements")
    print(f"Skipped tables: {skipped}")
    top_groups = {}
    for r in sorted_rows:
        t = r["top_level_requirement"]
        top_groups[t] = top_groups.get(t, 0) + 1
    print("\nDistribution by top-level requirement:")
    for k in sorted(top_groups, key=lambda x: int(x) if x.isdigit() else 99):
        print(f"  {k}: {top_groups[k]}")

    # Sanity check on first few
    print("\nFirst 3 requirements:")
    for r in sorted_rows[:3]:
        print(f"  {r['requirement_id']}: {r['requirement_text'][:80]}...")

    print(f"\nWrote {csv_path.name} and {json_path.name}")


if __name__ == "__main__":
    main()
