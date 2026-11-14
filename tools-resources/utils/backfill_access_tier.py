#!/usr/bin/env python3
"""Backfill `access_tier: 1` from government source hosts (method "host-suffix").

Under the 4-tier hosting rule a document from a public government website is Tier 1.
This script records that tier, with `tier_evidence` (see METADATA-SCHEMA.md), for
edition metadata whose recorded source URLs are ALL on government hosts, without
fetching anything. It writes an entry only when every condition holds:

  - the metadata has no `access_tier` yet (entries verified by hand are never touched);
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

The suffix list and the evidence rules live in check_tier_restrictions.py, which
validates the result in CI (method host-suffix may only claim Tier 1, on a listed host).

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


def candidate(gate, data: dict):
    """(evidence url, suffix) when the entry qualifies, else (None, reason)."""
    if "access_tier" in data or "tier_evidence" in data:
        return None, "already has tier fields"
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
    return (urls[0], suffixes[0]), None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    gate = load_gate()
    files, _ = gate.list_entries(args.repo)
    skipped: Counter = Counter()
    written = 0
    by_suffix: Counter = Counter()
    for rel in files:
        if not gate.is_edition_metadata(rel):
            continue
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
        found, reason = candidate(gate, data)
        if not found:
            skipped[reason] += 1
            continue
        style = style_of(text, data)
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
                     "recorded source URL (textUsed, retrieval_url, source) is on a government host."),
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
    verb = "wrote" if args.write else "would write"
    print(f"{verb} access_tier 1 (host-suffix) to {written} metadata files")
    for s, n in sorted(by_suffix.items()):
        print(f"  {s}: {n}")
    print("skipped:")
    for r, n in skipped.most_common():
        print(f"  {n:5d}  {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
