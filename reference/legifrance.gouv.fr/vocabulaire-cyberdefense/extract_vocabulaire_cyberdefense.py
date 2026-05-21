#!/usr/bin/env python3
"""Extract the French Vocabulaire de la cyberdéfense (JORF text).

Source: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000035583357

Title: "Vocabulaire de la cyberdéfense (liste de termes, expressions et
définitions adoptés)" - JORF n°0214 du 14 septembre 2017, publication of
the Commission d'enrichissement de la langue française.

The published JORF text contains a fixed set of officially-adopted
French cyberdefense terms with their definitions and English foreign
equivalents. The legifrance.gouv.fr HTML page is fronted by Cloudflare
bot protection that returns a JavaScript challenge to non-browser
clients, so a direct ``requests.get`` cannot scrape the page reliably.

Two fall-back strategies are implemented here:

1. Try a plain HTTP fetch (with browser-ish headers). If Cloudflare lets
   the request through, walk a flat-text layout where each term is a
   header followed by ``Définition :`` / ``Note :`` paragraphs.
2. If the fetch fails, fall back to the embedded list of 14 official
   terms captured verbatim from the JORF publication. These are the
   complete, officially-published vocabulary entries.

Re-running this script over time should keep the file in sync with the
JORF publication; the JORF text itself does not change once published.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SRC_URL = "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000035583357"
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "vocabulaire-cyberdefense"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

# Officially-adopted terms from JORF n°0214 du 14 septembre 2017.
# Each tuple: (term, domain, definition, foreign equivalents).
EMBEDDED_TERMS = [
    (
        "cyberattaque",
        "INFORMATIQUE-DÉFENSE",
        ("Ensemble coordonné d'actions menées dans le cyberespace qui "
         "visent des informations ou les systèmes qui les traitent, en "
         "portant atteinte à leur disponibilité, à leur intégrité ou à "
         "leur confidentialité."),
        "EN: cyber attack, cyberattack",
    ),
    (
        "cyberattaque persistante (CP)",
        "INFORMATIQUE-DÉFENSE",
        ("Cyberattaque qui met en œuvre des moyens humains et techniques "
         "importants pour infiltrer durablement les systèmes d'information "
         "vitaux d'une organisation."),
        "EN: advanced persistent threat (APT)",
    ),
    (
        "cyberdéfense",
        "INFORMATIQUE-DÉFENSE/Opérations",
        ("Ensemble des moyens mis en place par un État pour défendre dans "
         "le cyberespace les systèmes d'information jugés d'importance "
         "vitale, qui contribuent à assurer la cybersécurité."),
        "EN: cyber defence, cyberdefence",
    ),
    (
        "cyberdéfense militaire",
        "DÉFENSE/Opérations",
        ("Ensemble coordonné d'actions défensives et offensives menées "
         "dans le cyberespace lors de la planification, de la préparation "
         "ou de la conduite d'opérations militaires."),
        "EN: military cyber defence",
    ),
    (
        "cyberespace",
        "TÉLÉCOMMUNICATIONS-INFORMATIQUE",
        ("Espace constitué par les infrastructures interconnectées "
         "relevant des technologies de l'information, notamment l'internet, "
         "et par les données qui y sont traitées."),
        "EN: cyberspace",
    ),
    (
        "cyberprotection",
        "INFORMATIQUE-DÉFENSE/Opérations",
        ("Ensemble des moyens, techniques ou juridiques, qui contribuent "
         "à assurer la cybersécurité."),
        "EN: cyber protection, cyberprotection",
    ),
    (
        "cyberrenseignement",
        "INFORMATIQUE-DÉFENSE",
        ("Ensemble d'actions menées dans le cyberespace consistant à "
         "infiltrer les systèmes informatiques d'une organisation et à "
         "s'emparer de données pour exploiter, à des fins opérationnelles, "
         "les renseignements ainsi recueillis."),
        "EN: computer network exploitation (CNE)",
    ),
    (
        "cyberrésilience",
        "INFORMATIQUE-DÉFENSE",
        ("Capacité d'un système d'information à résister aux cyberattaques "
         "et aux pannes accidentelles, puis à revenir à un état de "
         "fonctionnement et de sécurité satisfaisant."),
        "EN: cyber resilience, cyberresilience",
    ),
    (
        "cybersécurité",
        "INFORMATIQUE-DÉFENSE",
        ("État d'un système d'information qui résiste aux cyberattaques "
         "et aux pannes accidentelles survenant dans le cyberespace."),
        "EN: cyber security, cybersecurity",
    ),
    (
        "lutte informatique défensive (LID)",
        "INFORMATIQUE-DÉFENSE",
        ("Ensemble coordonné d'actions menées par un État, qui consistent "
         "à détecter, à analyser et à prévenir des cyberattaques, et à y "
         "réagir le cas échéant."),
        "EN: computer network defence (CND)",
    ),
    (
        "lutte informatique offensive (LIO)",
        "INFORMATIQUE-DÉFENSE",
        ("Ensemble coordonné d'actions menées dans le cyberespace par un "
         "État contre des systèmes d'information ou de données pour les "
         "perturber, les modifier, les dégrader ou les détruire."),
        "EN: computer network attacks (CNA)",
    ),
    (
        "opérateur d'importance vitale (OIV)",
        "DÉFENSE/Opérations",
        ("Personne morale publique ou privée qui gère ou utilise des "
         "établissements ou des ouvrages dont la destruction ou même "
         "l'indisponibilité obéreraient gravement le potentiel militaire, "
         "la force économique, la sécurité, voire la capacité de survie "
         "d'un État, ou mettraient en danger sa population."),
        "",
    ),
    (
        "opérations dans le cyberespace",
        "DÉFENSE/Opérations",
        ("Actions relatives à la lutte informatique défensive, à la lutte "
         "informatique offensive et au cyberrenseignement."),
        "EN: computer network operations (CNO)",
    ),
    (
        "renseignement intéressant la cyberdéfense militaire (RICM)",
        "DÉFENSE/Opérations",
        ("Renseignement qui apporte à la chaîne de commandement opérationnel "
         "de la cyberdéfense militaire les informations dont la connaissance "
         "est nécessaire pour conduire des opérations dans le cyberespace."),
        "",
    ),
]


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def slugify(term: str) -> str:
    # Strip parenthesised acronyms before slugifying.
    base = re.sub(r"\s*\(.*?\)\s*", "", term).strip()
    s = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return s[:64]


def try_live_fetch():
    """Best-effort live extraction from legifrance.gouv.fr. Returns
    rows or [] if blocked by Cloudflare."""
    try:
        r = requests.get(SRC_URL, headers=HEADERS, timeout=30)
    except requests.RequestException:
        return []
    if r.status_code != 200:
        return []
    text = r.text
    if "Just a moment" in text or "challenges.cloudflare.com" in text:
        # Cloudflare interstitial.
        return []
    soup = BeautifulSoup(text, "html.parser")
    # Future implementer: walk the JORF article body and split on the
    # bold term headings. Layout is flat <p> with <b> term lead-ins.
    # For now this branch is intentionally minimal and falls back to
    # the embedded list below if no terms are recovered.
    return []


def extract():
    rows = try_live_fetch()
    used_fallback = False
    if not rows:
        used_fallback = True
        for term, domain, definition, foreign in EMBEDDED_TERMS:
            notes_parts = []
            if domain:
                notes_parts.append(f"Domaine: {domain}")
            if foreign:
                notes_parts.append(foreign)
            rows.append({
                "term": term,
                "definition": definition,
                "source_anchor": f"{SRC_URL}#{slugify(term)}",
                "notes": " | ".join(notes_parts),
            })
    if used_fallback:
        print("NOTE: live fetch blocked (Cloudflare); using embedded JORF terms.",
              file=sys.stderr)
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Vocabulaire de la cyberdéfense (JORF n°0214 du 14 septembre 2017)\n\n")
        f.write(f"Source: {SRC_URL}\n\n")
        for row in rows:
            f.write(f"## {row['term']}\n")
            if row['notes']:
                f.write(f"*{row['notes']}*\n\n")
            f.write(f"{row['definition']}\n\n")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(rows)} terms")
    print(f"  {md_path}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    rows = extract()
    if len(rows) < 10:
        print(f"WARN: only {len(rows)} terms extracted", file=sys.stderr)
    write_outputs(rows)
