#!/usr/bin/env python3
"""Fail when tier-restricted content is committed to this public repository.

The 4-tier hosting rule (Kurt Seifried, 2026-11-09, verbatim):

    "so in general anything we get from a public gov website, goes into the public
    dataset repo regardless of license. in general if it's on the web, and there's
    no login, we treat it as if we can mirror it. if there is a free login, ask me,
    and if it' a paid login, or paid access like iso.org, we do NOT mirror it
    publicly ever unless there is a specific exception granted, and it would have to
    be explicit and well documented and have solid reasons for it."

This gate was added after full text from four Tier 3/4 publishers (HITRUST, AICPA,
CIS, PCI SSC) was found in this repository, where it had been since the first commit
(dataset-public-laws-regulations-standards#148).

What it checks (blocking)
-------------------------
1. No symbolic links or submodule links anywhere in the repository. They could point
   enumeration at content outside the tracked tree.
2. Under any path segment that names a Tier 3 or Tier 4 publisher domain (see
   RESTRICTED_DOMAINS; subdomains match too, so `standards.iso.org` counts as
   `iso.org`), only metadata stubs may exist. A stub is checked by content, not only
   by name. It must sit in an edition directory inside a SecID type root
   (`<type>/<namespace>/<name>/` or `<type>/<namespace>/<name>/<version>/`) and be
   one of these:
   - the edition's own metadata, named `<dir>-metadata.json` or
     `<parent>-<dir>-metadata.json` (one per directory). It must be a JSON object of
     at most METADATA_MAX_BYTES, with no string longer than METADATA_MAX_STRING
     characters, and a `secid` that names this directory;
   - one `README.md` in a directory that has its own metadata, of at most
     README_MAX_BYTES.
   Anything else fails, including per-file `-file-metadata.json` sidecars and
   marker `_meta.json` files. The only way through is an entry in ALLOWLIST, below.
3. Every ALLOWLIST entry is itself validated, and binds to one exact edition
   directory and an explicit list of file names in it. Nothing inherits to
   subdirectories or to sibling editions.

The allowlist lives in this file on purpose. Adding an entry changes a CI gate, which
under the program's rules needs a different-vendor review and a decision record.
Edition metadata cannot grant itself an exception.

What it reports (non-blocking)
------------------------------
Every directory that holds content files while its metadata says
`license.publicly_redistributable: false`. The flag is not yet reliable across the
repository; once the metadata backfill is done, this report can become blocking.

Files come from `git ls-files -s` (tracked files with their modes), so gitignored
local source PDFs do not count. Outside a git work tree the script walks the
filesystem instead.

Usage:
    python3 -I tools-resources/utils/check_tier_restrictions.py [--repo PATH]
    python3 -I tools-resources/utils/check_tier_restrictions.py --self-test

Exit status: 0 pass, 1 violations found (or self-test failure), 2 usage error.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import PurePosixPath

# Publisher domains whose standards are behind a free login (Tier 3) or a paid /
# members-only wall (Tier 4). Sources: AGENTS.md "Licensed/restricted content is not
# committed here", SecID docs/reference/DATA-HOSTING-RULES.md (Rule 0) and
# CSA-Internal-Governance/SecID ADR-003. Add a domain here when a doc calls it
# Tier 3 or 4; removing one weakens the gate and needs a different-vendor review.
RESTRICTED_DOMAINS: dict[str, str] = {
    # Tier 4: paid access, licensed or members-only
    "iso.org": "Tier 4: paid standards",
    "iec.ch": "Tier 4: paid standards",
    "ieee.org": "Tier 4: paid standards",
    "bsigroup.com": "Tier 4: paid standards",
    "cen.eu": "Tier 4: paid standards",
    "isaca.org": "Tier 4: paid / members-only",
    "isc2.org": "Tier 4: paid / members-only",
    "asisonline.org": "Tier 4: paid standards",
    "hitrustalliance.net": "Tier 4: licensed / members-only",
    "securityforum.org": "Tier 4: members-only",
    "sharedassessments.org": "Tier 4: members-only",
    "swift.com": "Tier 4: members-only",
    "pcisecuritystandards.org": "Tier 4 as the program treats it: click-through licence",
    # Tier 3: free login or registration wall (needs Kurt's approval to mirror)
    "aicpa.org": "Tier 3: free AICPA & CIMA account",
    "aicpa-cima.com": "Tier 3: free AICPA & CIMA account",
    "cisecurity.org": "Tier 3: CIS WorkBench / download registration",
    "nfpa.org": "Tier 3: free login",
    "opengroup.org": "Tier 3: free login (TOGAF, Open FAIR)",
}

SECID_TYPES = frozenset({"advisory", "weakness", "ttp", "control", "capability", "methodology",
                         "disclosure", "regulation", "entity", "reference"})

# Stub caps. Set at about twice the largest legitimate stub under a restricted domain
# on 2026-11-13: metadata 7,997 bytes (control/aicpa.org/tsc/2017), longest metadata
# string 1,441 characters (same file), README 3,099 bytes (reference/cisecurity.org/oval).
METADATA_MAX_BYTES = 16 * 1024
METADATA_MAX_STRING = 3000
README_MAX_BYTES = 6 * 1024

# Only Kurt grants exceptions under the 4-tier rule. Changing this weakens the gate.
EXCEPTION_APPROVER = "Kurt Seifried"
RULE_DATE = _dt.date(2026, 11, 9)
_REFERENCE_RE = re.compile(
    r"^https://github\.com/(CloudSecurityAlliance|CloudSecurityAlliance-DataSets|"
    r"CloudSecurityAlliance-Internal|CSA-Internal-Governance)/[A-Za-z0-9._-]+/"
    r"(issues/\d+|pull/\d+|blob/[A-Za-z0-9._/-]+\.md(#[A-Za-z0-9._-]+)?)$")
_HTTPS_RE = re.compile(r"^https://[A-Za-z0-9.-]+\.[A-Za-z]{2,}/\S+$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Reviewed allowlist: the ONLY way content other than a metadata stub may sit under a
# restricted publisher domain. Each entry binds to one exact edition directory, the
# SecID its metadata carries, and an explicit list of file names (fnmatch patterns,
# no "/") directly in that directory. Two kinds:
#   "tier3-4-exception": an explicit, documented exception Kurt granted for Tier 3/4
#       content. approved_by must be EXCEPTION_APPROVER; reference must link the
#       GitHub issue, PR or decision document that records his decision.
#   "tier1-2-source": a source that is itself Tier 1/2 (public, no login) although its
#       publisher's standards are gated. Not an exception; evidence links the public
#       upstream. reference links the reviewed PR that classified it.
# Adding or widening an entry changes this gate: it needs a different-vendor review
# and a decision record. There are no Tier 3/4 exceptions today.
ALLOWLIST: list[dict] = [
    {
        "kind": "tier1-2-source",
        "path": "reference/cisecurity.org/oval",
        "secid": "secid:reference/cisecurity.org/oval",
        "files": ["oval.md", "oval-sections.csv", "oval-sections.json"],
        "approved_by": ("SecID governing agent (Claude), as a Tier 2 classification, not a Tier 3/4 "
                        "exception; subject to the cross-vendor review of PR #149"),
        "date": "2026-11-13",
        "reason": ("OVAL Repository README text and its section split. The upstream is the public GitHub "
                   "repository CISecurity/OVALRepo, readable with no login (Tier 2), although CIS gates "
                   "its Benchmarks and Controls downloads."),
        "reference": "https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/pull/149",
        "evidence": "https://github.com/CISecurity/OVALRepo",
    },
]


# ----------------------------------------------------------------------------- helpers
def restricted_domain(segment: str) -> str | None:
    """Return the restricted domain a path segment names (exact or subdomain), or None."""
    seg = segment.lower()
    for domain in RESTRICTED_DOMAINS:
        if seg == domain or seg.endswith("." + domain):
            return domain
    return None


def own_metadata_names(dir_path: str) -> set[str]:
    p = PurePosixPath(dir_path)
    names = {f"{p.name}-metadata.json"}
    if p.parent.name:
        names.add(f"{p.parent.name}-{p.name}-metadata.json")
    return names


def is_report_stub(name: str) -> bool:
    """Name-only stub test, used only by the non-blocking report."""
    return name == "README.md" or name.endswith("-metadata.json")


def list_entries(root: str, use_git: bool | None = None) -> tuple[list[str], list[str]]:
    """Return (files, links): repo-relative POSIX paths of regular files, and of
    symlinks / submodule links (each reported with its kind)."""
    if use_git is None:
        try:
            out = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                                 capture_output=True, text=True, timeout=60, check=False)
            use_git = out.returncode == 0 and os.path.realpath(out.stdout.strip()) == os.path.realpath(root)
        except (OSError, subprocess.SubprocessError):
            use_git = False
    files, links = [], []
    if use_git:
        out = subprocess.run(["git", "-C", root, "ls-files", "-s", "-z"],
                             capture_output=True, timeout=300, check=True)
        for rec in out.stdout.decode("utf-8").split("\0"):
            if not rec:
                continue
            meta, path = rec.split("\t", 1)
            mode = meta.split(" ", 1)[0]
            if mode == "120000":
                links.append(f"{path} (symlink, git mode 120000)")
            elif mode == "160000":
                links.append(f"{path} (submodule link, git mode 160000)")
            elif os.path.lexists(os.path.join(root, path)):
                # A tracked file deleted in the working tree but not yet staged is skipped.
                files.append(path)
        return sorted(set(files)), sorted(links)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        keep = []
        for d in dirnames:
            if d == ".git":
                continue
            full = os.path.join(dirpath, d)
            if os.path.islink(full):
                links.append(_rel(root, full) + " (symlinked directory)")
            else:
                keep.append(d)
        dirnames[:] = keep
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if os.path.islink(full):
                links.append(_rel(root, full) + " (symlink)")
            else:
                files.append(_rel(root, full))
    return sorted(files), sorted(links)


def _rel(root: str, full: str) -> str:
    return PurePosixPath(*os.path.relpath(full, root).split(os.sep)).as_posix()


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def secid_matches_dir(secid, dir_path: str) -> bool:
    """`secid:<type>/<ns>/<name>[@<version>]` must name this directory; a version
    directory may carry a leading `v` that the SecID omits (PCI `v4.0.1` -> `@4.0.1`)."""
    if not isinstance(secid, str) or not secid.startswith("secid:"):
        return False
    body = secid[len("secid:"):]
    base, _, version = body.partition("@")
    parts = PurePosixPath(dir_path).parts
    if len(parts) == 3:
        return not version and base == "/".join(parts)
    if len(parts) == 4:
        d = parts[3]
        return (base == "/".join(parts[:3]) and bool(version)
                and version in {d, d[1:] if d[:1] in "vV" else d})
    return False


def validate_allowlist(entries: list[dict], today: _dt.date | None = None) -> list[str]:
    """Return the problems with the allowlist (empty list = valid)."""
    today = today or _dt.date.today()
    problems = []
    seen = set()
    for i, e in enumerate(entries):
        tag = f"ALLOWLIST[{i}] ({e.get('path', '?') if isinstance(e, dict) else '?'})"
        if not isinstance(e, dict):
            problems.append(f"{tag}: not an object")
            continue
        for field in ("kind", "path", "secid", "approved_by", "date", "reason", "reference"):
            if not isinstance(e.get(field), str) or not e[field].strip():
                problems.append(f"{tag}: {field} is missing or empty")
        kind = e.get("kind")
        if kind not in ("tier3-4-exception", "tier1-2-source"):
            problems.append(f"{tag}: kind must be tier3-4-exception or tier1-2-source")
        path = e.get("path", "")
        if isinstance(path, str):
            parts = PurePosixPath(path).parts
            if (path != PurePosixPath(path).as_posix() or path.endswith("/") or len(parts) not in (3, 4)
                    or parts[0] not in SECID_TYPES or ".." in parts):
                problems.append(f"{tag}: path must be an exact <type>/<namespace>/<name>[/<version>] directory")
            elif not secid_matches_dir(e.get("secid"), path):
                problems.append(f"{tag}: secid does not name the directory {path}")
            if path in seen:
                problems.append(f"{tag}: duplicate path")
            seen.add(path)
        files = e.get("files")
        if not isinstance(files, list) or not files:
            problems.append(f"{tag}: files must be a non-empty list of file-name patterns")
        else:
            for pat in files:
                if not isinstance(pat, str) or not pat or "/" in pat or pat.strip("*?") == "":
                    problems.append(f"{tag}: bad file pattern {pat!r} (no '/', not a bare wildcard)")
        date = e.get("date")
        if isinstance(date, str) and date:
            try:
                d = _dt.date.fromisoformat(date) if _DATE_RE.match(date) else None
            except ValueError:
                d = None
            if d is None:
                problems.append(f"{tag}: date must be a real YYYY-MM-DD date")
            elif d > today:
                problems.append(f"{tag}: date {date} is in the future")
            elif d < RULE_DATE:
                problems.append(f"{tag}: date {date} predates the 4-tier rule ({RULE_DATE})")
        reason = e.get("reason")
        if isinstance(reason, str) and len(reason.strip()) < 40:
            problems.append(f"{tag}: reason is too short to be a documented reason")
        ref = e.get("reference")
        if isinstance(ref, str) and ref and not _REFERENCE_RE.match(ref):
            problems.append(f"{tag}: reference must link a GitHub issue, PR or decision .md in a CSA org")
        if kind == "tier3-4-exception" and e.get("approved_by") != EXCEPTION_APPROVER:
            problems.append(f"{tag}: a Tier 3/4 exception must be approved_by {EXCEPTION_APPROVER!r}")
        if kind == "tier1-2-source":
            ev = e.get("evidence")
            if not isinstance(ev, str) or not _HTTPS_RE.match(ev):
                problems.append(f"{tag}: a tier1-2-source needs an https evidence URL for the public upstream")
    return problems


# ----------------------------------------------------------------------------- checks
def check_restricted(root: str, files: list[str], allowlist: list[dict]) -> tuple[dict, list[str]]:
    """Blocking check. Returns ({location: {domain, files, reasons}}, notes)."""
    by_dir: dict[str, list[str]] = defaultdict(list)
    for f in files:
        p = PurePosixPath(f)
        by_dir[p.parent.as_posix()].append(p.name)
    entries = {e["path"]: e for e in allowlist}
    violations: dict[str, dict] = {}
    allowed: dict[str, int] = defaultdict(int)
    meta_cache: dict[str, tuple[dict | None, list[str]]] = {}

    def fail(loc, dom, rel, reason):
        v = violations.setdefault(loc, {"domain": dom, "files": [], "reasons": set()})
        v["files"].append(rel)
        v["reasons"].add(reason)

    def own_metadata(dir_path: str) -> tuple[str | None, str | None]:
        names = sorted(n for n in by_dir.get(dir_path, []) if n in own_metadata_names(dir_path))
        if len(names) == 1:
            return f"{dir_path}/{names[0]}", None
        if len(names) > 1:
            return None, f"{dir_path}/ has more than one own-metadata file ({', '.join(names)})"
        return None, None

    def metadata_problems(rel: str) -> tuple[dict | None, list[str]]:
        if rel in meta_cache:
            return meta_cache[rel]
        full = os.path.join(root, *rel.split("/"))
        probs = []
        data = None
        size = os.path.getsize(full)
        if size > METADATA_MAX_BYTES:
            probs.append(f"{rel}: {size} bytes, over the {METADATA_MAX_BYTES}-byte stub cap")
        else:
            try:
                with open(full, encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, ValueError) as exc:
                probs.append(f"{rel}: not valid JSON ({exc})")
            if data is not None and not isinstance(data, dict):
                probs.append(f"{rel}: not a JSON object")
                data = None
            if data is not None:
                longest = max((len(s) for s in _strings(data)), default=0)
                if longest > METADATA_MAX_STRING:
                    probs.append(f"{rel}: a string of {longest} characters, over the "
                                 f"{METADATA_MAX_STRING}-character stub cap")
                if not secid_matches_dir(data.get("secid"), PurePosixPath(rel).parent.as_posix()):
                    probs.append(f"{rel}: secid {data.get('secid')!r} does not name its directory")
        meta_cache[rel] = (data, probs)
        return data, probs

    for rel in files:
        p = PurePosixPath(rel)
        parts = p.parts
        hit = next(((i, d) for i, seg in enumerate(parts[:-1]) if (d := restricted_domain(seg))), None)
        if hit is None:
            continue
        _, dom = hit
        name, dir_path = p.name, p.parent.as_posix()
        dparts = p.parent.parts
        in_edition_dir = dparts[0] in SECID_TYPES and len(dparts) in (3, 4) and restricted_domain(dparts[1])

        # (a) the edition's own metadata
        if in_edition_dir and name in own_metadata_names(dir_path):
            meta_rel, amb = own_metadata(dir_path)
            if amb:
                fail(dir_path, dom, rel, amb)
                continue
            _, probs = metadata_problems(rel)
            for pr in probs:
                fail(dir_path, dom, rel, pr)
            continue

        # (b) one README.md in a directory that has its own valid metadata
        if name == "README.md":
            meta_rel, amb = own_metadata(dir_path) if in_edition_dir else (None, None)
            size = os.path.getsize(os.path.join(root, *parts))
            if not in_edition_dir or meta_rel is None:
                fail(dir_path, dom, rel, f"{rel}: README.md outside an edition directory with its own metadata")
            elif size > README_MAX_BYTES:
                fail(dir_path, dom, rel, f"{rel}: {size} bytes, over the {README_MAX_BYTES}-byte README cap")
            continue

        # (c) anything else needs an exact allowlist entry for this very directory
        entry = entries.get(dir_path)
        if entry is None:
            fail(dir_path, dom, rel, "content file with no ALLOWLIST entry for this exact directory "
                                     "(metadata-like files other than the edition's own count as content)")
            continue
        if not any(fnmatch.fnmatchcase(name, pat) for pat in entry["files"]):
            fail(dir_path, dom, rel, f"{name} is not in the ALLOWLIST entry's files for {dir_path}")
            continue
        meta_rel, amb = own_metadata(dir_path)
        data = metadata_problems(meta_rel)[0] if meta_rel else None
        if data is None or data.get("secid") != entry["secid"]:
            fail(dir_path, dom, rel, f"ALLOWLIST entry for {dir_path} names {entry['secid']}, but the "
                                     "directory's own metadata is missing, invalid or carries another secid")
            continue
        allowed[dir_path] += 1

    notes = []
    for path, n in sorted(allowed.items()):
        e = entries[path]
        notes.append(f"allowed by ALLOWLIST ({e['kind']}): {path}/ {n} files ({e.get('evidence') or e['reference']})")
    for path, e in sorted(entries.items()):
        present = set(by_dir.get(path, []))
        missing = [pat for pat in e["files"] if not any(fnmatch.fnmatchcase(n, pat) for n in present)]
        if missing:
            notes.append(f"stale ALLOWLIST entry {path}: no file matches {missing}")
    return violations, notes


def report_unflagged(root: str, files: list[str]) -> list[tuple[str, int]]:
    """Non-blocking: edition dirs with content files whose metadata says
    license.publicly_redistributable is false."""
    names_by_dir: dict[str, list[str]] = defaultdict(list)
    for f in files:
        p = PurePosixPath(f)
        names_by_dir[p.parent.as_posix()].append(p.name)
    counts: dict[str, int] = defaultdict(int)
    cache: dict[str, bool] = {}
    for rel in files:
        p = PurePosixPath(rel)
        if len(p.parts) < 3 or p.parts[0] not in SECID_TYPES or is_report_stub(p.name):
            continue
        cur = p.parent
        meta = None
        while len(cur.parts) >= 2:
            cands = sorted(n for n in names_by_dir.get(cur.as_posix(), [])
                           if n.endswith("-metadata.json") and not n.endswith("-file-metadata.json"))
            if cands:
                meta = f"{cur.as_posix()}/{cands[0]}"
                break
            cur = cur.parent
        if not meta:
            continue
        if meta not in cache:
            try:
                with open(os.path.join(root, *meta.split("/")), encoding="utf-8") as fh:
                    lic = json.load(fh).get("license")
            except (OSError, ValueError, AttributeError):
                lic = None
            cache[meta] = isinstance(lic, dict) and lic.get("publicly_redistributable") is False
        if cache[meta]:
            counts[PurePosixPath(meta).parent.as_posix()] += 1
    return sorted(counts.items())


# ----------------------------------------------------------------------------- output
def run(root: str, use_git: bool | None = None, out=sys.stdout, allowlist: list[dict] | None = None) -> int:
    allowlist = ALLOWLIST if allowlist is None else allowlist
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    files, links = list_entries(root, use_git)
    status = 0

    print(f"Tier-restriction gate: checked {len(files)} files against "
          f"{len(RESTRICTED_DOMAINS)} Tier 3/4 publisher domains; "
          f"{len(allowlist)} ALLOWLIST entries.", file=out)

    al_problems = validate_allowlist(allowlist)
    if al_problems:
        status = 1
        print("FAIL: the ALLOWLIST itself is invalid:", file=out)
        for pr in al_problems:
            print(f"  {pr}", file=out)
            if in_actions:
                print(f"::error title=Tier gate allowlist::{pr}", file=out)
        print("Fix the ALLOWLIST before anything else is checked.", file=out)
        return status

    if links:
        status = 1
        print(f"FAIL: {len(links)} symlinks or submodule links; none are allowed in this repository:", file=out)
        for ln in links:
            print(f"  {ln}", file=out)
            if in_actions:
                print(f"::error title=Symlink or submodule link::{ln}", file=out)

    violations, notes = check_restricted(root, files, allowlist)
    for n in notes:
        print(f"  {n}", file=out)

    unflagged = report_unflagged(root, files)
    print("", file=out)
    print(f"Non-blocking report: {len(unflagged)} directories hold content files while their "
          "metadata says publicly_redistributable: false.", file=out)
    for d, n in unflagged:
        print(f"  {d}/  ({n} content files)", file=out)
    if in_actions and unflagged:
        print(f"::notice title=Tier gate (non-blocking)::{len(unflagged)} directories hold content while "
              "their metadata says publicly_redistributable: false. See the job log.", file=out)

    print("", file=out)
    if not violations:
        if status == 0:
            print("PASS: no restricted-publisher content beyond validated metadata/README stubs.", file=out)
        return status
    total = sum(len(v["files"]) for v in violations.values())
    print(f"FAIL: {total} files in {len(violations)} directories under Tier 3/4 publisher domains.", file=out)
    print("Under these domains only an edition's own metadata and one README.md may exist, within the "
          "size caps, unless an exact ALLOWLIST entry in this script covers the file. Full text belongs in "
          "dataset-private-laws-regulations-standards.", file=out)
    for loc, v in sorted(violations.items()):
        print(f"  {loc}/  [{v['domain']}: {RESTRICTED_DOMAINS[v['domain']]}]  {len(v['files'])} files", file=out)
        for r in sorted(v["reasons"])[:5]:
            print(f"      reason: {r}", file=out)
        for f in v["files"][:5]:
            print(f"      {f}", file=out)
        if len(v["files"]) > 5:
            print(f"      ... and {len(v['files']) - 5} more", file=out)
        if in_actions:
            print(f"::error title=Tier-restricted content::{loc}/ holds {len(v['files'])} files under "
                  f"{v['domain']} ({RESTRICTED_DOMAINS[v['domain']]}) that are not valid stubs or allowlisted.",
                  file=out)
    return 1


# ----------------------------------------------------------------------------- self-test
def self_test() -> int:
    failures: list[str] = []

    def meta(secid, public=False, **extra):
        d = {"secid": secid, "license": {"spdx": "X", "publicly_redistributable": public}}
        d.update(extra)
        return json.dumps(d, indent=2)

    bogus = {"approved_by": "not Kurt", "date": "2999-01-01", "reference": "https://", "reason": "x"}
    test_exception = {
        "kind": "tier3-4-exception",
        "path": "control/iso.org/27701/2019",
        "secid": "secid:control/iso.org/27701@2019",
        "files": ["27701-2019.md"],
        "approved_by": EXCEPTION_APPROVER,
        "date": "2026-11-13",
        "reason": "Self-test fixture only: stands in for an explicit, documented exception.",
        "reference": "https://github.com/CSA-Internal-Governance/SecID/issues/1",
    }
    allowlist = ALLOWLIST + [test_exception]

    # (path, body, expected_to_fail, case-name). A failing file is expected inside the
    # violation keyed by its directory. Every case below is a separate regression test.
    cases = [
        # --- legitimate stubs
        ("control/iso.org/27001/2022/27001-2022-metadata.json", meta("secid:control/iso.org/27001@2022"), False, "own metadata (versioned)"),
        ("control/iso.org/27001/2022/README.md", "# stub", False, "README beside own metadata"),
        ("control/iso.org/27005/27005-metadata.json", meta("secid:control/iso.org/27005"), False, "own metadata (unversioned)"),
        ("control/pcisecuritystandards.org/pci-dss/v4.0.1/pci-dss-v4.0.1-metadata.json",
         meta("secid:control/pcisecuritystandards.org/pci-dss@4.0.1"), False, "own metadata, v-prefixed version dir"),
        # --- plain content
        ("control/iso.org/27002/2022/27002-2022-metadata.json", meta("secid:control/iso.org/27002@2022"), False, "own metadata"),
        ("control/iso.org/27002/2022/27002-2022.md", "text", True, "content without allowlist"),
        ("control/iso.org/stray.csv", "a,b", True, "content in the namespace directory"),
        ("control/standards.iso.org/x/1/x-1.md", "text", True, "subdomain of a restricted domain"),
        ("reference/ISO.ORG/vocab/vocab.md", "text", True, "upper-case namespace"),
        ("tools-resources/working/pcisecuritystandards.org/pci.md", "text", True, "restricted segment outside type roots"),
        ("tools-resources/working/iec.ch/README.md", "# x", True, "README outside type roots"),
        # --- look-alikes are not restricted
        ("control/notiso.org/a/1/a-1-metadata.json", meta("secid:control/notiso.org/a@1", True), False, "look-alike domain metadata"),
        ("control/notiso.org/a/1/a-1.md", "text", False, "look-alike domain content"),
        ("control/iso.org.example.com/b/b.md", "text", False, "domain as a prefix of another domain"),
        # --- P1-1: stub checks by content, not name
        ("control/iso.org/27017/2015/27017-2015-metadata.json", meta("secid:control/iso.org/27017@2015"), False, "own metadata"),
        ("control/iso.org/27017/2015/controls-file-metadata.json", json.dumps({"text": "x" * 100}), True, "P1-1 full text renamed to a -file-metadata.json sidecar"),
        ("control/iso.org/27017/2015/27017-2015_meta.json", "{}", True, "P1-1 marker _meta.json is content"),
        ("control/iso.org/27017/2015/other-metadata.json", meta("secid:control/iso.org/27017@2015"), True, "P1-1 orphan metadata not named for the directory"),
        ("control/iso.org/27018/2025/27018-2025-metadata.json", meta("secid:control/iso.org/27018@2025"), False, "own metadata"),
        ("control/iso.org/27018/2025/README.md", "# pasted\n" + "full text " * 800, True, "P1-1 full text pasted into README.md (over cap)"),
        ("control/iso.org/27019/2017/27019-2017-metadata.json", json.dumps({"secid": "secid:control/iso.org/27019@2017", "pad": ["y" * 2000] * 10}), True, "P1-1 metadata over the size cap"),
        ("control/iso.org/27031/2011/27031-2011-metadata.json", meta("secid:control/iso.org/27031@2011", description="z" * 3500), True, "P1-1 metadata with an over-long string (3,500 chars, file under the size cap)"),
        ("control/iso.org/27032/2023/27032-2023-metadata.json", "{not json", True, "P1-1 metadata that is not JSON"),
        ("control/iso.org/27033/1/27033-1-metadata.json", "[1, 2]", True, "P1-1 metadata that is not an object"),
        ("control/iso.org/27034/1/27034-1-metadata.json", meta("secid:control/iso.org/99999@1"), True, "P1-1 metadata whose secid names another directory"),
        ("control/iso.org/27035/1/README.md", "# no metadata here", True, "P1-1 README with no own metadata"),
        ("control/iso.org/README.md", "# namespace readme", True, "P1-1 README at the namespace level"),
        ("control/iso.org/27036/1/27036-1-metadata.json", meta("secid:control/iso.org/27036@1"), False, "own metadata"),
        ("control/iso.org/27036/1/readme.md", "lower-case readme", True, "P1-1 README with another spelling"),
        ("control/iso.org/27036/1/text/1-text-metadata.json", meta("secid:control/iso.org/27036@1"), True, "P1-1 fake edition directory nested below an edition"),
        ("control/iso.org/27037/2012/2012-metadata.json", meta("secid:control/iso.org/27037@2012"), True, "P1-1 two own-metadata files in one directory (a)"),
        ("control/iso.org/27037/2012/27037-2012-metadata.json", meta("secid:control/iso.org/27037@2012"), True, "P1-1 two own-metadata files in one directory (b)"),
        # --- P1-2: a self-declared exception in metadata grants nothing
        ("control/aicpa.org/tsc/2017/tsc-2017-metadata.json", meta("secid:control/aicpa.org/tsc@2017", public_exception=bogus), False, "metadata carrying a bogus public_exception (still a valid stub)"),
        ("control/aicpa.org/tsc/2017/tsc-2017.md", "text", True, "P1-2 public_exception in metadata does not allow content"),
        ("control/cisecurity.org/cis-controls/v8/cis-controls-v8-metadata.json",
         meta("secid:control/cisecurity.org/cis-controls@8", public_exception={"approved_by": "Kurt Seifried", "date": "2026-11-13", "reference": "https://github.com/CSA-Internal-Governance/SecID/issues/1", "reason": "A well-formed but self-declared exception in metadata."}),
         False, "metadata carrying a well-formed public_exception"),
        ("control/cisecurity.org/cis-controls/v8/cis-controls-v8.csv", "a,b", True, "P1-2 even a well-formed public_exception in metadata does not allow content"),
        # --- allowlisted exception: exact directory and files only (P2-3)
        ("control/iso.org/27701/2019/27701-2019-metadata.json", meta("secid:control/iso.org/27701@2019"), False, "own metadata"),
        ("control/iso.org/27701/2019/27701-2019.md", "text", False, "allowlisted file in the exact directory"),
        ("control/iso.org/27701/2019/27701-2019.csv", "a,b", True, "P2-3 file not named in the allowlist entry"),
        ("control/iso.org/27701/2019/scripts/parse.py", "print()", True, "P2-3 subdirectory does not inherit the exception"),
        ("control/iso.org/27701/2019/scripts/2019-scripts-metadata.json", meta("secid:control/iso.org/27701@2019"), True, "P2-3 nested metadata does not create an edition"),
        ("control/iso.org/27701/2022/27701-2022-metadata.json", meta("secid:control/iso.org/27701@2022"), False, "own metadata"),
        ("control/iso.org/27701/2022/27701-2019.md", "text", True, "P2-3 sibling edition does not inherit the exception"),
        ("control/iso.org/27701/27701.md", "text", True, "P2-3 parent directory does not inherit the exception"),
        # --- P2-5: OVAL is the exact reviewed files only
        ("reference/cisecurity.org/oval/oval-metadata.json", meta("secid:reference/cisecurity.org/oval", True), False, "OVAL own metadata"),
        ("reference/cisecurity.org/oval/README.md", "# OVAL", False, "OVAL README"),
        ("reference/cisecurity.org/oval/oval.md", "text", False, "OVAL reviewed file oval.md"),
        ("reference/cisecurity.org/oval/oval-sections.csv", "a,b", False, "OVAL reviewed file oval-sections.csv"),
        ("reference/cisecurity.org/oval/oval-sections.json", "[]", False, "OVAL reviewed file oval-sections.json"),
        ("reference/cisecurity.org/oval/extra.csv", "a,b", True, "P2-5 unlisted file beside OVAL"),
        ("reference/cisecurity.org/oval/iso.org/27001/data.csv", "a,b", True, "P2-5 nested path under OVAL"),
        # --- non-blocking report fixtures
        ("control/example.org/doc/1/doc-1-metadata.json", meta("secid:control/example.org/doc@1", False), False, "report: content + false"),
        ("control/example.org/doc/1/doc-1.md", "text", False, "report: content + false"),
        ("control/example.org/doc/2/doc-2-metadata.json", meta("secid:control/example.org/doc@2", True), False, "report: content + true"),
        ("control/example.org/doc/2/doc-2.md", "text", False, "report: content + true"),
    ]
    expected_unflagged = {"control/example.org/doc/1", "control/iso.org/27002/2022", "control/aicpa.org/tsc/2017",
                          "control/cisecurity.org/cis-controls/v8", "control/iso.org/27701/2019",
                          "control/iso.org/27701/2022", "control/iso.org/27017/2015",
                          "control/iso.org/27701/2019/scripts", "control/iso.org/27036/1"}

    if shutil.which("git") is None:
        print("SELF-TEST FAILED: git is required (the symlink check reads git file modes).")
        return 1

    with tempfile.TemporaryDirectory(prefix="tier-gate-selftest-") as tmp:
        for rel, body, _, _ in cases:
            path = os.path.join(tmp, *rel.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)

        files, links = list_entries(tmp, use_git=False)
        if links:
            failures.append(f"unexpected links before the symlink cases: {links}")
        violations, notes = check_restricted(tmp, files, allowlist)
        failing_files = {f for v in violations.values() for f in v["files"]}
        for rel, _, should_fail, name in cases:
            if should_fail and rel not in failing_files:
                failures.append(f"not caught: {name} ({rel})")
            if not should_fail and rel in failing_files:
                failures.append(f"false positive: {name} ({rel})")
        if not any("reference/cisecurity.org/oval/ 3 files" in n for n in notes):
            failures.append(f"OVAL allowance not reported as exactly 3 files: {notes}")
        unflagged = {d for d, _ in report_unflagged(tmp, files)}
        if unflagged != expected_unflagged:
            failures.append(f"non-blocking report: missing {sorted(expected_unflagged - unflagged)}, "
                            f"unexpected {sorted(unflagged - expected_unflagged)}")

        sink = open(os.devnull, "w", encoding="utf-8")
        try:
            if run(tmp, use_git=False, out=sink, allowlist=allowlist) != 1:
                failures.append("run() did not exit 1 on violations")
            for rel, _, should_fail, _ in cases:
                if should_fail:
                    os.remove(os.path.join(tmp, *rel.split("/")))
            if run(tmp, use_git=False, out=sink, allowlist=allowlist) != 0:
                failures.append("run() did not exit 0 once every failing case was removed")
            # P1-2: the bogus exception reproduced by the review, as an allowlist entry
            bad = dict(test_exception, **bogus)
            if run(tmp, use_git=False, out=sink, allowlist=ALLOWLIST + [bad]) != 1:
                failures.append("run() accepted an invalid ALLOWLIST")

            # P2-4: symlinks, by filesystem walk and by git file mode
            os.symlink("/etc/hosts", os.path.join(tmp, "control", "notiso.org", "a", "1", "linked.md"))
            os.symlink(os.path.join(tmp, "control", "iso.org"), os.path.join(tmp, "reference", "linked-dir"))
            _, walk_links = list_entries(tmp, use_git=False)
            if len(walk_links) != 2:
                failures.append(f"P2-4 filesystem walk found {len(walk_links)} links, expected 2: {walk_links}")
            if run(tmp, use_git=False, out=sink, allowlist=allowlist) != 1:
                failures.append("P2-4 run() did not fail on symlinks (walk)")
            subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", tmp], check=True, timeout=60,
                           capture_output=True)
            subprocess.run(["git", "-C", tmp, "-c", "core.symlinks=true", "add", "-A"], check=True, timeout=60,
                           capture_output=True)
            _, git_links = list_entries(tmp, use_git=True)
            if not any("linked.md (symlink, git mode 120000)" in ln for ln in git_links) or \
               not any("linked-dir (symlink, git mode 120000)" in ln for ln in git_links):
                failures.append(f"P2-4 git mode 120000 not detected: {git_links}")
            if run(tmp, use_git=True, out=sink, allowlist=allowlist) != 1:
                failures.append("P2-4 run() did not fail on symlinks (git)")
        finally:
            sink.close()

    today = _dt.date(2026, 11, 13)
    al_cases = [
        ("real ALLOWLIST is valid", ALLOWLIST, True),
        ("test exception is valid", [test_exception], True),
        ("P1-2 review's bogus exception rejected", [dict(test_exception, **bogus)], False),
        ("approved_by someone other than Kurt rejected", [dict(test_exception, approved_by="Someone Else")], False),
        ("future date rejected", [dict(test_exception, date="2026-12-01")], False),
        ("date before the rule rejected", [dict(test_exception, date="2026-01-01")], False),
        ("bare https:// reference rejected", [dict(test_exception, reference="https://")], False),
        ("non-CSA reference rejected", [dict(test_exception, reference="https://github.com/someone/repo/issues/1")], False),
        ("one-word reason rejected", [dict(test_exception, reason="x")], False),
        ("P2-3 publisher-level path rejected", [dict(test_exception, path="control/iso.org")], False),
        ("trailing-slash path rejected", [dict(test_exception, path="control/iso.org/27701/2019/")], False),
        ("secid naming another edition rejected", [dict(test_exception, secid="secid:control/iso.org/27701@2022")], False),
        ("bare wildcard file pattern rejected", [dict(test_exception, files=["*"])], False),
        ("file pattern with a slash rejected", [dict(test_exception, files=["scripts/*.py"])], False),
        ("empty files list rejected", [dict(test_exception, files=[])], False),
        ("unknown kind rejected", [dict(test_exception, kind="exception")], False),
        ("tier1-2-source without evidence rejected", [{k: v for k, v in ALLOWLIST[0].items() if k != "evidence"}], False),
        ("duplicate path rejected", [test_exception, test_exception], False),
    ]
    for name, entries, ok in al_cases:
        got = validate_allowlist(entries, today=today) == []
        if got != ok:
            failures.append(f"allowlist validation: {name} gave the wrong answer")

    n_cases = len(cases) + len(al_cases) + 4  # + exit 1/0 run, invalid-allowlist run, symlink walk, symlink git
    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Self-test passed ({n_cases} cases: {sum(1 for c in cases if c[2])} expected failures among "
          f"{len(cases)} fixture files, {len(al_cases)} allowlist validations, 4 run-level checks).")
    return 0


def list_self_test_cases() -> None:
    """Print the self-test case names (for review)."""
    src = open(__file__, encoding="utf-8").read()
    for m in re.finditer(r'(True|False), "([^"]+)"\),?\n', src):
        print(f"  [{'must fail' if m.group(1) == 'True' else 'must pass'}] {m.group(2)}")
    for m in re.finditer(r'\("([^"]+)", (?:\[|ALLOWLIST)[^\n]*, (True|False)\),\n', src):
        print(f"  [allowlist {'valid' if m.group(2) == 'True' else 'invalid'}] {m.group(1)}")
    for name in ("run() exits 1 on violations, then 0 once every must-fail fixture is removed",
                 "P1-2 run() fails when the review's bogus exception is added to ALLOWLIST",
                 "P2-4 symlinked file and symlinked directory found by the filesystem walk; run() fails",
                 "P2-4 the same links staged in git are found as mode 120000; run() fails"):
        print(f"  [run-level] {name}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=None, help="Repository root (default: two levels above this script)")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixtures and exit")
    ap.add_argument("--list-self-test-cases", action="store_true", help="Print the self-test case names")
    args = ap.parse_args(argv)
    if args.list_self_test_cases:
        list_self_test_cases()
        return 0
    if args.self_test:
        return self_test()
    root = args.repo or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
