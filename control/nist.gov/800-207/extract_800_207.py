#!/usr/bin/env python3
"""Parse NIST SP 800-207 (Zero Trust Architecture) into per-section CSV/JSON.

SP 800-207 is a guide (not a control framework) but has clear numbered
section structure: 7 chapters with hierarchical subsections (e.g.,
2.1 Tenets of Zero Trust, 3.1 Variations, 3.2 Deployed Variations,
3.2.1 Device Agent/Gateway-Based Deployment, etc.).

Marker emits each section as a level-1/2/3 markdown heading:
  # <span id="page-9-0"></span>**1 Introduction**
  # <span id="page-10-0"></span>**1.1 History of Zero Trust Efforts...**
  #### <span id="page-10-1"></span>**1.2 Structure of This Document**

The notable structured content is the **Tenets of Zero Trust** in §2.1
(7 numbered tenets) — preserved in the section body.

Output:
  800-207-sections.{csv,json}  — one row per numbered section
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^#+\s+(?:<span[^>]*></span>\s*)?\*\*(?P<id>\d+(?:\.\d+){0,3})\s+(?P<title>[^*]+?)\*\*\s*$",
    re.MULTILINE,
)


def main():
    md = open("800-207.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sid = m.group("id")
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        # Strip footnote refs and image refs
        body = re.sub(r"\[\d+\]\(#[^)]+\)", "", body)
        body = re.sub(r"!\[\]\([^)]+\)", "", body)
        body = re.sub(r"\s+", " ", body).strip()
        rows.append({
            "section_id": sid,
            "title": title,
            "depth": len(sid.split(".")),
            "content": body,
        })

    # Dedupe — keep longest content for each section_id (handles TOC + body dups)
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section_id"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section_id"]] = r

    def sort_key(r):
        parts = r["section_id"].split(".")
        return tuple(int(p) for p in parts) + (0,) * (4 - len(parts))

    final = sorted(by_id.values(), key=sort_key)
    fields = ["section_id", "title", "depth", "content"]
    with open("800-207-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-207-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    chapters = sorted({r["section_id"].split(".")[0] for r in final}, key=int)
    for ch in chapters:
        cnt = sum(1 for r in final if r["section_id"].split(".")[0] == ch)
        top = next((r["title"] for r in final if r["section_id"] == ch), "")
        print(f"  Ch {ch} ({cnt} sections): {top}")


if __name__ == "__main__":
    main()
