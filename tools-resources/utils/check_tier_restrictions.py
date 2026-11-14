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
The gate stops restricted content from entering the public repository under the
publisher domains listed in RESTRICTED_DOMAINS: every tracked file beneath one of those
domain directories must match a reviewed path + SHA-256 fingerprint, whether it is text,
data or an image, and whether it was committed by mistake or by an agent acting on its
own. It does NOT cover restricted text copied to a path outside those domains (e.g.
under another publisher's directory), nor publishers missing from RESTRICTED_DOMAINS;
those still depend on review. The guarantee also assumes changes to this gate are
themselves reviewed (below). It does this mechanically. It cannot
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
4. Metadata truth, for every edition metadata file in the repository (any
   `*-metadata.json` other than a `-file-metadata.json` sidecar, under a SecID type
   root). Content files are counted against the nearest ancestor directory that has
   metadata; README.md and metadata files are not content.
   a. A directory may not hold content while its metadata says
      `license.publicly_redistributable: false` (dataset-public-laws-regulations-
      standards#154 made this blocking once the metadata had been corrected).
   b. `access_tier`, when present, must be the integer 1, 2, 3 or 4 and come with a
      `tier_evidence` object: `url` (http or https), `checked` (a real YYYY-MM-DD date,
      not in the future), `method` (one of TIER_METHODS) and a `note`. `tier_evidence`
      without `access_tier` fails.
   c. Tier 1 or 2 requires `publicly_redistributable: true`. Tier 3 or 4 requires
      `false`, and no content in the directory, unless a `tier3-4-exception` ALLOWLIST
      entry names that exact directory.
   d. Method `host-suffix` proves only Tier 1, and only when the evidence URL's host
      ends in one of GOV_HOST_SUFFIXES. Method `recorded` (a classification the program
      recorded but this check did not re-observe) may only say Tier 3 or 4: a record
      can keep something private, never make it public.
   e. An edition metadata file that is not a readable JSON object fails.
   Check 4 makes the metadata agree with itself and with the rule. It cannot tell
   whether a recorded tier is true: a `fetch` or `browser` claim of Tier 2 is only as
   good as its evidence. `tier_evidence` exists so that a reviewer can re-check it, and
   a PR that sets or raises a tier on a directory holding content needs that check.

What it reports (non-blocking)
------------------------------
Any FINGERPRINTS or ALLOWLIST entries that no longer match a file.

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
_URL_RE = re.compile(r"^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(:\d+)?(/\S*)?$")

# How a metadata file's `tier_evidence` was obtained (check 4b/4d).
TIER_METHODS: dict[str, str] = {
    "fetch": "a scripted HTTP GET of the evidence URL showed the content with no login",
    "browser": "the evidence URL was loaded in a real browser (JS-rendered or bot-filtered sites)",
    "host-suffix": "Tier 1 only: the evidence URL's host is a government domain in GOV_HOST_SUFFIXES; not fetched",
    "recorded": "Tier 3/4 only: the program's own recorded classification, not re-observed in this check",
}

# Host suffixes treated as government websites (Tier 1) for method "host-suffix". Each is
# a domain whose registry limits registration to government bodies (`gov` is the US
# .gov, `int` holds intergovernmental treaty organisations). Listed exactly, not as a
# pattern, because some open ccTLDs let anyone register `go.<cc>` or `gov.<cc>`. A host
# matches when it equals a suffix or ends in "." + suffix. Adding a suffix lets metadata
# claim Tier 1 without a fetch, so it needs the same review as any other gate change.
GOV_HOST_SUFFIXES: tuple[str, ...] = (
    "gov", "mil", "int",
    "admin.ch", "bund.de", "canada.ca", "europa.eu", "fgov.be", "gc.ca", "gub.uy", "gv.at", "govt.nz",
    "nic.in",
    "go.cr", "go.id", "go.jp", "go.ke", "go.kr", "go.th",
    "gob.ar", "gob.cl", "gob.do", "gob.es", "gob.mx", "gob.pe", "gob.sv",
    "gouv.fr", "gouv.sn",
    "gov.ae", "gov.au", "gov.bd", "gov.bh", "gov.br", "gov.cn", "gov.co", "gov.cz", "gov.eg", "gov.et",
    "gov.fj", "gov.gh", "gov.gr", "gov.ie", "gov.il", "gov.in", "gov.it", "gov.jm", "gov.jo", "gov.kw",
    "gov.lk", "gov.lv", "gov.ma", "gov.mn", "gov.my", "gov.ng", "gov.np", "gov.om", "gov.pg", "gov.ph",
    "gov.pk", "gov.pl", "gov.pt", "gov.py", "gov.qa", "gov.ro", "gov.rs", "gov.ru", "gov.rw", "gov.sa",
    "gov.sg", "gov.si", "gov.sk", "gov.to", "gov.tr", "gov.tt", "gov.tw", "gov.ua", "gov.uk", "gov.vn",
    "gov.vu", "gov.ws", "gov.za", "gov.zm",
)

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
    # Re-fingerprinted for #154 on 2026-11-14: the metadata stubs of isaca.org/cobit and
    # pcisecuritystandards.org pa-dss, pci-pin and secure-software-standard (now
    # publicly_redistributable false, access_tier 4 with tier_evidence; still metadata only).
    "control/aicpa.org/tsc/2017/README.md": "e44d16a0f927da1b6d7f648e82e18240872125b14939ab1e60acd05605422bfe",
    "control/aicpa.org/tsc/2017/tsc-2017-metadata.json": "b83a91e6b8224bb70fe44dfb06d43bef382b12a7b9922090c68b81274c4688fb",
    "control/cisecurity.org/cis-controls/v8/README.md": "3cdab7b5885a301e311b4f5814453cf741add82359f636c28c2705aa7d628ef6",
    "control/cisecurity.org/cis-controls/v8/cis-controls-v8-metadata.json": "8b9f6b908a7e9a95b968aa2c81073082b4f8c7bdab7dc0734a9539dae04b4b08",
    "control/hitrustalliance.net/csf/v11.3.0/README.md": "236840a03ff4ee04085ea1775c2804e962bbb13c84ab86279056d55981d16317",
    "control/hitrustalliance.net/csf/v11.3.0/csf-v11.3.0-metadata.json": "09266092d21295587346960d7588d923ab732949a726c076a6b320cb3c282b6c",
    "control/isaca.org/cobit/README.md": "da4647a09b5e6e8135cb38b6c730c3b36e8758736c91f5e52ad7b9834e487bee",
    "control/isaca.org/cobit/cobit-metadata.json": "d3d6730fa1e2c38e61c7d8f8367965061aabd48a29b37798549aa60b0106f442",
    "control/pcisecuritystandards.org/pa-dss/README.md": "4e814862014a2c433dbca0b7e2d90c4cc0401a148e0386a747a34f7f4adec6f2",
    "control/pcisecuritystandards.org/pa-dss/pa-dss-metadata.json": "e93877401cc1e5d2b4f5b9c285669a43e4702ce8e84b57e3528ca6550e1f82bd",
    "control/pcisecuritystandards.org/pci-dss/v3.2.1/README.md": "347e4fcdbd6a49aa2f2c9d95470b0125efa84f8a9c4ebf7d326714dd6a6a8798",
    "control/pcisecuritystandards.org/pci-dss/v3.2.1/pci-dss-v3.2.1-metadata.json": "fa960e9089e08ee852db89f6ab2061b1c631b56ac1a18280866481f16ae092f7",
    "control/pcisecuritystandards.org/pci-dss/v4.0.1/README.md": "d297f1c3cb018443e049283d7753bb943b715095426991e9d175357b45e7327b",
    "control/pcisecuritystandards.org/pci-dss/v4.0.1/pci-dss-v4.0.1-metadata.json": "6d7ebe1f9bde741f8d0dd980f988de7ace3cea4e81cfc7e46fb5d94c685034d8",
    "control/pcisecuritystandards.org/pci-dss/v4.0/README.md": "fb43e327956a79ccca61cc4eeda6b78651cbbe8c3a1430acc31b5c7d29dac4a9",
    "control/pcisecuritystandards.org/pci-dss/v4.0/pci-dss-v4.0-metadata.json": "338d3956b4b5eaa6b419473708984b7cf5ff56018a4af93cdf9d23240afdc4f5",
    "control/pcisecuritystandards.org/pci-pin/README.md": "e726f77ef61727b21755ddea9203d29ef26b0a4c981e3fce889390fee5b22256",
    "control/pcisecuritystandards.org/pci-pin/pci-pin-metadata.json": "ae198b56bed02d8953ae1551aef4825e9539e1bfae49bd1b56f22ae83672a079",
    "control/pcisecuritystandards.org/secure-software-standard/README.md": "8105b428a0aa7f67e20d980c12e866c070b725c48d43271e11f0cc160fc4e024",
    "control/pcisecuritystandards.org/secure-software-standard/secure-software-standard-metadata.json": "51fbf50b2c2f73d9e3406765006cbf7c25a997936e1813ff2b1e6edab32808e9",
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


def is_edition_metadata(rel: str) -> bool:
    p = PurePosixPath(rel)
    return (len(p.parts) >= 3 and p.parts[0] in SECID_TYPES and p.name.endswith("-metadata.json")
            and not p.name.endswith("-file-metadata.json"))


def content_by_metadata(files: list[str]) -> dict[str, int]:
    """Map every edition metadata file to the number of content files it governs: files
    in its directory or below it, up to the next directory that has its own metadata.
    README.md and metadata files are not content. Where one directory holds several
    metadata files, the first by name governs (as before)."""
    names_by_dir: dict[str, list[str]] = defaultdict(list)
    for f in files:
        p = PurePosixPath(f)
        names_by_dir[p.parent.as_posix()].append(p.name)
    counts: dict[str, int] = {f: 0 for f in files if is_edition_metadata(f)}
    for rel in files:
        p = PurePosixPath(rel)
        if len(p.parts) < 3 or p.parts[0] not in SECID_TYPES or is_report_stub(p.name):
            continue
        cur = p.parent
        while len(cur.parts) >= 2:
            cands = sorted(n for n in names_by_dir.get(cur.as_posix(), [])
                           if n.endswith("-metadata.json") and not n.endswith("-file-metadata.json"))
            if cands:
                meta = f"{cur.as_posix()}/{cands[0]}"
                counts[meta] = counts.get(meta, 0) + 1
                break
            cur = cur.parent
    return counts


def _load_metadata(root: str, rel: str):
    try:
        with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def report_unflagged(root: str, files: list[str]) -> list[tuple[str, int]]:
    """Directories (of the governing metadata) with content files whose metadata says
    license.publicly_redistributable is false. Check 4a turns each into a failure."""
    out = []
    for meta, n in content_by_metadata(files).items():
        if not n:
            continue
        data = _load_metadata(root, meta)
        lic = data.get("license") if data else None
        if isinstance(lic, dict) and lic.get("publicly_redistributable") is False:
            out.append((PurePosixPath(meta).parent.as_posix(), n))
    return sorted(out)


def gov_host_suffix(url) -> str | None:
    """The GOV_HOST_SUFFIXES entry the URL's host ends in, or None."""
    if not isinstance(url, str) or not _URL_RE.match(url):
        return None
    host = url.split("://", 1)[1].split("/", 1)[0].split(":", 1)[0].lower().rstrip(".")
    for suffix in GOV_HOST_SUFFIXES:
        if host == suffix or host.endswith("." + suffix):
            return suffix
    return None


def tier_field_problems(data: dict, today: _dt.date) -> list[str]:
    """Check 4b/4d: the shape of access_tier and tier_evidence (empty list = valid)."""
    if "access_tier" not in data:
        return ["tier_evidence is present without access_tier"] if "tier_evidence" in data else []
    tier = data["access_tier"]
    if type(tier) is not int or tier not in (1, 2, 3, 4):  # bool and float (1.0) are rejected
        return [f"access_tier must be the integer 1, 2, 3 or 4, got {tier!r}"]
    ev = data.get("tier_evidence")
    if not isinstance(ev, dict):
        return ["access_tier needs a tier_evidence object (url, checked, method, note)"]
    probs = []
    if not isinstance(ev.get("url"), str) or not _URL_RE.match(ev["url"]):
        probs.append(f"tier_evidence.url must be an http(s) URL, got {ev.get('url')!r}")
    checked = ev.get("checked")
    d = None
    if isinstance(checked, str) and _DATE_RE.match(checked):
        try:
            d = _dt.date.fromisoformat(checked)
        except ValueError:
            d = None
    if d is None:
        probs.append(f"tier_evidence.checked must be a real YYYY-MM-DD date, got {checked!r}")
    elif d > today:
        probs.append(f"tier_evidence.checked {checked} is in the future")
    method = ev.get("method")
    if method not in TIER_METHODS:
        probs.append(f"tier_evidence.method must be one of {sorted(TIER_METHODS)}, got {method!r}")
    note = ev.get("note")
    if not isinstance(note, str) or len(note.strip()) < 15:
        probs.append("tier_evidence.note must say what was observed (at least 15 characters)")
    if method == "host-suffix":
        if tier != 1:
            probs.append(f"method host-suffix proves only Tier 1, not Tier {tier}")
        elif gov_host_suffix(ev.get("url")) is None:
            probs.append(f"method host-suffix needs a URL whose host is in GOV_HOST_SUFFIXES, got {ev.get('url')!r}")
    if method == "recorded" and tier in (1, 2):
        probs.append("method recorded may only say Tier 3 or 4: a record can keep a source private, never make it public")
    return probs


def check_metadata_truth(root: str, files: list[str], allowlist: list[dict],
                         today: _dt.date | None = None) -> dict[str, list[str]]:
    """Blocking check 4. Returns {metadata path: [problems]}."""
    today = today or _dt.date.today()
    exceptions = {e["path"] for e in allowlist if e.get("kind") == "tier3-4-exception"}
    problems: dict[str, list[str]] = {}
    for meta, n_content in sorted(content_by_metadata(files).items()):
        data = _load_metadata(root, meta)
        if data is None:
            problems[meta] = ["not a readable JSON object, so nothing can confirm that the content it governs may "
                              "be public"]
            continue
        lic = data.get("license") if isinstance(data.get("license"), dict) else {}
        public = lic.get("publicly_redistributable")
        probs = tier_field_problems(data, today)
        if n_content and public is False:
            probs.append(f"{n_content} content files sit under this metadata while license.publicly_redistributable "
                         "is false. Find the source's tier: Tier 1/2 -> set it true and record access_tier and "
                         "tier_evidence; Tier 3/4 -> the content belongs in dataset-private-laws-regulations-standards "
                         "unless Kurt grants an exception (ask first; do not move it on your own)")
        tier = data.get("access_tier")
        if type(tier) is int and tier in (1, 2, 3, 4):
            excepted = PurePosixPath(meta).parent.as_posix() in exceptions
            if tier in (1, 2) and public is not True:
                probs.append(f"access_tier {tier} means the rule allows public hosting, so "
                             f"license.publicly_redistributable must be true, got {public!r}")
            if tier in (3, 4) and not excepted:
                if public is not False:
                    probs.append(f"access_tier {tier} needs license.publicly_redistributable false (no "
                                 f"tier3-4-exception ALLOWLIST entry names this directory), got {public!r}")
                if n_content:
                    probs.append(f"access_tier {tier} source with {n_content} content files and no "
                                 "tier3-4-exception ALLOWLIST entry for this exact directory")
        if probs:
            problems[meta] = probs
    return problems


# ----------------------------------------------------------------------------- output
def run(root: str, use_git: bool | None = None, out=sys.stdout, allowlist: list[dict] | None = None,
        fingerprints: dict | None = None, today: _dt.date | None = None) -> int:
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

    meta_problems = check_metadata_truth(root, files, allowlist, today=today)
    n_meta = sum(1 for f in files if is_edition_metadata(f))
    tiered = 0
    for f in files:
        if is_edition_metadata(f):
            data = _load_metadata(root, f)
            tiered += bool(data and "access_tier" in data)
    print("", file=out)
    print(f"Metadata truth: {n_meta} edition metadata files, {tiered} with access_tier.", file=out)
    if meta_problems:
        status = 1
        print(f"FAIL: {len(meta_problems)} metadata files contradict the 4-tier rule or carry malformed tier "
              "fields (see METADATA-SCHEMA.md, access_tier):", file=out)
        for meta, probs in meta_problems.items():
            print(f"  {meta}", file=out)
            for pr in probs:
                print(f"      {pr}", file=out)
                if in_actions:
                    print(f"::error file={meta},title=Metadata truth::{pr}", file=out)
    else:
        print("  PASS: no directory holds content while its metadata says not redistributable, and every "
              "access_tier agrees with publicly_redistributable and carries valid evidence.", file=out)

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
        ("control/iso.org/27701/2019/27701-2019-metadata.json", meta("secid:control/iso.org/27701@2019", True), False,
         "own metadata (an excepted directory is publicly hosted, so its metadata says true)"),
        ("control/iso.org/27701/2019/27701-2019.md", "text", False, "allowlisted file in the exact directory"),
        ("control/iso.org/27701/2019/27701-2019.csv", "a,b", True, "P2-3 file not named in the allowlist entry"),
        ("control/iso.org/27701/2019/scripts/parse.py", "print()", True, "P2-3 subdirectory does not inherit the exception"),
        ("control/iso.org/27701/2019/scripts/2019-scripts-metadata.json", meta("secid:control/iso.org/27701@2019"), True, "P2-3 nested metadata does not create an edition"),
        ("control/iso.org/27701/2022/27701-2022-metadata.json", meta("secid:control/iso.org/27701@2022"), False, "own metadata"),
        ("control/iso.org/27701/2022/27701-2019.md", "text", True, "P2-3 sibling edition does not inherit the exception"),
        ("control/iso.org/27701/27701.md", "text", True, "P2-3 parent directory does not inherit the exception"),
        ("control/iso.org/27701/2019/27701-2019-extra.md", "text", True, "R2-P1 allowlisted directory, file not in the entry and not fingerprinted"),
        # --- round 2 P2: an exact allowance can authorize a README over the stub cap
        ("control/iso.org/27799/2016/27799-2016-metadata.json", meta("secid:control/iso.org/27799@2016", True), False,
         "own metadata (excepted, so true)"),
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
        # --- content-while-not-redistributable fixtures (check 4a; the run-level test shows it blocks)
        ("control/example.org/doc/1/doc-1-metadata.json", meta("secid:control/example.org/doc@1", False), False, "4a: content + false (metadata)"),
        ("control/example.org/doc/1/doc-1.md", "text", False, "4a: content + false (content; blocks in run())"),
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
                          "control/cisecurity.org/cis-controls/v8", "control/iso.org/27701/2022",
                          "control/iso.org/27017/2015", "control/iso.org/27701/2019/scripts",
                          "control/iso.org/27036/1"}

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
        "4a run() still exits 1 while one directory holds content under metadata saying false",
        "P1-2 run() fails when the review's bogus exception is added to ALLOWLIST",
        "R2-P1 run() fails when FINGERPRINTS holds a malformed digest",
        "P2-4 symlinked file and symlinked directory found by the filesystem walk; run() fails",
        "P2-4 the same links staged in git are found as mode 120000; run() fails",
        "4 run() exits 1 on the metadata-truth fixtures, then 0 once the must-fail ones are removed",
    ]

    # --- check 4 (metadata truth). (name, directory, metadata dict or raw text,
    # extra file paths relative to the directory (content), must_fail). Every case gets
    # its own edition directory; must_fail means check_metadata_truth flags its metadata.
    def tm(public, tier=None, ev=None, **extra):
        d = {"secid": "secid:reference/x/doc", "license": {"spdx": "X", "publicly_redistributable": public}}
        if public is None:
            del d["license"]["publicly_redistributable"]
        if tier is not None:
            d["access_tier"] = tier
        if ev is not None:
            d["tier_evidence"] = ev
        d.update(extra)
        return d

    def ev(url="https://www.example.com/doc.pdf", method="fetch", checked="2026-11-13",
           note="Direct PDF download, no login."):
        return {"url": url, "checked": checked, "method": method, "note": note}

    gov = "https://www.ipa.go.jp/security/doc.pdf"
    mcase = [
        ("legacy: content, true, no tier", tm(True), ["doc.md"], False),
        ("4a content while false", tm(False), ["doc.md"], True),
        ("4a content in a subdirectory, ancestor metadata says false", tm(False), ["sub/data.csv"], True),
        ("4a a -file-metadata.json sidecar saying false does not govern", tm(True), ["doc.md", "doc.pdf-file-metadata.json"], False),
        ("stub (README only) while false", tm(False), ["README.md"], False),
        ("Tier 1 host-suffix (go.jp), true, content", tm(True, 1, ev(gov, "host-suffix")), ["doc.md"], False),
        ("Tier 1 host-suffix (.gov), true", tm(True, 1, ev("https://csrc.nist.gov/pubs/sp/800/53", "host-suffix")), [], False),
        ("Tier 1 host-suffix (.int), true", tm(True, 1, ev("https://www.itu.int/x.pdf", "host-suffix")), [], False),
        ("4d host-suffix on a non-government host", tm(True, 1, ev("https://www.example.com/x", "host-suffix")), [], True),
        ("4d host-suffix on a look-alike (fakegov.uk)", tm(True, 1, ev("https://fakegov.uk/x", "host-suffix")), [], True),
        ("4d host-suffix on an open ccTLD (go.co)", tm(True, 1, ev("https://go.co/x", "host-suffix")), [], True),
        ("4d host-suffix claiming Tier 2", tm(True, 2, ev(gov, "host-suffix")), [], True),
        ("Tier 2 by fetch, true, content", tm(True, 2, ev()), ["doc.md"], False),
        ("Tier 2 by browser, true", tm(True, 2, ev(method="browser")), [], False),
        ("4c Tier 1 while false", tm(False, 1, ev(gov, "host-suffix")), [], True),
        ("4c Tier 2 with publicly_redistributable missing", tm(None, 2, ev()), [], True),
        ("4c Tier 3 while true, no exception", tm(True, 3, ev()), [], True),
        ("Tier 4 stub, false, recorded", tm(False, 4, ev(method="recorded", note="Program classification, not re-observed.")),
         ["README.md"], False),
        ("4c Tier 4 with content (and false)", tm(False, 4, ev()), ["doc.md"], True),
        ("4c Tier 3 with content and true, exact tier3-4-exception", tm(True, 3, ev()), ["doc.md"], False),
        ("4c Tier 3 with content, exception names a sibling directory", tm(True, 3, ev()), ["doc.md"], True),
        ("4d recorded claiming Tier 2", tm(True, 2, ev(method="recorded")), [], True),
        ("4b access_tier as a string", tm(True, "2", ev()), [], True),
        ("4b access_tier true (bool)", tm(True, True, ev()), [], True),
        ("4b access_tier 1.0 (float)", tm(True, 1.0, ev(gov, "host-suffix")), [], True),
        ("4b access_tier 5", tm(True, 5, ev()), [], True),
        ("4b access_tier without tier_evidence", tm(True, 2), [], True),
        ("4b tier_evidence without access_tier", tm(True, None, ev()), [], True),
        ("4b tier_evidence not an object", tm(True, 2, "fetched it"), [], True),
        ("4b evidence date in the future", tm(True, 2, ev(checked="2026-12-01")), [], True),
        ("4b evidence date that does not exist", tm(True, 2, ev(checked="2026-02-30")), [], True),
        ("4b evidence URL not http(s)", tm(True, 2, ev(url="ftp://example.com/x")), [], True),
        ("4b unknown evidence method", tm(True, 2, ev(method="guess")), [], True),
        ("4b empty evidence note", tm(True, 2, ev(note=" ")), [], True),
        ("4e metadata that is not valid JSON", "{not json", ["doc.md"], True),
        ("4e metadata that is a JSON list", "[1, 2]", [], True),
    ]
    meta_cases = []
    for i, (name, data, extra, must_fail) in enumerate(mcase):
        d = f"reference/case{i:02d}.example.org/doc"
        if isinstance(data, dict):
            data = dict(data, secid=f"secid:reference/case{i:02d}.example.org/doc")
        meta_cases.append((name, d, data, extra, must_fail))
    exc_dir = next(c[1] for c in meta_cases if "exact tier3-4-exception" in c[0])
    sib_dir = next(c[1] for c in meta_cases if "names a sibling directory" in c[0])
    meta_allowlist = [dict(test_exception, path=exc_dir, secid=f"secid:{exc_dir}"),
                      dict(test_exception, path=sib_dir + "-sibling", secid=f"secid:{sib_dir}-sibling")]
    return dict(cases=cases, fp_override=fp_override, expected_unflagged=expected_unflagged, al_cases=al_cases,
                fp_cases=fp_cases, run_cases=run_cases, allowlist=allowlist, test_exception=test_exception,
                bogus=bogus, meta_cases=meta_cases, meta_allowlist=meta_allowlist)


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
            # check 4a is blocking: the one content-while-false directory left still fails run()
            if run(tmp, use_git=False, out=sink, allowlist=allowlist, fingerprints=fingerprints) != 1:
                failures.append("4a run() did not exit 1 while a directory held content under metadata saying false")
            os.remove(os.path.join(tmp, "control", "example.org", "doc", "1", "doc-1.md"))
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

    # check 4: metadata truth, in its own tree
    with tempfile.TemporaryDirectory(prefix="tier-gate-selftest-meta-") as tmp:
        for _, d, data, extra, _ in t["meta_cases"]:
            os.makedirs(os.path.join(tmp, *d.split("/")), exist_ok=True)
            with open(os.path.join(tmp, *d.split("/"), "doc-metadata.json"), "w", encoding="utf-8") as fh:
                fh.write(data if isinstance(data, str) else json.dumps(data))
            for rel in extra:
                path = os.path.join(tmp, *d.split("/"), *rel.split("/"))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("{}" if rel.endswith(".json") else "text")
        files, _ = list_entries(tmp, use_git=False)
        flagged = check_metadata_truth(tmp, files, t["meta_allowlist"], today=FROZEN_TODAY)
        for name, d, _, _, must_fail in t["meta_cases"]:
            hit = f"{d}/doc-metadata.json" in flagged
            if must_fail and not hit:
                failures.append(f"metadata truth: not caught: {name}")
            if not must_fail and hit:
                failures.append(f"metadata truth: false positive: {name}: {flagged[f'{d}/doc-metadata.json']}")
        sink = open(os.devnull, "w", encoding="utf-8")
        try:
            if run(tmp, use_git=False, out=sink, allowlist=t["meta_allowlist"], fingerprints={},
                   today=FROZEN_TODAY) != 1:
                failures.append("4 run() did not exit 1 on the metadata-truth fixtures")
            for _, d, _, _, must_fail in t["meta_cases"]:
                if must_fail:
                    shutil.rmtree(os.path.join(tmp, *d.split("/")))
            if run(tmp, use_git=False, out=sink, allowlist=t["meta_allowlist"], fingerprints={},
                   today=FROZEN_TODAY) != 0:
                failures.append("4 run() did not exit 0 once the must-fail metadata-truth fixtures were removed")
        finally:
            sink.close()

    n = len(cases) + len(t["al_cases"]) + len(t["fp_cases"]) + len(t["run_cases"]) + len(t["meta_cases"])
    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Self-test passed ({n} cases: {len(cases)} fixture files, {sum(1 for c in cases if c[2])} of which must "
          f"fail; {len(t['al_cases'])} allowlist validations; {len(t['fp_cases'])} fingerprint validations; "
          f"{len(t['run_cases'])} run-level checks; {len(t['meta_cases'])} metadata-truth fixtures, "
          f"{sum(1 for c in t['meta_cases'] if c[4])} of which must fail).")
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
    for name, _, _, _, must_fail in t["meta_cases"]:
        print(f"  [metadata truth {'must fail' if must_fail else 'must pass'}] {name}")
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
