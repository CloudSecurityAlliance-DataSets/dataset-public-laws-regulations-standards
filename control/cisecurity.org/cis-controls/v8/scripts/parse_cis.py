#!/usr/bin/env python3
"""Parse CIS Controls v8 Excel files into JSON / CSV / Markdown.

Source XLSX files (not committed to this repo) are read from $CIS_V8_SRC, or
by default from ~/Downloads/. Outputs are written next to scripts/ in the
parent CIS-Controls-v8/ directory.

Two source files are processed:
- CIS_Controls_Version_8.xlsx       → cis-controls-v8.json/.csv/.md
- CIS_Controls_v8_Change_Log.xlsx   → cis-controls-v8-changelog.json
"""

import csv
import json
import os
import sys

import numpy as np
import pandas as pd

SRC_DIR = os.environ.get("CIS_V8_SRC", os.path.expanduser("~/Downloads"))
CTRL_XLSX = os.path.join(SRC_DIR, "CIS_Controls_Version_8.xlsx")
CHANGELOG_XLSX = os.path.join(SRC_DIR, "CIS_Controls_v8_Change_Log.xlsx")

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUT_JSON = os.path.join(OUT_DIR, "cis-controls-v8.json")
OUT_CSV = os.path.join(OUT_DIR, "cis-controls-v8.csv")
OUT_MD = os.path.join(OUT_DIR, "cis-controls-v8.md")
OUT_CHANGELOG = os.path.join(OUT_DIR, "cis-controls-v8-changelog.json")


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        # Source uses U+00A0 (NBSP) as a regular space inside text and as
        # leading/trailing padding on values like "Devices\xa0". Replace with
        # a regular space so downstream tools don't have to handle it.
        s = val.replace("\xa0", " ").strip()
        return s or None
    return val


def igs_from_marks(ig1, ig2, ig3):
    out = []
    for label, raw in (("IG1", ig1), ("IG2", ig2), ("IG3", ig3)):
        v = clean(raw)
        if v and str(v).strip().lower() == "x":
            out.append(label)
    return out


def normalize_ctrl_id(val):
    """Coerce a control-id cell (int/float/str with NBSP) to a clean str."""
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, (int, float)):
        return str(int(val))
    s = str(val).replace("\xa0", "").strip()
    return s or None


def parse_controls():
    """Parse the 'Controls V8' sheet.

    Safeguard IDs are derived from sequence position within each control,
    not from the cell value. The XLSX stores e.g. safeguard 3.10 as the
    float 3.1 (cell number_format='General' — Excel drops the trailing
    zero), so trusting column B would produce duplicate IDs and lose
    safeguards 3.10 / 4.10 / 8.10 / 13.10 / 16.10.
    """
    # keep_default_na=False so "N/A" survives as a literal string (used as
    # the asset_type for governance/process controls 14, 15, 17, 18).
    df = pd.read_excel(CTRL_XLSX, sheet_name="Controls V8", header=None,
                       skiprows=1, keep_default_na=False, na_values=[""])
    controls = []
    current = None
    seq = 0

    for _, row in df.iterrows():
        ctrl_id = normalize_ctrl_id(row[0])
        sg_cell = row[1]
        sg_present = not (isinstance(sg_cell, float) and np.isnan(sg_cell)) \
            and not (isinstance(sg_cell, str) and not sg_cell.strip())
        title = clean(row[4])
        desc = clean(row[5])

        if ctrl_id is None and not sg_present:
            continue

        if not sg_present:
            current = {
                "id": ctrl_id,
                "title": title,
                "description": desc,
                "safeguards": [],
            }
            controls.append(current)
            seq = 0
            continue

        if current is None or current["id"] != ctrl_id:
            raise RuntimeError(
                f"Safeguard row has no matching control header "
                f"(row ctrl={ctrl_id!r}, sg cell={sg_cell!r})"
            )

        seq += 1
        sg_id = f"{current['id']}.{seq}"

        # Sanity-check the cell against the derived ID. For seq < 10 the
        # cell's float should equal the derived ID exactly; for seq >= 10
        # Excel will have stored e.g. 3.10 as the float 3.1.
        if isinstance(sg_cell, (int, float)) and not (isinstance(sg_cell, float) and np.isnan(sg_cell)):
            if seq < 10:
                expected = float(sg_id)
                if abs(float(sg_cell) - expected) > 0.001:
                    raise RuntimeError(
                        f"Safeguard sequence mismatch: derived {sg_id} "
                        f"but cell shows {sg_cell!r}"
                    )

        current["safeguards"].append({
            "id": sg_id,
            "title": title,
            "description": desc,
            "asset_type": clean(row[2]),
            "security_function": clean(row[3]),
            "implementation_groups": igs_from_marks(row[6], row[7], row[8]),
        })

    return {
        "framework": {"name": "CIS Controls", "version": "8"},
        "source": "CIS Critical Security Controls v8 (Center for Internet Security)",
        "url": "https://www.cisecurity.org/controls/v8/",
        "controls": controls,
    }


def write_csv(data):
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "control_id", "control_title", "safeguard_id", "safeguard_title",
            "asset_type", "security_function", "ig1", "ig2", "ig3",
            "description",
        ])
        for c in data["controls"]:
            for s in c["safeguards"]:
                igs = set(s["implementation_groups"])
                w.writerow([
                    c["id"], c["title"], s["id"], s["title"],
                    s["asset_type"] or "", s["security_function"] or "",
                    "x" if "IG1" in igs else "",
                    "x" if "IG2" in igs else "",
                    "x" if "IG3" in igs else "",
                    s["description"] or "",
                ])


def write_markdown(data):
    fw = data["framework"]
    lines = [
        f"# {fw['name']} v{fw['version']}",
        "",
        f"Source: {data['source']}  ",
        f"URL: <{data['url']}>",
        "",
        "Implementation Groups are cumulative: IG1 ⊂ IG2 ⊂ IG3.",
        "",
    ]
    for c in data["controls"]:
        lines.append(f"## Control {c['id']}: {c['title']}")
        lines.append("")
        if c["description"]:
            lines.append(c["description"])
            lines.append("")
        for s in c["safeguards"]:
            igs = ", ".join(s["implementation_groups"]) or "—"
            lines.append(f"### {s['id']} {s['title']}")
            lines.append("")
            lines.append(
                f"- **Asset Type:** {s['asset_type'] or '—'}  "
                f"\n- **Security Function:** {s['security_function'] or '—'}  "
                f"\n- **Implementation Groups:** {igs}"
            )
            lines.append("")
            if s["description"]:
                lines.append(s["description"])
                lines.append("")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def parse_changelog():
    """Extract the abridged v8↔v7.1 mapping and deprecated v7.1 safeguards."""
    out = {
        "framework": {"name": "CIS Controls", "version": "8"},
        "source": "CIS Controls v8 Change Log",
        "v8_to_v71_mapping": [],
        "v71_deprecated": [],
    }

    abridged = pd.read_excel(
        CHANGELOG_XLSX,
        sheet_name="v8 CIS Controls > v7.1 Abridged",
        header=None,
        skiprows=1,
        keep_default_na=False,
        na_values=[""],
    )
    current_ctrl = None
    seq = 0
    for _, row in abridged.iterrows():
        ctrl_id = normalize_ctrl_id(row[0])
        sg_cell = row[1]
        sg_present = not (isinstance(sg_cell, float) and np.isnan(sg_cell)) \
            and not (isinstance(sg_cell, str) and not sg_cell.strip())
        if ctrl_id is None and not sg_present:
            continue
        if isinstance(row[0], str) and row[0].strip().lower() == "cis control":
            continue

        if not sg_present:
            current_ctrl = ctrl_id
            seq = 0
            out["v8_to_v71_mapping"].append({
                "v8_control_id": ctrl_id,
                "v8_safeguard_id": None,
                "v8_title": clean(row[4]),
                "v71_reference": clean(row[9]),
            })
        else:
            if current_ctrl != ctrl_id:
                raise RuntimeError(
                    f"Changelog safeguard row has no matching control "
                    f"(row ctrl={ctrl_id!r}, sg cell={sg_cell!r})"
                )
            seq += 1
            sg_id = f"{current_ctrl}.{seq}"
            out["v8_to_v71_mapping"].append({
                "v8_control_id": current_ctrl,
                "v8_safeguard_id": sg_id,
                "v8_title": clean(row[4]),
                "v71_reference": clean(row[9]),
            })

    deprecated = pd.read_excel(
        CHANGELOG_XLSX,
        sheet_name="v7.1 Deprecated CIS Safeguards",
        header=None,
        skiprows=1,
        keep_default_na=False,
        na_values=[""],
    )
    for _, row in deprecated.iterrows():
        v71_ctrl = clean(row[0])
        v71_sg = clean(row[1])
        title = clean(row[2])
        if v71_ctrl is None and v71_sg is None:
            continue
        out["v71_deprecated"].append({
            "v71_control_id": str(v71_ctrl) if v71_ctrl is not None else None,
            "v71_safeguard_id": str(v71_sg) if v71_sg is not None else None,
            "title": title,
        })

    return out


def main():
    if not os.path.exists(CTRL_XLSX):
        print(f"ERROR: source file not found: {CTRL_XLSX}", file=sys.stderr)
        print("Set CIS_V8_SRC to the directory containing the XLSX files.",
              file=sys.stderr)
        sys.exit(1)

    data = parse_controls()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    write_csv(data)
    write_markdown(data)

    n_ctrl = len(data["controls"])
    n_sg = sum(len(c["safeguards"]) for c in data["controls"])
    print(f"Wrote {OUT_JSON}  ({n_ctrl} controls, {n_sg} safeguards)")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")

    if os.path.exists(CHANGELOG_XLSX):
        cl = parse_changelog()
        with open(OUT_CHANGELOG, "w", encoding="utf-8") as f:
            json.dump(cl, f, indent=2, ensure_ascii=False)
        print(
            f"Wrote {OUT_CHANGELOG}  "
            f"({len(cl['v8_to_v71_mapping'])} mappings, "
            f"{len(cl['v71_deprecated'])} deprecated)"
        )
    else:
        print(f"(skipped changelog — {CHANGELOG_XLSX} not found)")


if __name__ == "__main__":
    main()
