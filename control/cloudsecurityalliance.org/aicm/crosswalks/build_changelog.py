#!/usr/bin/env python3
"""Build a per-control CHANGELOG for an AICM release.

Produces one row per control in the *new* release — what it is, what it was in
the previous release if anything, what changed, and whether its identifier
carried over cleanly. Controls that existed in the old release with no successor
get their own section, since by definition they have no row in a table keyed on
the new release.

Determinations come from comparing the two extractions directly: identifiers,
titles, and specification text. Nothing is taken from the publisher's own change
log — the point of this file is to be the delta, independently derived.

Reads the crosswalk produced by build_crosswalk.py for the old-ID → new-ID
mapping, so the changelog and the crosswalk can never disagree.

Usage:
    ./build_changelog.py \
        --old ../1.0.3/aicm-1.0.3.json \
        --new ../1.1.0/aicm-1.1.0.json \
        --crosswalk aicm-1.0.3-to-1.1.0-crosswalk.csv \
        --old-version 1.0.3 --new-version 1.1.0 \
        --output ../1.1.0/CHANGELOG.md \
        --json-output ../1.1.0/aicm-1.1.0-changelog.json
"""

import argparse
import csv
import difflib
import json
import re
import sys
from collections import Counter

# Specification similarity at or above which a text edit is treated as cosmetic
# — whitespace, a typo, a boilerplate clause — rather than a changed requirement.
COSMETIC_MIN = 0.95


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def domain_of(control_id):
    return control_id.rsplit("-", 1)[0]


def sort_key(control_id):
    dom, _, num = control_id.rpartition("-")
    return (dom, int(num) if num.isdigit() else 0)


def similarity(a, b):
    """Symmetric — difflib's ratio() depends on argument order."""
    return max(
        difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(),
        difflib.SequenceMatcher(None, norm(b), norm(a)).ratio(),
    )


def load_controls(path):
    with open(path, encoding="utf-8") as fh:
        return {c["control_id"]: c for c in json.load(fh)["controls"]}


def cell(text):
    """Make text safe for a markdown table cell."""
    return re.sub(r"\s+", " ", (text or "").replace("|", "\\|")).strip()


def build_rows(old, new, crosswalk):
    came_from = {r["new_id"]: (r["old_id"] or None) for r in crosswalk if r["new_id"]}
    went_to = {r["old_id"]: (r["new_id"] or None) for r in crosswalk if r["old_id"]}
    flagged = {(r["old_id"], r["new_id"]): r["review_needed"] == "yes" for r in crosswalk}

    rows = []
    for new_id in sorted(new, key=sort_key):
        old_id = came_from.get(new_id)
        ctl = new[new_id]
        row = {
            "id": new_id,
            "domain": domain_of(new_id),
            "title": ctl["control_title"],
            "previous_id": old_id,
            "previous_title": old[old_id]["control_title"] if old_id else None,
            "changes": [],
            "spec_similarity": None,
            "heuristic_match": flagged.get((old_id or "", new_id), False),
            "id_reuse": None,
        }

        if old_id is None:
            row["status"] = "new"
        else:
            prev = old[old_id]
            if old_id != new_id:
                row["changes"].append("renumbered")
            if norm(prev["control_title"]) != norm(ctl["control_title"]):
                row["changes"].append("retitled")
            spec_sim = similarity(prev["control_specification"], ctl["control_specification"])
            row["spec_similarity"] = round(spec_sim, 3)
            if norm(prev["control_specification"]) != norm(ctl["control_specification"]):
                row["changes"].append("rewritten" if spec_sim < COSMETIC_MIN else "edited")
            row["status"] = "unchanged" if not row["changes"] else "changed"

        # Did this identifier designate something else in the old release?
        if new_id in old and old_id != new_id:
            successor = went_to.get(new_id)
            row["id_reuse"] = {
                "previously_designated": old[new_id]["control_title"],
                "that_control_is_now": successor,
            }
        rows.append(row)

    removed = [{
        "id": old_id,
        "domain": domain_of(old_id),
        "title": old[old_id]["control_title"],
        "specification": old[old_id]["control_specification"],
        "id_reassigned_to": new[old_id]["control_title"] if old_id in new else None,
    } for old_id in sorted(old, key=sort_key) if went_to.get(old_id) is None]

    return rows, removed


CHANGE_LABEL = {
    "renumbered": "Renumbered",
    "retitled": "Retitled",
    "rewritten": "Rewritten",
    "edited": "Edited",
}


def describe(row):
    if row["status"] == "new":
        return "**New**"
    if row["status"] == "unchanged":
        return "Unchanged"
    return ", ".join(CHANGE_LABEL[c] for c in row["changes"])


def notes(row, old_version):
    bits = []
    if row["id_reuse"]:
        was = row["id_reuse"]["previously_designated"]
        moved = row["id_reuse"]["that_control_is_now"]
        where = f"is now `{moved}`" if moved else "was **removed** from this release"
        bits.append(f"⚠ **ID reuse** — in {old_version} `{row['id']}` was "
                    f"*{cell(was)}*, which {where}.")
    if "rewritten" in row["changes"]:
        bits.append(f"Requirement text materially changed ({row['spec_similarity']:.2f} similarity).")
    if "edited" in row["changes"]:
        bits.append("Wording tidied; requirement unchanged.")
    if row["status"] == "new":
        bits.append("No predecessor in " + old_version + ".")
    if row["heuristic_match"]:
        bits.append("*Matched heuristically — see crosswalk `review_needed`.*")
    return " ".join(bits)


def render(rows, removed, old_version, new_version, counts):
    out = []
    w = out.append

    w(f"# AICM {new_version} — control changelog\n")
    w(f"Every control in AICM {new_version}, with what it was in {old_version} and what")
    w("changed. Derived by comparing the two extractions directly — identifiers, titles,")
    w("and specification text — and generated by")
    w("[`../crosswalks/build_changelog.py`](../crosswalks/build_changelog.py).\n")

    w("## The short version\n")
    w(f"- **{counts['unchanged']} of {counts['total']} controls are unchanged** in every respect.")
    w(f"- **{counts['renumbered']} controls were renumbered** — same requirement, different identifier.")
    w(f"- **{counts['rewritten']} specifications were materially rewritten**; another")
    w(f"  {counts['edited']} were cosmetically edited.")
    w(f"- **{counts['new']} controls are new**; **{counts['removed']} were removed**.")
    w(f"- **{counts['id_reuse']} identifiers now designate a different control than they did**")
    w(f"  in {old_version}.\n")
    w(f"> ### Read this before reusing any {old_version} control ID")
    w(">")
    w(f"> The renumbering was done in place. {counts['id_reuse']} identifiers survived into")
    w(f"> {new_version} attached to a different control, while only")
    w(f"> {counts['ids_absent_from_new']} identifier from {old_version} is absent altogether.")
    w("> Comparing the two releases by their lists of control IDs therefore shows almost")
    w("> nothing wrong.")
    w(">")
    w(f"> A stored reference to `LOG-15` still resolves in {new_version}. It just answers")
    w("> with a different requirement than it used to. Rows where this applies are marked")
    w("> **⚠ ID reuse** below.")
    w(">")
    w(f"> Cite AICM control IDs with a version — `AICM {new_version} LOG-15`, never")
    w("> `AICM LOG-15` — and migrate stored references through")
    w(f"> [`../crosswalks/aicm-{old_version}-to-{new_version}-crosswalk.csv`]"
      f"(../crosswalks/aicm-{old_version}-to-{new_version}-crosswalk.csv),")
    w("> never by string match.\n")

    w("## How to read the table\n")
    w(f"**Was in {old_version}** names the identifier the same control carried in the previous")
    w("release, with its old title where that also changed. A dash means the control is new.\n")
    w("| Value in *What changed* | Meaning |")
    w("|---|---|")
    w("| `Unchanged` | Same identifier, same title, identical requirement text |")
    w("| `Renumbered` | Same control, different identifier |")
    w("| `Retitled` | Same control, different title |")
    w("| `Rewritten` | Requirement text materially changed (below 0.95 similarity) |")
    w("| `Edited` | Whitespace, typo, or boilerplate-clause change only |")
    w("| `New` | No predecessor in the previous release |")
    w("")
    w("Several values can apply at once — a control may be renumbered *and* retitled *and*")
    w("rewritten. The **Notes** column carries the ID-reuse warning, which is independent of")
    w("everything else: it describes what happened to the *identifier*, not to the control.\n")

    w("## Controls\n")
    w(f"| {new_version} ID | Title | Was in {old_version} | What changed | Notes |")
    w("|---|---|---|---|---|")
    for r in rows:
        if r["previous_id"] is None:
            was = "—"
        elif r["previous_id"] != r["id"] and r["previous_title"] and \
                norm(r["previous_title"]) != norm(r["title"]):
            was = f"`{r['previous_id']}` *{cell(r['previous_title'])}*"
        elif r["previous_id"] != r["id"]:
            was = f"`{r['previous_id']}`"
        elif r["previous_title"] and norm(r["previous_title"]) != norm(r["title"]):
            was = f"`{r['id']}` *{cell(r['previous_title'])}*"
        else:
            was = f"`{r['id']}`"
        flag = " ⚠" if r["id_reuse"] else ""
        w(f"| `{r['id']}`{flag} | {cell(r['title'])} | {was} | {describe(r)} | {notes(r, old_version)} |")
    w("")

    w(f"## Removed in {new_version}\n")
    if not removed:
        w("No controls were removed.\n")
    else:
        w(f"These controls existed in {old_version} and have no successor in {new_version}.")
        w("They have no row above because they are not part of this release.\n")
        for r in removed:
            w(f"### `{r['id']}` — {r['title']}\n")
            w(f"> {cell(r['specification'])}\n")
            if r["id_reassigned_to"]:
                w(f"⚠ The identifier `{r['id']}` still exists in {new_version}, reassigned to")
                w(f"*{cell(r['id_reassigned_to'])}*. A stored reference to `{r['id']}` will")
                w("resolve and return an unrelated requirement.\n")
            else:
                w(f"The identifier `{r['id']}` is retired and does not appear in {new_version}.\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--old-version", required=True)
    ap.add_argument("--new-version", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--json-output")
    args = ap.parse_args()

    old = load_controls(args.old)
    new = load_controls(args.new)
    with open(args.crosswalk, encoding="utf-8") as fh:
        crosswalk = list(csv.DictReader(fh))

    rows, removed = build_rows(old, new, crosswalk)
    tally = Counter(r["status"] for r in rows)
    counts = {
        "total": len(rows),
        "unchanged": tally["unchanged"],
        "changed": tally["changed"],
        "new": tally["new"],
        "removed": len(removed),
        "renumbered": sum(1 for r in rows if "renumbered" in r["changes"]),
        "retitled": sum(1 for r in rows if "retitled" in r["changes"]),
        "rewritten": sum(1 for r in rows if "rewritten" in r["changes"]),
        "edited": sum(1 for r in rows if "edited" in r["changes"]),
        "id_reuse": sum(1 for r in rows if r["id_reuse"]),
        # Identifiers that exist in the old release and not the new one. Distinct
        # from "removed controls": IAM-19's control survived as IAM-18, so the
        # identifier vanished while the requirement did not.
        "ids_absent_from_new": len(set(old) - set(new)),
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(render(rows, removed, args.old_version, args.new_version, counts))

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as fh:
            json.dump({
                "specification_name": "AI Controls Matrix",
                "version": args.new_version,
                "compared_against": args.old_version,
                "summary": counts,
                "controls": rows,
                "removed": removed,
            }, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(rows)} control rows + {len(removed)} removed to {args.output}")
    for k, v in counts.items():
        print(f"  {k:12} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
