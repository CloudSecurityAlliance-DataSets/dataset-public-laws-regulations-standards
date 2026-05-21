#!/usr/bin/env python3
"""Backfill desired_end_state in every metadata.json based on heuristics.

For each doc:
  1. Walk its dir to determine current_state (structured / extracted /
     metadata-only / etc.) — uses the same logic as build_index.py.
  2. Look at the SecID type + naming + license + lifecycle to infer
     desired_end_state.

Defaults conservatively: if uncertain, set desired = current_state so the
gap-analysis only flags clear gaps, not noise.

Dry-run by default; pass --apply to write changes.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path("/Volumes/MacMiniData/Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards")
TYPE_DIRS = ["control", "regulation", "weakness", "ttp", "methodology", "reference",
             "capability", "advisory", "disclosure", "entity"]

_VERSION_PATTERNS = [
    re.compile(r"^v?\d+(\.\d+)*$", re.I),
    re.compile(r"^r\d+$", re.I),
    re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$"),
    re.compile(r"^e\d{4}$", re.I),
    re.compile(r"^[A-Z]$"),
    re.compile(r"^ipd$", re.I),
    re.compile(r"^fpd$", re.I),
    re.compile(r"^draft$", re.I),
    re.compile(r"^current$", re.I),
]


def looks_like_version(name):
    return any(p.match(name) for p in _VERSION_PATTERNS)


def classify_files(p):
    state = {"has_markdown": False, "has_structured_csv": False, "has_structured_json": False,
             "has_metadata": False, "has_source": False, "has_readme": False,
             "n_files": 0}
    if not p.is_dir():
        return state
    for f in p.iterdir():
        if not f.is_file():
            continue
        state["n_files"] += 1
        name = f.name.lower()
        if name.endswith("-metadata.json") and not name.endswith("-file-metadata.json"):
            state["has_metadata"] = True
        elif re.search(r"-(requirements|controls|criteria|subcategories|tasks|attacks|terms|sections|attributes|relationship-types|mapping-styles|strm-rationales)\.csv$", name):
            state["has_structured_csv"] = True
        elif re.search(r"-(requirements|controls|criteria|subcategories|tasks|attacks|terms|sections|attributes|relationship-types|mapping-styles|strm-rationales)\.json$", name):
            state["has_structured_json"] = True
        elif name.startswith("readme"):
            state["has_readme"] = True
        elif name.endswith(".md") and not name.endswith("-metadata.md"):
            state["has_markdown"] = True
        elif name.endswith((".pdf", ".xlsx", ".docx", ".rtf", ".zip")):
            state["has_source"] = True
        elif name.endswith(".csv"):
            state["has_structured_csv"] = True
    return state


def current_state_label(s):
    if s["has_structured_csv"] or s["has_structured_json"]:
        return "structured"
    if s["has_markdown"]:
        return "extracted"
    if s["has_metadata"]:
        return "metadata-only"
    if s["has_source"]:
        return "source-only"
    if s["has_readme"] or s["n_files"] > 0:
        return "readme-only"
    return "empty"


# --- Heuristics for desired_end_state ---

def is_licensed_restricted(meta):
    """Returns True if metadata indicates licensed/restricted content."""
    lic = (meta.get("license") or {})
    if isinstance(lic, list) and lic:
        lic = lic[0]
    if not isinstance(lic, dict):
        return False
    redistrib = lic.get("redistribution")
    if isinstance(redistrib, dict):
        if redistrib.get("allowed") is False:
            return True
    spdx = (lic.get("spdx") or "").lower()
    if spdx in {"licenseref-iso", "licenseref-iec", "licenseref-ieee",
                "licenseref-ieee-isto", "licenseref-isaca"}:
        return True
    notes = (lic.get("notes") or "")
    if "iso/iec" in notes.lower() or "redistribut" in notes.lower() and "not" in notes.lower():
        return True
    return False


def is_withdrawn(meta):
    lc = meta.get("lifecycle", {}) or {}
    if lc.get("active") is False:
        notes = (lc.get("notes") or "").lower()
        if "withdrawn" in notes or "superseded" in notes:
            return True
    return False


def is_template(name, secid):
    """FedRAMP templates / forms — extract-terminal."""
    name = name.lower()
    return ("template" in name or name.endswith("-form")
            or "-rob-" in name or "letter" in name)


def is_playbook(name):
    return "playbook" in name.lower()


def is_algorithm_spec(secid, name):
    """FIPS algorithm specs."""
    return re.search(r"/fips-(180|186|197|198|201|202|203|204|205)", secid)


def is_glossary(meta):
    sub = meta.get("subtype") or []
    if isinstance(sub, list):
        return "glossary" in sub
    return sub == "glossary"


def is_upstream_only(meta):
    """Docs that should stay metadata-only because publisher hosts authoritative
    version-tagged data we shouldn't bulk-mirror."""
    notes = (meta.get("notes") or "")
    sid = meta.get("secid", "")
    if isinstance(notes, str) and ("upstream" in notes.lower() and "authoritative" in notes.lower()):
        return True
    # ATT&CK, ATLAS, CTID, etc.
    upstream_patterns = [
        r"/attack@", r"/atlas@", r"/cve@", r"^secid:ttp/mitre\.org/attack",
        r"^secid:ttp/mitre\.org/atlas", r"/cvelist", r"^secid:advisory/mitre\.org/cve",
    ]
    return any(re.search(p, sid) for p in upstream_patterns)


def is_methodology_process(secid):
    """methodology/ docs are process descriptions — extract-terminal unless
    they're taxonomy/mapping shape (e.g., IR 8477)."""
    if not secid.startswith("secid:methodology/"):
        return False
    return True  # methodology docs default to extracted-terminal


def infer_desired_end_state(secid, meta, name, current):
    """Return (state, reason, notes) for desired_end_state."""
    if is_withdrawn(meta):
        return ("dropped", "withdrawn", None)
    if is_licensed_restricted(meta):
        return ("metadata-only", "licensed", None)
    if is_upstream_only(meta):
        return ("metadata-only", "upstream-only", None)

    # SecID type drives most decisions
    if secid.startswith("secid:control/"):
        # Control catalogs should be structured
        return ("structured", "control-catalog", None)

    if secid.startswith("secid:regulation/"):
        # Regulations vary — if there's clear section structure they can be
        # structured (sections-rows), otherwise extracted-terminal.
        if current == "structured":
            return ("structured", "requirement-list", None)
        return ("extracted", "policy-doc", None)

    if secid.startswith("secid:weakness/") or secid.startswith("secid:ttp/"):
        return ("structured", "taxonomy", None)

    if secid.startswith("secid:methodology/"):
        # Methodology docs are process descriptions; usually extracted-terminal
        # but mapping/taxonomy methodologies (like IR 8477) are structured.
        if current == "structured":
            return ("structured", "taxonomy", None)
        return ("extracted", "prose-guidance", None)

    if secid.startswith("secid:reference/"):
        # Reference shapes vary widely
        if is_algorithm_spec(secid, name):
            return ("extracted", "algorithm-spec", None)
        if is_template(name, secid):
            return ("extracted", "template", None)
        if is_playbook(name):
            return ("extracted", "playbook", None)
        if is_glossary(meta):
            return ("structured", "glossary", None)
        # Currently-structured reference docs (taxonomies, glossaries, vendor
        # security guidance with structured data) — keep their structured state
        if current == "structured":
            return ("structured", "taxonomy", None)
        # Default: reference docs are extracted-terminal (prose guidance)
        return ("extracted", "prose-guidance", None)

    # Capability / advisory / disclosure / entity — uncommon types
    return (current, "unspecified", "Heuristic inferred default; review")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write changes (default: dry-run)")
    args = ap.parse_args()
    dry_run = not args.apply

    stats = Counter()
    gap_rows = []

    for type_dir in TYPE_DIRS:
        td = REPO_ROOT / type_dir
        if not td.is_dir():
            continue
        for meta_path in td.rglob("*-metadata.json"):
            if meta_path.name.endswith("-file-metadata.json"):
                continue
            try:
                meta = json.loads(meta_path.read_text())
            except Exception:
                continue
            secid = meta.get("secid", "")
            name = meta_path.parent.name
            cur = current_state_label(classify_files(meta_path.parent))
            state, reason, notes = infer_desired_end_state(secid, meta, name, cur)

            stats[f"{cur}/{state}"] += 1

            is_gap = (cur != state)
            if is_gap:
                gap_rows.append((str(meta_path.relative_to(REPO_ROOT)), cur, state, reason))

            desired = {"state": state, "reason": reason}
            if notes:
                desired["notes"] = notes
            existing = meta.get("desired_end_state")
            if existing == desired:
                continue

            if not dry_run:
                meta["desired_end_state"] = desired
                meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    print(f"Dry-run: {dry_run}\n")
    print("Distribution of (current_state, desired_end_state):")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:40} {v:>5}")

    print(f"\nGaps (current != desired): {len(gap_rows)}")
    by_target = Counter(g[2] for g in gap_rows)
    print(f"  Of which target state:")
    for k, v in by_target.most_common():
        print(f"    -> {k}: {v}")


if __name__ == "__main__":
    main()
