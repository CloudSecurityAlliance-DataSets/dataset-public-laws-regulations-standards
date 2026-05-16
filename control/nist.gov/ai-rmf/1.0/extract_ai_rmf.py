#!/usr/bin/env python3
"""Parse NIST AI Risk Management Framework Core (AI 100-1) into structured CSV/JSON.

The AI RMF Core has 4 Functions (GOVERN, MAP, MEASURE, MANAGE) → 19
Categories → 72 Subcategories. Marker emits the Core as a flat
table where each cell contains multiple `FUNCTION N.M: <description>`
entries separated by sentence boundaries.

The parser walks the flat markdown finding all `(GOVERN|MAP|MEASURE|MANAGE) N.M:`
patterns and extracting the description text up to the next subcategory
or "Continued on next page" marker. Category context (`GOVERN 1:`) is
inferred from the most recent `GOVERN N:` header text in the markdown.

Output:
  ai-rmf-1.0-subcategories.{csv,json}  — one row per subcategory
"""
import csv
import json
import re


FUNCTION_FULL = {
    "GOVERN": "Govern",
    "MAP": "Map",
    "MEASURE": "Measure",
    "MANAGE": "Manage",
}


def main():
    md = open("nist.ai.100-1.md", encoding="utf-8").read()
    # Normalize <br> and whitespace
    md = re.sub(r"<br\s*/?>", " ", md)
    md = re.sub(r"\{\d+\}-+", "", md)

    # Find all category-level definitions: "GOVERN 1: <text>" not followed
    # immediately by ".M" (i.e., not a subcategory)
    cat_re = re.compile(
        r"\b(?P<func>GOVERN|MAP|MEASURE|MANAGE)\s+(?P<num>\d+):\s*(?P<text>[^|\n]+?)(?=\s+(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+[\.:]|\s*\||$)",
    )
    categories = {}
    for m in cat_re.finditer(md):
        cid = f"{m.group('func')} {m.group('num')}"
        text = re.sub(r"\s+", " ", m.group("text")).strip().rstrip(".")
        if cid not in categories or len(text) > len(categories[cid]):
            categories[cid] = text

    # Find all subcategory definitions: "GOVERN 1.1: <text>"
    sub_re = re.compile(
        r"\b(?P<func>GOVERN|MAP|MEASURE|MANAGE)\s+(?P<num>\d+\.\d+):\s*(?P<text>[^|\n]+?)(?=\s+(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+\.\d+:|\s+Continued on next page|\s*\||$)",
    )
    rows = {}
    for m in sub_re.finditer(md):
        sid = f"{m.group('func')} {m.group('num')}"
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        if sid not in rows or len(text) > len(rows[sid]["description"]):
            cat_num = sid.split(".")[0]  # "GOVERN 1" from "GOVERN 1.1"
            rows[sid] = {
                "subcategory_id": sid,
                "function": FUNCTION_FULL.get(m.group("func"), m.group("func")),
                "category_id": cat_num,
                "category_text": categories.get(cat_num, ""),
                "description": text,
            }

    def sort_key(r):
        func_order = ["Govern", "Map", "Measure", "Manage"]
        parts = r["subcategory_id"].split(" ")[1].split(".")
        return (func_order.index(r["function"]) if r["function"] in func_order else 99,
                int(parts[0]), int(parts[1]))

    final = sorted(rows.values(), key=sort_key)
    fields = ["subcategory_id", "function", "category_id", "category_text", "description"]
    with open("ai-rmf-1.0-subcategories.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("ai-rmf-1.0-subcategories.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Subcategories: {len(final)}")
    funcs = {}
    for r in final:
        funcs.setdefault(r["function"], []).append(r["subcategory_id"])
    for f in ["Govern", "Map", "Measure", "Manage"]:
        if f in funcs:
            print(f"  {f}: {len(funcs[f])} subcategories")


if __name__ == "__main__":
    main()
