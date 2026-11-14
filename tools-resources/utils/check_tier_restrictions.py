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
own. Under ANY publisher domain, check 4 pins every file governed by a record (or marked
by a sidecar) that is not plainly public, so restricted text cannot be stuffed into a
restrictive stub anywhere either. What it does NOT cover: restricted text placed under a
record that falsely says it is public (outside RESTRICTED_DOMAINS), and the listed
infrastructure paths outside the type roots (check 5); those still depend on review. The guarantee also assumes changes to this gate are
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
4. Metadata truth, under ANY publisher domain (dataset-public-laws-regulations-standards#154).
   Governance: a directory's edition metadata is the file named for the directory,
   `<dir>-metadata.json` or `<parent>-<dir>-metadata.json` (also in lower-case slug form;
   see canonical_metadata_names). That rule is applied BEFORE the sidecar rule, so an
   edition named `x-file` is an edition. Every other tracked file under a type root is
   governed by the nearest directory at or above it that has edition metadata.
   Everything a record governs is content except one README.md directly beside it.
   a. A record is restrictive when `license.publicly_redistributable` is not true or its
      `access_tier` is 3 or 4. It may govern only a stub (its metadata and one README
      beside it) plus the files a matching exception lists (c); size and string caps
      (METADATA_MAX_BYTES, METADATA_MAX_STRING, README_MAX_BYTES) apply as a second layer.
   b. `access_tier`, when present, must be the integer 1, 2, 3 or 4 and come with a
      `tier_evidence` object: `url` (http or https), `checked` (a real YYYY-MM-DD date,
      not in the future), `method` (one of TIER_METHODS) and a `note`. `tier_evidence`
      without `access_tier` fails.
   c. Tier 1 or 2 requires `publicly_redistributable: true`. Tier 3 or 4 requires
      `false`, unless a `tier3-4-exception` ALLOWLIST entry names that exact directory
      and the record's own SecID; then the record may say `true` and the directory may
      hold exactly the entry's listed files, directly in it, and nothing else.
   d. Method `host-suffix` proves only Tier 1, only when the evidence URL's host ends in
      one of GOV_HOST_SUFFIXES, only for an acquired document (non-sidecar content in the
      directory), and only when neither the record's text, its tier_evidence note (URL
      and method excluded) nor its README matches ACCESS_RESTRICTION_RE (URLs and negated
      phrases such as "no login" removed first). Method `recorded` may only say Tier 3 or
      4: a record can keep something private, never make it public.
   e. An edition metadata file that is not a readable JSON object fails.
   f. One directory may hold only one edition metadata file, and a record that is not
      restrictive may not sit below a restrictive or ambiguous one.
   g. `license` must be an object and `license.publicly_redistributable` a boolean,
      present: a missing value or the string "false" fails.
   h. Every tracked file under a type root is governed or is listed exactly in
      TYPE_ROOT_INFRASTRUCTURE (CSA's own tooling and notes); a `*-metadata.json` that is
      neither canonical edition metadata nor a sidecar fails.
   i. Sidecars (`<file>-file-metadata.json`) only ever restrict. Each must be a JSON
      object naming a tracked file in its directory (or a gitignored original, see
      UNTRACKED_ORIGINAL_SUFFIXES), with a matching `filename` if it gives one. One whose
      `license` or `license_override` says publicly_redistributable false, or whose
      access_tier is 3 or 4, marks its file not public: that file may not be tracked here,
      and the sidecar is pinned (j). A sidecar saying true never loosens its record.
   j. Pinned only: every file governed by a restrictive record, the record itself, and
      every file a restrictive sidecar marks, must match a reviewed path + SHA-256 in
      FINGERPRINTS, whatever the publisher domain. This, not the caps, is what stops
      restricted text being stuffed into stubs or chunked across new edition directories.
   Check 4 makes the metadata agree with itself and with the rule. It cannot tell
   whether a recorded tier, or a record that says it is public, is true: a `fetch` or
   `browser` claim of Tier 2 is only as good as its evidence, and `tier_evidence` exists
   so a reviewer can re-check it.
5. Outside the SecID type roots, tracked files may only be root files matching
   ROOT_FILE_PATTERNS or sit under INFRASTRUCTURE_PREFIXES, and no `*-metadata.json`
   may sit there at all.

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
    "host-suffix": ("Tier 1 only, for an acquired document with no access restriction noted: the evidence URL's "
                    "host is a government domain in GOV_HOST_SUFFIXES; not fetched"),
    "recorded": "Tier 3/4 only: the program's own recorded classification, not re-observed in this check",
}

# Words that suggest the document itself is gated (members-only, purchase, subscription,
# registration, awaiting a licensed copy, ...). Method host-suffix may not claim Tier 1
# for metadata whose text (URLs removed) or README contains any of them (check 4d): a
# publisher's domain says nothing about how its document is reached. Deliberately broad;
# a false match only means the tier has to be established by fetching the document.
ACCESS_RESTRICTION_RE = re.compile(
    r"\bmembers?[- ]only\b|\bmember access\b|\bmembership (?:required|only|fee)|\brequires? (?:a )?(?:paid )?membership\b|"
    r"\bpurchas(?:e|ed|es|ing)\b|\bpaid\b|\bpaywall|\bsubscri(?:be|bed|ber|bers|ption|ptions)\b|"
    r"\bregistration\b|\bregister(?:ed)? (?:to|for|before|with)\b|\bregistered users?\b|"
    r"\blog[- ]?in\b|\bsign[- ]?(?:in|up)\b|\b(?:free|user) account\b|\bcreate an? (?:free )?account\b|"
    r"\bawaiting\b|\blicen[cs]ed copy\b|\blicen[cs]e (?:purchase|fee)s?\b|\bclick[- ]?through\b|"
    r"\bnot publicly (?:available|accessible|released)\b|\brestricted (?:access|distribution)\b|"
    r"\b(?:available|provided|copies|copy) (?:only )?(?:on|upon) request\b",
    re.I)
_URL_IN_TEXT_RE = re.compile(r"https?://\S+")
# "no login", "without registration" and the like say the opposite; they are removed first.
_NEGATED_ACCESS_RE = re.compile(
    r"\b(?:no|without|not requiring|does not require|doesn't require|requires no)[\s-]+(?:an?\s+)?(?:free\s+)?"
    r"(?:log[- ]?in|sign[- ]?in|registration|account|subscription|purchase|membership)\b", re.I)

# Host suffixes treated as government websites (Tier 1) for method "host-suffix". A host
# matches when it equals a suffix or ends in "." + suffix. Listed exactly, never as a
# pattern: some open ccTLDs let anyone register `go.<cc>`, and `.int` itself holds
# non-governmental organisations (www.ymca.int). Only suffixes that a tiered entry uses
# are listed. Adding one lets metadata claim Tier 1 without a fetch, so it needs the same
# review as any other gate change. The basis for each group:
#   - registry-restricted government namespaces: `gov` (US .gov, open only to government
#     organisations), and the `go.`, `gob.`, `gouv.`, `gov.` and `govt.` second-level
#     domains below, which their ccTLD registries reserve for government bodies;
#   - domains a government itself holds, so every host under them is that government's:
#     `admin.ch` (Swiss federal administration), `bund.de` (German federal government),
#     `canada.ca` and `gc.ca` (Government of Canada), `europa.eu` (EU institutions),
#     `nic.in` (India's National Informatics Centre);
#   - intergovernmental organisations, each checked on its own site on 2026-11-14:
#     `au.int` (https://au.int/en/overview: "a continental body consisting of the 55 member
#     states"), `coe.int` (https://www.coe.int/en/web/about-us/who-we-are: the Council of
#     Europe, "the continent's leading human rights organisation", and its member states),
#     `itu.int` (https://www.itu.int/en/about/Pages/default.aspx: "the United Nations
#     specialized agency for information and communication technologies").
GOV_HOST_SUFFIXES: tuple[str, ...] = (
    "gov",
    "admin.ch", "bund.de", "canada.ca", "europa.eu", "gc.ca", "nic.in",
    "au.int", "coe.int", "itu.int",
    "go.cr", "go.jp",
    "gob.ar", "gob.cl", "gob.do", "gob.es", "gob.mx",
    "gouv.fr",
    "gov.ae", "gov.au", "gov.bh", "gov.br", "gov.cn", "gov.co", "gov.cz", "gov.ie", "gov.il", "gov.in",
    "gov.it", "gov.jm", "gov.my", "gov.ph", "gov.pk", "gov.pl", "gov.rs", "gov.sa", "gov.sg", "gov.si",
    "gov.sk", "gov.tt", "gov.tw", "gov.uk", "gov.za",
    "govt.nz",
)

# Check 5: where tracked files outside the SecID type roots may live. Anything else
# outside a type root fails, and no `*-metadata.json` may sit outside a type root (it
# would govern nothing). Changing these needs the same review as any other gate change.
INFRASTRUCTURE_PREFIXES: tuple[str, ...] = (".github/", "docs/", "plans/", "resumption-summaries/", "tools-resources/")
ROOT_FILE_PATTERNS: tuple[str, ...] = ("*.md", "LICENSE", ".gitignore", ".gitattributes")

# Gitignored source originals (.gitignore) that a `<file>-file-metadata.json` sidecar may
# describe although they are not tracked.
UNTRACKED_ORIGINAL_SUFFIXES: tuple[str, ...] = (".pdf", ".xlsx", ".docx", ".zip", ".gz", ".xz")

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

# Check 4h: files inside a SecID type root that no edition metadata governs, and that are
# CSA's own tooling, analysis or orientation notes rather than a dataset's content (the
# AICM and CCM figure checks and crosswalk builders, the CWE AI-analysis kit, namespace-
# level extractors and READMEs). Exact paths, not prefixes: a new file here is a gate
# change. Any other ungoverned file under a type root fails. Reviewed for #154 on
# 2026-11-14 (61 files).
TYPE_ROOT_INFRASTRUCTURE: frozenset[str] = frozenset({
    'control/cloudsecurityalliance.org/aicm/README.md',
    'control/cloudsecurityalliance.org/aicm/VERSIONING.md',
    'control/cloudsecurityalliance.org/aicm/crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv',
    'control/cloudsecurityalliance.org/aicm/crosswalks/aicm-caiq-1.0.2-to-1.1.0-crosswalk.csv',
    'control/cloudsecurityalliance.org/aicm/crosswalks/build_caiq_changelog.py',
    'control/cloudsecurityalliance.org/aicm/crosswalks/build_changelog.py',
    'control/cloudsecurityalliance.org/aicm/crosswalks/build_crosswalk.py',
    'control/cloudsecurityalliance.org/aicm/crosswalks/check_figures.py',
    'control/cloudsecurityalliance.org/ccm/README.md',
    'control/cloudsecurityalliance.org/ccm/check_figures.py',
    'reference/amazon.com/security-guidance/AWS/README.md',
    'reference/amazon.com/security-guidance/AWS/convert-html-to-markdown-in-place.py',
    'reference/amazon.com/security-guidance/AWS/get-all-sitemaps-secur-files.sh',
    'reference/anthropic.com/model-cards/README.md',
    'reference/github.com/advisory-database/README.md',
    'reference/google.com/model-cards/README.md',
    'reference/google.com/security-guidance/GCP/README.md',
    'reference/google.com/security-guidance/GCP/convert-all-google-files-to-markdown-in-place.py',
    'reference/google.com/security-guidance/GCP/create-file-blocks-for-chatbot.sh',
    'reference/google.com/security-guidance/GCP/get-all-sitemaps-secur-files.sh',
    'reference/microsoft.com/security-guidance/Azure/README.md',
    'reference/openai.com/security-guidance/Economic-Blueprint/README.md',
    'reference/openai.com/system-cards/README.md',
    'regulation/europa.eu/extract_eu_regulation.py',
    'regulation/gov.uk/extract_uk_legislation.py',
    'regulation/govinfo.gov/extract_us_plaw.py',
    'regulation/us-state-regulations-overview.md',
    'weakness/mitre.org/cwe/README.md',
    'weakness/mitre.org/cwe/analysis/AI-ATTACK-SURFACE-MODEL.md',
    'weakness/mitre.org/cwe/analysis/CVE-AI-VULNERABILITY-HUNTING.md',
    'weakness/mitre.org/cwe/analysis/CWE-AI-METHODOLOGY.md',
    'weakness/mitre.org/cwe/analysis/CWE-AI-RELEVANCE-REPORT.md',
    'weakness/mitre.org/cwe/analysis/CWE-PRIMER.md',
    'weakness/mitre.org/cwe/analysis/USAGE.md',
    'weakness/mitre.org/cwe/scripts-extra/.gitignore',
    'weakness/mitre.org/cwe/scripts-extra/README.md',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/__init__.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/classifiers.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/cli.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/config.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/exporters.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/extractors.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/loaders.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/models.py',
    'weakness/mitre.org/cwe/scripts-extra/cwe_ai_analysis/utils.py',
    'weakness/mitre.org/cwe/scripts-extra/output/CWE-AI-Classifications-Report.md',
    'weakness/mitre.org/cwe/scripts-extra/output/CWE-AI-Classifications.csv',
    'weakness/mitre.org/cwe/scripts-extra/output/CWE-AI-Classifications.json',
    'weakness/mitre.org/cwe/scripts-extra/output/CWE-Basic-Data.csv',
    'weakness/mitre.org/cwe/scripts-extra/pyproject.toml',
    'weakness/mitre.org/cwe/scripts-extra/requirements-dev.txt',
    'weakness/mitre.org/cwe/scripts-extra/requirements.txt',
    'weakness/mitre.org/cwe/scripts-extra/tests/__init__.py',
    'weakness/mitre.org/cwe/scripts-extra/tests/conftest.py',
    'weakness/mitre.org/cwe/scripts-extra/tests/test_classifiers.py',
    'weakness/mitre.org/cwe/scripts-extra/tests/test_extractors.py',
    'weakness/mitre.org/cwe/scripts-extra/tests/test_loaders.py',
    'weakness/mitre.org/cwe/scripts-extra/tests/test_models.py',
    'weakness/mitre.org/cwe/scripts/download-cwe-documents.sh',
    'weakness/mitre.org/cwe/scripts/download-cwe-items.sh',
    'weakness/mitre.org/cwe/scripts/html_to_markdown.py',
})

# Reviewed SHA-256 of every file allowed under a restricted publisher domain (stubs:
# own metadata, README.md; and files an ALLOWLIST entry covers), and, under ANY publisher
# domain, of every file governed by a record that is not plainly public or marked by a
# restrictive sidecar (check 4j). Path -> hex digest.
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
    # Check 4j, reviewed for #154 on 2026-11-14: 332 stubs (294 edition metadata, 38 README) outside the
    # restricted domains whose record is not plainly public. Each was confirmed a content-free stub before
    # pinning: metadata at most 3,882 bytes with no string over 690 characters (licence and access notes),
    # READMEs at most 1,468 bytes, no other governed files.
    "control/agid.gov.it/spid/README.md": "9286d871302fef6c418ccc617559755aca0fc12b32737cc0b2fc0f06220bf01c",
    "control/agid.gov.it/spid/spid-metadata.json": "bc8a7c961ba6cdd1624945ab8fc26659a998db781cde649b3839e160822dddcb",
    "control/axelos.com/itil/README.md": "663e2287c1b655205995bef957fe19d777e30ad6daead86be99cf30eb513406f",
    "control/axelos.com/itil/itil-metadata.json": "cac0269d6ae0ec3d41fb84c6f08cca852047c3219e3e613a78b7ad7994ea1f7e",
    "control/banxico.org.mx/codi/README.md": "0d00bea9dc86a9e2fb2ccce6a4a9d017aec2ef9c93631ef5464cd5cc94885f24",
    "control/banxico.org.mx/codi/codi-metadata.json": "f69d67345ac6dbe148d4c2b9b7338c536ff83c235f8834f6e81ebf259fa90944",
    "control/bcb.gov.br/pix/README.md": "df471d282a42a6cebe6dba92877faa4017595ac0192a1dac31924c7eb2da640e",
    "control/bcb.gov.br/pix/pix-metadata.json": "b957582df6b40dce3025298c21d21e9e7a58d8b26387f3039d007f780dab3151",
    "control/berlin-group.org/nextgenpsd2/README.md": "c35791f04ed745e495195b532b98b27f4099d3898dd6183cd2a982776084d702",
    "control/berlin-group.org/nextgenpsd2/nextgenpsd2-metadata.json": "3cf5499eb49ff6f699ac346989ac8b97b5cfb5d801af900e1201879c107908e7",
    "control/bot.or.th/promptpay/README.md": "deb2ae24047d14ff2a4b84d1a3b97d8616c495af0017208115c081a5b4d12194",
    "control/bot.or.th/promptpay/promptpay-metadata.json": "a310a2688f7ab54f3150d60ec503541cba1e39eff380642dd731d415a0fc5309",
    "control/bsp.gov.ph/pesonet/README.md": "9122cf95ec526ba8ff129de7704704e2aa2e99bd320ff2416e85b497da806ab5",
    "control/bsp.gov.ph/pesonet/pesonet-metadata.json": "7a60d8dfd04d073c70e8dc645b6eb218033a599ac2e974d18b573cc1500f886c",
    "control/digilocker.gov.in/integration-spec/README.md": "9cc591d51f70a171367271b70a474916359653394660eda8a84f5d506cccbb00",
    "control/digilocker.gov.in/integration-spec/integration-spec-metadata.json": "8ed80603635ec81af0e66da3223032356805b38988e4fd72c0e7fc6d64d4ae7c",
    "control/digital.go.jp/my-number/README.md": "f98ca05416ab70d45de6207cda55a193cf8494cde0be803c33faff7c6ad3c7de",
    "control/digital.go.jp/my-number/my-number-metadata.json": "96056cbb69dcf20690de8da7eaf126912bba375b1836cd934b4064f162ac8010",
    "control/etsi.org/en-303-645/README.md": "d98932b7ffa38cebf890216b0ed9f879b7beb24c7879367f06ede2cdacfb6093",
    "control/etsi.org/en-303-645/en-303-645-metadata.json": "207ce680215e06933adef2bc8bcd8ca62215845385c4f110e33fb718a75f3868",
    "control/etsi.org/qsc/README.md": "73afde4a007d6f3253952e54c29bf51a672cee0f9bf4ba7db4290eaabdffe2cd",
    "control/etsi.org/qsc/qsc-metadata.json": "7427338ce2ea1ea86cceba6230464bccaef1fcd49d97dfc2d3f28470466d4296",
    "control/europeanpaymentscouncil.eu/sct/README.md": "467cb2ab91c087a8be5691c3d3e114e4cdc98168b9ff95f1851d9e5b74f57585",
    "control/europeanpaymentscouncil.eu/sct/sct-metadata.json": "e6435343a747b5c02d8c3b5d54987a61031b99a4534940a82488e5c0fc5a5751",
    "control/fisc.or.jp/security-guidelines/README.md": "8a90e08487981f9198cc4607c5b2468db975ba3ba9e7c314b9e372e05de86016",
    "control/fisc.or.jp/security-guidelines/security-guidelines-metadata.json": "49ce5dbae71650dc5c01cee778ab39502cfb9097314b94de4b4e0465ba65bd58",
    "control/gov.br/gov-br/README.md": "b6d2c74bb442a3faee82c7fd9dd1a2fba9052fb6d716dfe48a129e678ee873f1",
    "control/gov.br/gov-br/gov-br-metadata.json": "1f1f19873a125a8523de1f16d041d2104e130cb10fce9bcbda9c206208fc502e",
    "control/gov.uk/one-login/README.md": "84dee09b9753cba3e0f78b125a14aa642c7b2f1526577ebef213d38155166b12",
    "control/gov.uk/one-login/one-login-metadata.json": "840ea33022bcbd44d354fa2d30ebcaed85424ed967c7602ddf48af843c1d7775",
    "control/idrbt.ac.in/cybersecurity-framework/README.md": "85ba69adf84bfb49d7c12e21c64b53e3145e0bd9c64a2c14dc604812e61b949e",
    "control/idrbt.ac.in/cybersecurity-framework/cybersecurity-framework-metadata.json": "52bbe0aac5e32f077e1e55ce2a8f156a0e7e7ca3b869a7d1a730c6de313059f6",
    "control/kantarainitiative.org/iaf/README.md": "e76c56d7e3308ab46e07b98fe0e8be2e1580ca04861d3192c4674f8e8af2583f",
    "control/kantarainitiative.org/iaf/iaf-metadata.json": "2e2edde6d8db86c5eb194183a0f612d19d47725c307cc1fd1c47dfd68c5f9ad1",
    "control/logius.nl/digid/README.md": "d71da90b66519f0b36136acac1544d68a1bca4c2ad3116b5f79335fdb4867c78",
    "control/logius.nl/digid/digid-metadata.json": "48a1db53a1c2a432da1a0f8943aadd810a604d6d23f244b3dab97eb010eb3bf4",
    "control/mitid.dk/mitid/README.md": "e2f383d22a219cf317840390715579066516cda5c6f242a341e690163bfffaa7",
    "control/mitid.dk/mitid/mitid-metadata.json": "bd686186a3746fe47df730574cf91ff4dff75406c0c430b5878c2577cf1961ba",
    "control/mygovid.gov.au/myid/README.md": "2c26d5fe04a558006296d9e7eab2647cd35eac6d22843f4d6927d24283a545b0",
    "control/mygovid.gov.au/myid/myid-metadata.json": "d7e29665403c35dc324e9157a0184162c486ffd4603a8f1c299e6a7e35e561a8",
    "control/nia.gov.gh/ghana-card/README.md": "2ba56c3a2720a46a107bf1497ee58e90a6a342720bed3389991a50282a63cead",
    "control/nia.gov.gh/ghana-card/ghana-card-metadata.json": "bad90f6b630e4eef4a7adc400e2c81a106618d197d9d5f0983c4a6473cb98f33",
    "control/nic.gov.sa/nafath/README.md": "04b6dc463b52022b5b0ce12dd6128c5c93b825bfa3792dd3c53399e1417a4832",
    "control/nic.gov.sa/nafath/nafath-metadata.json": "50742fcfafe200844268d70c0b85a056045c84f2110fe9896c6a965bf7027979",
    "control/nimc.gov.ng/nin/README.md": "eb9988a917918db3fe60b6378363a9b85395c00617ef83e63a3cfdca00af8a1f",
    "control/nimc.gov.ng/nin/nin-metadata.json": "c1de79e170cb50c95bcd620ac6b031f623b1fe8bf60392f0157acc78fc5b55a6",
    "control/npci.org.in/upi/README.md": "d428f451d641a0e6d44da17e847e090edb9b191b70b76ab97432e42a64557a32",
    "control/npci.org.in/upi/upi-metadata.json": "74de9263f3ba984919b03a5ec4b14b4e45a7fa799b6f6fd52b07f3b6957f0b21",
    "control/numerique.gouv.fr/franceconnect/README.md": "90b25a3c19a3a50e268cb8de2f1df6b33b9cffa7f291345f7c03b3334b97ee63",
    "control/numerique.gouv.fr/franceconnect/franceconnect-metadata.json": "0aa1f39c1d8abdb8ebf10adf9a1132721a110c39ff72177adc20af372d4615ca",
    "control/openbanking.org.uk/read-write-api/README.md": "e3cc3c5d1260c1719aa6f0096837146f8efad0353aba83313cf6d33c1e3f0724",
    "control/openbanking.org.uk/read-write-api/read-write-api-metadata.json": "2a9fcb1bfff938a48a247e4412d0840f07cf018803c510a1c3f9767c3af302e3",
    "control/openidentityexchange.org/trust-framework/README.md": "599005801f880df115fc415028f192ec53831fa1ef8bccfdaa10951558d52cc0",
    "control/openidentityexchange.org/trust-framework/trust-framework-metadata.json": "3c0c8d8348f8f47acb627203932a32d2d9d19b2012a01cdecf21a0716dd6abe8",
    "control/payments.ca/lynx/README.md": "d8044391a36137d53449ee6a7b6e1615ea8d592467487c92222bddb7f635ac73",
    "control/payments.ca/lynx/lynx-metadata.json": "c189748a3c71ab41aa93eb4708bd352f110a19398e65a7b99990baa8a2e27feb",
    "control/philsys.gov.ph/philsys/README.md": "65982d2cf2d4cbe8ff6a06a647b252df89c863bd9546505a9364a0b8cd628770",
    "control/philsys.gov.ph/philsys/philsys-metadata.json": "83a754c5d24da5ea6ce44a7ab5560a64d6b2f9abe8749344e269ecd50fa94853",
    "control/polishapi.org/polishapi/README.md": "2d5d571e4a7dd85bfe41bf140967c1e414d7de98c686422772bfdf5723a3b995",
    "control/polishapi.org/polishapi/polishapi-metadata.json": "cb2f0052224b30398fc700fe24862893dc5f980a56c381b40e237fe3e4acc51b",
    "control/pqcc.org/migration-roadmap/README.md": "adea62104bd18f2191413f26bd0e12fefbd7a2d807dd2ab5fffbeb856a09ef98",
    "control/pqcc.org/migration-roadmap/migration-roadmap-metadata.json": "5ad9f0d6c234d87571d1953e8171413999ebe1b4162be28e876624e771a2b7dd",
    "control/psacertified.org/tmsa/README.md": "cad8008b839bdce95e3e7f6b74b644ff744c4bbccf9c90ef52495387ee459917",
    "control/psacertified.org/tmsa/tmsa-metadata.json": "3d26765ee0b419ed409b002d8f98578d3a5f4d689cd5ce1eceb734d01a7c2214",
    "control/realme.govt.nz/realme/README.md": "b99fdd7116dedd3d763791171ec2d54e82f1995958b2e024f7e893f4020c198a",
    "control/realme.govt.nz/realme/realme-metadata.json": "1169437775fe98de4493d9229bb93b94cda1a2ba14747a4029410455f8d208e0",
    "control/ria.ee/x-road/README.md": "4cd391674d702b061b4433126e43e54f27bca60829989093470a2d0adfcab80f",
    "control/ria.ee/x-road/x-road-metadata.json": "65d20251b354a5f6a79ebaf50534496f084f0abb26394d8acc19207b0297f675",
    "control/singpass.gov.sg/singpass/README.md": "98136512d7a8070c24785fb52cd095165587b2259beb66f468d74eeef81f07a0",
    "control/singpass.gov.sg/singpass/singpass-metadata.json": "73d1abeffd5288bfefd19f8d48e0dd79947e3c5f4050b8aff001530a04574c16",
    "control/stet.eu/psd2-api/README.md": "27ac3eb638df8d5e1f0eec43299c31b7a90b76be4813d50034bb8aa434b15662",
    "control/stet.eu/psd2-api/psd2-api-metadata.json": "2a44b092d36eb98c12d84b580f678f59d9ba5801f51e5fd489183455620c10da",
    "control/uaepass.ae/uaepass/README.md": "8d922ce1968c41654d413846d167c2fec5170a5d80088a1c39ea51771453c08d",
    "control/uaepass.ae/uaepass/uaepass-metadata.json": "c276f42941c6cf4b178025e93b13e1092154476d9e263d07f16c17b307786684",
    "control/uidai.gov.in/auth-api/README.md": "c009c08cebf53ba310e97d3057fd13902bd5bc26ae6585bb7f5129c3072d3c51",
    "control/uidai.gov.in/auth-api/auth-api-metadata.json": "202eb42785140a41fd98f1c7647b95f521e14b9707591b89e7446f546b8aa765",
    "reference/adilet.zan.kz/concept-for-development-of-ai-in-kazakhstan/2024/concept-for-development-of-ai-in-kazakhstan-2024-metadata.json": "eb30d580adf194457aa1f9c74d0f72b15dc77e20fea4e5e53ace9fdf9abebef3",
    "reference/adilet.zan.kz/cybershield-kazakhstan/2017/cybershield-kazakhstan-2017-metadata.json": "fa81ae912bddc07b2fdf64c8704a64d0b27a388abaa9805edbcbc033a171c2bc",
    "reference/adilet.zan.kz/cybershield-kazakhstan/2023/cybershield-kazakhstan-2023-metadata.json": "6673bfb2a264add85095a71c61af8db2c3669b718834a91a93a1a2e4c9d6e64f",
    "reference/adilet.zan.kz/national-security-strategy-of-kazakhstan/2021/national-security-strategy-of-kazakhstan-2021-metadata.json": "4214d106198ba7d1aab92d61d7dd317193d08d29d138720c524c3b77cb656760",
    "reference/aig.gob.pa/estrategia-nacional-ciberseguridad/2013/estrategia-nacional-ciberseguridad-2013-metadata.json": "e9a3eec7af3227278c130978699017aadb99bc9c3e728cfcfbe537864f1b27d3",
    "reference/aig.gob.pa/estrategia-nacional-ciberseguridad/2021-2024/estrategia-nacional-ciberseguridad-2021-2024-metadata.json": "a0f2f5cef477cf0196f9037cc0eeb15d51fa31a571d4bf31bcbf9d812ea5548c",
    "reference/aii.et/ethiopia-national-artificial-intelligence-policy/2024/ethiopia-national-artificial-intelligence-policy-2024-metadata.json": "4154a6ba67e67af3d411bdbeca2eb5a6c4ed77f0c5b16137dce4c7f9572220e0",
    "reference/aii.et/national-information-security-policy-of-ethiopia/2011/national-information-security-policy-of-ethiopia-2011-metadata.json": "39897e6090e5b63fce06e0d9c056046d2dbc3b9aa89548ae7b39cad04ac65476",
    "reference/argentina.gob.ar/directiva-politica-defensa-nacional/2021/directiva-politica-defensa-nacional-2021-metadata.json": "7f0420fda770e8148dce27a65f72f84cfaeb417eccdcb67409b8849b2a2eb41d",
    "reference/argentina.gob.ar/estrategia-nacional-ciberseguridad/2019/estrategia-nacional-ciberseguridad-2019-metadata.json": "8a833a6b1ed8e4adaf171b711a2ee69c5f54d77a99b22e543a5b785ee6b711cb",
    "reference/bankid.com/glossary/glossary-metadata.json": "391e5c70b0b9f40c440c1c98511b7d14b87b1e893fafe55b43e85b507ed485a0",
    "reference/bimco.org/cyber-security-onboard-ships-glossary/cyber-security-onboard-ships-glossary-metadata.json": "797b0d537972441131d805258f582a34ef80634ff8e0f0a4c00ab0e0d4daa82b",
    "reference/bitdefender.com/infozone-glossary/infozone-glossary-metadata.json": "e9fb50f72a562950392a7bda98870def8406c6b130d83e4fb4618f32ed733bb2",
    "reference/bka.gv.at/aim-at-2030/2021/aim-at-2030-2021-metadata.json": "75d434f644a393b4aad4ba61cf0f070fe810797a3c4354fcc2b0e49135eeda8f",
    "reference/bka.gv.at/oesterreichische-sicherheitsstrategie/2013/oesterreichische-sicherheitsstrategie-2013-metadata.json": "9f47b070b1fd41194636f82a3f717fc394ac82636f41bbcb274e9b03cc707e05",
    "reference/bka.gv.at/oesterreichische-sicherheitsstrategie/2024/oesterreichische-sicherheitsstrategie-2024-metadata.json": "a689142b90cfe8342fd97a2de192ab1914343410aff48c7a981be071417b6b5e",
    "reference/bka.gv.at/oesterreichische-strategie-fuer-cybersicherheit/2021/oesterreichische-strategie-fuer-cybersicherheit-2021-metadata.json": "61cb53fea300cdd73c33bb77cfcec91a2bebc5816ba1125217a4a3fd2ffabcb5",
    "reference/blackberry.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "c7c92a22ef033b45fdf9d4890dce14eb6004217afcc596ca004c5a00e0400b03",
    "reference/blackduck.com/application-security-glossary/application-security-glossary-metadata.json": "17746f8981b53a78c9ddd70ddcb16f6522c1605f60ac5029a754075a0796905f",
    "reference/broadcom.com/enterprise-security-glossary/enterprise-security-glossary-metadata.json": "b82abc2b6ec78e1b3bb0a881feae6aef614f0bb12b63170f04d9bf2a92797f9f",
    "reference/bssn.go.id/buku-putih-pertahanan-indonesia/2015/buku-putih-pertahanan-indonesia-2015-metadata.json": "6b3fe54680596888f17bafc51aae1daaeac8c3dab286a380ff955db356e312ac",
    "reference/bssn.go.id/strategi-keamanan-siber-nasional/2023/strategi-keamanan-siber-nasional-2023-metadata.json": "aebf3efef1bd4fb14a8f81c9f6eb26d61a6e393f6dfba6cc8c88503150a81acc",
    "reference/bssn.go.id/strategi-nasional-kecerdasan-artifisial/2020/strategi-nasional-kecerdasan-artifisial-2020-metadata.json": "e5df8efe3e70e6d87083ca7834ccf7e8c8a7979f6534cd4352ea9335582520ae",
    "reference/bugcrowd.com/glossary/glossary-metadata.json": "1208fa5a30fde1c5e76442d276b725ec9a9e432c73cdaab759d0bd60d7b4fa2a",
    "reference/catonetworks.com/it-security-glossary/it-security-glossary-metadata.json": "0ad0cc99fde22714d2cc07a7dace9050af88808320f2dc4abe21c7f0488099d1",
    "reference/ccb.fgov.be/ai4belgium/2022/ai4belgium-2022-metadata.json": "6959159655514cc2edeb1d4eedded63f89740b69635f36d59b5d272c5fd30a1e",
    "reference/ccb.fgov.be/cyber-security-strategy-belgium/2021/cyber-security-strategy-belgium-2021-metadata.json": "a8d45212206585c155c5b270a8d0f6de0dcfce594d3960c2294a81f8b75755e1",
    "reference/ccb.fgov.be/national-security-strategy/2022/national-security-strategy-2022-metadata.json": "16cdf785e3aba3d74fe93f2b501b747f6eb7c4dfc77598495fb958bf09e2abca",
    "reference/cert.gov.lk/national-information-and-cyber-security-strategy/2019/national-information-and-cyber-security-strategy-2019-metadata.json": "ab855e677059a841e939b196c7eba4c27fa364fc5c72a1036eb197eea54c99ae",
    "reference/cert.gov.lk/national-information-and-cyber-security-strategy/2025/national-information-and-cyber-security-strategy-2025-metadata.json": "73fd81559745c4137387f77e0b591354350f595807846a7528cff35b115dbb18",
    "reference/cert.gov.lk/sri-lanka-national-ai-strategy/2024/sri-lanka-national-ai-strategy-2024-metadata.json": "fc607a03cacb04081c577d89981dcd47de64fffa8b4155e1a1f41ab93a4e0a47",
    "reference/cfcs.dk/foreign-and-security-policy-strategy/2023/foreign-and-security-policy-strategy-2023-metadata.json": "b6ca8eea8445bd2eb5af9d34d00fdcab33e76d6a7c86e7a62c8b6916c3b599cf",
    "reference/cfcs.dk/national-strategy-for-artificial-intelligence/2019/national-strategy-for-artificial-intelligence-2019-metadata.json": "7230bebe919b0f7eda0c7169ddff20dde8a4f235ff986bb48c76905b6ce695ef",
    "reference/cfcs.dk/national-strategy-for-artificial-intelligence/2024/national-strategy-for-artificial-intelligence-2024-metadata.json": "451df2987e535c7b657faa3400da034723ea15516905d420d7eef727ce5045dc",
    "reference/cfcs.dk/national-strategy-for-cyber-and-information-security/2021/national-strategy-for-cyber-and-information-security-2021-metadata.json": "501c3fbac2c77b4b4a8f4bf1abfb84ffdb3d8b93ab2cbe3c2b4e6ac79adf9757",
    "reference/checkmarx.com/application-security-glossary/application-security-glossary-metadata.json": "9939ad486c5f861389d4147c246ae0f04449c1c53f80b7042318dc0a87def88d",
    "reference/checkpoint.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "430114dfe8a6b75fa3ce648374f113eca38aed5f72f56e1e998027c94818405c",
    "reference/chinhphu.vn/vietnam-national-defense-white-paper/2019/vietnam-national-defense-white-paper-2019-metadata.json": "cf568f17fda0ef3191f5b7de8489ebb80ee85023d180da50f9f0e2b768385039",
    "reference/citra.gov.kw/kuwait-national-cybersecurity-strategy/2017/kuwait-national-cybersecurity-strategy-2017-metadata.json": "a6f7b8a7f25ec66c5d25dab2e5e8f4916f5204328d35c0d3a888105417031ca7",
    "reference/citrix.com/glossary/glossary-metadata.json": "32cd2c32b7ca0213b8f0b3821f25d81d038fae11c68d9fa91f0b58ae6f69cd06",
    "reference/cloudflare.com/security-glossary/security-glossary-metadata.json": "7aa9ecf2ec36e580eb55aef36e3d5fb9cd0c93ff1ef42078d6bde8ab6c924e45",
    "reference/cmu.edu/iso-glossary/iso-glossary-metadata.json": "3f95c520c07dac8112a7f2e2782c0e496e0010ed0ad5a49960304a1d6b3fbc03",
    "reference/cncs.gob.do/estrategia-nacional-ciberseguridad/2018-2021/estrategia-nacional-ciberseguridad-2018-2021-metadata.json": "5513a1c63817cfd45ede71e26f755dd9dbc6e0b5b4bf9b152807f647e7858e8e",
    "reference/cncs.gov.pt/ai-portugal-2030/2019/ai-portugal-2030-2019-metadata.json": "2e7cb2cd7b33cab509146ff610b0c744982703db7365fc72b61857a2d94389a4",
    "reference/cncs.gov.pt/ai-portugal-2030/2026/ai-portugal-2030-2026-metadata.json": "d7dbbdff848d10e053f9c924d9b67799336d6828ea83d8a0ed814441a379b3c6",
    "reference/cncs.gov.pt/national-cyberspace-security-strategy/2019/national-cyberspace-security-strategy-2019-metadata.json": "864e45f5baed097ea048f08a248d2aff59893d6918209b503cf4f5b0634c231d",
    "reference/cncs.gov.pt/strategic-concept-of-national-defence/2013/strategic-concept-of-national-defence-2013-metadata.json": "865079638e1afd0aceced02f1d8effd58d0cf8bea2b4795c4f388f9bf6200f8e",
    "reference/connectwise.com/connectwise-cybersecurity-glossary/connectwise-cybersecurity-glossary-metadata.json": "140e287ce20add8688a78d3a2141ee4a039cc3e29608125281c743e1a89cdf1c",
    "reference/cribl.io/cribl-glossary/cribl-glossary-metadata.json": "42c8330d106ae9d885d61727cb781e8682e4260c7de9f9f8b90d85bb19918333",
    "reference/csa.gov.gh/ghana-national-artificial-intelligence-strategy/2023/ghana-national-artificial-intelligence-strategy-2023-metadata.json": "331f84c78326b4acbed98673f4a9a9ee5f356f5ece1dde68663a46c55d6cd697",
    "reference/csa.gov.gh/ghana-national-cybersecurity-policy-and-strategy/2015/ghana-national-cybersecurity-policy-and-strategy-2015-metadata.json": "26ced85002e150d726b3afa77d703629e20d79ccb2ad1185c29ce81ba6659e1f",
    "reference/csa.gov.gh/ghana-national-cybersecurity-policy-and-strategy/2024/ghana-national-cybersecurity-policy-and-strategy-2024-metadata.json": "a315db711e87dbdcad51548818315a293d25ea28e77189260d14a7d5aa6099a1",
    "reference/csa.gov.gh/ghana-national-security-strategy/2021/ghana-national-security-strategy-2021-metadata.json": "00b229e69d24ddbf81fdfc43bce0e2889f9052e36a828cb07d4ff5277a7f7f6b",
    "reference/cscouncil.gov.mn/national-cybersecurity-strategy-of-mongolia/2022/national-cybersecurity-strategy-of-mongolia-2022-metadata.json": "a1b7ee68f85ce06ecea3004d23acc34380f92d10743d1cc309b452bc0123a413",
    "reference/cscouncil.gov.mn/national-security-concept-of-mongolia/2010/national-security-concept-of-mongolia-2010-metadata.json": "cb34d317b0088e341f69476a9842fe03a68837b12229e55f6c508d0fa564e419",
    "reference/cybersecurityworks.com/csw-cyber-security-glossary/csw-cyber-security-glossary-metadata.json": "dccce3ec0303ddc9765c8f43138d3c1ef3eb6fbce03dbc89c16ae1e2288b6ad4",
    "reference/devolutions.net/devolutions-it-security-glossary/devolutions-it-security-glossary-metadata.json": "e44807f87fb331440f652156382f1f3b96c0e6d84aaa9ed2c724d9364370cb68",
    "reference/dgssi.gov.ma/maroc-digital-2030/2024/maroc-digital-2030-2024-metadata.json": "6cd48ac9e61440586f5a6d00e1885707d5164c71d5f7668bc0ec03b09a8f4b29",
    "reference/dgssi.gov.ma/national-cybersecurity-strategy/2012/national-cybersecurity-strategy-2012-metadata.json": "d007f9347427f652b047f47e2a1ed69bf16665794cbe786d53b3a954e8e8b793",
    "reference/dgssi.gov.ma/national-cybersecurity-strategy/2024/national-cybersecurity-strategy-2024-metadata.json": "ea6bd9fe9e17833624f117534ddec6a89cd7ece0647a334b7fd78e106330839e",
    "reference/dict.gov.ph/national-ai-strategy-roadmap/2021/national-ai-strategy-roadmap-2021-metadata.json": "861e1efe213111a2d0398b7c7ba1c9f84dc8a51e1d1e7a976efdaac6700c5764",
    "reference/dict.gov.ph/national-ai-strategy-roadmap/2024/national-ai-strategy-roadmap-2024-metadata.json": "b1a944498c286ee0b068c02525cf4592118c894f65f17638c3f1a7f14763c7fe",
    "reference/dict.gov.ph/national-cybersecurity-plan/2023/national-cybersecurity-plan-2023-metadata.json": "d0bfd7562d1a8d2395774534fcbc18e843aac4ab7126ff698cbbb75c20752c2f",
    "reference/dict.gov.ph/national-security-policy/2023/national-security-policy-2023-metadata.json": "348df0a0e5ed1f1836a4cd7b62f46f52499bc6a4ec92b6b4d4a9626b5a69e5a4",
    "reference/digital.gov.fj/fiji-national-cybersecurity-strategy/2015/fiji-national-cybersecurity-strategy-2015-metadata.json": "a66c822987b4f473d00b95bcba074e3a59c0fdcc11174389ef88557b6be2c6c1",
    "reference/digital.gov.fj/fiji-national-cybersecurity-strategy/2025/fiji-national-cybersecurity-strategy-2025-metadata.json": "06f6656c10204dba05e255d23ec52143e26807c3875647630e2bd725eb07d12a",
    "reference/digitaltransformation.gov.to/tonga-national-cybersecurity-strategy/2024/tonga-national-cybersecurity-strategy-2024-metadata.json": "27458c78124a73cf1f245989d7aa8186eb50c40dd429ef7392b1b67a474785f4",
    "reference/dnsc.gov.ro/national-cybersecurity-strategy/2021/national-cybersecurity-strategy-2021-metadata.json": "806387f9e54a911da8c567b6f3aff9d3369b86833fd256ee0378d1be60bd828b",
    "reference/dnsc.gov.ro/national-defence-strategy/2020/national-defence-strategy-2020-metadata.json": "6588a5e9b903b0912fdb07024c0efce294ae033a16812b32ff2c1ee733a94d8d",
    "reference/dnsc.gov.ro/national-defence-strategy/2025/national-defence-strategy-2025-metadata.json": "34d4c6eff6fb80e2fbc7b6ca89002478ec83192dd1e0749c0f78a93847956de5",
    "reference/dnsc.gov.ro/national-strategy-in-the-field-of-ai/2024/national-strategy-in-the-field-of-ai-2024-metadata.json": "621e2d3505780993cde56e9fa0e5ef63fa79d9db2b74f82a201ad699a1054a32",
    "reference/dragos.com/dragos-ot-cybersecurity-glossary/dragos-ot-cybersecurity-glossary-metadata.json": "07946b7706df7f6b324c3b24b64fe1a4be62f8c480be6d9527815cf75fdd296f",
    "reference/dsn.gob.es/estrategia-nacional-ciberseguridad/2022/estrategia-nacional-ciberseguridad-2022-metadata.json": "351609d1dffd6ce86b12252cc6bdbe3284affd7e69890d6471b3a130bf5587e7",
    "reference/e-qanun.az/artificial-intelligence-strategy-of-azerbaijan/2025/artificial-intelligence-strategy-of-azerbaijan-2025-metadata.json": "018d22ead93cc916609feb7f94519f2af13bc3c4c57f61affefd211e5a0a2dd7",
    "reference/e-qanun.az/national-security-concept-of-azerbaijan/2007/national-security-concept-of-azerbaijan-2007-metadata.json": "ce338aeb89c3edb29561886eed218ab397789ee89996e8df2dcea97c8d5050f1",
    "reference/e-qanun.az/strategy-of-information-and-cybersecurity-of-azerbaijan/2023/strategy-of-information-and-cybersecurity-of-azerbaijan-2023-metadata.json": "c685912f59cd230105b61097e3a0a9d25b29fa7e1e81bb5d38ac13754cd6800a",
    "reference/eset.com/eset-glossary/eset-glossary-metadata.json": "d14f7e2658be79f2a3318ae369a6666f68afa659f6a79ff9d235dc839d5b8641",
    "reference/f5.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "2440c00fb73d4cfe277a6ae3fca82f7b000b15a383dbdfbbdbf5b96d32b59175",
    "reference/fidelissecurity.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "d25e90da812e54171d8e49ea61d485b7cb0ce7fa30ae747e48584df7706d39e5",
    "reference/first.org/cti-sig-glossary/cti-sig-glossary-metadata.json": "59a91b4d64480e1032d7665092e9b6d4203a0f881632166e3fd62e93c4217b23",
    "reference/flexerasoftware.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "3be417059fd6a91acd10d801e6ca3085fb28502a0ff71f8e1d953dbb5249df62",
    "reference/forcepoint.com/cyber-edu-glossary/cyber-edu-glossary-metadata.json": "44d5dc25a6704cc340b6b10a660f9954344231a935428a32a9f6a3ff67425086",
    "reference/fortinet.com/cyberglossary/cyberglossary-metadata.json": "f68e8ebf4e703f2b3ee739f3508efbe1010e83faf71773469e23a1e0be41a165",
    "reference/gartner.com/it-glossary/it-glossary-metadata.json": "27fb985e6232918606aecab0bd9e74218716885051185d2bc172194b7ca5b8df",
    "reference/gob.cl/politica-nacional-ia/2024/politica-nacional-ia-2024-metadata.json": "2c86fcc9406f735ba7c7f6cba544fd532a2d683110c36ac35955e21b8ac8eec9",
    "reference/gob.mx/programa-seguridad-nacional/2009-2012/programa-seguridad-nacional-2009-2012-metadata.json": "21acf9f35224b3fd9c316bd9654b17798d6ea93fe649c918af001cff20dc26be",
    "reference/gob.pe/estrategia-nacional-ia/2025/estrategia-nacional-ia-2025-metadata.json": "241407f660cb945c2811e6b26d721356b5bd0976e200b2f6d3e429a4a92fdd20",
    "reference/gob.pe/marco-confianza-digital/2020/marco-confianza-digital-2020-metadata.json": "1ab98c5ee5d42316cfccc54ed4e6e80627c2a05a62c3b25f302dbbf164c8317f",
    "reference/gob.pe/politica-seguridad-defensa-nacional/2021-2030/politica-seguridad-defensa-nacional-2021-2030-metadata.json": "3a7c15452d4e2be4df42937ba226ebdcf808e893a248f52590d27942e6aae0a6",
    "reference/gov.br/e-ciber/2020/e-ciber-2020-metadata.json": "28dcc2561cca02bdb70b6ec9576aa3f0c0579c6c18f6bce07d97457c7446ee92",
    "reference/gov.br/e-ciber/2023/e-ciber-2023-metadata.json": "2f9a9f38c9e369788b1cf15fbd07c538226ffce57ad5d75aeb18800d962b3099",
    "reference/gov.br/e-ciber/2025/e-ciber-2025-metadata.json": "62b7889ce86716b3a13b060ed0b1d2d3f959dce7475352f50b4aa400cbf568c1",
    "reference/gov.br/pbia/2021/pbia-2021-metadata.json": "1e282d923cb001decc8526607e6d85235a417e65919885299b24638fb7278821",
    "reference/gov.br/pnd-end/2008/pnd-end-2008-metadata.json": "4e2df9d40cb52a04930cd7597fa0d5c88c89c689bf86348fdf7da2cfdf7b2428",
    "reference/gov.br/pnd-end/2012/pnd-end-2012-metadata.json": "d06ab2580bbc356514dc26b0fecaa89adccb083c8c9709b9e706a783c8a2159f",
    "reference/gov.br/pnd-end/2025/pnd-end-2025-metadata.json": "ce64dd2f2a21c80482b0dfb78005dbc3e745a9cd35bd4d5cd511e320dd8b1ce3",
    "reference/gov.cn/national-security-in-the-new-era/2025/national-security-in-the-new-era-2025-metadata.json": "9cc2bbb6dcd8f3b53a685abd578da4c9c649b2bd1c95a0b16dd5e683b66c7d55",
    "reference/gov.pl/national-security-strategy-of-poland/2020/national-security-strategy-of-poland-2020-metadata.json": "ad4057b5929ce1bc78cf50207168e38d2709650d6a1a712707eba74325b0555c",
    "reference/gov.pl/policy-for-ai-development-in-poland/2020/policy-for-ai-development-in-poland-2020-metadata.json": "7cead0d03ea08cab91a52d532c343357c748e00dcd071ddb55db91aee977e833",
    "reference/gov.si/national-programme-for-promoting-ai-in-slovenia/2021/national-programme-for-promoting-ai-in-slovenia-2021-metadata.json": "7ee9521abbe9e6a042ce6744d30f884a6eabaee8becebac8ba257a8b6d4e9ac1",
    "reference/gov.si/resolution-on-national-security-strategy-of-slovenia/2019/resolution-on-national-security-strategy-of-slovenia-2019-metadata.json": "34c2aed7045f1441d1802616cea8db04bbc504e8fd263fdf0686d8a40a366181",
    "reference/gov.vu/vanuatu-national-cybersecurity-strategy/2013/vanuatu-national-cybersecurity-strategy-2013-metadata.json": "bd803d0a71e0ac7c0db3eac4b29d0aefa80f872ef5c9442cf7ddeab68af608b5",
    "reference/gov.vu/vanuatu-national-cybersecurity-strategy/2021/vanuatu-national-cybersecurity-strategy-2021-metadata.json": "86907aebff343172011efd2f9651ea19d5b79caf663aee82d2acb2c79d06d395",
    "reference/gov.vu/vanuatu-national-security-strategy/2019/vanuatu-national-security-strategy-2019-metadata.json": "6f86e2071dd27398c2a87521e4ba66a247de115282f18280b61f4424a86e6f0b",
    "reference/gov.za/south-africa-national-ai-policy-framework/2024/south-africa-national-ai-policy-framework-2024-metadata.json": "2548bd08421fbb7f7a39c9427723b0b847e3c563fbb082f1f64abb262869029d",
    "reference/gov.za/south-african-defence-review/2015/south-african-defence-review-2015-metadata.json": "5c1e3c073a25b121dc89321794e240df04ce5850a719c69e2032fbdfeec7f3d9",
    "reference/gub.uy/estrategia-nacional-ciberseguridad/2024-2030/estrategia-nacional-ciberseguridad-2024-2030-metadata.json": "347f32640feecc6ba221d5d6e8d87720fff33e6c8b60ebd7c913ce74285087d7",
    "reference/h-isac.org/health-isac-acronyms/health-isac-acronyms-metadata.json": "8e0ae5cf25e43aaf633a0a23d1e4d8c33ad3ba69755a7bb86e15b21423dd55e0",
    "reference/hackerone.com/hackerone-glossary/hackerone-glossary-metadata.json": "39c3abb318469ff66b103ec13a0449f203c6a2631c299bbce8d2e272a37659e6",
    "reference/himss.org/infosec-cybersecurity-terms/infosec-cybersecurity-terms-metadata.json": "b2e87c17d4cbeb32ffa04cdaca588a58451c6bd0cd925bc30a3e13ff3f893f52",
    "reference/huntresslabs.com/cybersecurity-101-glossary/cybersecurity-101-glossary-metadata.json": "a025e93385fb6d1042ea978f6a16dc563a9d52bb2534d8e9756d8f33b5b666ec",
    "reference/hypr.com/security-encyclopedia/security-encyclopedia-metadata.json": "a3527cddbe4810b8241ff35e0b1fb19c4accc03c5171842426b7ecd33b5e5517",
    "reference/iapp.org/privacy-glossary/privacy-glossary-metadata.json": "41ccd2e5b92218fece2095d0011d24a6204ba19bd6d1fc46b6d6afd92d34d77e",
    "reference/ibm.com/security-terminology/security-terminology-metadata.json": "7ea56ce4baa909b54dced3fd00a75fb86f1adfccfab27c7ce7c5e4a56cfa836a",
    "reference/ict.go.ke/kenya-national-artificial-intelligence-strategy/2025/kenya-national-artificial-intelligence-strategy-2025-metadata.json": "348966399581189a399967162511ca736fd8f48c4158d21a09c2c02cecef50c6",
    "reference/ict.go.ke/kenya-national-cybersecurity-strategy/2014/kenya-national-cybersecurity-strategy-2014-metadata.json": "9c08b3a444ca779a8b833a714edd7bb99ccb8f42bba592dc993f3bf4c7371c3d",
    "reference/ict.go.ke/kenya-national-cybersecurity-strategy/2022/kenya-national-cybersecurity-strategy-2022-metadata.json": "938b53f4ccfd348a280f17f87ce9cba06b4198caa91d295b52dea41358bb9834",
    "reference/ict.gov.pg/national-cyber-security-strategy/2021/national-cyber-security-strategy-2021-metadata.json": "67241fbd29d93af4b72b03a5c91fd0dd867c27b81ff339506508cb7db2766442",
    "reference/ict.gov.pg/national-cyber-security-strategy/2024/national-cyber-security-strategy-2024-metadata.json": "c435bc36262697ec09682f340ebff8cca50dcc9da192d90ea7b7f5f1f62a4eba",
    "reference/ict.gov.pg/papua-new-guinea-national-security-policy/2013/papua-new-guinea-national-security-policy-2013-metadata.json": "e06dff16da5d36f7f8a4ca891785400a8449a5daa867429d9b94b974a6e51685",
    "reference/ictd.gov.bd/bangladesh-cybersecurity-strategy/2021/bangladesh-cybersecurity-strategy-2021-metadata.json": "79e490f1f0b360a214e9ec8c8d252c1ec30de80e61d911ea1c330371ab591b63",
    "reference/ictd.gov.bd/national-strategy-for-artificial-intelligence-bangladesh/2020/national-strategy-for-artificial-intelligence-bangladesh-2020-metadata.json": "db121e7f82c3de72465e55c0dbe5e8f281a895e21effa3401e82030984691a7b",
    "reference/illumio.com/cybersecurity-101-glossary/cybersecurity-101-glossary-metadata.json": "4c0ae85cfce730f5f218a1656965456ddab0947c88d78354faf3a9c522793112",
    "reference/intel.com/software-security-glossary/software-security-glossary-metadata.json": "93591b17795d883f841db4171324f94341f8afd3a498cdd8aba12321a0ef3a67",
    "reference/itu.int/cybex-x.1500/cybex-x.1500-metadata.json": "84e79c37be3e30e0f3930b304f4dd6e6d080426ce6a9c4e8668b54886afb65fb",
    "reference/ivanti.com/ivanti-glossary/ivanti-glossary-metadata.json": "40ed0bdb23670d7bbeff5557284efc74b346ad858f8d4c20673f2b339b9852a6",
    "reference/jamf.com/jamf-platform-glossary/jamf-platform-glossary-metadata.json": "83d5c2a249ac242df5f391cfcd6bba03aeba26e20da5eacc4e80c480ecb42135",
    "reference/juniper.net/juniper-glossary/juniper-glossary-metadata.json": "afeb48bf9ed5013c5edb0667137ab3b061244190cd342229011a19560945280e",
    "reference/jupiterone.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "8def09b0d96b60b5081e9bdaf674f98bacacfbf4fdb0ffd2c299d15d5f9b1c8f",
    "reference/kam.lrv.lt/national-cyber-security-strategy/2018/national-cyber-security-strategy-2018-metadata.json": "417eef24033b460756cba7f4e735ca64857ab309b6991899a3cecf6b27d72f29",
    "reference/kam.lrv.lt/national-security-strategy/2021/national-security-strategy-2021-metadata.json": "5ebc5f2fd6a37f9bb5d87be50f339c250aea017339db95f2f0c05f5cb787285a",
    "reference/kaspersky.com/it-encyclopedia-glossary/it-encyclopedia-glossary-metadata.json": "14ed3002a3019d9f670a34685f32c9b58eb7260192652e775e78b5a63150fbb4",
    "reference/keepersecurity.com/iam-glossary/iam-glossary-metadata.json": "8ed89ac142ccfb1f8aae97fdbeae98efb4c4e234ab7cac46af2b390bfa177539",
    "reference/mcit.gov.eg/egypt-national-artificial-intelligence-strategy/2021/egypt-national-artificial-intelligence-strategy-2021-metadata.json": "cd85d63d885185bbcea8c66b3b4d37c428ae3cd7046014a651a65f3b72075ff9",
    "reference/mcit.gov.eg/egypt-national-artificial-intelligence-strategy/2025/egypt-national-artificial-intelligence-strategy-2025-metadata.json": "23f001037be16b41cc3b6b5c9fbcb4d793604a17732605c2766cacbadb6f8700",
    "reference/mcit.gov.eg/national-cybersecurity-strategy/2017/national-cybersecurity-strategy-2017-metadata.json": "8289abb8443c6a65654160e51b473bdd14c5504fbde38c4d63ebb33506bb3672",
    "reference/mcit.gov.eg/national-cybersecurity-strategy/2023/national-cybersecurity-strategy-2023-metadata.json": "161f186e4954f4587c65c3c26678cc38971e8b621d1b1c9b6e64dbe16b231255",
    "reference/mcit.gov.ws/samoa-national-cybersecurity-strategy/2016/samoa-national-cybersecurity-strategy-2016-metadata.json": "adb5adc0a86e16bae604b3868f70cf1124ad973c84e0e6535770711b314212c4",
    "reference/mcit.gov.ws/samoa-national-cybersecurity-strategy/2024/samoa-national-cybersecurity-strategy-2024-metadata.json": "11dddd99763e99041abdcd79d742ec9247d545384b3f0c29f1100790c1b31709",
    "reference/mcit.gov.ws/samoa-national-security-policy/2018/samoa-national-security-policy-2018-metadata.json": "1338993986fbd40297cf5c59a532fcb10a14bf6ab01f2b4422ded825d1371ad5",
    "reference/mctn.sn/strategie-nationale-d-intelligence-artificielle-du-senegal/2023/strategie-nationale-d-intelligence-artificielle-du-senegal-2023-metadata.json": "419cc48b1b9cf0b810a135dd2defcba10280624dffea6f1af971236beba5310a",
    "reference/mctn.sn/strategie-nationale-de-cybersecurite-du-senegal/2017/strategie-nationale-de-cybersecurite-du-senegal-2017-metadata.json": "df47c4995afe142dd0d00c3767ececcfbbffe3507e30449e0adcf3a26f77f2c7",
    "reference/mindigital.gov.gr/blueprint-for-greeces-ai-transformation/2024/blueprint-for-greeces-ai-transformation-2024-metadata.json": "7a3526a43a9a2a21d4455612bcfcff38259e044fddedcc82112cd9d98f9279b3",
    "reference/mindigital.gov.gr/national-cybersecurity-strategy/2020/national-cybersecurity-strategy-2020-metadata.json": "25f2241e17a8babffd495a524326df730a2890c7f210c9336f780d2dee3d911f",
    "reference/minict.gov.rw/rwanda-national-artificial-intelligence-policy/2023/rwanda-national-artificial-intelligence-policy-2023-metadata.json": "c1587a3a547ca660b8c877836f68d192a1a22bae82c628ecdccab2b4dfd5cd12",
    "reference/minict.gov.rw/rwanda-national-cyber-security-strategic-plan/2015/rwanda-national-cyber-security-strategic-plan-2015-metadata.json": "8581692317491daa9494324b3c66980293f8818ee179229673ce4a0214aa0c71",
    "reference/minict.gov.rw/rwanda-national-cyber-security-strategic-plan/2024/rwanda-national-cyber-security-strategic-plan-2024-metadata.json": "330345047bcb9e1190419f961e8ad2a771fb79bd9832fd88e7fcd5b98e1a69a9",
    "reference/mit.edu/infoprotect-definitions/infoprotect-definitions-metadata.json": "52fefe659c62830d96c551fee30b3d635869f5096da014a85ea21d5ab219452f",
    "reference/mitic.gov.py/estrategia-nacional-ciberseguridad/2017/estrategia-nacional-ciberseguridad-2017-metadata.json": "197b8dcb25436647cbfa7b3ce6b78ecab0dfe5f9973f5270cffabcc838bdf62c",
    "reference/mitic.gov.py/estrategia-nacional-ciberseguridad/2025-2028/estrategia-nacional-ciberseguridad-2025-2028-metadata.json": "b08045c4685925e2dba0a806dbe6c36ff786b932be378cc888183e611b40ac7f",
    "reference/mkm.ee/cybersecurity-strategy/2008-2013/cybersecurity-strategy-2008-2013-metadata.json": "713a2d21ae9b520b0f6e6ec6f840134ebe00d28360f14ba9e7ff0a3826de655e",
    "reference/mkm.ee/cybersecurity-strategy/2014-2017/cybersecurity-strategy-2014-2017-metadata.json": "e034cec45e700bfa6a0fd1d6edb49acce1404de89da938d00558e3a9c5f41077",
    "reference/mkm.ee/cybersecurity-strategy/2019-2022/cybersecurity-strategy-2019-2022-metadata.json": "98378b2fb25574d6301cd97c97a7798d1138dfbacf0c444567acb8992ac98251",
    "reference/mkm.ee/cybersecurity-strategy/2024-2027/cybersecurity-strategy-2024-2027-metadata.json": "629b724b7ae2da95bb643e71a5ab8cade9db096072cacc28bfbd414ba4bd5bfb",
    "reference/mlcommons.org/ai-safety-glossary/ai-safety-glossary-metadata.json": "44126eab850f91f2f55b7900ac580df9319f563a96c93a6b4cf97baf7a3e7e22",
    "reference/mocit.gov.np/national-artificial-intelligence-policy/2025/national-artificial-intelligence-policy-2025-metadata.json": "87393ed52dd42c964a92ff66feea8003de026e24679c10790da4a034ee2dbe3a",
    "reference/mocit.gov.np/national-cyber-security-policy/2023/national-cyber-security-policy-2023-metadata.json": "b27c66367959871083841a17743427b1f1ee2f8749d70bd3fc899ef727f2dcc1",
    "reference/mod.gov.lv/cybersecurity-strategy-of-latvia/2023/cybersecurity-strategy-of-latvia-2023-metadata.json": "987b851d466e3e1f1595da94c6393dc88dafac71d3605689bfd135b89ebe35cd",
    "reference/mod.gov.lv/informative-report-on-development-of-ai-solutions/2020/informative-report-on-development-of-ai-solutions-2020-metadata.json": "f5e3cf1fd71d74a4636749b926c7cb1aefd2f105ab96a91a17bb90ac0e7902e0",
    "reference/mod.gov.lv/national-security-concept/2023/national-security-concept-2023-metadata.json": "6e23a3a50c7a72aa65e10fd30dbef1f102ff71f25e36a7958833c810a2b02a99",
    "reference/modee.gov.jo/jordanian-artificial-intelligence-strategy/2022/jordanian-artificial-intelligence-strategy-2022-metadata.json": "94f8709b1173999adae1b45c8fc822459b57a069e8a56ca1bb4d10e7b470deda",
    "reference/modee.gov.jo/national-cyber-security-strategy/2018/national-cyber-security-strategy-2018-metadata.json": "d79c31beb877e9b7ef8c1c0b6f129a5a518475a1011d2b1277c3ef475861c106",
    "reference/moitt.gov.pk/national-artificial-intelligence-policy/2025/national-artificial-intelligence-policy-2025-metadata.json": "a48bbc50c328600230822254115b4e5ee4f448fe3c9b96c89074e7c93955e4c4",
    "reference/moitt.gov.pk/national-cyber-security-policy/2021/national-cyber-security-policy-2021-metadata.json": "158c7aea71bba9d2db46809466402f1537b5442d298a33f7d1a76d7e0c672198",
    "reference/mots.gov.zm/zambia-national-artificial-intelligence-strategy/2024/zambia-national-artificial-intelligence-strategy-2024-metadata.json": "b0f4ba33d1eb4ee0ffd9eff3f083ff431725290a370c3f3ffc2d24fbf0f62e0e",
    "reference/mots.gov.zm/zambia-national-cyber-security-policy/2021/zambia-national-cyber-security-policy-2021-metadata.json": "f515335ffc5bd67f3ef789d9f327c3032e45f4f8bff8b03a15d13daa067ad820",
    "reference/mtcit.gov.om/national-program-for-ai-and-advanced-digital-technologies/2024/national-program-for-ai-and-advanced-digital-technologies-2024-metadata.json": "20d0307501f12e6252a8c9bfa32760259233987d7f7b911f0c0624c40fdee374",
    "reference/mtt.gov.rs/ai-development-strategy-in-serbia/2019/ai-development-strategy-in-serbia-2019-metadata.json": "ec31aea08721fe7be6a0d68ff031cc2664289f51b750adc701fa12615cdc8fe4",
    "reference/mtt.gov.rs/ai-development-strategy-in-serbia/2025/ai-development-strategy-in-serbia-2025-metadata.json": "d34349dab787b63b65233a4f109e6fdd61b81bc4b1327a1b23504d5a4b84dcf4",
    "reference/mtt.gov.rs/strategy-for-development-of-information-society-and-information-security/2021/strategy-for-development-of-information-society-and-information-security-2021-metadata.json": "2d97b0eaa3daf498e45342f3a2ca30570ef12e8508b7bdb3108c8fd886a6fe6a",
    "reference/nbu.gov.sk/action-plan-for-digital-transformation-of-slovakia/2023/action-plan-for-digital-transformation-of-slovakia-2023-metadata.json": "266b9b90a975b661491d38f4b1e1e5241408ff43237058c2d15969299c8fcde3",
    "reference/nbu.gov.sk/national-cybersecurity-strategy-of-slovakia/2021/national-cybersecurity-strategy-of-slovakia-2021-metadata.json": "3431ec9ce8e98f04bd03bc47a24524e0e6c1194c78f9c9cf6a431b096ccb36f6",
    "reference/ncsa.or.th/national-cybersecurity-strategic-plan/2022/national-cybersecurity-strategic-plan-2022-metadata.json": "62bbca6e4b28620fefa1f789b4b10605a7b005c26a621a491c44eec76ef7eee2",
    "reference/ncsa.or.th/national-security-policy-and-plan/2023/national-security-policy-and-plan-2023-metadata.json": "b9ba04adbb4dbe7dcc16360db65ba4d3e67bd106f5a74e4d4c4c26fb106d9847",
    "reference/ncsa.or.th/thailand-national-ai-strategy-and-action-plan/2022/thailand-national-ai-strategy-and-action-plan-2022-metadata.json": "d30208b86d1f332071862cacbaae1b4302803f47727cacb825f370027fe63f51",
    "reference/ncsc.ch/ncsc-ch-glossary/ncsc-ch-glossary-metadata.json": "ca8d9273c196b7158d70d5f484b31354bb467b7729514499aaf655123c032cf3",
    "reference/ncsc.fi/foreign-and-security-policy-report/2020/foreign-and-security-policy-report-2020-metadata.json": "6a48eaf7b0f39bc131a8f3629db52248f3003d1e3dd4d0bdae3072a821003c23",
    "reference/ncsc.fi/foreign-and-security-policy-report/2024/foreign-and-security-policy-report-2024-metadata.json": "e3f9d367a0c7be90fe576c619bc56cff41d19524f436274a48eb6d4db77998ec",
    "reference/ncsc.fi/kyberturvallisuusstrategia/2024-2035/kyberturvallisuusstrategia-2024-2035-metadata.json": "afbfe936522fd876846acc1b66458459e65c128eac5a2a3594ea61c45c6c0dde",
    "reference/ncsc.gov.bh/bahrain-national-cybersecurity-strategy/2017/bahrain-national-cybersecurity-strategy-2017-metadata.json": "3ba043984f8166ebfe0cbf763baa87d5a203f46c5e71222d0a0ec97d4ffacd9b",
    "reference/ncsc.gov.bh/bahrain-national-cybersecurity-strategy/2023/bahrain-national-cybersecurity-strategy-2023-metadata.json": "4d89364b4b4f2999a8c7f86136452ce55ba3650663540c24514ca2dc980f9c37",
    "reference/ncsc.gov.ie/national-cyber-security-strategy/2023/national-cyber-security-strategy-2023-metadata.json": "0e5847577d1cdef4af13a0a577181bcdc74ddacfedd2556ee355522aea464f21",
    "reference/netapp.com/netapp-glossary/netapp-glossary-metadata.json": "40be5a813777acd22f59850ce1682a1c1138ab03c9f582a24ebee9aa805cb361",
    "reference/netskope.com/security-defined/security-defined-metadata.json": "2ac8a906bc76dad10d6e9b676eea8f0130b051510b35db6467f998e2717ab356",
    "reference/nitda.gov.ng/national-cybersecurity-policy-and-strategy/2014/national-cybersecurity-policy-and-strategy-2014-metadata.json": "3afdce72cf4f95e1d879a40694811c5fd9ea56aac40cb35ad530c492b43dd17c",
    "reference/nitda.gov.ng/national-cybersecurity-policy-and-strategy/2021/national-cybersecurity-policy-and-strategy-2021-metadata.json": "e9e954a214323266bc5b8aa763dbd6429731ae068dedb31799dcb267b4a200b3",
    "reference/nitda.gov.ng/national-security-strategy-of-nigeria/2014/national-security-strategy-of-nigeria-2014-metadata.json": "1c1d4a94bb3caea65f87c3f5495b3ddacd405eb5b8ab83a428e5637a2c05d0c0",
    "reference/nitda.gov.ng/national-security-strategy-of-nigeria/2019/national-security-strategy-of-nigeria-2019-metadata.json": "4504c6aaa33ecef32a175c85a0e9291c124d3b4b0eb1b902223a3bf57ffdf7f1",
    "reference/nitda.gov.ng/nigeria-national-artificial-intelligence-strategy/2024/nigeria-national-artificial-intelligence-strategy-2024-metadata.json": "06b33352c170a477ea96431fab8c7fb20f3f99318a23687dd3304c4457e1fe53",
    "reference/nukib.gov.cz/national-ai-strategy/2019/national-ai-strategy-2019-metadata.json": "04040d81aa3d1cbd1c9925d56da0aa787ce51afd947431dac00efc838f95f65b",
    "reference/nukib.gov.cz/national-ai-strategy/2024/national-ai-strategy-2024-metadata.json": "1969c98d3c4d5f60d1f6ecbc639ac1c12109d2cfed024c4a39a3135cbcd7e493",
    "reference/nvidia.com/nvidia-glossary/nvidia-glossary-metadata.json": "e6e955867e1a2a12cb4339a20cee3b5c7a44f9d4c0c6fee90dc4e0a960435f46",
    "reference/okta.com/iam-glossary/iam-glossary-metadata.json": "f8b621d0c1543fc8ea6e6019cd50f272d534dd6c285a32233f1c193c2b0f378e",
    "reference/openidentityexchange.org/identity-glossary/identity-glossary-metadata.json": "5cf7c96597749dea00ba6a84362f5748a7c983b88bb605fa4551275475f082d2",
    "reference/opentext.com/appsec-glossary/appsec-glossary-metadata.json": "ae5a7ff0daae20f183ae3acd1249471f12c703aa56c60627c078b5d1c6dfc7b4",
    "reference/oracle.com/oci-glossary/oci-glossary-metadata.json": "ce81542b40bddae24c9b27463e84649b756f912663dd890f018f19cac06926ef",
    "reference/palantir.com/foundry-security-glossary/foundry-security-glossary-metadata.json": "0719333c53573dedf419d6e7a4b710d2470c07b9a8d33f25801e5573f1a97489",
    "reference/panasonic.com/security-system-glossary/security-system-glossary-metadata.json": "6b9f26cdef89661e654b785713e9179b9206a0048a6e2656fb99dc656623c7dd",
    "reference/papercut.com/print-security-acronyms/print-security-acronyms-metadata.json": "1dc9b5e85004fa3f2c49088b79a6ac89fef38c5f319deb20cd939f804ab3f1e7",
    "reference/partnershiponai.org/synthetic-media-glossary/synthetic-media-glossary-metadata.json": "16f68252eb263f68d67310144531fac3e5c2b61bebe9162ba1f6fe6edc4253f2",
    "reference/pingidentity.com/identity-glossary/identity-glossary-metadata.json": "1b0cfaaee441fea058dfe28c89b72a6c29f003199bf4187c6a39173971a283f1",
    "reference/pravo.gov.ru/doctrine-of-information-security-of-the-russian-federation/2016/doctrine-of-information-security-of-the-russian-federation-2016-metadata.json": "6e3581c96b28ca998b47cb9bcaadac08c56ee74d9892fb289f620133e69fdb01",
    "reference/pravo.gov.ru/national-security-strategy-of-the-russian-federation/2021/national-security-strategy-of-the-russian-federation-2021-metadata.json": "dd9e5d1053b65da80e6eb5cb3eb82ecfe1119cfe58a0888a1d8337fe8e2d0a92",
    "reference/pravo.gov.ru/national-strategy-for-the-development-of-ai-until-2030/2019/national-strategy-for-the-development-of-ai-until-2030-2019-metadata.json": "3d4df6cee8c4229d6191a41dbefd4cbc543585c01473a151045926a2cf88dce8",
    "reference/pravo.gov.ru/national-strategy-for-the-development-of-ai-until-2030/2024/national-strategy-for-the-development-of-ai-until-2030-2024-metadata.json": "ccc00c182bf70fdf8a892e8cc80c0440e284b0ea0984cb6f1b42b266984d1794",
    "reference/profibus.com/pi-glossary/pi-glossary-metadata.json": "3edbf170c6f4b3fc2376be0c6f483db94be9ce03180ac5731127871911f97f71",
    "reference/progress.com/data-protection-privacy-glossary/data-protection-privacy-glossary-metadata.json": "5f55088dcd2ed2a02fd0ac2b54d55400d4c284934d0fe57e232edfab2e6f393a",
    "reference/proofpoint.com/threat-reference/threat-reference-metadata.json": "5d40e8d44f910c9be7a676ce137b8706f893bdfbbeb16bf807d847b7e889334a",
    "reference/proton.me/encryption-glossary/encryption-glossary-metadata.json": "8d1dd7252dabb3988442e30bf6c8b78208e3c0ec44d8ae4f921fb92bc2bfc0db",
    "reference/rapid7.com/cloud-security-glossary/cloud-security-glossary-metadata.json": "a94c92f43b9fb5e514998a17de77348efc3c381059fe7bcaee80874e6dee7e8d",
    "reference/redhat.com/security-glossary/security-glossary-metadata.json": "e089e1497d00cbd1814a9818707789f5e3e2c192726f785f45a73a5629d710d5",
    "reference/regjeringen.no/national-cyber-security-strategy/2019/national-cyber-security-strategy-2019-metadata.json": "d0c625902553e86b8eedf694b4dbf926423037f567195e6eaab0849a9f9e37c4",
    "reference/regjeringen.no/national-security-strategy/2025/national-security-strategy-2025-metadata.json": "2975f70f6e35e179fb697629feec5e0d1253234dfca15f305bc136b9057f37cd",
    "reference/rijksoverheid.nl/nederlandse-cybersecuritystrategie/2018/nederlandse-cybersecuritystrategie-2018-metadata.json": "5850c3506b2d4879dcc49eeddb9315f5144c134017e52ff83937eb51b1b0f978",
    "reference/rijksoverheid.nl/veiligheidsstrategie/2019/veiligheidsstrategie-2019-metadata.json": "d4c5651b70f8b916bd29862b0a67c47344f7063ffad95d928516e32156cc6beb",
    "reference/rnbo.gov.ua/concept-for-development-of-ai-in-ukraine/2020/concept-for-development-of-ai-in-ukraine-2020-metadata.json": "836f9aee8f5c5e2727cba2184fa0fc9b4034b8dc053f6d0cc8f7e8a4462ef723",
    "reference/rnbo.gov.ua/concept-for-development-of-ai-in-ukraine/2024/concept-for-development-of-ai-in-ukraine-2024-metadata.json": "b8bc1c52e68d74c0461e43a177db6b99dcc1b70ae0bf4afce458dc31aada81c4",
    "reference/rnbo.gov.ua/cybersecurity-strategy-of-ukraine/2021/cybersecurity-strategy-of-ukraine-2021-metadata.json": "5c3445bd33f4bdd63ff7d0ef1eaaa1a2e7efd5da243dcd6f9b02e81980a74bec",
    "reference/rnbo.gov.ua/national-security-strategy-of-ukraine/2020/national-security-strategy-of-ukraine-2020-metadata.json": "086929b9583ff7f1c96b5ac007975ea5b166465a6802d1509054ab8629eb6ee8",
    "reference/sailpoint.com/identity-security-glossary/identity-security-glossary-metadata.json": "87d8992664ac117da26562123504f5f661052cd1fc434f80f1850738d6effcc0",
    "reference/sans.org/glossary/glossary-metadata.json": "159a67c3f414bc5ecd10f808d380b003f121ef2fe4ebe4a534241008d4a0d2c0",
    "reference/saviynt.com/identity-security-glossary/identity-security-glossary-metadata.json": "8017e0a91aa25de22d399f51b8bf60de5a9cd7c5e4bf84643417dda71fc066d3",
    "reference/sdaia.gov.sa/nsdai/2020/nsdai-2020-metadata.json": "4a294ef4515137150052d2fe095b0363272e6c914c39412e13d75073826f5833",
    "reference/securityscorecard.com/securityscorecard-glossary/securityscorecard-glossary-metadata.json": "9321d2d858b883433192b5aee294098466b297ded1c9c19102a650d1e4413f02",
    "reference/silabs.com/security-glossary/security-glossary-metadata.json": "25895ab9ad348b416c0d8356628f3e93320c654579a98b714545a127eb3acc84",
    "reference/snyk.io/ai-cybersecurity-glossary/ai-cybersecurity-glossary-metadata.json": "e642e4659723e6a70f1fa61d40454646e7f99f2e533f79c4fb6ec5a758fbc049",
    "reference/socradar.io/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "8f706f3bf054457b01dfdc1ba6dd06ef6ff792f464acbdda26832859ffffa5b5",
    "reference/solarwinds.com/it-glossary/it-glossary-metadata.json": "faa9cf35beb4e0a62bc85c050fd71855bbc77ba6c14a6d9d0b781e62979f4a48",
    "reference/sonicwall.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "4d74a4eb29ad2431d886d9d88137df8fb8bb49d37499b9550f01e4f9de932451",
    "reference/sophos.com/cybersecurity-explained/cybersecurity-explained-metadata.json": "99d947e2c3132070ca02299a93265554af2ffeb2a7e2d527c220821ede928408",
    "reference/stjornarradid.is/icelandic-national-cybersecurity-strategy/2022/icelandic-national-cybersecurity-strategy-2022-metadata.json": "9f2b1775ec3150536b5931ec601ccd76fb922554cc6c75e878b959bd22d78a6e",
    "reference/stjornarradid.is/national-security-policy/2016/national-security-policy-2016-metadata.json": "08593b147b4f72e9d6b8162e4158b16aecdaf4132c42bd1451fcfbf8f1bcdbbf",
    "reference/stjornarradid.is/national-security-policy/2023/national-security-policy-2023-metadata.json": "777447717bafe9fde47956fc5d047bd98a719efdf06356c809c484f0a686ceba",
    "reference/stjornarradid.is/policy-on-artificial-intelligence/2021/policy-on-artificial-intelligence-2021-metadata.json": "e1a68e2fd6b5caba547eb73539e5932657bdfc7c2172289fd7d8157c09493db6",
    "reference/stjornarradid.is/policy-on-artificial-intelligence/2024/policy-on-artificial-intelligence-2024-metadata.json": "15bf5763753cf3a236d8403dbb9185cf6efe6defeb490a2916a482596053d79a",
    "reference/strongdm.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "8b34023920c7aa408cc4ca619efae634d548b2f98f31e4a663065178aa674880",
    "reference/techtarget.com/security-definitions/security-definitions-metadata.json": "0403be92561e51c2dff91dee2673367083fbe0e76e9afbba54394777d5718a86",
    "reference/tenable.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "91af19594af35a64bb16dda4aca8898a1452b5e4f46efd03823e04363dbd868e",
    "reference/thecyberwire.com/glossary/glossary-metadata.json": "a0cb3eef576a23192ac42568e094990b4708a70d8c673b751dcab9daf0a2edd6",
    "reference/treasury.govmu.org/mauritius-artificial-intelligence-strategy/2018/mauritius-artificial-intelligence-strategy-2018-metadata.json": "278df296d86e9fc523985917013e2ae124d1deb946c5ff9abb5239ce6b8d502f",
    "reference/treasury.govmu.org/mauritius-national-cyber-security-strategy/2014/mauritius-national-cyber-security-strategy-2014-metadata.json": "ca683e0fdcaba029847c7c8a6b0e5ecba51788ecfea3f6d67f01981bf5c86f1f",
    "reference/treasury.govmu.org/mauritius-national-cyber-security-strategy/2023/mauritius-national-cyber-security-strategy-2023-metadata.json": "3b7fb4e3aa7f11e512702dc0f4b460279edf6040b58e6d73949ebf48cc66fc2b",
    "reference/trendmicro.com/what-is-cybersecurity-terms/what-is-cybersecurity-terms-metadata.json": "31283df5bce5a050e5e8e4f0cd2d6f156251f9b46e214db14bd2e13073d259e4",
    "reference/txone.com/ot-cybersecurity-glossary/ot-cybersecurity-glossary-metadata.json": "c0da330f639cbe0656a2f360e7793f5a47a082ebff8fd364a52fb7d277e55b6e",
    "reference/uab.gov.tr/national-cyber-security-strategy-and-action-plan/2020/national-cyber-security-strategy-and-action-plan-2020-metadata.json": "8d870a121dc7fcd63a82b6ebe0ee72ff5a6927b43ab29d26f03e7e209ab5dc55",
    "reference/uab.gov.tr/national-cyber-security-strategy-and-action-plan/2024/national-cyber-security-strategy-and-action-plan-2024-metadata.json": "d2b8d364117e32bcbf33c1974b4e5b0b1a222cc73fb35e97cbbe8b53ab41cd1f",
    "reference/upguard.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "6bacaaca916a257e301e03e6a21f8a655cf4ba87e9bff170d54049a56abe916b",
    "reference/valitsus.ee/national-security-concept/2004/national-security-concept-2004-metadata.json": "ad1a86d8ea811c054f62b0bcd3b7e22ee89fafd19d1146376d104c88cd9fdca2",
    "reference/valitsus.ee/national-security-concept/2010/national-security-concept-2010-metadata.json": "322cc0ec1574cc0c1b1cebcbb5bfff8d6fbb972e651b1703a403d21bf67ff8df",
    "reference/valitsus.ee/national-security-concept/2017/national-security-concept-2017-metadata.json": "6c5a76c32dbdca0512378baa59fa0e29e2cd5f023cba75e4a96bf84765a069a4",
    "reference/valitsus.ee/national-security-concept/2023/national-security-concept-2023-metadata.json": "2d597bc6f8ffbd29658126b62beede8383747d0cb657a7a24b4467ca0fbc1ec5",
    "reference/watchguard.com/network-security-glossary/network-security-glossary-metadata.json": "4a9e6aa2a91b771cf27f11744e24f00b70bd6de9654d23b533e3e941e9846dca",
    "reference/wpscan.com/wpscan-glossary/wpscan-glossary-metadata.json": "0b89289fb0283b0151a6fa097445e0567ec2b690d2d6c876656bff0ce8e55f3e",
    "reference/xonasystems.com/cybersecurity-glossary/cybersecurity-glossary-metadata.json": "6506b9de2a8a27e0098f48a1c19a68dda29626dfbb1963a06c854c4f75bf81a5",
    "reference/zohocorp.com/eprotect-security-glossary/eprotect-security-glossary-metadata.json": "e9e166188a34fd8e548fab7e8db6dfffcae6815ed2bdf772d4774104b4823f91",
    "reference/zscaler.com/security-terms-glossary/security-terms-glossary-metadata.json": "c7e7efed0f2bb18bfce6c283395e341b10b492f10992071b35e3d361b59ec2be",
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
        elif restricted_hit(path) is None and not in_type_root(path):
            problems.append(f"FINGERPRINTS: {path} is neither under a restricted publisher domain nor in a SecID "
                            "type root")
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


_SIDECAR_SUFFIX = "-file-metadata.json"


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9.]+", "-", s.lower()).strip("-")


def canonical_metadata_names(dir_path: str) -> set[str]:
    """The names a directory's own edition metadata may have: `<dir>-metadata.json`, or
    `<parent>-<dir>-metadata.json` below a namespace, each also in lower-case slug form
    (`Generative AI Controls Framework Whitepaper` -> `generative-ai-controls-...`).
    Recognised BEFORE any sidecar rule: an edition directory named `x-file` has the
    edition metadata `x-file-metadata.json`, never a sidecar for a file `x`."""
    p = PurePosixPath(dir_path)
    names = {f"{p.name}-metadata.json", f"{_slug(p.name)}-metadata.json"}
    if len(p.parts) >= 3:
        names |= {f"{p.parent.name}-{p.name}-metadata.json", f"{_slug(p.parent.name)}-{_slug(p.name)}-metadata.json"}
    return names


def in_type_root(rel: str) -> bool:
    parts = PurePosixPath(rel).parts
    return len(parts) >= 2 and parts[0] in SECID_TYPES


def is_edition_metadata(rel: str) -> bool:
    p = PurePosixPath(rel)
    return (in_type_root(rel) and len(p.parent.parts) >= 2
            and p.name in canonical_metadata_names(p.parent.as_posix()))


def is_sidecar(rel: str) -> bool:
    name = PurePosixPath(rel).name
    return (in_type_root(rel) and not is_edition_metadata(rel) and name.endswith(_SIDECAR_SUFFIX)
            and len(name) > len(_SIDECAR_SUFFIX))


def sidecar_target(rel: str) -> str:
    p = PurePosixPath(rel)
    return (p.parent / p.name[:-len(_SIDECAR_SUFFIX)]).as_posix()


def governance(files: list[str]) -> tuple[dict[str, list[str]], dict[str, list[str]], list[str]]:
    """(metas, governed, ungoverned). metas maps each directory to its canonical edition
    metadata files. governed maps those directories to every other tracked file under a
    type root whose nearest directory with edition metadata (itself or an ancestor, at
    least `<type>/<namespace>`) is that directory: content, READMEs, sidecars and stray
    metadata alike. ungoverned lists the type-root files no edition metadata governs."""
    metas: dict[str, list[str]] = defaultdict(list)
    for f in files:
        if is_edition_metadata(f):
            metas[PurePosixPath(f).parent.as_posix()].append(f)
    governed: dict[str, list[str]] = defaultdict(list)
    ungoverned: list[str] = []
    for f in files:
        if not in_type_root(f) or is_edition_metadata(f):
            continue
        cur = PurePosixPath(f).parent
        while len(cur.parts) >= 2:
            if cur.as_posix() in metas:
                governed[cur.as_posix()].append(f)
                break
            cur = cur.parent
        else:
            ungoverned.append(f)
    return dict(metas), dict(governed), ungoverned


def is_content(rel: str, meta_dir: str) -> bool:
    """Everything a record governs is content except one README.md directly beside it.
    Sidecars and stray metadata count as content."""
    p = PurePosixPath(rel)
    return not (p.name == "README.md" and p.parent.as_posix() == meta_dir)


def content_by_metadata(files: list[str]) -> dict[str, int]:
    """Number of content files each directory's metadata governs (see is_content)."""
    metas, governed, _ = governance(files)
    return {d: sum(1 for f in governed.get(d, []) if is_content(f, d)) for d in metas}


def _load_metadata(root: str, rel: str):
    try:
        with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def report_unflagged(root: str, files: list[str]) -> list[tuple[str, int]]:
    """Directories with content files whose single metadata says publicly_redistributable
    is false (check 4a fails each)."""
    metas, _, _ = governance(files)
    out = []
    for d, n in content_by_metadata(files).items():
        if not n or len(metas[d]) != 1:
            continue
        data = _load_metadata(root, metas[d][0])
        lic = data.get("license") if data else None
        if isinstance(lic, dict) and lic.get("publicly_redistributable") is False:
            out.append((d, n))
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


def access_text(data: dict, readme_text: str = "") -> str:
    """The text check 4d searches for access-restriction wording: the record's string
    values, the tier_evidence note (its url, method and date excluded) and the README,
    with URLs and negated phrases ("no login", "no-login") removed."""
    def values(o):
        if isinstance(o, str):
            yield o
        elif isinstance(o, dict):
            for v in o.values():
                yield from values(v)
        elif isinstance(o, list):
            for v in o:
                yield from values(v)
    ev = data.get("tier_evidence")
    note = ev.get("note") if isinstance(ev, dict) and isinstance(ev.get("note"), str) else ""
    text = "\n".join(values({k: v for k, v in data.items() if k != "tier_evidence"})) + "\n" + note + "\n" + readme_text
    return _NEGATED_ACCESS_RE.sub(" ", _URL_IN_TEXT_RE.sub(" ", text))


def restriction_words(text: str) -> list[str]:
    return sorted({m.group(0).lower() for m in ACCESS_RESTRICTION_RE.finditer(text)})


def tier_field_problems(data: dict, today: _dt.date, n_content: int = 0, text: str = "") -> list[str]:
    """Check 4b/4d: the shape of access_tier and tier_evidence (empty list = valid).
    n_content is the number of non-sidecar content files the metadata governs; text is
    access_text() for it."""
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
        if not n_content:
            probs.append("method host-suffix needs acquired content in the directory: a publisher's domain says "
                         "nothing about how a document that was never acquired can be reached (fetch it instead)")
        words = restriction_words(text)
        if words:
            probs.append(f"method host-suffix cannot certify a source whose metadata, evidence note or README "
                         f"mentions {', '.join(repr(w) for w in words[:4])}: establish the tier from the document "
                         "itself")
    if method == "recorded" and tier in (1, 2):
        probs.append("method recorded may only say Tier 3 or 4: a record can keep a source private, never make it public")
    return probs


def _stub_cap_problems(root: str, meta: str, data: dict) -> list[str]:
    probs = []
    size = os.path.getsize(os.path.join(root, *meta.split("/")))
    if size > METADATA_MAX_BYTES:
        probs.append(f"restrictive metadata is {size} bytes, over the {METADATA_MAX_BYTES}-byte stub cap")
    longest = max((len(s) for s in _strings(data)), default=0)
    if longest > METADATA_MAX_STRING:
        probs.append(f"restrictive metadata holds a string of {longest} characters, over the "
                     f"{METADATA_MAX_STRING}-character stub cap")
    return probs


def _is_restrictive(data) -> bool:
    if not isinstance(data, dict):
        return True  # unreadable or ambiguous: assume the worst
    lic = data.get("license") if isinstance(data.get("license"), dict) else {}
    tier = data.get("access_tier")
    return lic.get("publicly_redistributable") is not True or (type(tier) is int and tier in (3, 4))


def _sidecar_check(root: str, rel: str, tracked: set[str]) -> tuple[list[str], bool]:
    """Check 4i: (problems, restrictive) for one `<file>-file-metadata.json` sidecar.
    A sidecar is restrictive when its `license` or `license_override` says
    publicly_redistributable false, or its access_tier is 3 or 4; a malformed one counts
    as restrictive. A sidecar never loosens its enclosing record."""
    target = sidecar_target(rel)
    tname = PurePosixPath(target).name
    probs: list[str] = []
    if target not in tracked and not tname.lower().endswith(UNTRACKED_ORIGINAL_SUFFIXES):
        probs.append(f"sidecar names {tname}, which is neither a tracked file in its directory nor a gitignored "
                     f"original ({', '.join(UNTRACKED_ORIGINAL_SUFFIXES)})")
    data = _load_metadata(root, rel)
    if data is None:
        return probs + ["sidecar is not a readable JSON object"], True
    restrictive = False
    if data.get("filename") is not None and data.get("filename") != tname:
        probs.append(f"sidecar filename {data.get('filename')!r} does not match the file it is named for ({tname})")
    for key in ("license", "license_override"):
        lic = data.get(key)
        if lic is None:
            continue
        if not isinstance(lic, dict):
            probs.append(f"sidecar {key} must be an object or null")
            restrictive = True
            continue
        if "publicly_redistributable" in lic:
            v = lic["publicly_redistributable"]
            if not isinstance(v, bool):
                probs.append(f"sidecar {key}.publicly_redistributable must be true or false, got {v!r}")
                restrictive = True
            elif v is False:
                restrictive = True
    if "access_tier" in data:
        tier = data["access_tier"]
        if type(tier) is not int or tier not in (1, 2, 3, 4):
            probs.append(f"sidecar access_tier must be the integer 1, 2, 3 or 4, got {tier!r}")
            restrictive = True
        elif tier in (3, 4):
            restrictive = True
    return probs, restrictive


def analyse_metadata(root: str, files: list[str], allowlist: list[dict], fingerprints: dict,
                     today: _dt.date | None = None) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Blocking checks 4 and 5. Returns ({path: [problems]}, {path: why it must be pinned})."""
    today = today or _dt.date.today()
    tracked = set(files)
    exceptions = {e["path"]: e for e in allowlist if e.get("kind") == "tier3-4-exception"}
    metas, governed, ungoverned = governance(files)
    loaded = {d: _load_metadata(root, ms[0]) for d, ms in metas.items() if len(ms) == 1}
    problems: dict[str, list[str]] = defaultdict(list)
    pins: dict[str, str] = {}

    # check 5 and 4h: where files may live
    for f in files:
        p = PurePosixPath(f)
        if in_type_root(f):
            if p.name.endswith("-metadata.json") and not is_edition_metadata(f) and not is_sidecar(f):
                names = " or ".join(sorted(canonical_metadata_names(p.parent.as_posix()))[:2])
                problems[f].append(f"is not its directory's canonical edition metadata ({names}); rename it, or name "
                                   "a per-file sidecar `<file>-file-metadata.json`")
        elif p.name.endswith("-metadata.json"):
            problems[f].append("metadata outside a SecID type root governs nothing and is not allowed")
        elif not (len(p.parts) == 1 and any(fnmatch.fnmatchcase(p.name, pat) for pat in ROOT_FILE_PATTERNS)) \
                and not f.startswith(INFRASTRUCTURE_PREFIXES):
            problems[f].append("tracked file outside the SecID type roots and outside the listed infrastructure "
                               f"paths ({', '.join(INFRASTRUCTURE_PREFIXES)} and root files {', '.join(ROOT_FILE_PATTERNS)})")
    for f in ungoverned:
        if f not in TYPE_ROOT_INFRASTRUCTURE:
            problems[f].append("no edition metadata governs this file: add the directory's canonical metadata "
                               "(<dir>-metadata.json) or, for CSA's own tooling, a reviewed TYPE_ROOT_INFRASTRUCTURE "
                               "entry")

    for d, ms in sorted(metas.items()):
        if len(ms) > 1:  # 4f: which record governs would be ambiguous
            names = ", ".join(sorted(PurePosixPath(m).name for m in ms))
            for m in ms:
                problems[m].append(f"{d}/ holds {len(ms)} edition metadata files ({names}); exactly one may govern "
                                   "a directory")
            continue
        meta, data = ms[0], loaded[d]
        if data is None:  # 4e
            problems[meta].append("not a readable JSON object, so nothing can confirm that the content it governs "
                                  "may be public")
            continue
        lic = data.get("license")
        public = lic.get("publicly_redistributable") if isinstance(lic, dict) else None
        if not isinstance(lic, dict):  # 4g
            problems[meta].append("license must be an object holding publicly_redistributable")
        elif not isinstance(public, bool):
            problems[meta].append(f"license.publicly_redistributable must be true or false, got {public!r}"
                                  if "publicly_redistributable" in lic else
                                  "license.publicly_redistributable is missing (it is required, true or false)")
        tier = data.get("access_tier")
        tier_ok = type(tier) is int and tier in (1, 2, 3, 4)
        gfiles = governed.get(d, [])
        content = [f for f in gfiles if is_content(f, d)]
        readme = f"{d}/README.md" if f"{d}/README.md" in gfiles else None
        readme_text = ""
        if readme:
            try:
                with open(os.path.join(root, *readme.split("/")), encoding="utf-8", errors="replace") as fh:
                    readme_text = fh.read(README_MAX_BYTES * 4)
            except OSError:
                pass
        real_content = [f for f in content if not is_sidecar(f)]
        problems[meta] += tier_field_problems(data, today, len(real_content), access_text(data, readme_text))

        entry = exceptions.get(d)
        excepted = (entry is not None and tier_ok and tier in (3, 4) and public is True
                    and data.get("secid") == entry["secid"])
        restrictive = public is not True or (tier_ok and tier in (3, 4))
        if restrictive:
            # 4j: not plainly public -> every file under this record is pinned to a reviewed SHA-256
            why = f"governed by a record that is not plainly public ({meta})"
            pins[meta] = why
            for f in gfiles:
                pins[f] = why
            # 4a/4c (second layer): only a capped stub, plus an exception's listed files
            problems[meta] += _stub_cap_problems(root, meta, data)
            if readme and os.path.getsize(os.path.join(root, *readme.split("/"))) > README_MAX_BYTES and not (
                    excepted and any(fnmatch.fnmatchcase("README.md", pat) for pat in entry["files"])):
                problems[meta].append(f"{readme} is over the {README_MAX_BYTES}-byte README cap for a restrictive "
                                      "record")
            bad = [f for f in content if not (
                excepted and PurePosixPath(f).parent.as_posix() == d
                and any(fnmatch.fnmatchcase(PurePosixPath(f).name, pat) for pat in entry["files"]))]
            if bad:
                shown = ", ".join(bad[:3]) + (" ..." if len(bad) > 3 else "")
                if public is not True:
                    why_bad = (f"{len(bad)} content files sit under this metadata while "
                               f"license.publicly_redistributable is {public!r}")
                elif entry is None or data.get("secid") != entry.get("secid"):
                    why_bad = (f"access_tier {tier} source with {len(bad)} content files and no tier3-4-exception "
                               "ALLOWLIST entry for this exact directory and SecID")
                else:
                    why_bad = (f"{len(bad)} files are not covered by the tier3-4-exception for {d} (only its listed "
                               "files, directly in that directory, are)")
                problems[meta].append(f"{why_bad}: {shown}. Find the source's tier: Tier 1/2 -> set "
                                      "publicly_redistributable true and record access_tier and tier_evidence; "
                                      "Tier 3/4 -> the content belongs in dataset-private-laws-regulations-standards "
                                      "unless Kurt grants an exception (ask first; do not move it on your own)")
        else:
            cur = PurePosixPath(d).parent  # 4f: a nested record may not loosen a restrictive one above it
            while len(cur.parts) >= 2:
                a = cur.as_posix()
                if a in metas:
                    if len(metas[a]) > 1 or _is_restrictive(loaded.get(a)):
                        problems[meta].append(f"says publicly redistributable, but the metadata of the enclosing "
                                              f"directory {a}/ is restrictive or ambiguous; a nested record may not "
                                              "loosen it")
                    break
                cur = cur.parent
        if tier_ok and tier in (1, 2) and public is not True:
            problems[meta].append(f"access_tier {tier} means the rule allows public hosting, so "
                                  f"license.publicly_redistributable must be true, got {public!r}")
        if tier_ok and tier in (3, 4) and not excepted and public is not False:
            problems[meta].append(f"access_tier {tier} needs license.publicly_redistributable false (no "
                                  f"tier3-4-exception ALLOWLIST entry names this directory and SecID), got {public!r}")

    # 4i: sidecars only ever restrict
    for f in files:
        if not is_sidecar(f):
            continue
        sprobs, restr = _sidecar_check(root, f, tracked)
        problems[f] += sprobs
        if restr:
            why = f"marked not publicly redistributable by its sidecar {f}"
            pins[f] = why
            target = sidecar_target(f)
            if target in tracked:
                pins[target] = why
                problems[f].append(f"marks {PurePosixPath(target).name} not publicly redistributable, but that file "
                                   "is tracked in this public repository; a file that may not be public belongs in "
                                   "dataset-private-laws-regulations-standards (ask first; do not move it on your own)")

    # 4j: every pinned file must match a reviewed fingerprint
    for f, why in sorted(pins.items()):
        if f not in tracked:
            continue
        fp = fingerprint_problem(root, f, fingerprints)
        if fp:
            problems[f].append(f"{why}, so it must match a reviewed SHA-256 in FINGERPRINTS. {fp}")
    return {k: v for k, v in problems.items() if v}, pins


def check_metadata_truth(root: str, files: list[str], allowlist: list[dict], fingerprints: dict | None = None,
                         today: _dt.date | None = None) -> dict[str, list[str]]:
    """Blocking checks 4 and 5. Returns {path: [problems]}."""
    return analyse_metadata(root, files, allowlist, FINGERPRINTS if fingerprints is None else fingerprints, today)[0]


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

    meta_problems, pins = analyse_metadata(root, files, allowlist, fingerprints, today=today)
    n_meta = sum(1 for f in files if is_edition_metadata(f))
    tiered = 0
    for f in files:
        if is_edition_metadata(f):
            data = _load_metadata(root, f)
            tiered += bool(data and "access_tier" in data)
    print("", file=out)
    print(f"Metadata truth: {n_meta} edition metadata files, {tiered} with access_tier; {len(pins)} files sit "
          "under a record or sidecar that is not plainly public and must match a reviewed fingerprint.", file=out)
    if meta_problems:
        status = 1
        print(f"FAIL: {len(meta_problems)} files break the metadata rules (governance, pinning, 4-tier "
              "consistency; see METADATA-SCHEMA.md, access_tier):", file=out)
        for meta, probs in meta_problems.items():
            print(f"  {meta}", file=out)
            for pr in probs:
                print(f"      {pr}", file=out)
                if in_actions:
                    print(f"::error file={meta},title=Metadata truth::{pr}", file=out)
    else:
        print("  PASS: every file is governed or listed infrastructure; everything under a record that is not "
              "plainly public is a pinned stub; every access_tier agrees with publicly_redistributable and carries "
              "valid evidence.", file=out)

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
    """FINGERPRINTS lines for every file that needs one: everything under a restricted
    publisher domain, and everything under a record or sidecar that is not plainly
    public (check 4j). Paste only what a reviewer has opened and checked."""
    files, _ = list_entries(root)
    _, pins = analyse_metadata(root, files, ALLOWLIST, FINGERPRINTS)
    for rel in sorted({f for f in files if restricted_hit(f)} | (set(pins) & set(files))):
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
        ("control/iso.org.example.com/b/b-metadata.json", meta("secid:control/iso.org.example.com/b", True), False,
         "look-alike domain metadata"),
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
    # In control/iso.org/27017/2015, other-metadata.json is not canonical: it is a stray
    # (check 4h fails it) and the directory's content counts against 27017-2015-metadata.json.
    expected_unflagged = {"control/example.org/doc/1", "control/iso.org/27002/2022", "control/aicpa.org/tsc/2017",
                          "control/cisecurity.org/cis-controls/v8", "control/iso.org/27701/2022",
                          "control/iso.org/27701/2019/scripts", "control/iso.org/27036/1", "control/iso.org/27017/2015"}

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
        ("fingerprint for a path in a type root (check 4j pins) is valid", {"control/nist.gov/a/a-metadata.json": "a" * 64}, True),
        ("fingerprint for a path outside type roots and restricted domains rejected", {"tools-resources/x/x.md": "a" * 64}, False),
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
        d = {"license": {"spdx": "X", "publicly_redistributable": public}}
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
    hs = ev(gov, "host-suffix", note="Classified from the URL host; not fetched.")
    big = "Clause 5.1 The organization shall determine external and internal issues. " * 100  # ~7.6 KB
    pub_meta = json.dumps({"secid": "secid:reference/x/doc", "license": {"publicly_redistributable": True}})
    # (name, metadata dict or raw text, extra files (path or (path, body)), must_fail[, flagged
    # metadata file if not doc-metadata.json])
    mcase = [
        ("legacy: content, true, no tier", tm(True), ["doc.md"], False),
        ("4a content while false", tm(False), ["doc.md"], True),
        ("4a content in a subdirectory, ancestor metadata says false", tm(False), ["sub/data.csv"], True),
        ("a -file-metadata.json sidecar under public metadata is fine", tm(True), ["doc.md", "doc.pdf-file-metadata.json"], False),
        ("stub (README only) while false", tm(False), ["README.md"], False),
        # --- Codex review of #155, finding 2: content accounting outside the restricted-domain list
        ("R155-2 restricted text in README.md beside false metadata (over the README cap)", tm(False),
         [("README.md", "# Standard\n\n" + big)], True),
        ("R155-2 restricted text in a -file-metadata.json sidecar under false metadata", tm(False),
         [("doc.pdf-file-metadata.json", json.dumps({"text": big}))], True),
        ("R155-2 an alphabetically earlier public metadata file beside the restrictive one", tm(False),
         [("a-metadata.json", pub_meta), "doc.md"], True),
        ("R155-2 README.md in a subdirectory under false metadata is content", tm(False), [("sub/README.md", "# x")], True),
        ("R155-2 public metadata nested below a false record may not loosen it", tm(False),
         [("sub/sub-metadata.json", pub_meta), "sub/doc.md"], True, "sub/sub-metadata.json"),
        ("R155-2 restrictive metadata over the stub size cap", tm(False, notes=[big[:2900]] * 6), [], True),
        ("R155-2 restrictive metadata with an over-long string", tm(False, description="z" * 3500), [], True),
        # --- finding 3: publicly_redistributable is a required boolean
        ("R155-3 publicly_redistributable missing (no tier, stub)", tm(None), [], True),
        ("R155-3 publicly_redistributable is the string 'false'", tm("false"), [], True),
        ("R155-3 publicly_redistributable is the string 'true', with content", tm("true"), ["doc.md"], True),
        ("R155-3 license is not an object", tm(True, license="CC-BY-4.0"), [], True),
        # --- check 4b-4d: tier fields
        ("Tier 1 host-suffix (go.jp), true, content", tm(True, 1, hs), ["doc.md"], False),
        ("Tier 1 host-suffix (.gov), true, content", tm(True, 1, ev("https://csrc.nist.gov/pubs/sp/800/53", "host-suffix")), ["doc.md"], False),
        ("Tier 1 host-suffix (itu.int, listed), true, content", tm(True, 1, ev("https://www.itu.int/x.pdf", "host-suffix")), ["doc.md"], False),
        ("R155-5 host-suffix on a non-governmental .int (ymca.int)", tm(True, 1, ev("https://www.ymca.int/x", "host-suffix")), ["doc.md"], True),
        ("4d host-suffix on a non-government host", tm(True, 1, ev("https://www.example.com/x", "host-suffix")), ["doc.md"], True),
        ("4d host-suffix on a look-alike (fakegov.uk)", tm(True, 1, ev("https://fakegov.uk/x", "host-suffix")), ["doc.md"], True),
        ("4d host-suffix on an open ccTLD (go.co)", tm(True, 1, ev("https://go.co/x", "host-suffix")), ["doc.md"], True),
        ("4d host-suffix claiming Tier 2", tm(True, 2, hs), ["doc.md"], True),
        # --- finding 1: host-suffix needs an acquired document with no access restriction noted
        ("R155-1 host-suffix on a stub with no acquired content", tm(True, 1, hs), ["README.md"], True),
        ("R155-1 host-suffix where only a sidecar exists", tm(True, 1, hs), ["doc.pdf-file-metadata.json"], True),
        ("R155-1 host-suffix whose notes say Members-only", tm(True, 1, hs, notes="Members-only."), ["doc.md"], True),
        ("R155-1 host-suffix whose README says awaiting a licensed copy", tm(True, 1, hs),
         ["doc.md", ("README.md", "# PESONet\n\nStub-only - awaiting CSA's licensed copy.\n")], True),
        ("R155-1 host-suffix whose licence notes mention a subscription", tm(True, 1, hs, license={
            "publicly_redistributable": True, "notes": "Requires a paid subscription."}), ["doc.md"], True),
        ("R155r2-P2-5 Codex: host-suffix whose own evidence note says members-only, paid subscription",
         tm(True, 1, ev("https://www.nist.gov/", "host-suffix",
                        note="Members-only document; requires a paid subscription.")), ["doc.md"], True),
        ("R155-1 restriction words inside a URL are ignored", tm(True, 1, hs, links={
            "source": "https://www.federalregister.gov/register/members-only"}), ["doc.md"], False),
        ("R155-1 negated wording ('no login required') is not a restriction", tm(True, 1, hs, notes=(
            "Public government page, no login required; published without registration.")), ["doc.md"], False),
        ("Tier 2 by fetch, true, content", tm(True, 2, ev()), ["doc.md"], False),
        ("Tier 2 by browser, true", tm(True, 2, ev(method="browser")), [], False),
        ("4c Tier 1 while false", tm(False, 1, ev()), [], True),
        ("4c Tier 2 with publicly_redistributable missing", tm(None, 2, ev()), [], True),
        ("4c Tier 3 while true, no exception", tm(True, 3, ev()), [], True),
        ("Tier 4 stub, false, recorded", tm(False, 4, ev(method="recorded", note="Program classification, not re-observed.")),
         ["README.md"], False),
        ("4c Tier 4 with content (and false)", tm(False, 4, ev()), ["doc.md"], True),
        # --- finding 4: an exception binds its exact directory, SecID and file list everywhere
        ("R155-4 Tier 3 with true and an exact exception: the listed file passes", tm(True, 3, ev()), ["approved.md"], False),
        ("R155-4 the exception does not admit an unlisted file", tm(True, 3, ev()), ["approved.md", "extra.md"], True),
        ("R155-4 the exception does not admit a nested file", tm(True, 3, ev()), ["approved.md", "nested/extra.md"], True),
        ("R155-4 the exception does not admit a listed file name in a subdirectory", tm(True, 3, ev()),
         ["approved.md", "nested/approved.md"], True),
        ("R155-4 the exception does not apply to metadata with another SecID",
         tm(True, 3, ev(), secid="secid:reference/elsewhere.example.org/doc"), ["approved.md"], True),
        ("R155-4 an exception for a sibling directory grants nothing", tm(True, 3, ev()), ["approved.md"], True),
        ("4d recorded claiming Tier 2", tm(True, 2, ev(method="recorded")), [], True),
        ("4b access_tier as a string", tm(True, "2", ev()), [], True),
        ("4b access_tier true (bool)", tm(True, True, ev()), [], True),
        ("4b access_tier 1.0 (float)", tm(True, 1.0, hs), ["doc.md"], True),
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
    for i, c in enumerate(mcase):
        name, data, extra, must_fail = c[:4]
        flagged = c[4] if len(c) > 4 else "doc-metadata.json"
        d = f"reference/case{i:02d}.example.org/doc"
        if isinstance(data, dict) and "secid" not in data:
            data = dict(data, secid=f"secid:{d}")
        extra = [x if isinstance(x, tuple) else (x, "{}" if x.endswith(".json") else "text") for x in extra]
        meta_cases.append((name, d, data, extra, must_fail, flagged))
    exc_dirs = [c[1] for c in meta_cases if c[0].startswith("R155-4") and "sibling" not in c[0]]
    sib_dir = next(c[1] for c in meta_cases if "sibling directory" in c[0])
    meta_allowlist = [dict(test_exception, path=d, secid=f"secid:{d}", files=["approved.md"]) for d in exc_dirs]
    pub = {"license": {"publicly_redistributable": True}}
    t4 = {"license": {"publicly_redistributable": False}, "access_tier": 4,
          "tier_evidence": ev(method="recorded", note="Program classification, not re-observed.")}
    chunk = "Requirement 7.4.2 Access to cardholder data shall be restricted by role. " * 28  # ~2 KB
    pesonet = {"secid": "secid:control/bsp.gov.ph/pesonet",
               "license": {"spdx": "LicenseRef-Publisher-Restricted", "publicly_redistributable": False,
                           "notes": "Members-only. Corrected 2026-11-14: not marked publicly redistributable."},
               "notes": "Authored 2026-05-14. Stub-only - awaiting CSA's licensed copy."}
    J = json.dumps
    # (name, {path: body}, must_fail, flagged path or None, unpinned paths, {path: reviewed body if stale})
    rcase = [
        ("R155r2-P1-2 Codex pair: an edition named restricted-file is an edition, not a sidecar",
         {"reference/nist.gov/restricted-file/restricted-file-metadata.json":
              J({"secid": "secid:reference/nist.gov/restricted-file", "license": {"publicly_redistributable": False}}),
          "reference/nist.gov/restricted-file/restricted-file.md": big},
         True, "reference/nist.gov/restricted-file/restricted-file-metadata.json", set(), {}),
        ("R155r2-P1-2 a public edition named public-file is recognised as an edition (passes with content)",
         {"reference/nist.gov/public-file/public-file-metadata.json":
              J({"secid": "secid:reference/nist.gov/public-file", "license": {"publicly_redistributable": True}}),
          "reference/nist.gov/public-file/public-file.md": "text"}, False, None, set(), {}),
        ("R155r2-P1-2 a file under a type root that no metadata governs fails",
         {"reference/nist.gov/loose/loose.md": big}, True, "reference/nist.gov/loose/loose.md", set(), {}),
        ("R155r2-P1-2 a listed TYPE_ROOT_INFRASTRUCTURE file passes ungoverned",
         {"regulation/us-state-regulations-overview.md": "# overview"}, False, None, set(), {}),
        ("R155r2-P1-2 metadata outside a type root fails",
         {"tools-resources/hidden/hidden-metadata.json": J({"license": {"publicly_redistributable": False}})},
         True, "tools-resources/hidden/hidden-metadata.json", set(), {}),
        ("R155r2-P1-2 a file outside the type roots and infrastructure paths fails",
         {"datasets/x/x.md": big}, True, "datasets/x/x.md", set(), {}),
        ("R155r2-P1-2 non-canonical metadata beside the canonical record fails",
         {"reference/casenc.example.org/doc/doc-metadata.json": J(pub),
          "reference/casenc.example.org/doc/other-metadata.json": J(pub)},
         True, "reference/casenc.example.org/doc/other-metadata.json", set(), {}),
        ("R155r2-P1-3 Tier 4 stub with a 4,000-byte README of restricted text, unpinned",
         {"reference/casereadme.example.org/doc/doc-metadata.json": J(t4),
          "reference/casereadme.example.org/doc/README.md": big[:4000]},
         True, "reference/casereadme.example.org/doc/README.md", {"reference/casereadme.example.org/doc/README.md"}, {}),
        ("R155r2-P1-3 Tier 4 stub whose metadata text array holds five 2,000-character strings, unpinned",
         {"reference/casetext.example.org/doc/doc-metadata.json": J(dict(t4, text=[chunk[:2000]] * 5))},
         True, "reference/casetext.example.org/doc/doc-metadata.json", {"reference/casetext.example.org/doc/doc-metadata.json"}, {}),
        ("R155r2-P1-3 restricted text chunked across canonical version directories, unpinned",
         {f"reference/casechunk.example.org/doc/v{i}/doc-v{i}-metadata.json":
              J(dict(t4, description=chunk[:2000])) for i in (1, 2, 3)},
         True, "reference/casechunk.example.org/doc/v2/doc-v2-metadata.json", "all", {}),
        ("R155r2-P1-3 a reviewed (pinned) restrictive stub passes",
         {"reference/casepinned.example.org/doc/doc-metadata.json": J(t4),
          "reference/casepinned.example.org/doc/README.md": "# Stub\n\nMetadata only."},
         False, None, set(), {}),
        ("R155r2-P1-3 a pinned stub's README edited after review fails",
         {"reference/casestale.example.org/doc/doc-metadata.json": J(t4),
          "reference/casestale.example.org/doc/README.md": "# Stub\n\n" + chunk[:3000]},
         True, "reference/casestale.example.org/doc/README.md", set(),
         {"reference/casestale.example.org/doc/README.md": "# Stub\n\nMetadata only."}),
        ("R155r2-P1-4 Codex: a sidecar marking doc.md not redistributable under public metadata",
         {"reference/nist.gov/doc/doc-metadata.json": J(pub), "reference/nist.gov/doc/doc.md": big,
          "reference/nist.gov/doc/doc.md-file-metadata.json": J({"license": {"publicly_redistributable": False}})},
         True, "reference/nist.gov/doc/doc.md-file-metadata.json", set(), {}),
        ("R155r2-P1-4 a sidecar saying true does not loosen a false record",
         {"reference/caseloosen.example.org/doc/doc-metadata.json": J({"license": {"publicly_redistributable": False}}),
          "reference/caseloosen.example.org/doc/doc.md": big,
          "reference/caseloosen.example.org/doc/doc.md-file-metadata.json": J({"license": {"publicly_redistributable": True}})},
         True, "reference/caseloosen.example.org/doc/doc-metadata.json", set(), {}),
        ("R155r2-P1-4 a restrictive sidecar for a gitignored original passes once pinned",
         {"reference/casepdf.example.org/doc/doc-metadata.json": J(pub), "reference/casepdf.example.org/doc/doc.md": "text",
          "reference/casepdf.example.org/doc/doc.pdf-file-metadata.json": J({"license_override": {"publicly_redistributable": False}})},
         False, None, set(), {}),
        ("R155r2-P1-4 the same sidecar unpinned fails",
         {"reference/casepdf2.example.org/doc/doc-metadata.json": J(pub), "reference/casepdf2.example.org/doc/doc.md": "text",
          "reference/casepdf2.example.org/doc/doc.pdf-file-metadata.json": J({"license_override": {"publicly_redistributable": False}})},
         True, "reference/casepdf2.example.org/doc/doc.pdf-file-metadata.json",
         {"reference/casepdf2.example.org/doc/doc.pdf-file-metadata.json"}, {}),
        ("R155r2-P1-4 a sidecar naming a file that does not exist fails",
         {"reference/casemissing.example.org/doc/doc-metadata.json": J(pub),
          "reference/casemissing.example.org/doc/gone.md-file-metadata.json": "{}"},
         True, "reference/casemissing.example.org/doc/gone.md-file-metadata.json", set(), {}),
        ("R155r2-P1-4 a sidecar whose filename field names another file fails",
         {"reference/casefn.example.org/doc/doc-metadata.json": J(pub), "reference/casefn.example.org/doc/doc.md": "text",
          "reference/casefn.example.org/doc/doc.md-file-metadata.json": J({"filename": "other.md"})},
         True, "reference/casefn.example.org/doc/doc.md-file-metadata.json", set(), {}),
        ("R155r2-P1-4 a sidecar that is not JSON fails",
         {"reference/casebadsc.example.org/doc/doc-metadata.json": J(pub), "reference/casebadsc.example.org/doc/doc.md": "text",
          "reference/casebadsc.example.org/doc/doc.md-file-metadata.json": "{not json"},
         True, "reference/casebadsc.example.org/doc/doc.md-file-metadata.json", set(), {}),
        ("R155r2-P1-1 PESONet as corrected (false), with content added: fails",
         {"control/bsp.gov.ph/pesonet/pesonet-metadata.json": J(pesonet),
          "control/bsp.gov.ph/pesonet/README.md": "# PESONet\n\n## License and access\n\nMembers-only.\n",
          "control/bsp.gov.ph/pesonet/pesonet.md": "Members-only operating rules. " + big},
         True, "control/bsp.gov.ph/pesonet/pesonet-metadata.json", {"control/bsp.gov.ph/pesonet/pesonet.md"}, {}),
    ]
    meta_allowlist.append(dict(test_exception, path=sib_dir + "-sibling", secid=f"secid:{sib_dir}-sibling",
                               files=["approved.md"]))
    return dict(cases=cases, fp_override=fp_override, expected_unflagged=expected_unflagged, al_cases=al_cases,
                fp_cases=fp_cases, run_cases=run_cases, allowlist=allowlist, test_exception=test_exception,
                bogus=bogus, meta_cases=meta_cases, meta_allowlist=meta_allowlist, raw_cases=rcase)


def self_test() -> int:
    t = _self_test_data()
    cases, allowlist = t["cases"], t["allowlist"]
    failures: list[str] = []

    if shutil.which("git") is None:
        print("SELF-TEST FAILED: git is required (the symlink check reads git file modes).")
        return 1

    fingerprints = {}
    for rel, body, _, _ in cases:
        if restricted_hit(rel) is None and not in_type_root(rel):
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

    # check 4: metadata truth, in its own tree. Every fixture file is pinned (treated as
    # reviewed) unless a raw case says otherwise, so each case fails for its own reason.
    with tempfile.TemporaryDirectory(prefix="tier-gate-selftest-meta-") as tmp:
        written: dict[str, str] = {}
        for _, d, data, extra, _, _ in t["meta_cases"]:
            written[f"{d}/doc-metadata.json"] = data if isinstance(data, str) else json.dumps(data)
            for rel, body in extra:
                written[f"{d}/{rel}"] = body
        unpinned: set[str] = set()
        reviewed: dict[str, str] = {}
        for _, rfiles, _, _, rel_unpinned, stale in t["raw_cases"]:
            written.update(rfiles)
            unpinned |= set(rfiles) if rel_unpinned == "all" else rel_unpinned
            reviewed.update(stale)
        for rel, body in written.items():
            path = os.path.join(tmp, *rel.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        fps = {rel: hashlib.sha256(reviewed.get(rel, body).encode("utf-8")).hexdigest()
               for rel, body in written.items()
               if rel not in unpinned and (in_type_root(rel) or restricted_hit(rel))}
        files, _ = list_entries(tmp, use_git=False)
        flagged = check_metadata_truth(tmp, files, t["meta_allowlist"], fingerprints=fps, today=FROZEN_TODAY)
        for name, d, _, _, must_fail, which in t["meta_cases"]:
            hit = f"{d}/{which}" in flagged
            if must_fail and not hit:
                failures.append(f"metadata truth: not caught: {name}")
            if not must_fail and any(k.startswith(d + "/") for k in flagged):
                failures.append(f"metadata truth: false positive: {name}: "
                                f"{[v for k, v in flagged.items() if k.startswith(d + '/')]}")
        for name, rfiles, must_fail, which, _, _ in t["raw_cases"]:
            dirs = {PurePosixPath(r).parent.as_posix() for r in rfiles}
            mine = [k for k in flagged if k in rfiles or PurePosixPath(k).parent.as_posix() in dirs]
            if must_fail and which not in flagged:
                failures.append(f"metadata truth: not caught: {name} (expected {which} flagged; got {mine})")
            if not must_fail and mine:
                failures.append(f"metadata truth: false positive: {name}: {[flagged[k] for k in mine]}")
        sink = open(os.devnull, "w", encoding="utf-8")
        try:
            if run(tmp, use_git=False, out=sink, allowlist=t["meta_allowlist"], fingerprints=fps,
                   today=FROZEN_TODAY) != 1:
                failures.append("4 run() did not exit 1 on the metadata-truth fixtures")
            for _, d, _, _, must_fail, _ in t["meta_cases"]:
                if must_fail:
                    shutil.rmtree(os.path.join(tmp, *d.split("/")))
            for _, rfiles, must_fail, _, _, _ in t["raw_cases"]:
                if must_fail:
                    for rel in rfiles:
                        os.remove(os.path.join(tmp, *rel.split("/")))
            if run(tmp, use_git=False, out=sink, allowlist=t["meta_allowlist"], fingerprints=fps,
                   today=FROZEN_TODAY) != 0:
                left = check_metadata_truth(tmp, list_entries(tmp, use_git=False)[0], t["meta_allowlist"],
                                            fingerprints=fps, today=FROZEN_TODAY)
                failures.append(f"4 run() did not exit 0 once the must-fail metadata-truth fixtures were removed: {left}")
        finally:
            sink.close()

    n = (len(cases) + len(t["al_cases"]) + len(t["fp_cases"]) + len(t["run_cases"]) + len(t["meta_cases"])
         + len(t["raw_cases"]))
    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Self-test passed ({n} cases: {len(cases)} fixture files, {sum(1 for c in cases if c[2])} of which must "
          f"fail; {len(t['al_cases'])} allowlist validations; {len(t['fp_cases'])} fingerprint validations; "
          f"{len(t['run_cases'])} run-level checks; {len(t['meta_cases'])} metadata-truth fixtures, "
          f"{sum(1 for c in t['meta_cases'] if c[4])} of which must fail; {len(t['raw_cases'])} path-level cases, "
          f"{sum(1 for c in t['raw_cases'] if c[2])} of which must fail).")
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
    for name, _, _, _, must_fail, _ in t["meta_cases"]:
        print(f"  [metadata truth {'must fail' if must_fail else 'must pass'}] {name}")
    for name, _, must_fail, _, _, _ in t["raw_cases"]:
        print(f"  [path level {'must fail' if must_fail else 'must pass'}] {name}")
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
