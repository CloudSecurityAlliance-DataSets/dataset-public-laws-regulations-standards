#!/usr/bin/env python3
"""Audit metadata SecIDs against the SecID registry.

For every *-metadata.json in this repo (and the private companion repo
if present), extract the secid field, derive the expected registry
namespace path, and report any namespace that isn't registered.

Exit code: 0 if no missing namespaces, 1 if any are missing.

Usage:
  python3 tools-resources/utils/audit_secid_alignment.py [--registry PATH]
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_REGISTRY = Path.home() / "GitHub/CloudSecurityAlliance/SecID/registry"
DEFAULT_REPOS = [
    Path("/Volumes/MacMiniData/Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards"),
    Path("/Volumes/MacMiniData/Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards"),
]


def derive_registry_path(secid: str):
    """secid:control/nist.gov/800-53@r5 -> control/gov/nist.json
       secid:regulation/bsi.bund.de/c5 -> regulation/de/bund/bsi.json
       secid:regulation/gov.uk/atrs -> regulation/uk/gov.json"""
    if not secid or not secid.startswith("secid:"):
        return None
    body = secid[len("secid:"):]
    parts = body.split("/", 2)
    if len(parts) < 2 or "." not in parts[1]:
        return None
    type_, ns = parts[0], parts[1]
    rev = list(reversed(ns.split(".")))
    if len(rev) == 1:
        return f"{type_}/{rev[0]}.json"
    sub = "/".join(rev[1:-1])
    leaf = rev[-1]
    return f"{type_}/{rev[0]}/{sub}/{leaf}.json" if sub else f"{type_}/{rev[0]}/{leaf}.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                    help="Path to SecID registry (default: %(default)s)")
    args = ap.parse_args()
    registry = Path(args.registry)

    if not registry.is_dir():
        print(f"error: registry not found at {registry}", file=sys.stderr)
        return 2

    missing = defaultdict(list)
    total = 0
    for repo in DEFAULT_REPOS:
        if not repo.is_dir():
            continue
        for p in repo.rglob("*-metadata.json"):
            if p.name.endswith("-file-metadata.json"):
                continue
            try:
                d = json.loads(p.read_text())
            except json.JSONDecodeError as e:
                print(f"warning: failed to parse {p}: {e}", file=sys.stderr)
                continue
            sid = d.get("secid")
            if not sid:
                continue
            total += 1
            rel = derive_registry_path(sid)
            if rel and not (registry / rel).exists():
                missing[rel].append((sid, str(p.relative_to(repo)), repo.name))

    print(f"Scanned: {total} metadata files")
    print(f"Missing namespaces: {len(missing)}")
    if not missing:
        return 0

    for rel in sorted(missing):
        print(f"\n[MISSING] {rel}")
        seen = set()
        for sid, path, repo_name in missing[rel]:
            key = sid.split("@")[0]
            if key in seen:
                continue
            seen.add(key)
            print(f"  {sid}")
            print(f"    {repo_name}: {path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
