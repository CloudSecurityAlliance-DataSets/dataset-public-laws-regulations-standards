#!/usr/bin/env python3
"""Extract NCSC (UK National Cyber Security Centre) glossary.

Source: https://www.ncsc.gov.uk/section/advice-guidance/glossary

STATUS: Manual / headless-browser extraction needed.

The NCSC glossary page (Drupal 11 / Lakes theme) ships only a navigation
shell at https://www.ncsc.gov.uk/section/advice-guidance/glossary . The
A-Z term list is rendered client-side from a JavaScript module that is
not discoverable from the static HTML, and a quick scan of the
``main-*.js`` Vite bundle, the sitemap, and common Drupal Views Ajax
endpoints (``/views/ajax``, ``?az=a``, etc.) all failed to surface either
a JSON API or per-term URLs.

To extract this glossary, render the page with a headless browser
(Playwright / Puppeteer), wait for the term list to appear, and serialise
the DOM. The expected post-render structure is roughly:

  <ul ...>
    <li>
      <h3>Term name</h3>
      <p>Definition...</p>
    </li>
    ...
  </ul>

See sibling extractors (kubernetes-glossary, cyberdico) for the
DOM-walking pattern once a fully rendered HTML snapshot is available.
"""
from __future__ import annotations


def main():  # pragma: no cover - intentional stub
    raise NotImplementedError(
        "Manual extraction needed: NCSC glossary is JS-rendered with no "
        "discoverable JSON endpoint or per-term URLs. Use a headless "
        "browser snapshot, then re-implement the parser."
    )


if __name__ == "__main__":
    main()
