#!/usr/bin/env python3
"""Parse AWS Well-Architected Security Pillar into per-best-practice CSV/JSON.

The Security Pillar is organized as 11 questions (SEC 1 through SEC 11)
that decompose into 64 best practices (SEC01-BP01 through SEC11-BPxx).
Marker flattens the question-level headings but preserves the BP-level
text. We parse at the BP level since that is the natural unit of
assessment ("for each best practice, is it implemented?").

Output:
  wa-security-pillar-bps.{csv,json}  — 64 best practices
"""
import csv
import json
import re


# Best practice section start: "## <span id="page-N"></span>**SECNN-BPNN Title**"
# Marker emits BP headings as level-2 markdown with optional anchor span and
# always bold the entire heading text. Title is everything after the BP id.
BP_RE = re.compile(
    r"^#{1,3}\s+(?:<span[^>]*></span>)?\s*\*\*(SEC\d{2}-BP\d{2})\s+([^*]+?)\*\*\s*$",
    re.MULTILINE,
)


def main():
    md = open("well-architected-security-pillar.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    matches = list(BP_RE.finditer(md))
    # Build per-BP entries: first occurrence is usually the TOC line, later
    # occurrences mark body sections. Take the LONGEST body block for each
    # BP id (the actual section, not a TOC reference or page footer).
    by_bp = {}
    for i, m in enumerate(matches):
        bp = m.group(1)
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        title = re.sub(r"<br>", " ", title).strip()
        bstart = m.end()
        bend = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[bstart:bend]).strip()
        existing = by_bp.get(bp)
        if not existing or len(body) > len(existing["content"]):
            by_bp[bp] = {
                "bp_id": bp,
                "question": bp[:5],   # "SEC01"
                "title": title[:300],
                "content": body,
            }

    final = sorted(by_bp.values(), key=lambda r: r["bp_id"])

    fields = ["bp_id", "question", "title", "content"]
    with open("wa-security-pillar-bps.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("wa-security-pillar-bps.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Best practices: {len(final)}")
    by_q = {}
    for r in final:
        by_q.setdefault(r["question"], []).append(r["bp_id"])
    for q in sorted(by_q):
        print(f"  {q}: {len(by_q[q])} BPs")


if __name__ == "__main__":
    main()
