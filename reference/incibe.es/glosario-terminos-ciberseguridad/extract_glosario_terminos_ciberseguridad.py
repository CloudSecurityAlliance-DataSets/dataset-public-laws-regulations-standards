#!/usr/bin/env python3
"""
Extractor stub for INCIBE — Glosario de terminos de ciberseguridad: una guia de
aproximacion para el empresario (2021).

Publisher: Instituto Nacional de Ciberseguridad (INCIBE), Spain.
Source page:
    https://www.incibe.es/empresas/materiales/glosario-de-terminos-de-ciberseguridad-una-guia-de-aproximacion-para-el
Direct PDF:
    https://www.incibe.es/sites/default/files/contenidos/guias/doc/guia_glosario_ciberseguridad_2021.pdf

STATUS: NOT YET EXTRACTED.

The INCIBE source page exposes the glossary ONLY as a downloadable PDF. There
is no HTML, JSON, CSV, or plain-text version of the term/definition pairs
published by INCIBE. The terms do not appear inline on the source page.

Because this repository's PDF -> markdown pipeline requires the marker GPU box
(see ../../../CLAUDE.md, section "Extraction Pipeline"), this extractor cannot
run from a plain-CPU agent environment. To produce the structured outputs
listed under "Expected outputs" below, the PDF must first be converted to
markdown on the GPU box, then a structured parser walks the marker block tree
to emit one row per glossary term.

Expected outputs (to be produced once marker extraction is available):
    - glosario-terminos-ciberseguridad.md
    - glosario-terminos-ciberseguridad-terms.csv
        header: term,definition,source_anchor,notes
    - glosario-terminos-ciberseguridad-terms.json
        list of objects with the same fields as the CSV
    Spanish definitions must be preserved verbatim.

Reproduction recipe (run from a host with access to markersinglehost):

    # 1. Fetch the PDF (publicly redistributable per INCIBE reuse notice).
    curl -L -o guia_glosario_ciberseguridad_2021.pdf \
        https://www.incibe.es/sites/default/files/contenidos/guias/doc/guia_glosario_ciberseguridad_2021.pdf

    # 2. Convert to markdown on the GPU box.
    ../../../tools-resources/utils/pdf_to_md_via_gpu.sh \
        --output-dir reference/incibe.es/glosario-terminos-ciberseguridad \
        guia_glosario_ciberseguridad_2021.pdf

    # 3. Rename marker outputs to match the SecID-derived filename prefix:
    #      guia_glosario_ciberseguridad_2021.md     -> glosario-terminos-ciberseguridad.md
    #      guia_glosario_ciberseguridad_2021.json   -> glosario-terminos-ciberseguridad.json
    #      guia_glosario_ciberseguridad_2021_meta.json
    #          -> glosario-terminos-ciberseguridad_meta.json

    # 4. Replace this stub with a parser that walks the marker block tree
    #    (glosario-terminos-ciberseguridad.json) and emits the CSV + JSON
    #    structured term lists per the header above.

This file intentionally raises NotImplementedError so any pipeline that
inadvertently invokes the extractor before marker output exists fails loudly
instead of producing empty CSV/JSON artifacts.
"""

from __future__ import annotations

SOURCE_PAGE_URL = (
    "https://www.incibe.es/empresas/materiales/"
    "glosario-de-terminos-de-ciberseguridad-una-guia-de-aproximacion-para-el"
)
SOURCE_PDF_URL = (
    "https://www.incibe.es/sites/default/files/contenidos/guias/doc/"
    "guia_glosario_ciberseguridad_2021.pdf"
)


def main() -> None:
    raise NotImplementedError(
        "INCIBE Glosario de terminos de ciberseguridad is PDF-only at the "
        f"publisher: {SOURCE_PDF_URL}. Run the marker GPU pipeline first "
        "(see docstring for the full reproduction recipe), then replace this "
        "stub with the structured parser."
    )


if __name__ == "__main__":
    main()
