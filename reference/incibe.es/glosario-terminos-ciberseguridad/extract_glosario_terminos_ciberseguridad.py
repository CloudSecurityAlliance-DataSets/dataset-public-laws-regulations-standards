#!/usr/bin/env python3
"""Extract the INCIBE Glosario de terminos de ciberseguridad into structured CSV/JSON.

Source: https://www.incibe.es/empresas/materiales/glosario-de-terminos-de-ciberseguridad-una-guia-de-aproximacion-para-el
Direct PDF: https://www.incibe.es/sites/default/files/contenidos/guias/doc/guia_glosario_ciberseguridad_2021.pdf
License: INCIBE / Spanish Government content (CC-BY-NC-SA per INCIBE policy).

Reproduction recipe:
  1. Download the PDF.
  2. Process via the marker GPU box wrapper from the repo root:
       tools-resources/utils/pdf_to_md_via_gpu.sh \\
         --output-dir reference/incibe.es/glosario-terminos-ciberseguridad/_marker/ \\
         /path/to/guia_glosario_ciberseguridad_2021.pdf
  3. Re-run this script.

Marker output lives at _marker/incibe-glosario.md. Spanish definitions
preserved verbatim.

Produces:
  glosario-terminos-ciberseguridad.md
  glosario-terminos-ciberseguridad-terms.csv  (term,definition,source_anchor,notes)
  glosario-terminos-ciberseguridad-terms.json
"""

import csv
import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "glosario-terminos-ciberseguridad"
MARKER_MD = OUT_DIR / "_marker" / "incibe-glosario.md"
SOURCE_URL = "https://www.incibe.es/sites/default/files/contenidos/guias/doc/guia_glosario_ciberseguridad_2021.pdf"

TERM_HEADING_RE = re.compile(
    r"^##\s+[*_]+\s*(\d+\.\d+\.\d+)\.\s+(.+?)\s*[*_]+\s*$"
)
LETTER_HEADING_RE = re.compile(r"^##\s+\*\*(\d+\.\d+)\.\s+([A-Z])\*\*\s*$")
DEF_TAG_RE = re.compile(r"^####\s+\*\*Definici[oó]n:\*\*\s*$")
SKIP_RE = re.compile(r"^(!\[.*\]|\{\d+\}-+|\s*$|---)")


def clean_marker_line(line):
    line = re.sub(r"!\[.*?\]\([^)]*\)", "", line)
    line = re.sub(r"\{\d+\}-+", "", line)
    return line.rstrip()


def _finalize_body(lines):
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    out = []
    blank = False
    for l in lines:
        if l.strip():
            out.append(l)
            blank = False
        else:
            if not blank and out:
                out.append("")
                blank = True
    text = "\n".join(out)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def parse_marker(text):
    lines = text.splitlines()
    in_definitions = False
    terms = []
    current_term = None
    current_section_id = None
    current_body = []

    for raw in lines:
        line = raw.rstrip()
        # Marker's output skips the "2. Definiciones" heading, so we enter the
        # definitions section as soon as we see the first letter sub-heading
        # ("2.1. A").
        if LETTER_HEADING_RE.match(line):
            in_definitions = True
            continue
        if not in_definitions:
            continue
        # Exit if a higher-level section ("3. ..." onwards) appears.
        if re.match(r"^##\s+\*\*[3-9]\.\s", line):
            break
        m = TERM_HEADING_RE.match(line)
        if m:
            if current_term:
                terms.append({
                    "term": current_term,
                    "section_id": current_section_id,
                    "definition": _finalize_body(current_body),
                })
            current_section_id = m.group(1)
            current_term = m.group(2).strip()
            current_body = []
            continue
        if DEF_TAG_RE.match(line):
            continue
        if SKIP_RE.match(line):
            current_body.append("")
            continue
        if current_term:
            current_body.append(clean_marker_line(line))

    if current_term:
        terms.append({
            "term": current_term,
            "section_id": current_section_id,
            "definition": _finalize_body(current_body),
        })

    return terms


def to_anchor(section_id):
    return f"{SOURCE_URL}#section-{section_id}"


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# INCIBE Glosario de términos de ciberseguridad\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: INCIBE / Spanish Government (CC-BY-NC-SA per INCIBE policy).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        for t in terms:
            w.writerow({
                "term": t["term"],
                "definition": t["definition"],
                "source_anchor": to_anchor(t["section_id"]),
                "notes": f"section {t['section_id']}" if t.get("section_id") else "",
            })
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    out = [
        {
            "term": t["term"],
            "definition": t["definition"],
            "source_anchor": to_anchor(t["section_id"]),
            "notes": f"section {t['section_id']}" if t.get("section_id") else "",
        }
        for t in terms
    ]
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return path


def main():
    if not MARKER_MD.exists():
        raise SystemExit(
            f"Missing marker output at {MARKER_MD}. Run the GPU marker wrapper first "
            "(see this file's docstring)."
        )
    text = MARKER_MD.read_text()
    terms = parse_marker(text)
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
