#!/usr/bin/env python3
"""Consolidate BSI IT-Grundschutz Compendium 2022 cross-reference tables
into a master per-requirement CSV/JSON.

The IT-Grundschutz Compendium is the German federal baseline IT-security
catalogue. BSI publishes:
  - The Compendium PDF itself (~800 pages of module narratives)
  - A separate "Cross-Reference Tables" XLSX with one sheet per module
    mapping each requirement to the elementary threats it counters

The 800-page Compendium PDF overflows the marker GPU box's memory in a
single pass (OOM at ~88 seconds), so we use the cross-reference XLSX as
the structured source. tools-resources/utils/excel_to_csv.py splits the
XLSX into 104 per-module CSVs in
`it-grundschutz-compendium-2022-cross-reference/`. This script
consolidates those into a single per-requirement file.

Each requirement is identified as MODULE.AN (e.g., APP.1.1.A2 = "Limiting
Active Content" in the Office Products module). Total: 1,685 requirements
across 104 modules.

Output:
  it-grundschutz-requirements.{csv,json}
"""
import csv
import json
import os
import re


REQ_RE = re.compile(r"^[A-Z]+(?:\.[A-Z0-9]+)+\.A\d+")
THREAT_COL_RE = re.compile(r"^G\s*0?\.?\d")


def main():
    src = "it-grundschutz-compendium-2022-cross-reference"
    if not os.path.isdir(src):
        raise SystemExit(
            f"Missing {src}/ — generate first via "
            f"`python3 ../../../tools-resources/utils/excel_to_csv.py "
            f"--input it-grundschutz-compendium-2022-cross-reference.xlsx`"
        )

    rows = []
    for fn in sorted(os.listdir(src)):
        m = re.match(r".*KRT_(.+)\.xlsx\.csv", fn)
        if not m:
            continue
        module = m.group(1)
        with open(os.path.join(src, fn), encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                continue
            threat_cols = [(i, h.strip()) for i, h in enumerate(header) if THREAT_COL_RE.match(h)]
            for row in reader:
                if not row or not row[0]:
                    continue
                req_id = row[0].strip()
                if not REQ_RE.match(req_id):
                    continue
                name = row[1].strip() if len(row) > 1 else ""
                if name == "ELIMINATED":
                    continue
                cia = row[2].strip() if len(row) > 2 else ""
                applicable_threats = [
                    threat
                    for col_i, threat in threat_cols
                    if col_i < len(row) and row[col_i].strip().upper() == "X"
                ]
                rows.append({
                    "requirement_id": req_id,
                    "module": module,
                    "name": name,
                    "cia": cia,
                    "applicable_threats": applicable_threats,
                })

    # CSV with pipe-joined threats
    csv_rows = [
        {**r, "applicable_threats": "|".join(r["applicable_threats"])} for r in rows
    ]
    with open("it-grundschutz-requirements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["requirement_id", "module", "name", "cia", "applicable_threats"],
            quoting=csv.QUOTE_ALL,
        )
        w.writeheader()
        w.writerows(csv_rows)
    with open("it-grundschutz-requirements.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"Requirements: {len(rows)}")
    modules = sorted({r["module"] for r in rows})
    print(f"Modules: {len(modules)}")
    # Layer breakdown — IT-Grundschutz uses 10 layers (first segment of module ID)
    layers = {}
    for r in rows:
        layer = r["module"].split(".")[0]
        layers[layer] = layers.get(layer, 0) + 1
    for layer in sorted(layers):
        print(f"  {layer}: {layers[layer]} requirements")


if __name__ == "__main__":
    main()
