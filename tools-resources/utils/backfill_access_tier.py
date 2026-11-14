#!/usr/bin/env python3
"""Backfill `access_tier: 1` from government source hosts (method "host-suffix").

Under the 4-tier hosting rule a document from a public government website is Tier 1.
This script records that tier, with `tier_evidence` (see METADATA-SCHEMA.md), for
edition metadata whose recorded source URLs are ALL on government hosts, without
fetching anything. A publisher's domain is weak evidence: the tier belongs to the
document, not the domain. So it writes an entry only when every condition holds:

  - the metadata has no `access_tier` yet (entries verified by hand are never touched);
  - the document was acquired: the directory holds content other than README.md,
    metadata and sidecars. A stub whose document was never fetched says nothing about
    how that document is reached;
  - neither the metadata's text (URLs removed) nor its README mentions an access
    restriction (members-only, purchase, subscription, registration, awaiting a licensed
    copy, ...: the gate's ACCESS_RESTRICTION_RE);
  - `license.publicly_redistributable` is already true. A government-host entry that
    says false is usually a stub whose document was never acquired, so whether it is
    public on the web is unknown; the script does not flip it;
  - at least one of `links.textUsed`, `current_extraction.retrieval_url`, `links.source`
    is an http(s) URL, and every one present has a host in the gate's GOV_HOST_SUFFIXES.
    Text taken from a mirror (web.archive.org, a university copy) does not qualify;
  - the file is not under a Tier 3/4 publisher domain (those are fingerprinted by the
    tier gate and change only in a reviewed gate change);
  - the file re-serialises byte-for-byte with json.dumps(indent=2), so the only diff is
    the two inserted fields.

It also reconciles: an entry it tagged earlier (method host-suffix) that no longer meets
these conditions loses both fields again. Entries with any other method are never
touched.

The suffix list, the restriction wording and the evidence rules live in
check_tier_restrictions.py, which validates the result in CI (check 4d).

Usage:
    python3 -I tools-resources/utils/backfill_access_tier.py            # dry run: report only
    python3 -I tools-resources/utils/backfill_access_tier.py --write    # update the files
    options: --repo PATH, --date YYYY-MM-DD (the check date to record; default today)

Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def load_gate():
    spec = importlib.util.spec_from_file_location("check_tier_restrictions",
                                                  os.path.join(HERE, "check_tier_restrictions.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def style_of(text: str, data: dict):
    for ensure_ascii in (False, True):
        for nl in ("\n", ""):
            if json.dumps(data, indent=2, ensure_ascii=ensure_ascii) + nl == text:
                return ensure_ascii, nl
    return None


def qualifies(gate, data: dict, n_content: int, readme_text: str):
    """(evidence url, suffix) when host-suffix may classify the entry, else (None, reason).
    Ignores any tier fields the entry already has."""
    lic = data.get("license") if isinstance(data.get("license"), dict) else {}
    if lic.get("publicly_redistributable") is not True:
        return None, "publicly_redistributable is not true"
    links = data.get("links") if isinstance(data.get("links"), dict) else {}
    ce = data.get("current_extraction") if isinstance(data.get("current_extraction"), dict) else {}
    urls = [u for u in (links.get("textUsed"), ce.get("retrieval_url"), links.get("source"))
            if isinstance(u, str) and u.startswith(("http://", "https://"))]
    if not urls:
        return None, "no source URL"
    suffixes = [gate.gov_host_suffix(u) for u in urls]
    if not all(suffixes):
        return None, "a source URL is not on a government host"
    if not n_content:
        return None, "no acquired content (stub)"
    if gate.restriction_words(gate.access_text(data, readme_text)):
        return None, "metadata or README mentions an access restriction"
    return (urls[0], suffixes[0]), None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    gate = load_gate()
    files, _ = gate.list_entries(args.repo)
    metas, governed = gate.governance(files)
    skipped: Counter = Counter()
    removed_why: Counter = Counter()
    written = removed = kept = 0
    by_suffix: Counter = Counter()
    for d, ms in sorted(metas.items()):
        if len(ms) != 1:
            skipped["more than one metadata file in the directory"] += 1
            continue
        rel = ms[0]
        if gate.restricted_hit(rel):
            skipped["under a Tier 3/4 publisher domain"] += 1
            continue
        path = os.path.join(args.repo, *rel.split("/"))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        try:
            data = json.loads(text)
        except ValueError:
            skipped["not valid JSON"] += 1
            continue
        if not isinstance(data, dict):
            skipped["not a JSON object"] += 1
            continue
        ev = data.get("tier_evidence") if isinstance(data.get("tier_evidence"), dict) else {}
        ours = ev.get("method") == "host-suffix"
        if ("access_tier" in data or "tier_evidence" in data) and not ours:
            skipped["has a tier from another method"] += 1
            continue
        n_content = sum(1 for f in governed.get(d, [])
                        if gate.is_content(f, d) and not f.endswith("-file-metadata.json"))
        readme = os.path.join(args.repo, *d.split("/"), "README.md")
        readme_text = ""
        if f"{d}/README.md" in governed.get(d, []):
            with open(readme, encoding="utf-8", errors="replace") as fh:
                readme_text = fh.read()
        found, reason = qualifies(gate, data, n_content, readme_text)
        style = style_of(text, data)
        if ours:
            if found and found[0] == ev.get("url"):
                kept += 1
                continue
            if style is None:
                skipped["formatting would change (edit by hand)"] += 1
                print(f"  cannot remove (formatting): {rel}")
                continue
            removed += 1
            removed_why[reason or "evidence URL changed"] += 1
            if args.write:
                new = {k: v for k, v in data.items() if k not in ("access_tier", "tier_evidence")}
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(new, indent=2, ensure_ascii=style[0]) + style[1])
            continue
        if not found:
            skipped[reason] += 1
            continue
        if style is None:
            skipped["formatting would change (edit by hand)"] += 1
            print(f"  skip (formatting): {rel}")
            continue
        url, suffix = found
        evidence = {
            "url": url,
            "checked": args.date,
            "method": "host-suffix",
            "note": (f"Classified from the URL host (government suffix {suffix}); not fetched in this pass. Every "
                     "recorded source URL (textUsed, retrieval_url, source) is on a government host, the document "
                     "was acquired, and no access restriction is noted."),
        }
        new = {}
        for k, v in data.items():
            new[k] = v
            if k == "license":
                new["access_tier"] = 1
                new["tier_evidence"] = evidence
        if "access_tier" not in new:
            new["access_tier"] = 1
            new["tier_evidence"] = evidence
        written += 1
        by_suffix[suffix] += 1
        if args.write:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(new, indent=2, ensure_ascii=style[0]) + style[1])
    verb = "" if args.write else "(dry run) "
    print(f"{verb}host-suffix Tier 1: {kept} kept, {written} added, {removed} removed")
    for r, n in removed_why.most_common():
        print(f"  removed because: {r}: {n}")
    for s_, n in sorted(by_suffix.items()):
        print(f"  added via {s_}: {n}")
    print("not classified:")
    for r, n in skipped.most_common():
        print(f"  {n:5d}  {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
