"""Test support: the CWE editions held here and their git-ignored XML zips.

Each edition's original, ``cwec_v<version>.xml.zip``, is git-ignored: it is kept
in S3 at the same path and pinned by the committed sidecar
``cwec_v<version>.xml.zip-file-metadata.json``. In a clean clone or in CI the zips
are absent, so every test that reads one skips and says which zip to fetch. Set
``CWE_REQUIRE_ZIPS=1`` to turn those skips into failures, for a gate that has
fetched the zips and must not pass by skipping.
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

CWE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = CWE_DIR.parents[2]
SIDECAR = "cwec_v{v}.xml.zip-file-metadata.json"

# Catalog facts per edition, measured from MITRE's XML (the spec's Input table).
# Adding an edition folder without an entry here fails the tests that compare counts.
EXPECTED = {
    "4.19.1": {"weaknesses": 969, "deprecated": 25, "groups": 420, "views": 58,
               "references": 1012, "schema_major": 7},
    "4.20": {"weaknesses": 969, "deprecated": 25, "groups": 422, "views": 59,
             "references": 1026, "schema_major": 7},
    "4.21": {"weaknesses": 984, "deprecated": 28, "groups": 431, "views": 62,
             "references": 1081, "schema_major": 7},
    "5.0": {"weaknesses": 984, "deprecated": 28, "groups": 431, "views": 62,
            "references": 1081, "schema_major": 8},
}


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", version))


def editions() -> list[str]:
    """Every edition folder under weakness/mitre.org/cwe/ that has a zip sidecar,
    in version order (whether or not its zip is present)."""
    return sorted(
        (p.name for p in CWE_DIR.iterdir()
         if p.is_dir() and (p / SIDECAR.format(v=p.name)).is_file()),
        key=_version_key,
    )


def zip_path(version: str) -> Path:
    return CWE_DIR / version / f"cwec_v{version}.xml.zip"


def present(version: str) -> bool:
    return zip_path(version).is_file()


def zips_required() -> bool:
    return os.environ.get("CWE_REQUIRE_ZIPS") == "1"


def missing_reason(version: str) -> str | None:
    """Why the edition's zip cannot be read, or None when it is present."""
    if present(version):
        return None
    rel = zip_path(version).relative_to(REPO_ROOT).as_posix()
    return (
        f"{rel} is absent (a git-ignored original): fetch it per its sidecar "
        f"{SIDECAR.format(v=version)} (from S3 at the same path, or its retrieved_from "
        "URL; the sha256 must match)"
    )


def require(*versions: str) -> None:
    """Skip the running test when any of these editions' zips is absent, or fail it
    when CWE_REQUIRE_ZIPS=1. Call it from a test method, setUp or a subTest block
    (an exception in setUpClass or setUpModule would be an error, not a failure)."""
    reasons = [r for r in map(missing_reason, versions) if r]
    if not reasons:
        return
    message = "; ".join(reasons)
    if zips_required():
        raise AssertionError(f"CWE_REQUIRE_ZIPS=1 and {message}")
    raise unittest.SkipTest(message)
