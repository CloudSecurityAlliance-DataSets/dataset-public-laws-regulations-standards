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

What it checks
--------------
1. BLOCKING. A path segment that names a Tier 3 or Tier 4 publisher domain (see
   RESTRICTED_DOMAINS; subdomains match too, so `standards.iso.org` counts as
   `iso.org`) may hold only stub files: `README.md`, `<name>-metadata.json` and
   `<file>-file-metadata.json`. Any other file below it fails the check, unless
   (a) the edition's directory metadata carries a valid `public_exception` object
       recording an explicit, documented exception from Kurt:
           "public_exception": {
             "approved_by": "...",          # who granted it
             "date": "YYYY-MM-DD",          # when
             "reference": "https://...",    # issue/ADR that records it
             "reason": "..."                # the solid reasons the rule asks for
           }
       The edition's metadata is the nearest `*-metadata.json` (not a per-file
       sidecar) at or above the file, up to the publisher directory; or
   (b) the edition is listed in OPEN_SOURCES_UNDER_RESTRICTED_DOMAINS: a source
       that is itself Tier 1/2 (public web, no login) although its publisher's
       standards are gated. Each entry carries its evidence and changes only by
       reviewed PR to this file.
2. NON-BLOCKING report. Every directory that holds content files while its metadata
   says `license.publicly_redistributable: false` is printed. That flag is not yet
   reliable across the repository; once the metadata backfill is done, this report
   can become blocking.

Files come from `git ls-files` (tracked files only), so gitignored local source PDFs
do not count. Outside a git work tree the script walks the filesystem instead.

Usage:
    python3 -I tools-resources/utils/check_tier_restrictions.py [--repo PATH]
    python3 -I tools-resources/utils/check_tier_restrictions.py --self-test

Exit status: 0 pass, 1 violations found (or self-test failure), 2 usage error.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
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

# Editions under a restricted publisher domain whose own source is public web with no
# login (Tier 1/2), so the tier rule does not restrict them. Keys are repo-relative
# directory paths. These are classifications, not exceptions: an exception to the
# rule for Tier 3/4 content goes in the edition's metadata as `public_exception`.
OPEN_SOURCES_UNDER_RESTRICTED_DOMAINS: dict[str, dict[str, str]] = {
    "reference/cisecurity.org/oval": {
        "tier": "Tier 2",
        "basis": "The OVAL Repository README and docs, published openly on GitHub with no login.",
        "evidence": "https://github.com/CISecurity/OVALRepo",
    },
}

EXCEPTION_FIELDS = ("approved_by", "date", "reference", "reason")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ----------------------------------------------------------------------------- helpers
def is_stub_file(name: str) -> bool:
    """README.md, directory metadata and per-file metadata sidecars are stub files."""
    return name == "README.md" or name.endswith("-metadata.json")


def is_dir_metadata(name: str) -> bool:
    return name.endswith("-metadata.json") and not name.endswith("-file-metadata.json")


def restricted_domain(segment: str) -> str | None:
    """Return the restricted domain a path segment names (exact or subdomain), or None."""
    seg = segment.lower()
    for domain in RESTRICTED_DOMAINS:
        if seg == domain or seg.endswith("." + domain):
            return domain
    return None


def list_files(root: str, use_git: bool | None = None) -> list[str]:
    """Repo-relative POSIX paths of the files to check (tracked files when in git)."""
    if use_git is None:
        try:
            out = subprocess.run(
                ["git", "-C", root, "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=60, check=False,
            )
            use_git = out.returncode == 0 and os.path.realpath(out.stdout.strip()) == os.path.realpath(root)
        except (OSError, subprocess.SubprocessError):
            use_git = False
    if use_git:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-z"],
            capture_output=True, timeout=300, check=True,
        )
        files = [p for p in out.stdout.decode("utf-8").split("\0") if p]
        # A tracked file deleted in the working tree but not yet staged is skipped.
        return sorted(p for p in files if os.path.isfile(os.path.join(root, p)))
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            found.append(PurePosixPath(*rel.split(os.sep)).as_posix())
    return sorted(found)


def load_json(root: str, rel: str) -> tuple[dict | None, str | None]:
    try:
        with open(os.path.join(root, rel), encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, f"{rel}: unreadable metadata ({exc})"
    if not isinstance(data, dict):
        return None, f"{rel}: metadata is not a JSON object"
    return data, None


def validate_exception(obj) -> list[str]:
    """Return the problems with a public_exception object (empty list = valid)."""
    if not isinstance(obj, dict):
        return ["public_exception must be an object"]
    problems = []
    for field in EXCEPTION_FIELDS:
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"public_exception.{field} is missing or empty")
    date = obj.get("date")
    if isinstance(date, str) and date.strip():
        if not _DATE_RE.match(date):
            problems.append("public_exception.date must be YYYY-MM-DD")
        else:
            try:
                _dt.date.fromisoformat(date)
            except ValueError:
                problems.append("public_exception.date is not a real date")
    ref = obj.get("reference")
    if isinstance(ref, str) and ref.strip() and not ref.startswith("https://"):
        problems.append("public_exception.reference must be an https:// URL")
    return problems


class Index:
    """Directory -> filenames, built from the file list (so only checked files count)."""

    def __init__(self, files: list[str]):
        self.by_dir: dict[str, list[str]] = defaultdict(list)
        for f in files:
            p = PurePosixPath(f)
            self.by_dir[p.parent.as_posix()].append(p.name)

    def edition_metadata(self, file_dir: str, stop_dir: str) -> tuple[str | None, str | None]:
        """Nearest directory-metadata file at or above file_dir, not above stop_dir.

        Returns (metadata_path, problem). Several candidate metadata files in one
        directory are ambiguous unless one is named after the directory.
        """
        cur = PurePosixPath(file_dir)
        stop = PurePosixPath(stop_dir)
        while True:
            names = sorted(n for n in self.by_dir.get(cur.as_posix(), []) if is_dir_metadata(n))
            if names:
                if len(names) == 1:
                    return (cur / names[0]).as_posix(), None
                preferred = [n for n in names
                             if n in (f"{cur.name}-metadata.json", f"{cur.parent.name}-{cur.name}-metadata.json")]
                if len(preferred) == 1:
                    return (cur / preferred[0]).as_posix(), None
                return None, f"{cur.as_posix()}/: several directory metadata files ({', '.join(names)})"
            if cur == stop or cur == PurePosixPath(".") or cur == cur.parent:
                return None, None
            cur = cur.parent


# ----------------------------------------------------------------------------- checks
def check_restricted(root: str, files: list[str]) -> tuple[dict, list[str]]:
    """Blocking check. Returns ({edition_dir: {domain, files, reasons}}, notes)."""
    index = Index(files)
    violations: dict[str, dict] = {}
    allowed_notes: dict[str, str] = {}
    meta_cache: dict[str, tuple[dict | None, str | None]] = {}

    for rel in files:
        parts = PurePosixPath(rel).parts
        if len(parts) < 2:
            continue
        hit = None
        for i, seg in enumerate(parts[:-1]):
            dom = restricted_domain(seg)
            if dom:
                hit = (i, dom)
                break
        if hit is None or is_stub_file(parts[-1]):
            continue
        i, dom = hit
        publisher_dir = PurePosixPath(*parts[: i + 1]).as_posix()
        file_dir = PurePosixPath(rel).parent.as_posix()

        open_key = next((k for k in OPEN_SOURCES_UNDER_RESTRICTED_DOMAINS
                         if rel.startswith(k.rstrip("/") + "/")), None)
        if open_key:
            entry = OPEN_SOURCES_UNDER_RESTRICTED_DOMAINS[open_key]
            allowed_notes[open_key] = f"{entry['tier']} source under a restricted publisher: {entry['evidence']}"
            continue

        meta_path, meta_problem = index.edition_metadata(file_dir, publisher_dir)
        reason = None
        if meta_problem:
            reason = meta_problem
        elif meta_path is None:
            reason = "no edition metadata, so no public_exception"
        else:
            if meta_path not in meta_cache:
                meta_cache[meta_path] = load_json(root, meta_path)
            data, err = meta_cache[meta_path]
            if err:
                reason = err
            elif "public_exception" not in data:
                reason = f"{meta_path} has no public_exception"
            else:
                problems = validate_exception(data["public_exception"])
                if problems:
                    reason = f"{meta_path}: invalid public_exception ({'; '.join(problems)})"
                else:
                    allowed_notes[PurePosixPath(meta_path).parent.as_posix()] = (
                        "public_exception approved by {approved_by} on {date} ({reference})".format(
                            **data["public_exception"]))
                    continue

        edition = PurePosixPath(meta_path).parent.as_posix() if meta_path else file_dir
        v = violations.setdefault(edition, {"domain": dom, "files": [], "reasons": set()})
        v["files"].append(rel)
        v["reasons"].add(reason)

    notes = [f"allowed: {k}/ ({msg})" for k, msg in sorted(allowed_notes.items())]
    return violations, notes


def report_unflagged(root: str, files: list[str]) -> list[tuple[str, int]]:
    """Non-blocking: edition dirs with content files whose metadata says
    license.publicly_redistributable is false."""
    index = Index(files)
    counts: dict[str, int] = defaultdict(int)
    cache: dict[str, bool] = {}
    for rel in files:
        parts = PurePosixPath(rel).parts
        if len(parts) < 3 or is_stub_file(parts[-1]):
            continue
        type_root = parts[0]
        if type_root not in {"control", "regulation", "weakness", "ttp", "methodology", "reference",
                             "advisory", "capability", "disclosure", "entity"}:
            continue
        meta_path, _ = index.edition_metadata(PurePosixPath(rel).parent.as_posix(), type_root)
        if not meta_path:
            continue
        if meta_path not in cache:
            data, err = load_json(root, meta_path)
            lic = data.get("license") if data else None
            cache[meta_path] = bool(isinstance(lic, dict) and lic.get("publicly_redistributable") is False)
        if cache[meta_path]:
            counts[PurePosixPath(meta_path).parent.as_posix()] += 1
    return sorted(counts.items())


# ----------------------------------------------------------------------------- output
def run(root: str, use_git: bool | None = None, out=sys.stdout) -> int:
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    files = list_files(root, use_git)
    violations, notes = check_restricted(root, files)
    unflagged = report_unflagged(root, files)

    print(f"Tier-restriction gate: checked {len(files)} files against "
          f"{len(RESTRICTED_DOMAINS)} Tier 3/4 publisher domains.", file=out)
    for n in notes:
        print(f"  {n}", file=out)

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
        print("PASS: no restricted-publisher content beyond metadata/README stubs.", file=out)
        return 0
    total = sum(len(v["files"]) for v in violations.values())
    print(f"FAIL: {total} content files in {len(violations)} editions under Tier 3/4 publisher domains.",
          file=out)
    print("Only README.md and *-metadata.json may live under these domains unless the edition's metadata "
          "carries a public_exception {approved_by, date, reference, reason}. Full text belongs in "
          "dataset-private-laws-regulations-standards.", file=out)
    for edition, v in sorted(violations.items()):
        print(f"  {edition}/  [{v['domain']}: {RESTRICTED_DOMAINS[v['domain']]}]  "
              f"{len(v['files'])} files", file=out)
        for r in sorted(v["reasons"]):
            print(f"      reason: {r}", file=out)
        for f in v["files"][:5]:
            print(f"      {f}", file=out)
        if len(v["files"]) > 5:
            print(f"      ... and {len(v['files']) - 5} more", file=out)
        if in_actions:
            print(f"::error title=Tier-restricted content::{edition}/ holds {len(v['files'])} content files "
                  f"under {v['domain']} ({RESTRICTED_DOMAINS[v['domain']]}) with no valid public_exception.",
                  file=out)
    return 1


# ----------------------------------------------------------------------------- self-test
def self_test() -> int:
    valid_exc = {"approved_by": "Approver", "date": "2026-11-20",
                 "reference": "https://example.invalid/issues/1", "reason": "Documented reasons."}

    def meta(public=True, exception=None):
        d = {"secid": "secid:x", "license": {"spdx": "X", "publicly_redistributable": public}}
        if exception is not None:
            d["public_exception"] = exception
        return json.dumps(d)

    fixtures = {
        # stubs under a restricted domain: allowed
        "control/iso.org/27001/2022/27001-2022-metadata.json": meta(False),
        "control/iso.org/27001/2022/README.md": "# stub",
        "control/iso.org/27001/2022/27001.pdf-file-metadata.json": "{}",
        "control/iso.org/README.md": "# namespace",
        # content without exception: violation
        "control/iso.org/27002/2022/27002-2022-metadata.json": meta(False),
        "control/iso.org/27002/2022/27002-2022.md": "text",
        # content directly in the namespace dir: violation
        "control/iso.org/stray.csv": "a,b",
        # subdomain counts; no metadata at all: violation
        "control/standards.iso.org/x/1/x-1.md": "text",
        # upper-case namespace still matches: violation
        "reference/ISO.ORG/vocab/vocab.md": "text",
        # look-alikes do not match: allowed
        "control/notiso.org/a/1/a-1-metadata.json": meta(True),
        "control/notiso.org/a/1/a-1.md": "text",
        "control/iso.org.example.com/b/b.md": "text",
        # valid exception, including nested subdir: allowed
        "control/cisecurity.org/cis-controls/v8/v8-metadata.json": meta(False, valid_exc),
        "control/cisecurity.org/cis-controls/v8/cis-controls-v8.csv": "a,b",
        "control/cisecurity.org/cis-controls/v8/scripts/parse_cis.py": "print()",
        # malformed exception (no reference, bad date): violation
        "control/cisecurity.org/cis-controls/v7/v7-metadata.json":
            meta(False, {"approved_by": "x", "date": "2026-13-40", "reason": "r"}),
        "control/cisecurity.org/cis-controls/v7/cis-controls-v7.csv": "a,b",
        # exception must be an object: violation
        "control/aicpa.org/tsc/2017/tsc-2017-metadata.json": meta(False, "yes"),
        "control/aicpa.org/tsc/2017/tsc-2017.md": "text",
        # unreadable metadata: violation
        "control/hitrustalliance.net/csf/v11/csf-v11-metadata.json": "{not json",
        "control/hitrustalliance.net/csf/v11/csf-v11.md": "text",
        # listed open source under a restricted domain: allowed
        "reference/cisecurity.org/oval/oval-metadata.json": meta(True),
        "reference/cisecurity.org/oval/oval.md": "text",
        # non-blocking report: content + publicly_redistributable false
        "control/example.org/doc/1/doc-1-metadata.json": meta(False),
        "control/example.org/doc/1/doc-1.md": "text",
        "control/example.org/doc/2/doc-2-metadata.json": meta(True),
        "control/example.org/doc/2/doc-2.md": "text",
        "control/example.org/stub/stub-metadata.json": meta(False),
        "control/example.org/stub/README.md": "# stub",
        # outside type roots, restricted segment still blocks
        "tools-resources/working/pcisecuritystandards.org/pci.md": "text",
    }
    expected_violations = {
        "control/iso.org/27002/2022",
        "control/iso.org",
        "control/standards.iso.org/x/1",
        "reference/ISO.ORG/vocab",
        "control/cisecurity.org/cis-controls/v7",
        "control/aicpa.org/tsc/2017",
        "control/hitrustalliance.net/csf/v11",
        "tools-resources/working/pcisecuritystandards.org",
    }
    expected_unflagged = {
        "control/example.org/doc/1",
        "control/iso.org/27002/2022",
        "control/cisecurity.org/cis-controls/v8",
        "control/cisecurity.org/cis-controls/v7",
        "control/aicpa.org/tsc/2017",
    }

    failures = []
    with tempfile.TemporaryDirectory(prefix="tier-gate-selftest-") as tmp:
        for rel, body in fixtures.items():
            path = os.path.join(tmp, *rel.split("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        files = list_files(tmp, use_git=False)
        violations, notes = check_restricted(tmp, files)
        got = set(violations)
        if got != expected_violations:
            failures.append(f"violations: missing {sorted(expected_violations - got)}, "
                            f"unexpected {sorted(got - expected_violations)}")
        v7 = violations.get("control/cisecurity.org/cis-controls/v7", {}).get("reasons", set())
        if not any("reference" in r and "real date" in r for r in v7):
            failures.append(f"malformed exception reasons not reported precisely: {sorted(v7)}")
        if not any("cisecurity.org/oval" in n for n in notes):
            failures.append("open-source allowance for reference/cisecurity.org/oval not reported")
        if not any("cis-controls/v8" in n and "public_exception" in n for n in notes):
            failures.append("valid public_exception for cis-controls/v8 not reported")
        unflagged = {d for d, _ in report_unflagged(tmp, files)}
        if unflagged != expected_unflagged:
            failures.append(f"non-blocking report: missing {sorted(expected_unflagged - unflagged)}, "
                            f"unexpected {sorted(unflagged - expected_unflagged)}")
        sink = open(os.devnull, "w", encoding="utf-8")
        try:
            if run(tmp, use_git=False, out=sink) != 1:
                failures.append("run() did not exit 1 on violations")
            doomed = {f for f in files for d in expected_violations
                      if f.startswith(d + "/") and not is_stub_file(f.rsplit("/", 1)[-1])}
            for f in doomed:
                os.remove(os.path.join(tmp, *f.split("/")))
            if run(tmp, use_git=False, out=sink) != 0:
                failures.append("run() did not exit 0 once violating content was removed")
        finally:
            sink.close()

    for name, ok in (("validate_exception(valid)", validate_exception(valid_exc) == []),
                     ("validate_exception(http)", validate_exception(dict(valid_exc, reference="http://x")) != []),
                     ("validate_exception(blank)", validate_exception(dict(valid_exc, approved_by=" ")) != [])):
        if not ok:
            failures.append(f"{name} gave the wrong answer")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"Self-test passed ({len(fixtures)} fixture files, {len(expected_violations)} expected violations).")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=None, help="Repository root (default: two levels above this script)")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixtures and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    root = args.repo or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
