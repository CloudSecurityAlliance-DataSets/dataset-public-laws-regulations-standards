# CAPEC (Common Attack Pattern Enumeration and Classification)

A public catalog of common attack patterns — how adversaries exploit weaknesses in applications and other cyber-enabled capabilities. CAPEC sits at a lower level of abstraction than ATT&CK and pairs directly with CWE: **CAPEC attack patterns exploit CWE weaknesses**.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/capec` |
| **Upstream version** | **3.9, dated 2023-01-24** |
| **License** | MITRE CAPEC [Terms of Use](https://capec.mitre.org/about/termsofuse.html) (free use with attribution) |
| **Status** | ⚠ **Effectively dormant** — see below |
| **In this directory** | Metadata only. See [What's here](#whats-in-this-directory). |

## ⚠ Release status

`capec_latest.xml` reports `Version="3.9" Date="2023-01-24"`, and the HTTP `Last-Modified` header agrees. **CAPEC has not shipped a release in over three years.**

Treat CAPEC as a stable, essentially frozen reference rather than a moving target. This matters when planning work against it: mappings built on CAPEC 3.9 are unlikely to be invalidated by a new release, but CAPEC also will not reflect recent attack patterns — notably nothing AI/ML-specific from the last three years. For current attack-pattern coverage, [ATT&CK](../attack/) and [ATLAS](../atlas/) are the live frameworks.

## Upstream

CAPEC has **no dedicated GitHub data repository** — the weakest GitHub story of the MITRE frameworks in this tree, alongside [FiGHT](../fight/). The authoritative distribution is direct download from `capec.mitre.org`.

| Channel | Location |
|---|---|
| **Official downloads** | <https://capec.mitre.org/data/downloads.html> — XML, CSV, HTML |
| **STIX** | [`mitre/cti`](https://github.com/mitre/cti) under `capec/2.0/` and `capec/2.1/`, documented in [`USAGE-CAPEC.md`](https://github.com/mitre/cti/blob/master/USAGE-CAPEC.md) |
| **Web** | <https://capec.mitre.org/data/definitions/> |

## Getting the data

```bash
# Full catalog, XML (~3.8 MB)
curl -LO https://capec.mitre.org/data/xml/capec_latest.xml

# STIX form, via the CTI repo
curl -s https://api.github.com/repos/mitre/cti/contents/capec/2.1 | jq -r '.[].name'
```

Because CAPEC is frozen at 3.9, `capec_latest.xml` is currently stable — but it is an unversioned URL, so record the `Version` and `Date` attributes from the XML root element with any extraction.

## Identifiers

`CAPEC-<n>`, unpadded (e.g. `CAPEC-1`, `CAPEC-100`). The catalog is organized into **attack patterns**, **categories**, and **views**, all sharing the same ID space — so a bare `CAPEC-n` does not tell you which kind of object you have; check the containing element.

## What's in this directory

Metadata only, per the repository's [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream). MITRE publishes the authoritative catalog as XML/CSV downloads; a copy here would add nothing.

If a structured extraction is ever wanted, CAPEC's dormancy makes it a good candidate — a one-time parse of 3.9 will not go stale quickly.

## Relationship to sibling frameworks

- **CWE** (`weakness/mitre.org/cwe/`) — the tightest coupling; each CWE entry links the CAPEC patterns that exploit it, and vice versa.
- **[ATT&CK](../attack/)** — CAPEC patterns are finer-grained and map upward to ATT&CK techniques. CAPEC's STIX form ships in the same `mitre/cti` repo as ATT&CK.
- **[D3FEND](../d3fend/)** — countermeasures defend against CAPEC patterns.

## Last verified

2026-08-12 — `capec_latest.xml` served version 3.9, dated 2023-01-24.
