#!/usr/bin/env python3
"""Parse NIST AI 100-2 e2023 (Adversarial ML Taxonomy) into structured CSV/JSON.

NIST AI 100-2 (Adversarial Machine Learning: A Taxonomy and Terminology of
Attacks and Mitigations) organizes adversarial-ML knowledge as a two-level
taxonomy under Sections 2 and 3:

  Section 2 — Predictive AI taxonomy:
    2.1 Attack Classification (dimensions: stages of learning, attacker goals,
        capabilities, knowledge, data modality)
    2.2 Evasion Attacks (white-box, black-box, transferability)
    2.3 Poisoning Attacks (availability, targeted, backdoor, model)
    2.4 Privacy Attacks (data reconstruction, membership inference,
        model extraction, property inference)

  Section 3 — Generative AI taxonomy:
    3.1 Attack Classification
    3.2 AI Supply Chain Attacks (deserialization, poisoning)
    3.3 Direct Prompt Injection (data extraction)
    3.4 Indirect Prompt Injection (availability, integrity, privacy, abuse)

Output: ai-100-2-e2023-attacks.{csv,json} — one row per taxonomy node
(category and leaf), with columns:

    node_id          e.g., "2.2.1"
    ai_type          "Predictive AI" or "Generative AI"
    category_id      e.g., "2.2" (the parent attack-category)
    category_name    e.g., "Evasion Attacks and Mitigations"
    is_leaf          true if this is an attack type, false if a category
    name             section heading
    description      the prose body of this section

Section 4 (Discussion) is NOT structured — it's prose commentary, not a
catalog. Appendix Glossary is NOT structured here — glossary terms are
handled in a separate workstream.
"""
import csv
import json
import re
from pathlib import Path

# Section heading: ## 2.2. Evasion Attacks And **Mitigations**
# Some headings collapse onto one line: ## 4. Discussion ... 4.1. The Scale **Challenge**
HEADING_RE = re.compile(
    r"^##\s+(\d+(?:\.\d+){0,2})\.\s+(.+?)\s*$",
    re.MULTILINE,
)

# Markdown punctuation escapes
MD_ESCAPE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")


def normalize_name(s: str) -> str:
    """Clean section heading text: drop bold markers, normalize spacing,
    title-case-ish."""
    s = re.sub(r"\*+", "", s)  # strip markdown bold
    s = re.sub(r"\s+", " ", s).strip()
    # The marker output title-cases most words; restore reasonable casing for
    # known acronyms.
    for upper in ("Ai", "Nlp", "Pgd", "Fgsm", "Mlcommons", "Owasp"):
        s = re.sub(rf"\b{upper}\b", upper.upper(), s)
    return s


def normalize_body(s: str) -> str:
    s = MD_ESCAPE_RE.sub(r"\1", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def parse_node_id(node_id: str):
    parts = node_id.split(".")
    return tuple(int(p) for p in parts)


def main():
    here = Path(__file__).parent
    md = (here / "ai-100-2-e2023.md").read_text(encoding="utf-8")

    matches = list(HEADING_RE.finditer(md))
    # Keep only nodes under sections 2 and 3 (the taxonomy sections).
    taxonomy = [m for m in matches if m.group(1).startswith(("2", "3"))]
    # Drop section-4 nodes that may have been picked up if they're part of a
    # "## 4. ... 4.1." collapsed heading. (Defensive — the regex above is
    # restrictive enough that this is usually empty.)
    taxonomy = [m for m in taxonomy if m.group(1)[0] in ("2", "3")]

    rows = []
    for i, m in enumerate(taxonomy):
        node_id = m.group(1)
        raw_name = m.group(2)
        name = normalize_name(raw_name)

        # Body runs to the next heading (any heading)
        body_start = m.end()
        next_any = next(
            (mm for mm in matches if mm.start() > m.start()),
            None,
        )
        body_end = next_any.start() if next_any else len(md)
        body = md[body_start:body_end]

        parts = parse_node_id(node_id)
        depth = len(parts)
        ai_type = "Predictive AI" if parts[0] == 2 else "Generative AI"

        is_leaf = depth == 3
        if depth == 2:
            category_id = node_id  # this row IS the category
            category_name = name
        elif depth == 3:
            category_id = ".".join(node_id.split(".")[:2])
            # Find the matching category row's name
            cat_match = next(
                (r for r in rows if r["node_id"] == category_id),
                None,
            )
            category_name = cat_match["name"] if cat_match else ""
        else:
            # depth == 1: top-level section "2." or "3." — emit as the root
            category_id = ""
            category_name = ""

        rows.append({
            "node_id": node_id,
            "ai_type": ai_type,
            "depth": depth,
            "category_id": category_id,
            "category_name": category_name,
            "is_leaf": "true" if is_leaf else "false",
            "name": name,
            "description": normalize_body(body),
        })

    # Backfill category_name for leaves whose category row didn't get its own
    # heading (marker sometimes collapses "## 2. X 2.1. Y" onto one line, so
    # the 2.1 category row is missing). Predictive's 2.1 is "Attack
    # Classification" — derive it directly so 2.1.x leaves have a category.
    KNOWN_MERGED_CATEGORIES = {
        "2.1": "Attack Classification",
    }
    for r in rows:
        if r["is_leaf"] != "true":
            continue
        if r["category_name"]:
            continue
        cid = r["category_id"]
        if cid in KNOWN_MERGED_CATEGORIES:
            r["category_name"] = KNOWN_MERGED_CATEGORIES[cid]

    # Sort by numeric node id
    rows.sort(key=lambda r: parse_node_id(r["node_id"]))

    csv_path = here / "ai-100-2-e2023-attacks.csv"
    json_path = here / "ai-100-2-e2023-attacks.json"
    fields = ["node_id", "ai_type", "depth", "category_id", "category_name",
              "is_leaf", "name", "description"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_pred = sum(1 for r in rows if r["ai_type"] == "Predictive AI")
    n_gen = sum(1 for r in rows if r["ai_type"] == "Generative AI")
    n_leaves = sum(1 for r in rows if r["is_leaf"] == "true")
    print(f"Nodes: {len(rows)}  ({n_pred} predictive + {n_gen} generative; {n_leaves} leaves)")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
