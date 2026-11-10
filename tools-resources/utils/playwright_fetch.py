#!/usr/bin/env python3
"""Open a URL in a visible Playwright/Chromium window and save the rendered DOM.

Two modes:

  --pause     Pause for the user to clear an anti-bot challenge by hand.
              The script polls for a sentinel file (default /tmp/playwright-go);
              the user runs `touch /tmp/playwright-go` from any terminal once
              the page is ready, and the script proceeds to capture.

  --auto      No-pause auto-capture. Waits for networkidle + an extra dwell
              for client-side hydration, then saves. Use for sources that are
              JS-rendered but NOT behind anti-bot challenges.

This is the human-in-the-loop fetcher referenced in PROCESSING-GLOSSARIES.md.
The saved file is committed as .source-cache.html alongside the per-source
extractor, and the extractor parses it locally — re-running the extractor
doesn't need the browser, only the cache.

Usage:
  python3 tools-resources/utils/playwright_fetch.py URL OUTPUT_PATH (--auto | --pause)
                                                    [--wait-for SELECTOR]
                                                    [--dwell SECONDS]
                                                    [--sentinel PATH]
"""

import argparse
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


def fetch(url, output_path, mode, wait_for_selector=None, dwell_s=5,
          sentinel_path="/tmp/playwright-go", timeout_s=60):
    # Remove any stale sentinel before launching, so a leftover file from a
    # previous run doesn't make this run skip the pause.
    sp = Path(sentinel_path)
    if mode == "pause" and sp.exists():
        sp.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
            ),
            viewport={"width": 1400, "height": 900},
            locale="en-US",
        )
        page = context.new_page()
        print(f"navigating: {url}")
        page.goto(url, timeout=timeout_s * 1000, wait_until="domcontentloaded")

        if wait_for_selector:
            print(f"waiting for selector: {wait_for_selector}")
            try:
                page.wait_for_selector(wait_for_selector, timeout=timeout_s * 1000)
            except Exception as e:
                print(f"  (wait_for_selector failed: {e}; continuing anyway)")

        if mode == "pause":
            print("")
            print("=" * 70)
            print(f"  Browser window is open. Clear any anti-bot challenge / accept")
            print(f"  cookies / etc. in the visible browser.")
            print(f"")
            print(f"  When the page shows the real content, run this in any terminal:")
            print(f"    touch {sentinel_path}")
            print(f"")
            print(f"  Script will poll for that file every second and capture when it")
            print(f"  appears. Ctrl-C this script to abort.")
            print("=" * 70)
            waited = 0
            while not sp.exists():
                # Keep the browser alive while waiting.
                try:
                    page.wait_for_timeout(1000)
                except Exception:
                    pass
                waited += 1
                if waited % 30 == 0:
                    print(f"  (still waiting for {sentinel_path}, {waited}s elapsed)")
            print(f"sentinel detected, capturing...")
            # Clean up the sentinel so the next run starts clean.
            sp.unlink()
        else:  # auto
            print(f"waiting for networkidle...")
            try:
                page.wait_for_load_state("networkidle", timeout=timeout_s * 1000)
            except Exception as e:
                print(f"  (networkidle wait failed: {e}; continuing)")
            print(f"dwell {dwell_s}s for client-side hydration...")
            page.wait_for_timeout(dwell_s * 1000)

        html = page.content()
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print(f"wrote {len(html)} bytes to {out}")

        browser.close()
    return output_path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("output_path")
    mode_group = ap.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--pause", dest="mode", action="store_const",
                            const="pause",
                            help="Wait for sentinel file before capturing "
                                 "(use for anti-bot pages)")
    mode_group.add_argument("--auto", dest="mode", action="store_const",
                            const="auto",
                            help="Auto-capture after networkidle + dwell "
                                 "(use for JS-rendered, no anti-bot)")
    ap.add_argument("--wait-for", default=None,
                    help="CSS selector to wait for after navigation")
    ap.add_argument("--dwell", type=int, default=5,
                    help="Extra seconds to wait after networkidle (auto mode, default 5)")
    ap.add_argument("--sentinel", default="/tmp/playwright-go",
                    help="Sentinel file path for --pause mode (default /tmp/playwright-go)")
    ap.add_argument("--timeout", type=int, default=60,
                    help="Per-step timeout in seconds (default 60)")
    args = ap.parse_args()

    fetch(args.url, args.output_path, args.mode,
          wait_for_selector=args.wait_for,
          dwell_s=args.dwell,
          sentinel_path=args.sentinel,
          timeout_s=args.timeout)


if __name__ == "__main__":
    main()
