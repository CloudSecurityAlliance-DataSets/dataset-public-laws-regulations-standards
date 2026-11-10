#!/usr/bin/env python3
"""Extract the Cloudflare Ssl Glossary into CSV/JSON.

Source:        https://developers.cloudflare.com/ssl/keyless-ssl/glossary/
Markdown alt:  https://developers.cloudflare.com/ssl/keyless-ssl/glossary/index.md
License:       LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only).

Thin wrapper around tools-resources/utils/cloudflare_glossary.py.
The shared module auto-detects the source's parser shape (markdown table vs.
'## Term' headings) and emits the canonical four-file output set.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools-resources" / "utils"))
from cloudflare_glossary import run  # noqa: E402

SOURCE_URL = "https://developers.cloudflare.com/ssl/keyless-ssl/glossary/"
MD_URL = "https://developers.cloudflare.com/ssl/keyless-ssl/glossary/index.md"
PREFIX = "ssl-glossary"
TITLE = "Ssl Glossary"

if __name__ == "__main__":
    n = run(SOURCE_URL, MD_URL, Path(__file__).parent, PREFIX, TITLE)
    print(f"Extracted {n} terms")
