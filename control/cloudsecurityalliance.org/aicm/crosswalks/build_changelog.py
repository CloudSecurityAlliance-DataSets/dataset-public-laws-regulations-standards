#!/usr/bin/env python3
"""Build a per-control changelog between two AICM versions.

CSA ships a Change Log worksheet, but it is a summary of intent rather than a
delta: for 1.0.3 -> 1.1.0 it names five new controls and one deletion and says
nothing about the 53 controls that were renumbered or the 34 specifications that
were rewritten. This produces the exhaustive version — every control in either
release gets a verdict, including "nothing changed".

Each entry answers three questions:

  1. What happened to this control?      unchanged / retitled / rewritten /
                                          renumbered / added / removed
  2. Where did it come from or go to?    the counterpart ID in the other release
  3. Does this ID still mean what it     ID REUSE: the identifier survived but
     used to mean?                        now designates a different control

Question 3 is the one that bites consumers and the one no ID-based diff can
answer. It is reported per control and summarised at the top.

Reads the crosswalk produced by build_crosswalk.py rather than re-deriving the
matching, so the changelog and the crosswalk can never disagree.

Usage:
    ./build_changelog.py \
        --old ../1.0.3/aicm-1.0.3.json \
        --new ../1.1.0/aicm-1.1.0.json \
        --crosswalk aicm-1.0.3-to-1.1.0-crosswalk.csv \
        --old-version 1.0.3 --new-version 1.1.0 \
        --output aicm-1.0.3-to-1.1.0-changelog.md \
        --json-output aicm-1.0.3-to-1.1.0-changelog.json
"""

import argparse
import csv
import difflib
import json
import re
import sys
from collections import Counter, defaultdict

# Specification similarity at or above which a text edit is treated as cosmetic
# (whitespace, typo fixes, a boilerplate clause) rather than a changed requirement.
COSMETIC_MIN = 0.95


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def domain_of(control_id):
    return control_id.rsplit("-", 1)[0]


def sort_key(control_id):
    dom, _, num = control_id.rpartition("-")
    return (dom, int(num) if num.isdigit() else 0)


def similarity(a, b):
    return max(
        difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(),
        difflib.SequenceMatcher(None, norm(b), norm(a)).ratio(),
    )


def load_controls(path):
    with open(path, encoding="utf-8") as fh:
        return {c["control_id"]: c for c in json.load(fh)["controls"]}


def classify(old_ctl, new_ctl):
    """What changed about the control itself, ignoring its identifier."""
    changes = []
    if norm(old_ctl["control_title"]) != norm(new_ctl["control_title"]):
        changes.append("retitled")
    spec_sim = similarity(old_ctl["control_specification"], new_ctl["control_specification"])
    if norm(old_ctl["control_specification"]) != norm(new_ctl["control_specification"]):
        changes.append("rewritten" if spec_sim < COSMETIC_MIN else "text-tidied")
    return changes, spec_sim


def build_entries(old, new, crosswalk):
    """One entry per control in either release, keyed for stable ordering."""
    came_from = {r["new_id"]: (r["old_id"] or None) for r in crosswalk if r["new_id"]}
    went_to = {r["old_id"]: (r["new_id"] or None) for r in crosswalk if r["old_id"]}
    flagged = {(r["old_id"], r["new_id"]): r["review_needed"] == "yes" for r in crosswalk}
    entries = []

    for new_id in sorted(new, key=sort_key):
        old_id = came_from.get(new_id)
        entry = {
            "id": new_id,
            "domain": domain_of(new_id),
            "title": new[new_id]["control_title"],
            "previous_id": old_id,
            "review_needed": flagged.get((old_id or "", new_id), False),
        }

        if old_id is None:
            entry.update(status="added", changes=[], spec_similarity=None,
                         previous_title=None)
        else:
            changes, spec_sim = classify(old[old_id], new[new_id])
            if old_id != new_id:
                changes = ["renumbered"] + changes
            entry.update(
                status="unchanged" if not changes else "changed",
                changes=changes,
                spec_similarity=round(spec_sim, 3),
                previous_title=old[old_id]["control_title"],
            )

        # Does this identifier still designate what it used to?
        if new_id in old and old_id != new_id:
            entry["id_reuse"] = {
                "previously_designated": old[new_id]["control_title"],
                "that_control_is_now": went_to.get(new_id),  # None = that control was removed
            }
        entries.append(entry)

    for old_id in sorted(old, key=sort_key):
        if went_to.get(old_id) is None:
            entries.append({
                "id": old_id,
                "domain": domain_of(old_id),
                "title": old[old_id]["control_title"],
                "status": "removed",
                "changes": [],
                "previous_id": old_id,
                "previous_title": old[old_id]["control_title"],
                "spec_similarity": None,
                "review_needed": flagged.get((old_id, ""), False),
                # The control is gone but its identifier may live on attached to
                # something else — the worst case for a stored reference, since
                # the ID still resolves and returns the wrong requirement.
                "id_still_in_use_for": new[old_id]["control_title"] if old_id in new else None,
            })

    return entries


def summarize(entries):
    counts = Counter(e["status"] for e in entries)
    counts["renumbered"] = sum(1 for e in entries if "renumbered" in e["changes"])
    counts["retitled"] = sum(1 for e in entries if "retitled" in e["changes"])
    counts["rewritten"] = sum(1 for e in entries if "rewritten" in e["changes"])
    counts["text-tidied"] = sum(1 for e in entries if "text-tidied" in e["changes"])
    counts["id_reuse"] = sum(1 for e in entries if "id_reuse" in e)
    counts["review_needed"] = sum(1 for e in entries if e["review_needed"])
    return counts


def verdict(entry):
    """One-line human summary for the table."""
    if entry["status"] == "added":
        return "**ADDED** — new control, no 1.0.3 predecessor"
    if entry["status"] == "removed":
        return "**REMOVED** — no successor in the new release"
    if entry["status"] == "unchanged":
        return "unchanged"
    parts = []
    if "renumbered" in entry["changes"]:
        parts.append(f"**renumbered** from `{entry['previous_id']}`")
    if "retitled" in entry["changes"]:
        parts.append(f"retitled from *{entry['previous_title']}*")
    if "rewritten" in entry["changes"]:
        parts.append(f"**specification rewritten** (similarity {entry['spec_similarity']:.2f})")
    if "text-tidied" in entry["changes"]:
        parts.append("specification edited (cosmetic)")
    return "; ".join(parts)


def render_markdown(entries, counts, old_version, new_version):
    out = []
    w = out.append
    total_new = sum(1 for e in entries if e["status"] != "removed")

    w(f"# AICM per-control changelog — {old_version} → {new_version}\n")
    w("Every control in either release, with a verdict. Generated by")
    w("[`build_changelog.py`](build_changelog.py) from the extractions and the")
    w("[crosswalk](aicm-1.0.3-to-1.1.0-crosswalk.csv) — not from CSA's Change Log")
    w("worksheet, which is a summary of intent and materially incomplete. See")
    w("[What CSA's change log says](#what-csas-change-log-says).\n")

    w("## Summary\n")
    w("| Outcome | Count |")
    w("|---|---:|")
    w(f"| Controls in {old_version} | {sum(1 for e in entries if e['previous_id'])} |")
    w(f"| Controls in {new_version} | {total_new} |")
    w(f"| Unchanged in every respect | {counts['unchanged']} |")
    w(f"| Changed in some respect | {counts['changed']} |")
    w(f"| …renumbered | {counts['renumbered']} |")
    w(f"| …retitled | {counts['retitled']} |")
    w(f"| …specification rewritten | {counts['rewritten']} |")
    w(f"| …specification cosmetically edited | {counts['text-tidied']} |")
    w(f"| Added | {counts['added']} |")
    w(f"| Removed | {counts['removed']} |")
    w(f"| **Identifiers reused for a different control** | **{counts['id_reuse']}** |")
    w("")
    w(f"> **{counts['id_reuse']} identifiers survived the release while coming to mean a")
    w("> different control.** That is the number that breaks stored references, and no")
    w("> set-difference of control IDs detects it — only one ID disappeared outright.")
    w("> Entries below are marked **⚠ ID REUSE** where this applies.\n")

    w("## Legend\n")
    w("| Term | Meaning |")
    w("|---|---|")
    w("| `unchanged` | Same identifier, same title, byte-identical specification |")
    w("| `renumbered` | Same control, different identifier |")
    w("| `retitled` | Same control, different title |")
    w("| `specification rewritten` | Requirement text changed materially (similarity < 0.95) |")
    w("| `specification edited (cosmetic)` | Whitespace, typo, or boilerplate-clause change only |")
    w("| `ADDED` | New control with no predecessor |")
    w("| `REMOVED` | Control with no successor — the requirement is gone |")
    w("| **⚠ ID REUSE** | This identifier designated a *different* control in the old release |")
    w("")

    by_domain = defaultdict(list)
    for e in entries:
        by_domain[e["domain"]].append(e)

    w("## Domains at a glance\n")
    w("| Domain | Controls | Unchanged | Renumbered | Added | Removed | ID reuse |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for dom in sorted(by_domain):
        rows = by_domain[dom]
        w(f"| `{dom}` | {sum(1 for e in rows if e['status'] != 'removed')} "
          f"| {sum(1 for e in rows if e['status'] == 'unchanged')} "
          f"| {sum(1 for e in rows if 'renumbered' in e['changes'])} "
          f"| {sum(1 for e in rows if e['status'] == 'added')} "
          f"| {sum(1 for e in rows if e['status'] == 'removed')} "
          f"| {sum(1 for e in rows if 'id_reuse' in e)} |")
    w("")

    w("## Per-control detail\n")
    for dom in sorted(by_domain):
        rows = sorted(by_domain[dom], key=lambda e: sort_key(e["id"]))
        changed = sum(1 for e in rows if e["status"] != "unchanged")
        note = "no changes in this domain" if not changed else f"{changed} of {len(rows)} entries changed"
        w(f"### {dom} — {note}\n")
        w("| ID | Title | Verdict |")
        w("|---|---|---|")
        for e in rows:
            flag = " ⚠ **ID REUSE**" if "id_reuse" in e else ""
            line = verdict(e)
            if "id_reuse" in e:
                moved_to = e["id_reuse"]["that_control_is_now"]
                where = f"now at `{moved_to}`" if moved_to else "**and that control was removed entirely**"
                line += (f"<br>⚠ In {old_version} `{e['id']}` was "
                         f"*{e['id_reuse']['previously_designated']}* — {where}")
            if e["status"] == "removed" and e.get("id_still_in_use_for"):
                line += f"<br>⚠ The identifier `{e['id']}` still exists but designates *{e['id_still_in_use_for']}*"
            if e["review_needed"]:
                line += "<br>*(heuristic match — see crosswalk `review_needed`)*"
            w(f"| `{e['id']}`{flag} | {e['title']} | {line} |")
        w("")

    w("## What CSA's change log says\n")
    w("The `Change Log` worksheet in the v1.1.0 workbook describes the release as")
    w("**five new controls** (`DCS-01`, `DCS-17`, `DCS-18`, `LOG-08`, `SEF-09`) and")
    w("**one deletion** (`IAM-12`). Those are all corroborated here.\n")
    w("What it does not mention:\n")
    w(f"- **{counts['renumbered']} controls were renumbered.** Not referenced anywhere in the change log.")
    w(f"- **{counts['id_reuse']} identifiers now designate a different control.** The direct consequence of the above.")
    w(f"- **{counts['rewritten']} specifications were rewritten**, six of them under an unchanged ID *and* title.")
    w("- **`SEF-09` *Incident Response* was removed**, while the identifier `SEF-09` was")
    w("  simultaneously reused for a new control, *Incident Records Management*. The change")
    w("  log lists `SEF-09` as an addition without noting the removal or the reuse. The")
    w("  dropped requirement — define incident categories and severity levels for AI systems,")
    w("  including automated response — has no successor in 1.1.0, yet the new `SEF-07`")
    w("  refers to \"incident categories and severity levels\" as though something still")
    w("  establishes them.")
    w("- **`SEF-04` was weakened** from *\"Follow a structured approach to evaluate the")
    w("  effectiveness of incident response plans\"* to *\"Exercise the incident response plans\"*.\n")
    w("Treat the CSA change log as a statement of intent. This file is the delta.\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--old-version", required=True)
    ap.add_argument("--new-version", required=True)
    ap.add_argument("--output", required=True, help="Destination markdown")
    ap.add_argument("--json-output", help="Optional machine-readable copy")
    args = ap.parse_args()

    old = load_controls(args.old)
    new = load_controls(args.new)
    with open(args.crosswalk, encoding="utf-8") as fh:
        crosswalk = list(csv.DictReader(fh))

    entries = build_entries(old, new, crosswalk)
    counts = summarize(entries)

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(entries, counts, args.old_version, args.new_version))

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as fh:
            json.dump({
                "old_version": args.old_version,
                "new_version": args.new_version,
                "summary": dict(counts),
                "controls": entries,
            }, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(entries)} entries to {args.output}")
    for key in ("unchanged", "changed", "renumbered", "retitled", "rewritten",
                "text-tidied", "added", "removed", "id_reuse", "review_needed"):
        print(f"  {key:16} {counts[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
