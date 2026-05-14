#!/usr/bin/env python3
"""Parse Ontario Personal Health Information Protection Act, 2004 into CSV/JSON.

Source: phipa.html fetched via Playwright from
https://www.ontario.ca/laws/statute/04p03 (ontario.ca rejects automated
curl with HTTP 403 — Playwright bypasses).

Ontario e-Laws renders each section as `<p class="section">` containing
the section's lead text. The section title (the marginal "headnote") is
in the immediately-preceding `<p class="headnote">`. Subsections follow
as `<p class="subsection">`, paragraphs as `<p class="paragraph">`, etc.
For each section we concatenate the section paragraph and all following
paragraphs until the next `p.section` or `p.headnote`-followed-by-section.

Output:
  phipa-sections.{csv,json}  — one row per section
"""
import csv
import json
import re
from bs4 import BeautifulSoup


SEC_NUM_RE = re.compile(r"^(\d+(?:\.\d+)?)\s+(.+)", re.DOTALL)


def main():
    soup = BeautifulSoup(open("phipa.html", encoding="utf-8").read(), "html.parser")
    section_ps = soup.find_all("p", class_="section")

    rows = []
    for i, sp in enumerate(section_ps):
        # Title: preceding p.headnote
        headnote = None
        prev = sp.find_previous_sibling()
        for _ in range(5):
            if prev is None:
                break
            cls = prev.get("class") or []
            if "headnote" in cls:
                headnote = prev
                break
            prev = prev.find_previous_sibling()
        title = headnote.get_text(" ", strip=True) if headnote else ""

        # Build body — start with this p.section text, then walk siblings
        # until we hit the next p.section
        body_parts = [sp.get_text(" ", strip=True)]
        sib = sp.find_next_sibling()
        while sib is not None:
            scls = sib.get("class") or []
            if sib.name == "p" and "section" in scls:
                break
            # Skip TOC entries and amendments
            if sib.name == "p" and any(c in scls for c in (
                "TOCid", "TOCheadCenter", "TOCpartCenter",
                "footnoteLeft", "partnum", "heading1",
            )):
                sib = sib.find_next_sibling()
                continue
            text = sib.get_text(" ", strip=True)
            if text:
                body_parts.append(text)
            sib = sib.find_next_sibling()

        combined = " ".join(body_parts)
        combined = re.sub(r"\s+", " ", combined).strip()
        m = SEC_NUM_RE.match(combined)
        if m:
            sec_num = m.group(1)
            content = m.group(2).strip()
        else:
            sec_num = ""
            content = combined

        rows.append({
            "section": sec_num,
            "title": title[:300],
            "content": content,
        })

    # Dedupe by section number — keep longest body
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r

    def sort_key(r):
        if not r["section"]:
            return (999, 0)
        parts = r["section"].split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

    final = sorted(by_id.values(), key=sort_key)
    fields = ["section", "title", "content"]
    with open("phipa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("phipa-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    print(f"  First: § {final[0]['section']} — {final[0]['title'][:60]}")
    print(f"  Last:  § {final[-1]['section']} — {final[-1]['title'][:60]}")


if __name__ == "__main__":
    main()
