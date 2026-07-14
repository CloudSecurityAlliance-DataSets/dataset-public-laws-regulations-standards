# A5 — AI Audit and Assurance Assessment Architecture (BSI)

BSI's modular, expandable audit architecture for demonstrating the trustworthiness of AI systems, targeting all actors along the AI value chain (providers, operators, and those overseeing AI). Published machine-readable in **OSCAL**. Broader than AIC4 (which is limited to AI cloud services).

- **SecID:** `secid:control/bsi.bund.de/a5`
- **Owner:** Bundesamt für Sicherheit in der Informationstechnik (BSI)
- **Source:** https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/A5/A5_node.html

## Contents

| File | What |
|---|---|
| `A5-Basismodul-2026-06-30.json` | **Verbatim OSCAL catalog** — horizontal Trustworthiness baseline module (57 controls, 6 groups: GCS, DEI, VAV, DEP, OPS, RET) |
| `A5-Cloudmodul-2026-06-30.json` | **Verbatim OSCAL catalog** — Cloud-Infrastructure operational module (1 control) |
| `A5-Basismodul-controls.csv` / `.json` | Flattened per-control view of the Basismodul (group/subgroup/id/title/statement/guidance/props) |
| `A5-Cloudmodul-controls.csv` / `.json` | Flattened per-control view of the Cloudmodul |

Control ID format: `GROUP.SUBGROUP.N` (e.g. `GCS.1.1`). The separate **Prüfmethodik** (audit methodology) is prose (PDF) and is linked in the metadata, not extracted per-item.

## Status & License

**Community Draft**, Basismodul document version **0.9** (dated 2026-06-30; OSCAL catalog v1.0.0). Public comments to `aisecurity@bsi.bund.de` until **2026-08-31**. German only.

Published via BSI's [Stand-der-Technik-Bibliothek](https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek), licensed **CC BY-SA 4.0** (© BSI 2026). The flattened CSV/JSON is a derivative of BSI's official OSCAL and is shared under the same license (ShareAlike) with attribution. Re-extract when BSI publishes the final A5.
