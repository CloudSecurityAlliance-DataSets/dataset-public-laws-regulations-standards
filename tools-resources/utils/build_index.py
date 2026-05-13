#!/usr/bin/env python3
"""Generate INDEX.md for this repo.

Walks the SecID-mirror tree (type/namespace/name/version/) and reports per-doc
state: markdown, structured CSV/JSON, marker meta, metadata.json (with SecID),
source files (PDF/XLSX), page images, parser scripts.

Output: INDEX.md at the repo root.

Usage: python3 tools-resources/utils/build_index.py
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

# SecID type roots we know about
TYPE_DIRS = ["control", "regulation", "weakness", "ttp", "methodology", "reference",
             "capability", "advisory", "disclosure", "entity"]


def repo_root() -> Path:
    """Find repo root (containing this script's grandparent)."""
    here = Path(__file__).resolve()
    # script is tools-resources/utils/build_index.py
    return here.parent.parent.parent


# Recognize version-like dir names (case-insensitive). Anything matching is
# treated as a version subdir; anything else is treated as auxiliary content
# inside the document directory (e.g., images/, scripts/, attachments/).
_VERSION_PATTERNS = [
    re.compile(r"^v?\d+(\.\d+)*$", re.I),     # 1, 1.0, v4.0.1
    re.compile(r"^r\d+$", re.I),                # r5, r2
    re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$"),   # 2023, 2024-02, 2024-02-26
    re.compile(r"^e\d{4}$", re.I),              # e2023 (NIST AI 100-2 e2023)
    re.compile(r"^[A-Z]$"),                      # E (FDIS edition), A (annex)
    re.compile(r"^ipd$", re.I),                 # initial public draft (NIST)
    re.compile(r"^fpd$", re.I),                 # final public draft
    re.compile(r"^draft$", re.I),
    re.compile(r"^current$", re.I),
]


def looks_like_version(name: str) -> bool:
    return any(p.match(name) for p in _VERSION_PATTERNS)


def classify_files(p: Path) -> dict:
    """Inspect a directory and return a flag dict describing what's there.

    Heuristics-based: looks at filename patterns to determine roles.
    """
    state = {
        "has_markdown": False,
        "has_marker_json": False,
        "has_marker_meta": False,
        "has_structured_csv": False,
        "has_structured_json": False,
        "has_metadata": False,
        "secid": None,
        "has_source": False,
        "has_images": False,
        "has_parser": False,
        "has_readme": False,
        "n_files": 0,
        "n_images": 0,
    }
    if not p.is_dir():
        return state

    for f in p.iterdir():
        if not f.is_file():
            continue
        state["n_files"] += 1
        name = f.name.lower()

        if name.endswith("-metadata.json"):
            state["has_metadata"] = True
            try:
                data = json.loads(f.read_text())
                state["secid"] = data.get("secid")
            except Exception:
                pass
        elif name.endswith("_meta.json"):
            state["has_marker_meta"] = True
        elif re.search(r"-(requirements|controls|criteria|subcategories)\.csv$", name):
            state["has_structured_csv"] = True
        elif re.search(r"-(requirements|controls|criteria|subcategories)\.json$", name):
            state["has_structured_json"] = True
        elif name.startswith("readme"):
            state["has_readme"] = True
        elif name.endswith(".md") and not name.endswith("-metadata.md"):
            state["has_markdown"] = True
        elif name.endswith(".json") and not name.endswith("-metadata.json") and not name.endswith("_meta.json"):
            # Treat as marker JSON if there's a sibling .md or _meta.json with same prefix
            # else as structured (fallback)
            base = name.rsplit(".", 1)[0]
            if any((p / f"{base}.md").exists() or (p / f"{base}_meta.json").exists() for _ in [0]):
                state["has_marker_json"] = True
            else:
                state["has_structured_json"] = True
        elif name.endswith(".csv"):
            # Bare CSV not matching the structured pattern — count as structured
            state["has_structured_csv"] = True
        elif name.endswith((".pdf", ".xlsx", ".docx", ".rtf", ".zip")):
            state["has_source"] = True
        elif name.endswith((".jpeg", ".jpg", ".png")):
            state["n_images"] += 1
            state["has_images"] = True
        elif name.endswith(".py") and ("parse" in name or "extract" in name or "build" in name):
            state["has_parser"] = True

    return state


def state_label(s: dict) -> str:
    """Short label summarizing extraction state, ordered by completeness."""
    if s["has_structured_csv"] or s["has_structured_json"]:
        return "structured"
    if s["has_markdown"] or s["has_marker_json"]:
        return "extracted"
    if s["has_metadata"]:
        return "metadata-only"
    if s["has_source"]:
        return "source-only"
    if s["has_readme"] or s["n_files"] > 0:
        return "readme-only"
    return "empty"


def state_glyphs(s: dict) -> str:
    """Compact glyph string for at-a-glance state."""
    return "".join([
        "M" if s["has_metadata"] else "·",
        "X" if s["has_markdown"] else "·",
        "J" if s["has_marker_json"] else "·",
        "C" if s["has_structured_csv"] else "·",
        "S" if s["has_structured_json"] else "·",
        "P" if s["has_parser"] else "·",
        "I" if s["has_images"] else "·",
    ])


def walk(root: Path) -> dict:
    """Walk type/namespace/name/version paths.

    Returns nested dict: {type: {namespace: {name: {version: state}}}}.
    For documents without a version subdir, version key is the empty string.
    """
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for type_dir in TYPE_DIRS:
        type_path = root / type_dir
        if not type_path.is_dir():
            continue
        for ns_path in sorted(type_path.iterdir()):
            if not ns_path.is_dir():
                continue
            namespace = ns_path.name
            for name_path in sorted(ns_path.iterdir()):
                if not name_path.is_dir():
                    # Files at namespace level (e.g., README.md) are treated as
                    # namespace-level docs with empty name/version
                    continue
                name = name_path.name
                # Version subdirs look like: 1, 1.0, 1.0.0, v1, v1.0.1, r5, E,
                # ipd, e2023, 2022, 2024-02-26, etc. Anything else is treated as
                # content within the document dir (e.g., images/, scripts/,
                # attachments/, sub-doc folders).
                version_subdirs = [
                    v for v in name_path.iterdir()
                    if v.is_dir() and looks_like_version(v.name)
                ]
                if version_subdirs:
                    for v_path in sorted(version_subdirs):
                        tree[type_dir][namespace][name][v_path.name] = classify_files(v_path)
                else:
                    # No version subdirs — name dir IS the document (its sub-
                    # dirs like images/, scripts/ are auxiliary content).
                    tree[type_dir][namespace][name][""] = classify_files(name_path)
    return tree


def render(tree: dict) -> str:
    """Render the tree as a markdown INDEX."""
    lines = []
    lines.append("# Index")
    lines.append("")
    lines.append("**Auto-generated by `tools-resources/utils/build_index.py`.** Re-run after adding or restructuring content.")
    lines.append("")
    lines.append("Per-doc state glyphs (left to right):")
    lines.append("")
    lines.append("- **M** = `<name>-<version>-metadata.json` present (with `secid` field)")
    lines.append("- **X** = markdown extraction (`<name>-<version>.md`)")
    lines.append("- **J** = marker JSON block tree (`<name>-<version>.json` alongside markdown)")
    lines.append("- **C** = structured CSV (`<name>-<version>-{controls,requirements,criteria,subcategories}.csv`)")
    lines.append("- **S** = structured JSON (matching CSV pattern)")
    lines.append("- **P** = reproducibility parser script (`parse_*.py` / `extract_*.py` / `build_*.py`)")
    lines.append("- **I** = page images (jpeg/png from marker)")
    lines.append("")
    lines.append("State label: `structured` > `extracted` > `metadata-only` > `source-only` > `empty`")
    lines.append("")

    # Overall summary
    n_docs = 0
    n_by_state = defaultdict(int)
    n_by_type = defaultdict(int)
    n_by_namespace = defaultdict(int)
    for type_name, namespaces in tree.items():
        for ns, names in namespaces.items():
            for name, versions in names.items():
                for v, s in versions.items():
                    n_docs += 1
                    n_by_state[state_label(s)] += 1
                    n_by_type[type_name] += 1
                    n_by_namespace[ns] += 1

    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Total documents indexed:** {n_docs}")
    lines.append("")
    lines.append("| State | Count |")
    lines.append("|---|---|")
    for label in ["structured", "extracted", "metadata-only", "source-only", "readme-only", "empty"]:
        if n_by_state[label]:
            lines.append(f"| {label} | {n_by_state[label]} |")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|---|---|")
    for t in TYPE_DIRS:
        if n_by_type[t]:
            lines.append(f"| {t} | {n_by_type[t]} |")
    lines.append("")

    # Per-type rendering
    for type_name in TYPE_DIRS:
        if type_name not in tree:
            continue
        namespaces = tree[type_name]
        lines.append(f"## {type_name}/")
        lines.append("")
        lines.append("| Path | State | Files | Glyphs (MXJCSPI) | SecID |")
        lines.append("|---|---|---|---|---|")
        for ns in sorted(namespaces):
            for name in sorted(namespaces[ns]):
                versions = namespaces[ns][name]
                for v in sorted(versions):
                    s = versions[v]
                    path = f"{type_name}/{ns}/{name}/{v}/" if v else f"{type_name}/{ns}/{name}/"
                    label = state_label(s)
                    glyphs = state_glyphs(s)
                    n_files = s["n_files"]
                    n_imgs = s["n_images"]
                    nf = f"{n_files} (+{n_imgs} imgs)" if n_imgs else str(n_files)
                    secid = f"`{s['secid']}`" if s["secid"] else "—"
                    lines.append(f"| `{path}` | {label} | {nf} | `{glyphs}` | {secid} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    root = repo_root()
    tree = walk(root)
    md = render(tree)
    out = root / "INDEX.md"
    out.write_text(md)
    print(f"Wrote {out.relative_to(root)} ({len(md):,} chars)")


if __name__ == "__main__":
    main()
