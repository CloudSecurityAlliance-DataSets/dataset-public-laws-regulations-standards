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

Threat model
------------
The gate stops restricted content from entering the public repository: text, data or
images from a Tier 3 (free login) or Tier 4 (paid / members-only) publisher committed
by mistake or by an agent acting on its own. It does this mechanically. It cannot
judge whether an approval is authentic.

The ALLOWLIST and FINGERPRINTS below are checked for syntax only: required fields, a
plausible date, a link of the right shape, well-formed hashes. A typed name such as
`approved_by: "Kurt Seifried"` proves nothing. Approval is authentic only because every
change to ALLOWLIST or FINGERPRINTS is a change to this CI gate. Under the program's
rules, such a change needs a different-vendor review, and that review must:
  - open the linked `reference` (and `evidence`) and confirm that Kurt approved that
    exact entry (path, SecID, files) for a Tier 3/4 exception, or that the upstream is
    really public with no login for a Tier 1/2 source;
  - open every new or changed fingerprinted file and confirm that it is only a stub
    (identity metadata and a short description, no restricted text), or that an
    approved ALLOWLIST entry covers it.
A reviewer who does not do this turns the gate into a rubber stamp.

What it checks (blocking)
-------------------------
1. No symbolic links or submodule links anywhere in the repository. They could point
   enumeration at content outside the tracked tree.
2. Every file under a path segment that names a Tier 3 or Tier 4 publisher domain (see
   RESTRICTED_DOMAINS; subdomains match, so `standards.iso.org` counts as `iso.org`)
   must pass BOTH layers:
   Layer 1, reviewed fingerprint: its path and SHA-256 must appear in FINGERPRINTS. A
     new file, or any edit to an existing one, fails until a reviewed gate change adds
     or updates its entry. This stops restricted text from being slipped into a
     capped stub, chunked across new edition directories, or swapped into an existing
     README.
   Layer 2, content rules:
     a. If an exact ALLOWLIST entry covers the file (same directory, file name in the
        entry's list) and the directory's own metadata carries the entry's SecID, the
        file is allowed. The stub caps below do not apply to it.
     b. Otherwise only stubs are allowed: the edition's own metadata, named
        `<dir>-metadata.json` or `<parent>-<dir>-metadata.json` (one per directory,
        in an edition directory `<type>/<namespace>/<name>[/<version>]`): a JSON
        object of at most METADATA_MAX_BYTES, no string longer than
        METADATA_MAX_STRING characters, with a `secid` that names the directory; and
        one `README.md` beside that metadata, of at most README_MAX_BYTES. Anything
        else fails, including `-file-metadata.json` sidecars and `_meta.json` files.
3. ALLOWLIST and FINGERPRINTS are validated. An ALLOWLIST entry binds to one exact
   edition directory and an explicit list of file names in it; nothing inherits to
   subdirectories, siblings or parents.

What it reports (non-blocking)
------------------------------
Every directory that holds content files while its metadata says
`license.publicly_redistributable: false` (a later metadata backfill can make this
blocking), and any FINGERPRINTS or ALLOWLIST entries that no longer match a file.

Files come from `git ls-files -s` (tracked files with their modes), so gitignored local
source PDFs do not count. Outside a git work tree the script walks the filesystem.

Usage:
    python3 -I tools-resources/utils/check_tier_restrictions.py [--repo PATH]
    python3 -I tools-resources/utils/check_tier_restrictions.py --self-test
    python3 -I tools-resources/utils/check_tier_restrictions.py --list-self-test-cases
    python3 -I tools-resources/utils/check_tier_restrictions.py --print-fingerprints
        (prints FINGERPRINTS lines for every file under a restricted domain; paste
        only what a reviewer has checked)

Exit status: 0 pass, 1 violations found (or self-test failure), 2 usage error.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import PurePosixPath

SCRIPT_PATH = "tools-resources/utils/check_tier_restrictions.py"

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

# Stub caps (second layer). Set at about twice the largest legitimate stub under a
# restricted domain on 2026-11-13: metadata 7,997 bytes (control/aicpa.org/tsc/2017),
# longest metadata string 1,441 characters (same file), README 3,099 bytes
# (reference/cisecurity.org/oval).
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
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# ======================================================================================
# REVIEWED GATE DATA. Every change below is a CI-gate change: it needs a different-vendor
# review that verifies the linked decision/evidence and the fingerprinted file contents
# (see "Threat model" above). Syntax checks here do not establish approval.
# ======================================================================================

# The ONLY way content other than a metadata stub may sit under a restricted publisher
# domain. Each entry binds to one exact edition directory, the SecID its metadata
# carries, and an explicit list of file names (fnmatch patterns, no "/") directly in
# that directory. Two kinds:
#   "tier3-4-exception": an explicit, documented exception Kurt granted for Tier 3/4
#       content. approved_by must be EXCEPTION_APPROVER; reference must link the GitHub
#       issue, PR or decision document that records his decision.
#   "tier1-2-source": a source that is itself Tier 1/2 (public, no login) although its
#       publisher's standards are gated. Not an exception; evidence links the public
#       upstream; reference links the reviewed PR that classified it.
# There are no Tier 3/4 exceptions today.
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

# Reviewed SHA-256 of every file allowed under a restricted publisher domain: stubs
# (own metadata, README.md) and files an ALLOWLIST entry covers. Path -> hex digest.
# A new file or an edited one fails until its entry here is added or updated in a
# reviewed gate change. `--print-fingerprints` prints current values; paste only what a
# reviewer has opened and checked.
FINGERPRINTS: dict[str, str] = {
    # 35 stubs (23 metadata, 12 README) and 3 OVAL files covered by ALLOWLIST, reviewed for
    # dataset-public-laws-regulations-standards#149 on 2026-11-13.
    "control/aicpa.org/tsc/2017/README.md": "e44d16a0f927da1b6d7f648e82e18240872125b14939ab1e60acd05605422bfe",
    "control/aicpa.org/tsc/2017/tsc-2017-metadata.json": "b83a91e6b8224bb70fe44dfb06d43bef382b12a7b9922090c68b81274c4688fb",
    "control/cisecurity.org/cis-controls/v8/README.md": "3cdab7b5885a301e311b4f5814453cf741add82359f636c28c2705aa7d628ef6",
    "control/cisecurity.org/cis-controls/v8/cis-controls-v8-metadata.json": "73c6cfa5f4018e54a553f901179bb27bb8081be1d97aa15e068ab6a82921565a",
    "control/hitrustalliance.net/csf/v11.3.0/README.md": "236840a03ff4ee04085ea1775c2804e962bbb13c84ab86279056d55981d16317",
    "control/hitrustalliance.net/csf/v11.3.0/csf-v11.3.0-metadata.json": "09266092d21295587346960d7588d923ab732949a726c076a6b320cb3c282b6c",
    "control/isaca.org/cobit/README.md": "da4647a09b5e6e8135cb38b6c730c3b36e8758736c91f5e52ad7b9834e487bee",
    "control/isaca.org/cobit/cobit-metadata.json": "4e287aebfea350311e3f6f7f20c81f09a74b1834432d0e17c3a2888a18ace041",
    "control/pcisecuritystandards.org/pa-dss/README.md": "4e814862014a2c433dbca0b7e2d90c4cc0401a148e0386a747a34f7f4adec6f2",
    "control/pcisecuritystandards.org/pa-dss/pa-dss-metadata.json": "7e4f055987157aa606ad540adf604e0706e9753bc323d7ff068f91ae4d8f7591",
    "control/pcisecuritystandards.org/pci-dss/v3.2.1/README.md": "347e4fcdbd6a49aa2f2c9d95470b0125efa84f8a9c4ebf7d326714dd6a6a8798",
    "control/pcisecuritystandards.org/pci-dss/v3.2.1/pci-dss-v3.2.1-metadata.json": "fa960e9089e08ee852db89f6ab2061b1c631b56ac1a18280866481f16ae092f7",
    "control/pcisecuritystandards.org/pci-dss/v4.0.1/README.md": "d297f1c3cb018443e049283d7753bb943b715095426991e9d175357b45e7327b",
    "control/pcisecuritystandards.org/pci-dss/v4.0.1/pci-dss-v4.0.1-metadata.json": "6d7ebe1f9bde741f8d0dd980f988de7ace3cea4e81cfc7e46fb5d94c685034d8",
    "control/pcisecuritystandards.org/pci-dss/v4.0/README.md": "fb43e327956a79ccca61cc4eeda6b78651cbbe8c3a1430acc31b5c7d29dac4a9",
    "control/pcisecuritystandards.org/pci-dss/v4.0/pci-dss-v4.0-metadata.json": "338d3956b4b5eaa6b419473708984b7cf5ff56018a4af93cdf9d23240afdc4f5",
    "control/pcisecuritystandards.org/pci-pin/README.md": "e726f77ef61727b21755ddea9203d29ef26b0a4c981e3fce889390fee5b22256",
    "control/pcisecuritystandards.org/pci-pin/pci-pin-metadata.json": "2e8854acf1274542555262afb3edc3d9d9f59c35ea4d4f9618c1161259caf53a",
    "control/pcisecuritystandards.org/secure-software-standard/README.md": "8105b428a0aa7f67e20d980c12e866c070b725c48d43271e11f0cc160fc4e024",
    "control/pcisecuritystandards.org/secure-software-standard/secure-software-standard-metadata.json": "9c5d0764b55b86bcb050db54618d165aed51a9baa67296437e9f8bb77e604d2e",
    "control/securityforum.org/sogp/2022/sogp-2022-metadata.json": "9ba4191550fec35211c10513dfe120664c3fa167ff85df412730f7bcc2701fd6",
    "control/swift.com/csp/README.md": "e58e96052b989af111189acfa9ede5b2a65c3136e00b8c2f062f9fdf8aee166c",
    "control/swift.com/csp/csp-metadata.json": "f5ebaece38fa0310a26df2d1e6fc9cc528f2b175b4d6d0d5b9feb661cda5e49f",
    "reference/asisonline.org/security-industry-glossary/security-industry-glossary-metadata.json": "52a274d680f4427479f77383493cb381d8045d006a0bfef7da51092ca79e4f4f",
    "reference/bsigroup.com/cyber-security-glossary/cyber-security-glossary-metadata.json": "fc7bf73780d6d339c066b285b9464cc2bbef706e9c5470e89062c0be6b5b18dc",
    "reference/cisecurity.org/cybersecurity-terms-definitions/cybersecurity-terms-definitions-metadata.json": "b8d3d5b0141e812ba58847ffaeb9d6c0472e4410d2b242db5ddb60e7fdc80b2e",
    "reference/cisecurity.org/oval/README.md": "c456a117bd26199f27dae84b0e875cd8a667767e09d81c8cfb6bf4636c834d8f",
    "reference/cisecurity.org/oval/oval-metadata.json": "b0669bef4a8efd06527dd149b435843ec42d13f4ad345139dcf247bede9ec1a7",
    "reference/cisecurity.org/oval/oval-sections.csv": "c43122b33a10c3745edd28ad982ca7f954d1a978610b717df236ad09b8ff8b2c",
    "reference/cisecurity.org/oval/oval-sections.json": "1bb87dabd644d152a2c2334022f8126c0f1f066c09470fce8471473b133c2e90",
    "reference/cisecurity.org/oval/oval.md": "481602d98f7c8fdd9460d4f801b4a84b9b79e8a23e6cf8bfadb8baf4a1d023eb",
    "reference/hitrustalliance.net/glossary-of-terms-and-acronyms/glossary-of-terms-and-acronyms-metadata.json": "a7851c9d76f5bf26948621a391125ca4269c5ea18f4e269d693f251f7cad9247",
    "reference/iec.ch/iec-glossary/iec-glossary-metadata.json": "aa15f8e3440890863dfc105b9eba5febfe05665ac27950256c253ed750ea4cd6",
    "reference/isaca.org/cybersecurity-fundamentals-glossary/cybersecurity-fundamentals-glossary-metadata.json": "3c5b0f73dd5cb5e9df74de0521cae6cdc45a3f1997728b769ac99e48ae0e659d",
    "reference/nfpa.org/nfpa-glossary/nfpa-glossary-metadata.json": "83be9009994dc2a9232c1e7d99c5dc713d5ae3c6897608bc86d2792f86d68a26",
    "reference/opengroup.org/opaf-glossary/opaf-glossary-metadata.json": "2da669fd698a03db1eec663c7319d6fd5ca9dfa90347c385731365f63a0fa775",
    "reference/pcisecuritystandards.org/pci-glossary/pci-glossary-metadata.json": "c2de0eb19370b7e75984b6095edeeb3f37e6eec41269a1588e211b482bd615ec",
    "reference/sharedassessments.org/tprm-glossary/tprm-glossary-metadata.json": "e746a7dc49adb0ed9945e03ad0338f9d706ba6fe41129b8e784e0b3097042eb7",
}


# ----------------------------------------------------------------------------- helpers
def restricted_domain(segment: str) -> str | None:
    """Return the restricted domain a path segment names (exact or subdomain), or None."""
    seg = segment.lower()
    for domain in RESTRICTED_DOMAINS:
        if seg == domain or seg.endswith("." + domain):
            return domain
    return None


def restricted_hit(rel: str) -> str | None:
    """The restricted domain named by any directory segment of rel, or None."""
    for seg in PurePosixPath(rel).parts[:-1]:
        dom = restricted_domain(seg)
        if dom:
            return dom
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


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
    """Syntax checks on ALLOWLIST (empty list = valid). These do not establish approval;
    see the threat model."""
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


def validate_fingerprints(fingerprints: dict) -> list[str]:
    """Syntax checks on FINGERPRINTS (empty list = valid)."""
    if not isinstance(fingerprints, dict):
        return ["FINGERPRINTS must be a dict of path -> sha256"]
    problems = []
    for path, digest in fingerprints.items():
        if (not isinstance(path, str) or path != PurePosixPath(path).as_posix() or ".." in PurePosixPath(path).parts
                or path.startswith("/")):
            problems.append(f"FINGERPRINTS: bad path {path!r}")
        elif restricted_hit(path) is None:
            problems.append(f"FINGERPRINTS: {path} is not under a restricted publisher domain")
        if not isinstance(digest, str) or not _SHA256_RE.match(digest):
            problems.append(f"FINGERPRINTS: {path} needs a lower-case 64-hex SHA-256, got {digest!r}")
    return problems


def fingerprint_problem(root: str, rel: str, fingerprints: dict) -> str | None:
    """Layer 1: the file's path and SHA-256 must match a reviewed FINGERPRINTS entry."""
    actual = sha256_file(os.path.join(root, *rel.split("/")))
    expected = fingerprints.get(rel)
    line = f'    "{rel}": "{actual}",'
    if expected is None:
        return (f"{rel} has no reviewed fingerprint. If it is a stub (or an approved ALLOWLIST entry covers "
                f"it), add this line to FINGERPRINTS in {SCRIPT_PATH}:\n{line}\n"
                "        That is a CI-gate change: it needs a cross-vendor review that opens the file and confirms "
                "it holds no restricted text.")
    if expected != actual:
        return (f"{rel} changed since its fingerprint was reviewed ({expected[:12]}... -> {actual[:12]}...). "
                f"If the new content is still only a stub, replace its FINGERPRINTS entry in {SCRIPT_PATH} with:\n"
                f"{line}\n        That is a CI-gate change and needs a cross-vendor review of the new content.")
    return None


# ----------------------------------------------------------------------------- checks
def check_restricted(root: str, files: list[str], allowlist: list[dict],
                     fingerprints: dict) -> tuple[dict, list[str], int]:
    """Blocking check. Returns ({location: {domain, files, reasons}}, notes, n_restricted)."""
    by_dir: dict[str, list[str]] = defaultdict(list)
    for f in files:
        p = PurePosixPath(f)
        by_dir[p.parent.as_posix()].append(p.name)
    entries = {e["path"]: e for e in allowlist}
    violations: dict[str, dict] = {}
    allowed: dict[str, int] = defaultdict(int)
    meta_cache: dict[str, tuple[dict | None, list[str]]] = {}
    seen_restricted: set[str] = set()

    def fail(loc, dom, rel, reason):
        v = violations.setdefault(loc, {"domain": dom, "files": [], "reasons": []})
        if rel not in v["files"]:
            v["files"].append(rel)
        if reason not in v["reasons"]:
            v["reasons"].append(reason)

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
        dom = restricted_hit(rel)
        if dom is None:
            continue
        seen_restricted.add(rel)
        p = PurePosixPath(rel)
        name, dir_path = p.name, p.parent.as_posix()
        dparts = p.parent.parts
        in_edition_dir = bool(dparts[0] in SECID_TYPES and len(dparts) in (3, 4) and restricted_domain(dparts[1]))

        # Layer 1: reviewed fingerprint (applies to every file, stub or allowlisted)
        fp = fingerprint_problem(root, rel, fingerprints)
        if fp:
            fail(dir_path, dom, rel, fp)

        # Layer 2a: an exact ALLOWLIST allowance, evaluated first
        entry = entries.get(dir_path)
        if entry is not None and any(fnmatch.fnmatchcase(name, pat) for pat in entry["files"]):
            meta_rel, amb = own_metadata(dir_path)
            data = metadata_problems(meta_rel)[0] if meta_rel else None
            if amb or data is None or data.get("secid") != entry["secid"]:
                fail(dir_path, dom, rel, f"ALLOWLIST entry for {dir_path} names {entry['secid']}, but the "
                                         "directory's own metadata is missing, invalid, ambiguous or carries "
                                         "another secid")
            elif not fp:
                allowed[dir_path] += 1
            continue

        # Layer 2b: fallback stub rules for files no allowance covers
        if in_edition_dir and name in own_metadata_names(dir_path):
            _, amb = own_metadata(dir_path)
            if amb:
                fail(dir_path, dom, rel, amb)
            else:
                for pr in metadata_problems(rel)[1]:
                    fail(dir_path, dom, rel, pr)
            continue
        if name == "README.md":
            meta_rel, _ = own_metadata(dir_path) if in_edition_dir else (None, None)
            size = os.path.getsize(os.path.join(root, *p.parts))
            if not in_edition_dir or meta_rel is None:
                fail(dir_path, dom, rel, f"{rel}: README.md outside an edition directory with its own metadata")
            elif size > README_MAX_BYTES:
                fail(dir_path, dom, rel, f"{rel}: {size} bytes, over the {README_MAX_BYTES}-byte README cap "
                                         "(an exact ALLOWLIST entry can allow a larger one)")
            continue
        if entry is None:
            fail(dir_path, dom, rel, "content file with no ALLOWLIST entry for this exact directory "
                                     "(metadata-like files other than the edition's own count as content)")
        else:
            fail(dir_path, dom, rel, f"{name} is not in the ALLOWLIST entry's files for {dir_path}")

    notes = []
    for path, n in sorted(allowed.items()):
        e = entries[path]
        notes.append(f"allowed by ALLOWLIST ({e['kind']}): {path}/ {n} files ({e.get('evidence') or e['reference']})")
    for path, e in sorted(entries.items()):
        present = set(by_dir.get(path, []))
        missing = [pat for pat in e["files"] if not any(fnmatch.fnmatchcase(n, pat) for n in present)]
        if missing:
            notes.append(f"stale ALLOWLIST entry {path}: no file matches {missing}")
    stale = sorted(set(fingerprints) - set(files))
    if stale:
        notes.append(f"{len(stale)} stale FINGERPRINTS entries (file no longer present): {', '.join(stale[:5])}"
                     + (" ..." if len(stale) > 5 else ""))
    return violations, notes, len(seen_restricted)


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
def run(root: str, use_git: bool | None = None, out=sys.stdout, allowlist: list[dict] | None = None,
        fingerprints: dict | None = None) -> int:
    allowlist = ALLOWLIST if allowlist is None else allowlist
    fingerprints = FINGERPRINTS if fingerprints is None else fingerprints
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    files, links = list_entries(root, use_git)
    status = 0

    print(f"Tier-restriction gate: checked {len(files)} files against "
          f"{len(RESTRICTED_DOMAINS)} Tier 3/4 publisher domains; {len(allowlist)} ALLOWLIST entries; "
          f"{len(fingerprints)} reviewed FINGERPRINTS.", file=out)

    data_problems = validate_allowlist(allowlist) + validate_fingerprints(fingerprints)
    if data_problems:
        print("FAIL: the gate's reviewed data (ALLOWLIST / FINGERPRINTS) is invalid:", file=out)
        for pr in data_problems:
            print(f"  {pr}", file=out)
            if in_actions:
                print(f"::error title=Tier gate data::{pr}", file=out)
        print("Fix the gate data before anything else is checked.", file=out)
        return 1

    if links:
        status = 1
        print(f"FAIL: {len(links)} symlinks or submodule links; none are allowed in this repository:", file=out)
        for ln in links:
            print(f"  {ln}", file=out)
            if in_actions:
                print(f"::error title=Symlink or submodule link::{ln}", file=out)

    violations, notes, n_restricted = check_restricted(root, files, allowlist, fingerprints)
    print(f"  {n_restricted} files sit under restricted publisher domains; each needs a reviewed fingerprint.",
          file=out)
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
            print("PASS: every file under a restricted publisher domain matches a reviewed fingerprint and is "
                  "a valid stub or exactly allowlisted.", file=out)
        return status
    total = sum(len(v["files"]) for v in violations.values())
    print(f"FAIL: {total} files in {len(violations)} directories under Tier 3/4 publisher domains.", file=out)
    print("Under these domains a file must (1) match a reviewed SHA-256 in FINGERPRINTS and (2) be the edition's "
          "own metadata or one README.md within the size caps, unless an exact ALLOWLIST entry covers it. Both "
          f"lists live in {SCRIPT_PATH}; changing them is a CI-gate change that needs a cross-vendor review. "
          "Full text belongs in dataset-private-laws-regulations-standards.", file=out)
    for loc, v in sorted(violations.items()):
        print(f"  {loc}/  [{v['domain']}: {RESTRICTED_DOMAINS[v['domain']]}]  {len(v['files'])} files", file=out)
        for r in v["reasons"][:4]:
            print(f"      reason: {r}", file=out)
        if len(v["reasons"]) > 4:
            print(f"      ... and {len(v['reasons']) - 4} more reasons", file=out)
        for f in v["files"][:5]:
            print(f"      {f}", file=out)
        if len(v["files"]) > 5:
            print(f"      ... and {len(v['files']) - 5} more", file=out)
        if in_actions:
            print(f"::error title=Tier-restricted content::{loc}/ holds {len(v['files'])} files under "
                  f"{v['domain']} ({RESTRICTED_DOMAINS[v['domain']]}) without a reviewed fingerprint or that are "
                  "not valid stubs / allowlisted. See the job log for the exact lines to add after review.",
                  file=out)
    return 1


def print_fingerprints(root: str) -> int:
    files, _ = list_entries(root)
    for rel in files:
        if restricted_hit(rel):
            print(f'    "{rel}": "{sha256_file(os.path.join(root, *rel.split("/")))}",')
    return 0


# ----------------------------------------------------------------------------- self-test
FROZEN_TODAY = _dt.date(2026, 11, 13)  # synthetic fixtures only; the real data uses today's date


def _self_test_data():
    """All self-test cases, shared by --self-test and --list-self-test-cases."""
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
    readme_exception = dict(test_exception, path="control/iso.org/27799/2016", secid="secid:control/iso.org/27799@2016",
                            files=["README.md", "27799-2016.md"])
    allowlist = ALLOWLIST + [test_exception, readme_exception]
    restricted_text = "Clause 5.1 The organization shall determine external and internal issues. " * 20  # ~1.5 KB

    # (path, body, must_fail, name). Every file under a restricted domain is fingerprinted
    # with its own body unless FP_OVERRIDE says otherwise, so the content cases below
    # fail on layer 2 alone and the fingerprint cases fail on layer 1 alone.
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
        # --- round 2 P1: every restricted file needs a reviewed fingerprint (layer 1)
        ("control/iso.org/27099/2022/27099-2022-metadata.json",
         meta("secid:control/iso.org/27099@2022", description=restricted_text), True,
         "R2-P1 under-cap restricted text in a new edition's metadata (not fingerprinted)"),
        ("control/iso.org/27100/2020/27100-2020-metadata.json",
         meta("secid:control/iso.org/27100@2020", text=restricted_text[:700]), True,
         "R2-P1 restricted text chunked across new edition dirs (chunk 1)"),
        ("control/iso.org/27102/2019/27102-2019-metadata.json",
         meta("secid:control/iso.org/27102@2019", text=restricted_text[700:1400]), True,
         "R2-P1 restricted text chunked across new edition dirs (chunk 2)"),
        ("control/hitrustalliance.net/csf/v11.3.0/csf-v11.3.0-metadata.json",
         meta("secid:control/hitrustalliance.net/csf@v11.3.0"), False, "own metadata"),
        ("control/hitrustalliance.net/csf/v11.3.0/README.md", "# HITRUST CSF\n\n" + restricted_text, True,
         "R2-P1 existing README edited to hold restricted text under the cap (fingerprint mismatch)"),
        ("control/iso.org/27103/2018/27103-2018-metadata.json", meta("secid:control/iso.org/27103@2018"), False, "own metadata"),
        ("control/iso.org/27103/2018/README.md", "# a short new README", True,
         "R2-P1 new README with no fingerprint in an existing edition"),
        # --- P1-1 (round 1): stub checks by content, not name (layer 2; fingerprinted)
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
        ("control/iso.org/27701/2019/27701-2019-extra.md", "text", True, "R2-P1 allowlisted directory, file not in the entry and not fingerprinted"),
        # --- round 2 P2: an exact allowance can authorize a README over the stub cap
        ("control/iso.org/27799/2016/27799-2016-metadata.json", meta("secid:control/iso.org/27799@2016"), False, "own metadata"),
        ("control/iso.org/27799/2016/README.md", "# approved long README\n" + "approved text " * 800, False,
         "R2-P2 README over the stub cap passes when an exact ALLOWLIST entry lists it"),
        ("control/iso.org/27799/2016/27799-2016.md", "approved text", False, "allowlisted content beside it"),
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
    # path -> None (no fingerprint) or the reviewed original body (fingerprint mismatch)
    fp_override = {
        "control/iso.org/27099/2022/27099-2022-metadata.json": None,
        "control/iso.org/27100/2020/27100-2020-metadata.json": None,
        "control/iso.org/27102/2019/27102-2019-metadata.json": None,
        "control/hitrustalliance.net/csf/v11.3.0/README.md": "# HITRUST CSF\n\nMetadata-only stub.\n",
        "control/iso.org/27103/2018/README.md": None,
        "control/iso.org/27701/2019/27701-2019-extra.md": None,
    }
    expected_unflagged = {"control/example.org/doc/1", "control/iso.org/27002/2022", "control/aicpa.org/tsc/2017",
                          "control/cisecurity.org/cis-controls/v8", "control/iso.org/27701/2019",
                          "control/iso.org/27701/2022", "control/iso.org/27017/2015",
                          "control/iso.org/27701/2019/scripts", "control/iso.org/27036/1",
                          "control/iso.org/27799/2016"}

    today = _dt.date.today()
    al_cases = [  # (name, entries, valid?, clock) clock None = today's real date
        ("production ALLOWLIST is valid against today's date", ALLOWLIST, True, None),
        ("R2-P2 production-style entry dated today validates", [dict(test_exception, date=today.isoformat())], True, None),
        ("test exception is valid", [test_exception], True, FROZEN_TODAY),
        ("P1-2 review's bogus exception rejected", [dict(test_exception, **bogus)], False, FROZEN_TODAY),
        ("approved_by someone other than Kurt rejected", [dict(test_exception, approved_by="Someone Else")], False, FROZEN_TODAY),
        ("future date rejected", [dict(test_exception, date="2026-12-01")], False, FROZEN_TODAY),
        ("future date rejected against today's date", [dict(test_exception, date=(today + _dt.timedelta(days=1)).isoformat())], False, None),
        ("date before the rule rejected", [dict(test_exception, date="2026-01-01")], False, FROZEN_TODAY),
        ("bare https:// reference rejected", [dict(test_exception, reference="https://")], False, FROZEN_TODAY),
        ("non-CSA reference rejected", [dict(test_exception, reference="https://github.com/someone/repo/issues/1")], False, FROZEN_TODAY),
        ("one-word reason rejected", [dict(test_exception, reason="x")], False, FROZEN_TODAY),
        ("P2-3 publisher-level path rejected", [dict(test_exception, path="control/iso.org")], False, FROZEN_TODAY),
        ("trailing-slash path rejected", [dict(test_exception, path="control/iso.org/27701/2019/")], False, FROZEN_TODAY),
        ("secid naming another edition rejected", [dict(test_exception, secid="secid:control/iso.org/27701@2022")], False, FROZEN_TODAY),
        ("bare wildcard file pattern rejected", [dict(test_exception, files=["*"])], False, FROZEN_TODAY),
        ("file pattern with a slash rejected", [dict(test_exception, files=["scripts/*.py"])], False, FROZEN_TODAY),
        ("empty files list rejected", [dict(test_exception, files=[])], False, FROZEN_TODAY),
        ("unknown kind rejected", [dict(test_exception, kind="exception")], False, FROZEN_TODAY),
        ("tier1-2-source without evidence rejected", [{k: v for k, v in ALLOWLIST[0].items() if k != "evidence"}], False, FROZEN_TODAY),
        ("duplicate path rejected", [test_exception, test_exception], False, FROZEN_TODAY),
    ]
    fp_cases = [  # (name, fingerprints, valid?)
        ("production FINGERPRINTS is valid", FINGERPRINTS, True),
        ("fingerprint that is not 64 hex rejected", {"control/iso.org/a/a-metadata.json": "abc"}, False),
        ("upper-case hex fingerprint rejected", {"control/iso.org/a/a-metadata.json": "A" * 64}, False),
        ("fingerprint for a path outside restricted domains rejected", {"control/nist.gov/a/a-metadata.json": "a" * 64}, False),
        ("fingerprint path with .. rejected", {"control/iso.org/../x/a.md": "a" * 64}, False),
    ]
    run_cases = [
        "run() exits 1 on violations, then 0 once every must-fail fixture is removed",
        "P1-2 run() fails when the review's bogus exception is added to ALLOWLIST",
        "R2-P1 run() fails when FINGERPRINTS holds a malformed digest",
        "P2-4 symlinked file and symlinked directory found by the filesystem walk; run() fails",
        "P2-4 the same links staged in git are found as mode 120000; run() fails",
    ]
    return dict(cases=cases, fp_override=fp_override, expected_unflagged=expected_unflagged, al_cases=al_cases,
                fp_cases=fp_cases, run_cases=run_cases, allowlist=allowlist, test_exception=test_exception,
                bogus=bogus)


def self_test() -> int:
    t = _self_test_data()
    cases, allowlist = t["cases"], t["allowlist"]
    failures: list[str] = []

    if shutil.which("git") is None:
        print("SELF-TEST FAILED: git is required (the symlink check reads git file modes).")
        return 1

    fingerprints = {}
    for rel, body, _, _ in cases:
        if restricted_hit(rel) is None:
            continue
        reviewed = t["fp_override"].get(rel, body) if rel in t["fp_override"] else body
        if reviewed is not None:
            fingerprints[rel] = hashlib.sha256(reviewed.encode("utf-8")).hexdigest()

    with tempfile.TemporaryDirectory(prefix="tier-gate-selftest-") as tmp:
        for rel, body, _, _ in cases:
            path = os.path.join(tmp, *rel.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(body)

        files, links = list_entries(tmp, use_git=False)
        if links:
            failures.append(f"unexpected links before the symlink cases: {links}")
        violations, notes, _ = check_restricted(tmp, files, allowlist, fingerprints)
        failing_files = {f for v in violations.values() for f in v["files"]}
        for rel, _, should_fail, name in cases:
            if should_fail and rel not in failing_files:
                failures.append(f"not caught: {name} ({rel})")
            if not should_fail and rel in failing_files:
                failures.append(f"false positive: {name} ({rel})")
        if not any("reference/cisecurity.org/oval/ 3 files" in n for n in notes):
            failures.append(f"OVAL allowance not reported as exactly 3 files: {notes}")
        hit_msgs = [r for v in violations.values() for r in v["reasons"] if "27099-2022-metadata.json has no reviewed" in r]
        if not hit_msgs or "add this line to FINGERPRINTS" not in hit_msgs[0] or "cross-vendor review" not in hit_msgs[0]:
            failures.append("the missing-fingerprint message does not say exactly what to add and that it needs review")
        unflagged = {d for d, _ in report_unflagged(tmp, files)}
        if unflagged != t["expected_unflagged"]:
            failures.append(f"non-blocking report: missing {sorted(t['expected_unflagged'] - unflagged)}, "
                            f"unexpected {sorted(unflagged - t['expected_unflagged'])}")

        sink = open(os.devnull, "w", encoding="utf-8")
        try:
            if run(tmp, use_git=False, out=sink, allowlist=allowlist, fingerprints=fingerprints) != 1:
                failures.append("run() did not exit 1 on violations")
            for rel, _, should_fail, _ in cases:
                if should_fail:
                    os.remove(os.path.join(tmp, *rel.split("/")))
            if run(tmp, use_git=False, out=sink, allowlist=allowlist, fingerprints=fingerprints) != 0:
                failures.append("run() did not exit 0 once every failing case was removed")
            bad = dict(t["test_exception"], **t["bogus"])
            if run(tmp, use_git=False, out=sink, allowlist=ALLOWLIST + [bad], fingerprints=fingerprints) != 1:
                failures.append("run() accepted an invalid ALLOWLIST")
            if run(tmp, use_git=False, out=sink, allowlist=allowlist,
                   fingerprints=dict(fingerprints, **{"control/iso.org/27001/2022/README.md": "0" * 63})) != 1:
                failures.append("run() accepted a malformed FINGERPRINTS digest")

            # P2-4: symlinks, by filesystem walk and by git file mode
            os.symlink("/etc/hosts", os.path.join(tmp, "control", "notiso.org", "a", "1", "linked.md"))
            os.symlink(os.path.join(tmp, "control", "iso.org"), os.path.join(tmp, "reference", "linked-dir"))
            _, walk_links = list_entries(tmp, use_git=False)
            if len(walk_links) != 2:
                failures.append(f"P2-4 filesystem walk found {len(walk_links)} links, expected 2: {walk_links}")
            if run(tmp, use_git=False, out=sink, allowlist=allowlist, fingerprints=fingerprints) != 1:
                failures.append("P2-4 run() did not fail on symlinks (walk)")
            subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", tmp], check=True, timeout=60,
                           capture_output=True)
            subprocess.run(["git", "-C", tmp, "-c", "core.symlinks=true", "add", "-A"], check=True, timeout=60,
                           capture_output=True)
            _, git_links = list_entries(tmp, use_git=True)
            if not any("linked.md (symlink, git mode 120000)" in ln for ln in git_links) or \
               not any("linked-dir (symlink, git mode 120000)" in ln for ln in git_links):
                failures.append(f"P2-4 git mode 120000 not detected: {git_links}")
            if run(tmp, use_git=True, out=sink, allowlist=allowlist, fingerprints=fingerprints) != 1:
                failures.append("P2-4 run() did not fail on symlinks (git)")
        finally:
            sink.close()

    for name, entries, ok, clock in t["al_cases"]:
        if (validate_allowlist(entries, today=clock) == []) != ok:
            failures.append(f"allowlist validation: {name} gave the wrong answer")
    for name, fps, ok in t["fp_cases"]:
        if (validate_fingerprints(fps) == []) != ok:
            failures.append(f"fingerprint validation: {name} gave the wrong answer")

    n = len(cases) + len(t["al_cases"]) + len(t["fp_cases"]) + len(t["run_cases"])
    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Self-test passed ({n} cases: {len(cases)} fixture files, {sum(1 for c in cases if c[2])} of which must "
          f"fail; {len(t['al_cases'])} allowlist validations; {len(t['fp_cases'])} fingerprint validations; "
          f"{len(t['run_cases'])} run-level checks).")
    return 0


def list_self_test_cases() -> int:
    t = _self_test_data()
    for rel, _, must_fail, name in t["cases"]:
        print(f"  [{'must fail' if must_fail else 'must pass'}] {name}")
    for name, _, ok, _ in t["al_cases"]:
        print(f"  [allowlist {'valid' if ok else 'invalid'}] {name}")
    for name, _, ok in t["fp_cases"]:
        print(f"  [fingerprints {'valid' if ok else 'invalid'}] {name}")
    for name in t["run_cases"]:
        print(f"  [run-level] {name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=None, help="Repository root (default: two levels above this script)")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixtures and exit")
    ap.add_argument("--list-self-test-cases", action="store_true", help="Print the self-test case names")
    ap.add_argument("--print-fingerprints", action="store_true",
                    help="Print FINGERPRINTS lines for every file under a restricted domain (review before pasting)")
    args = ap.parse_args(argv)
    if args.list_self_test_cases:
        return list_self_test_cases()
    if args.self_test:
        return self_test()
    root = args.repo or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    if args.print_fingerprints:
        return print_fingerprints(root)
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
