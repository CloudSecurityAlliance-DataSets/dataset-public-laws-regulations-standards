#!/usr/bin/env python3
"""Build the AI-CAIQ question crosswalk and per-question CHANGELOG between two releases.

AI-CAIQ question IDs are derived from AICM control IDs — `LOG-15.1` is the first
question for control `LOG-15` — so the control renumbering moved the questions
with it. The drift is worse than for the controls it derives from.

Questions are matched *through their parent controls* rather than by text alone.
The control crosswalk is already verified (50 of 53 renumberings land on an
identical title), so it is far stronger evidence than question text, which is
short, highly templated, and routinely rewords without changing meaning. Only
within a matched control pair do we compare question text.

Three outputs:
    aicm-caiq-<old>-to-<new>-crosswalk.csv   machine-readable question mapping
    <new>/CHANGELOG.md                       per-question changelog
    <new>/aicm-caiq-<new>-changelog.json     same, machine-readable

Usage:
    ./build_caiq_changelog.py \
        --old ../../aicm-caiq/1.0.2/aicm-caiq-1.0.2.json \
        --new ../../aicm-caiq/1.1.0/aicm-caiq-1.1.0.json \
        --control-crosswalk aicm-1.0.3-to-1.1.0-crosswalk.csv \
        --old-version 1.0.2 --new-version 1.1.0 \
        --crosswalk-output aicm-caiq-1.0.2-to-1.1.0-crosswalk.csv \
        --output ../../aicm-caiq/1.1.0/CHANGELOG.md \
        --json-output ../../aicm-caiq/1.1.0/aicm-caiq-1.1.0-changelog.json
"""

import argparse
import csv
import difflib
import json
import re
import sys
from collections import Counter, defaultdict

# Question text similarity at or above which an edit is treated as cosmetic
# rather than a changed question.
COSMETIC_MIN = 0.95

# Floor for pairing two questions inside an already-matched control pair. Lower
# than a standalone text threshold would be, because the parent-control match has
# already established these are the same requirement's questions.
PAIR_MIN = 0.55


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def control_of(question_id):
    """A&A-01.1 -> A&A-01"""
    return question_id.rsplit(".", 1)[0]


def sort_key(question_id):
    control, _, ordinal = question_id.rpartition(".")
    dom, _, num = control.rpartition("-")
    return (dom, int(num) if num.isdigit() else 0, int(ordinal) if ordinal.isdigit() else 0)


def similarity(a, b):
    """Symmetric — difflib's ratio() depends on argument order."""
    return max(
        difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(),
        difflib.SequenceMatcher(None, norm(b), norm(a)).ratio(),
    )


def cell(text):
    return re.sub(r"\s+", " ", (text or "").replace("|", "\\|")).strip()


def load_questions(path):
    with open(path, encoding="utf-8") as fh:
        return {q["question_id"]: q for q in json.load(fh)["questions"]}


def match_questions(old, new, control_map):
    """Return {new_qid: (old_qid, how)} using parent-control anchoring.

    control_map maps an old control ID to its new one. Questions are grouped by
    parent control; within each matched pair we take exact text matches first,
    then mutual-best fuzzy matches, then fall back to ordinal position.
    """
    old_by_control = defaultdict(list)
    for qid, q in old.items():
        old_by_control[control_of(qid)].append(qid)
    new_by_control = defaultdict(list)
    for qid, q in new.items():
        new_by_control[control_of(qid)].append(qid)

    # Invert: which old control feeds each new control?
    source_control = {new_c: old_c for old_c, new_c in control_map.items() if new_c}

    matches = {}
    for new_control, new_qids in new_by_control.items():
        old_control = source_control.get(new_control)
        if old_control is None:
            continue  # new control — all its questions are new
        candidates = sorted(old_by_control.get(old_control, []), key=sort_key)
        remaining = list(candidates)
        pending = sorted(new_qids, key=sort_key)

        # exact text
        for nq in list(pending):
            for oq in list(remaining):
                if norm(new[nq]["question"]) == norm(old[oq]["question"]):
                    matches[nq] = (oq, "exact-text")
                    remaining.remove(oq)
                    pending.remove(nq)
                    break

        # mutual best within the control pair
        for nq in list(pending):
            if not remaining:
                break
            scored = sorted(((similarity(new[nq]["question"], old[oq]["question"]), oq)
                             for oq in remaining), reverse=True)
            score, oq = scored[0]
            if score < PAIR_MIN:
                continue
            back = max(((similarity(old[oq]["question"], new[x]["question"]), x)
                        for x in pending), default=(0, None))
            if back[1] == nq:
                matches[nq] = (oq, f"text({score:.2f})")
                remaining.remove(oq)
                pending.remove(nq)

        # ordinal fallback — same position under the same control
        for nq in list(pending):
            ordinal = nq.rsplit(".", 1)[1]
            twin = [oq for oq in remaining if oq.rsplit(".", 1)[1] == ordinal]
            if twin:
                matches[nq] = (twin[0], "ordinal")
                remaining.remove(twin[0])
                pending.remove(nq)

    return matches


def build_rows(old, new, matches, control_map):
    came_from = matches
    went_to = {oq: nq for nq, (oq, _) in matches.items()}
    rows = []

    for qid in sorted(new, key=sort_key):
        old_qid, how = came_from.get(qid, (None, None))
        q = new[qid]
        row = {
            "question_id": qid,
            "control_id": q["aicm_control_id"],
            "question": q["question"],
            "previous_question_id": old_qid,
            "previous_control_id": old[old_qid]["aicm_control_id"] if old_qid else None,
            "changes": [],
            "text_similarity": None,
            "match_how": how,
            "id_reuse": None,
        }
        if old_qid is None:
            row["status"] = "new"
        else:
            if old_qid != qid:
                row["changes"].append("renumbered")
            sim = similarity(old[old_qid]["question"], q["question"])
            row["text_similarity"] = round(sim, 3)
            if norm(old[old_qid]["question"]) != norm(q["question"]):
                row["changes"].append("reworded" if sim < COSMETIC_MIN else "edited")
            row["status"] = "unchanged" if not row["changes"] else "changed"

        if qid in old and old_qid != qid:
            row["id_reuse"] = {
                "previously_asked": old[qid]["question"],
                "that_question_is_now": went_to.get(qid),
            }
        rows.append(row)

    removed = [{
        "question_id": qid,
        "control_id": old[qid]["aicm_control_id"],
        "question": old[qid]["question"],
        "id_reassigned": qid in new,
    } for qid in sorted(old, key=sort_key) if qid not in went_to]

    return rows, removed


LABEL = {"renumbered": "Renumbered", "reworded": "Reworded", "edited": "Edited"}


def describe(row):
    if row["status"] == "new":
        return "**New**"
    if row["status"] == "unchanged":
        return "Unchanged"
    return ", ".join(LABEL[c] for c in row["changes"])


def notes(row, old_version):
    bits = []
    if row["id_reuse"]:
        moved = row["id_reuse"]["that_question_is_now"]
        where = f"is now `{moved}`" if moved else "was **removed** from this release"
        bits.append(f"⚠ **ID reuse** — in {old_version} `{row['question_id']}` asked a "
                    f"different question, which {where}.")
    if row["previous_control_id"] and row["previous_control_id"] != row["control_id"]:
        bits.append(f"Parent control renumbered `{row['previous_control_id']}` → "
                    f"`{row['control_id']}`.")
    if "reworded" in row["changes"]:
        bits.append(f"Question text materially changed ({row['text_similarity']:.2f} similarity).")
    if "edited" in row["changes"]:
        bits.append("Wording tidied; question unchanged in substance.")
    if row["match_how"] == "ordinal":
        bits.append("*Matched by position within the control — text differs substantially.*")
    return " ".join(bits)


def render(rows, removed, old_version, new_version, counts):
    out = []
    w = out.append
    w(f"# AI-CAIQ {new_version} — question changelog\n")
    w(f"Every question in AI-CAIQ {new_version}, with what it was in {old_version} and")
    w("what changed. Derived by comparing the two extractions directly and generated by")
    w("[`../../aicm/crosswalks/build_caiq_changelog.py`](../../aicm/crosswalks/build_caiq_changelog.py).\n")
    w("Questions are matched **through their parent controls** rather than by text alone.")
    w("Question IDs derive from AICM control IDs, and the")
    w(f"[control crosswalk](../../aicm/crosswalks/aicm-1.0.3-to-{new_version}-crosswalk.csv)")
    w("is independently verified, so it is stronger evidence than question text — which is")
    w("short, heavily templated, and reworded routinely without changing meaning.\n")

    w("## The short version\n")
    w(f"- **{counts['unchanged']} of {counts['total']} questions are unchanged** in every respect.")
    w(f"- **{counts['renumbered']} questions were renumbered** — same question, different ID.")
    w(f"- **{counts['reworded']} questions were materially reworded**; another {counts['edited']}")
    w("  were cosmetically edited.")
    w(f"- **{counts['new']} questions are new**; **{counts['removed']} were removed**.")
    w(f"- **{counts['id_reuse']} question IDs now ask a different question** than they did in")
    w(f"  {old_version}.\n")
    w(f"> ### A completed {old_version} questionnaire cannot be re-scored against {new_version}")
    w(">")
    w(f"> {counts['id_reuse']} question IDs carried over attached to a different question.")
    w("> Matching a vendor's stored answers to this release by question ID will silently")
    w("> attach responses to questions they never answered.")
    w(">")
    w(f"> This follows from the AICM control renumbering — see")
    w("> [`../../aicm/VERSIONING.md`](../../aicm/VERSIONING.md). Migrate through the")
    w(f"> [question crosswalk](../../aicm/crosswalks/aicm-caiq-{old_version}-to-{new_version}-crosswalk.csv),")
    w("> never by string match.\n")

    w("## How to read the table\n")
    w("| Value | Meaning |")
    w("|---|---|")
    w("| `Unchanged` | Same ID, identical question text |")
    w("| `Renumbered` | Same question, different ID |")
    w("| `Reworded` | Question text materially changed (below 0.95 similarity) |")
    w("| `Edited` | Whitespace or trivial wording change only |")
    w("| `New` | No predecessor in the previous release |")
    w("")
    w("**Notes** carries the ID-reuse warning — what happened to the *identifier*, which is")
    w("independent of what happened to the question — plus any parent-control renumbering.\n")

    w("## Machine-readable form\n")
    w(f"Use [`aicm-caiq-{new_version}-changelog.json`](aicm-caiq-{new_version}-changelog.json)")
    w("rather than parsing this table. Each entry in `questions` carries `question_id`,")
    w("`control_id`, `question`, `previous_question_id`, `previous_control_id`, `changes[]`,")
    w("`text_similarity`, `status`, `match_how`, and `id_reuse`.\n")
    w("```python")
    w("import json")
    w(f'changelog = json.load(open("aicm-caiq-{new_version}-changelog.json"))')
    w('repointed = [q for q in changelog["questions"] if q["id_reuse"]]')
    w("```\n")

    w("## Questions\n")
    w(f"| {new_version} ID | Question | Was in {old_version} | What changed | Notes |")
    w("|---|---|---|---|---|")
    for r in rows:
        was = "—" if r["previous_question_id"] is None else f"`{r['previous_question_id']}`"
        flag = " ⚠" if r["id_reuse"] else ""
        q = cell(r["question"])
        if len(q) > 150:
            q = q[:147] + "…"
        w(f"| `{r['question_id']}`{flag} | {q} | {was} | {describe(r)} | {notes(r, old_version)} |")
    w("")

    w(f"## Removed in {new_version}\n")
    if not removed:
        w("No questions were removed.\n")
    else:
        w(f"These questions existed in {old_version} and have no successor in {new_version}.\n")
        w(f"| {old_version} ID | Control | Question | Note |")
        w("|---|---|---|---|")
        for r in removed:
            note = (f"⚠ The identifier `{r['question_id']}` still exists in {new_version}, "
                    "asking a different question."
                    if r["id_reassigned"] else
                    f"Identifier retired — absent from {new_version}.")
            w(f"| `{r['question_id']}` | `{r['control_id']}` | {cell(r['question'])} | {note} |")
        w("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--control-crosswalk", required=True)
    ap.add_argument("--old-version", required=True)
    ap.add_argument("--new-version", required=True)
    ap.add_argument("--crosswalk-output", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--json-output")
    args = ap.parse_args()

    old = load_questions(args.old)
    new = load_questions(args.new)
    with open(args.control_crosswalk, encoding="utf-8") as fh:
        control_map = {r["old_id"]: (r["new_id"] or None)
                       for r in csv.DictReader(fh) if r["old_id"]}

    matches = match_questions(old, new, control_map)
    rows, removed = build_rows(old, new, matches, control_map)

    with open(args.crosswalk_output, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["status", "old_question_id", "new_question_id",
                         "old_control_id", "new_control_id", "change",
                         "text_similarity", "match_how", "id_reuse"])
        for r in rows:
            writer.writerow([
                r["status"], r["previous_question_id"] or "", r["question_id"],
                r["previous_control_id"] or "", r["control_id"],
                "+".join(r["changes"]) or ("added" if r["status"] == "new" else "unchanged"),
                r["text_similarity"] if r["text_similarity"] is not None else "",
                r["match_how"] or "", "yes" if r["id_reuse"] else "no",
            ])
        for r in removed:
            writer.writerow(["removed", r["question_id"], "", r["control_id"], "",
                             "removed", "", "", "yes" if r["id_reassigned"] else "no"])

    tally = Counter(r["status"] for r in rows)
    counts = {
        "total": len(rows),
        "unchanged": tally["unchanged"],
        "changed": tally["changed"],
        "new": tally["new"],
        "removed": len(removed),
        "renumbered": sum(1 for r in rows if "renumbered" in r["changes"]),
        "reworded": sum(1 for r in rows if "reworded" in r["changes"]),
        "edited": sum(1 for r in rows if "edited" in r["changes"]),
        "id_reuse": sum(1 for r in rows if r["id_reuse"]),
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(render(rows, removed, args.old_version, args.new_version, counts))

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as fh:
            json.dump({
                "specification_name": "AI Consensus Assessments Initiative Questionnaire",
                "version": args.new_version,
                "compared_against": args.old_version,
                "summary": counts,
                "questions": rows,
                "removed": removed,
            }, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(rows)} question rows + {len(removed)} removed")
    for k, v in counts.items():
        print(f"  {k:12} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
