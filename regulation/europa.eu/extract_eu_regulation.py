#!/usr/bin/env python3
"""Parse an EUR-Lex HTML rendering of an EU regulation into structured CSV/JSON.

EUR-Lex regulations use ELI (European Legislation Identifier) HTML markup:
  - <div id="art_N" class="eli-subdivision"> ...    Article N
    - <p class="oj-ti-art">Article N</p>            (header marker)
    - <div class="eli-title"><p class="oj-sti-art">  Title
    - <p class="oj-normal"> ...                      Body paragraphs
  - <div id="rct_N">                                Recital N (preamble)
  - <div id="cpt_X">                                Chapter X (Roman numeral)
  - <div id="anx_N">                                Annex N

Usage (from a regulation dir):
  python3 ../extract_eu_regulation.py <input.html> <slug>

Output per regulation:
  <slug>-articles.{csv,json}     one row per article
  <slug>-recitals.{csv,json}     one row per recital
  <slug>-annexes.{csv,json}      one row per annex (if any)
"""
import csv
import json
import re
import sys
from bs4 import BeautifulSoup


def text(el):
    if el is None:
        return ""
    s = el.get_text(" ", strip=True)
    s = re.sub(r"\s+", " ", s)
    return s


def parse_article(art_div):
    aid = art_div.get("id", "")
    m = re.match(r"^art_(\d+)$", aid)
    if not m:
        return None, "", ""
    num = int(m.group(1))
    title_div = art_div.find("div", class_="eli-title", recursive=False)
    name = text(title_div) if title_div else ""
    body_parts = []
    for child in art_div.children:
        if not hasattr(child, "name") or not child.name:
            continue
        cls = child.get("class") or []
        if "oj-ti-art" in cls:
            continue
        if child.name == "div" and "eli-title" in cls:
            continue
        body_parts.append(text(child))
    body = " ".join(p for p in body_parts if p)
    return num, name, body


def chapter_index(soup):
    mapping = {}
    for c in soup.find_all(id=re.compile(r"^cpt_[IVX]+$")):
        cid = c.get("id")
        title_div = c.find("div", class_="eli-title", recursive=False)
        cname = text(title_div) if title_div else ""
        roman = cid.replace("cpt_", "")
        for art in c.find_all(id=re.compile(r"^art_\d+$")):
            num = int(art.get("id").replace("art_", ""))
            mapping[num] = (roman, cname)
    return mapping


def parse_articles(soup):
    ch_map = chapter_index(soup)
    rows = []
    seen = set()
    for art in soup.find_all(id=re.compile(r"^art_\d+$")):
        num, name, body = parse_article(art)
        if num is None or num in seen:
            continue
        seen.add(num)
        chapter, chapter_name = ch_map.get(num, ("", ""))
        rows.append({
            "article": num,
            "article_name": name,
            "chapter": chapter,
            "chapter_name": chapter_name,
            "content": body,
        })
    rows.sort(key=lambda r: r["article"])
    return rows


def parse_recitals(soup):
    rows = []
    seen = set()
    for r in soup.find_all(id=re.compile(r"^rct_\d+$")):
        num = int(r.get("id").replace("rct_", ""))
        if num in seen:
            continue
        seen.add(num)
        s = text(r)
        s = re.sub(r"^\(\d+\)\s+", "", s)
        rows.append({"recital": num, "content": s})
    rows.sort(key=lambda r: r["recital"])
    return rows


def parse_annexes(soup):
    rows = []
    seen = set()
    for a in soup.find_all(id=re.compile(r"^anx_[IVX]+$|^anx_\d+$")):
        aid = a.get("id").replace("anx_", "")
        if aid in seen:
            continue
        seen.add(aid)
        title_div = a.find("div", class_="eli-title", recursive=False)
        name = text(title_div) if title_div else ""
        body_parts = []
        for child in a.children:
            if not hasattr(child, "name") or not child.name:
                continue
            cls = child.get("class") or []
            if child.name == "div" and "eli-title" in cls:
                continue
            body_parts.append(text(child))
        body = " ".join(p for p in body_parts if p)
        rows.append({"annex": aid, "annex_name": name, "content": body[:200000]})
    return rows


def write(rows, fields, base):
    if not rows:
        return 0
    with open(f"{base}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return len(rows)


def main():
    if len(sys.argv) != 3:
        print("usage: extract_eu_regulation.py <input.html> <slug>", file=sys.stderr)
        sys.exit(2)
    html_path, slug = sys.argv[1], sys.argv[2]
    soup = BeautifulSoup(open(html_path, encoding="utf-8").read(), "html.parser")

    articles = parse_articles(soup)
    recitals = parse_recitals(soup)
    annexes = parse_annexes(soup)

    n_art = write(articles, ["article", "article_name", "chapter", "chapter_name", "content"], f"{slug}-articles")
    n_rct = write(recitals, ["recital", "content"], f"{slug}-recitals")
    n_anx = write(annexes, ["annex", "annex_name", "content"], f"{slug}-annexes")

    print(f"Articles: {n_art}")
    print(f"Recitals: {n_rct}")
    print(f"Annexes:  {n_anx}")


if __name__ == "__main__":
    main()
