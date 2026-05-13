#!/usr/bin/env python3
"""Build a flat CSV from the structured CCM v3.0.1 JSON.

Each row = one control. Nested objects (architectural_relevance,
service_delivery_model, supplier_relationship, framework_mappings)
are flattened into namespaced columns.
"""
import csv
import json


def flatten(d, prefix=""):
    """Recursively flatten a nested dict into {dotted_key: value}."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        elif isinstance(v, bool):
            out[key] = "Y" if v else "N"
        elif v is None:
            out[key] = ""
        else:
            out[key] = str(v)
    return out


def main():
    doc = json.loads(open("ccm-3.0.1.json").read())
    controls = doc["controls"]
    # controls is a dict keyed by control_id; flatten each into a row
    rows = [flatten(controls[cid]) for cid in controls]

    # Determine all fields seen across rows
    fields = []
    seen = set()
    for r in rows:
        for k in r:
            if k not in seen:
                fields.append(k)
                seen.add(k)

    # Reorder: identity fields first
    priority = ["control_id", "control_domain", "control_specification"]
    ordered = [f for f in priority if f in seen] + [f for f in fields if f not in priority]

    # Natural sort by control_id (AIS-01 before AIS-02 before AAC-01 etc.)
    def sort_key(r):
        cid = r.get("control_id", "")
        if "-" in cid:
            prefix, num = cid.rsplit("-", 1)
            try:
                return (prefix, int(num))
            except ValueError:
                return (prefix, num)
        return (cid, 0)

    rows = sorted(rows, key=sort_key)

    with open("ccm-3.0.1.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ordered, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote ccm-3.0.1.csv: {len(rows)} controls, {len(ordered)} columns")


if __name__ == "__main__":
    main()
