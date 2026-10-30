# CAIQ v4.1.0 (CCM-CAIQ)

`secid:control/cloudsecurityalliance.org/ccm-caiq@4.1.0` · 283 questions · 207 CCM controls

The Consensus Assessments Initiative Questionnaire for CCM v4.1: the yes/no
questions submitted to the CSA STAR Registry for a Level 1 self-assessment.

> ## ⚠️ CSA changed 26 question texts without changing the version label
>
> CSA has issued two different workbooks under the label CAIQ 4.1.0:
>
> | | First generation | Second generation |
> |---|---|---|
> | Workbook | `CAIQv4.1.0-star_security_questionnaire-generated_at_2026_01_13.xlsx` | `CAIQv4.1.0-star_security_questionnaire-generated_at_2026_10_02.xlsx` |
> | Cell A1 | `{"specification_version":"4.1.0","caiq_version":"4.1.0"}` | `{"specification_version":"4.1.1","caiq_version":"4.1.0"}` |
> | Served by CSA | from the January 2026 release until the bundle was repacked on 2026-10-06 | since 2026-10-06 |
>
> The questionnaire's own Change Log gains no row for this regeneration. Its
> two rows (CAIQ v4.1 and CAIQ v4.0.3) were only reformatted: the first reads
> "CAIQ v4.1 | 2025/11/01 | Question(s)" in January and "CAIQ v4.1.0 |
> 2025-11-01 | assessment_questionnaire" in October. The second generation was built from
> [CCM 4.1.1](../../ccm/4.1.1/), whose edits to control text carried into the
> questions. 26 of 283 question texts differ: 19 in punctuation only, 7 in wording.
>
> **This directory now holds the second generation**, the one CSA serves. The
> first-generation extraction was replaced in place on 2026-10-23. It is on
> `main` unchanged from `6f737db` through `74ff4b8`, so
> `git show 74ff4b8:control/cloudsecurityalliance.org/ccm-caiq/4.1.0/ccm-caiq-4.1.0.json`
> retrieves it. Both workbooks are archived in S3 under this directory's path.
>
> If you answered the questionnaire before October 2026, your answers were to
> the first-generation text. The table below lists every question whose text
> differs, so you can tell whether an answer needs another look.

Question IDs are unchanged: the same 283 IDs under the same 207 controls.

**More differs than the 26 question texts**, which matters if you diff this
file against the January one. These were counted on 2026-10-23 against git
`74ff4b8`, and are not machine-checked:

- **Line breaks** changed in 233 of the 283 raw `question` strings. Only 26 of
  those differ once whitespace is normalised.
- **`ccm_control_specification`** differs in 150 of 283 records once
  normalised. It is the control text as printed in the questionnaire, and 101
  CCM specifications were reworded in 4.1.1.
- **`ccm_control`** is now embedded from CCM 4.1.1
  ([`../../ccm/4.1.1/ccm-4.1.1.json`](../../ccm/4.1.1/ccm-4.1.1.json)) rather
  than 4.1.0. It differs in 280 of 283 records, mostly in line breaks.

The questions as they shipped with CCM 4.1.0 are also embedded in
[`../../ccm/4.1.0/ccm-4.1.0.json`](../../ccm/4.1.0/ccm-4.1.0.json)
(`caiq_questions`).

## The seven wording changes

Five of these are corrections that bring the question in line with its control
or with ordinary English: `DCS-02.2` drops a doubled "information", `DCS-06.2`
straightens an apostrophe, `I&S-05.1` hyphenates "non-production", `LOG-07.1`
changes "meta/data" to "metadata", and `IAM-13.1` pluralises "application" as the
control does.

Two change what is asked:

- **`UEM-02.1`**: the list is now "applied" where it was "applicable". The
  control (UEM-02) says "Define, document, apply, and evaluate", so the new
  wording matches the control.
- **`DCS-11.1`**: the question drops "and surveillance systems". The control
  (DCS-11) still requires surveillance systems "at the external perimeter and at
  all the ingress and egress points". The old question asked about both
  locations; read literally, the new one asks about one: "external perimeter
  datacenter surveillance systems at all ingress and egress points". Recorded
  as found, not corrected: the extraction keeps CSA's text.

## Changed questions

Texts are whitespace-normalised: CSA also changed line breaks in many cells
without changing their words, and those are not listed. "Punctuation only" means
the two texts are identical once whitespace, commas, semicolons and full stops
are removed and case is ignored. The 2026-01-13 column is the text this directory
held before 2026-10-23.

| Question | 2026-01-13 | 2026-10-02 | Punctuation only |
|---|---|---|---|
| `CCC-02.1` | Is a defined quality change control, approval and testing process, incorporating baselines, testing, and release standards, established, maintained and implemented? | Is a defined quality change control, approval, and testing process, incorporating baselines, testing, and release standards, established, maintained, and implemented? | yes |
| `CCC-03.1` | Is a change management procedure implemented to manage the risks associated with applying changes to assets, owned, controlled or used by the organization? | Is a change management procedure implemented to manage the risks associated with applying changes to assets, owned, controlled, or used by the organization? | yes |
| `CCC-06.1` | Are change management and configuration baselines established, documented and implemented for all relevant authorized changes on organizational assets? | Are change management and configuration baselines established, documented, and implemented for all relevant authorized changes on organizational assets? | yes |
| `CEK-14.1` | Are processes, procedures and technical measures to securely destroy cryptographic keys when they are no longer needed, defined, implemented, and evaluated, and include provisions for legal and regulatory requirements? | Are processes, procedures, and technical measures to securely destroy cryptographic keys when they are no longer needed, defined, implemented, and evaluated, and include provisions for legal and regulatory requirements? | yes |
| `CEK-16.1` | Are processes, procedures, and technical measures to monitor, review and approve key transitions (e.g., from any state to/from suspension) being defined, implemented, and evaluated to include legal and regulatory requirement provisions? | Are processes, procedures, and technical measures to monitor, review, and approve key transitions (e.g., from any state to/from suspension) being defined, implemented, and evaluated to include legal and regulatory requirement provisions? | yes |
| `DCS-02.2` | Is a data destruction procedure applied that renders information recovery information impossible if equipment is not physically destroyed? | Is a data destruction procedure applied that renders information recovery impossible if equipment is not physically destroyed? | no |
| `DCS-06.2` | Are assets’ classifications reviewed and updated at least annually or upon significant changes? | Are assets' classifications reviewed and updated at least annually or upon significant changes? | no |
| `DCS-11.1` | Are external perimeter datacenter surveillance systems and surveillance systems at all ingress and egress points implemented, maintained, and operated? | Are external perimeter datacenter surveillance systems at all ingress and egress points implemented, maintained, and operated? | no |
| `DCS-14.1` | Are data center environmental control systems designed to monitor, maintain, and test that on-site temperature and humidity conditions fall within accepted industry standards effectively implemented and maintained? | Are datacenter environmental control systems designed to monitor, maintain, and test that on-site temperature and humidity conditions fall within accepted industry standards effectively implemented and maintained? | yes |
| `DCS-17.1` | Are datacenter security metrics established, monitored, and reported to secure data center assets and services? | Are datacenter security metrics established, monitored, and reported to secure datacenter assets and services? | yes |
| `DSP-03.1` | Is a data inventory created and maintained for sensitive, regulated and personal information (at a minimum)? | Is a data inventory created and maintained for sensitive, regulated, and personal information (at a minimum)? | yes |
| `DSP-09.1` | Is a data protection impact assessment (DPIA) conducted when processing personal data and evaluating the origin, nature, particularity, and severity of risks according to any applicable laws, regulations and industry best practices? | Is a data protection impact assessment (DPIA) conducted when processing personal data and evaluating the origin, nature, particularity, and severity of risks according to any applicable laws, regulations, and industry best practices? | yes |
| `HRS-09.1` | Are employee roles and responsibilities relating to information assets' security and privacy, established, documented and communicated? | Are employee roles and responsibilities relating to information assets' security and privacy, established, documented, and communicated? | yes |
| `HRS-11.1` | Is a security awareness training program for all employees of the organization established, documented, approved, communicated, applied, evaluated and maintained? | Is a security awareness training program for all employees of the organization established, documented, approved, communicated, applied, evaluated, and maintained? | yes |
| `I&S-05.1` | Are the environments separated into production and non production environments to reduce the risk of sensitive production data being used in non-production environments? | Are the environments separated into production and non-production environments to reduce the risk of sensitive production data being used in non-production environments? | no |
| `IAM-11.1` | Are processes and procedures for service customers to participate, where applicable, in granting access for agreed, high risk as (defined by the organizational risk assessment) privileged access roles defined, implemented and evaluated? | Are processes and procedures for service customers to participate, where applicable, in granting access for agreed, high risk as (defined by the organizational risk assessment) privileged access roles defined, implemented, and evaluated? | yes |
| `IAM-13.1` | Are processes, procedures, and technical measures for authenticating access to systems, application, and data assets including multifactor authentication for a least-privileged user and sensitive data access defined, implemented, and evaluated? | Are processes, procedures, and technical measures for authenticating access to systems, applications, and data assets including multifactor authentication for a least-privileged user and sensitive data access defined, implemented, and evaluated? | no |
| `LOG-07.1` | Are logging requirements for information meta/data system events established, documented, and implemented? | Are logging requirements for information metadata system events established, documented, and implemented? | no |
| `SEF-05.1` | Are information security incident metrics established, monitored and reported? | Are information security incident metrics established, monitored, and reported? | yes |
| `SEF-10.1` | Are points of contact maintained for applicable regulation authorities, national and local law enforcement, and other legal jurisdictional authorities? | Are points of contact maintained for applicable regulation authorities, national, and local law enforcement, and other legal jurisdictional authorities? | yes |
| `STA-11.1` | Do service agreements between service providers and service customers (tenants) incorporate at least the following mutually agreed upon provisions and/or terms? • Scope, characteristics, and location of business relationship and services offered • Information security requirements (including SSRM) • Change management process • Logging and monitoring capability • Incident management and communication procedures • Right to audit and third-party assessment • Service termination • Interoperability and portability requirements • Data privacy • Operational Resilience | Do service agreements between service providers and service customers (tenants) incorporate at least the following mutually agreed upon provisions and/or terms? • Scope, characteristics, and location of business relationship and services offered • Information security requirements (including SSRM) • Change management process • Logging and monitoring capability • Incident management and communication procedures • Right to audit and third-party assessment • Service termination • Interoperability and portability requirements • Data privacy • Operational resilience | yes |
| `TVM-07.1` | Are processes, procedures and technical measures defined, implemented and evaluated for the periodic performance of penetration testing by independent third parties? | Are processes, procedures, and technical measures defined, implemented, and evaluated for the periodic performance of penetration testing by independent third parties? | yes |
| `TVM-08.1` | Are processes, procedures and technical measures defined, implemented and evaluated based on identified risks to support scheduled and emergency responses to vulnerability identification? | Are processes, procedures, and technical measures defined, implemented, and evaluated based on identified risks to support scheduled and emergency responses to vulnerability identification? | yes |
| `UEM-02.1` | Is there a defined, documented, applicable and evaluated list containing approved services, applications, and the sources of applications (stores) acceptable for use by endpoints when accessing or storing organization-managed data? | Is there a defined, documented, applied, and evaluated list containing approved services, applications, and the sources of applications (stores) acceptable for use by endpoints when accessing or storing organization-managed data? | no |
| `UEM-04.1` | Is an inventory of all endpoints used and maintained to store, access and process company data? | Is an inventory of all endpoints used and maintained to store, access, and process company data? | yes |
| `UEM-05.1` | Are processes, procedures, and technical measures defined, implemented and evaluated, to enforce policies and controls for all endpoints permitted to access systems and/or store, transmit, or process organizational data? | Are processes, procedures, and technical measures defined, implemented, and evaluated, to enforce policies and controls for all endpoints permitted to access systems and/or store, transmit, or process organizational data? | yes |

`../../ccm/check_figures.py` checks this table against the data: exactly 26
rows, each old cell equal to the CCM 4.1.0 text, each new cell equal to the
committed extraction, and each "Punctuation only" flag correct.

## Files

| File | What it is |
|---|---|
| `ccm-caiq-4.1.0.json` | 283 questions, each with its CCM control embedded from [`../../ccm/4.1.1/ccm-4.1.1.json`](../../ccm/4.1.1/ccm-4.1.1.json) |
| `ccm-caiq-4.1.0-metadata.json` | Document metadata, including both generations in `extraction_history` |
| `scripts/parse_caiq.py` | The extractor |
| `CAIQv4.1.0-…generated_at_2026_10_02.xlsx`, `…_2026_01_13.xlsx` | Source workbooks (gitignored; in S3) |

## Rebuilding

Pull the workbook from
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/ccm-caiq/4.1.0/`,
then:

```bash
cd scripts
./parse_caiq.py --input ../CAIQv4.1.0-star_security_questionnaire-generated_at_2026_10_02.xlsx
```

The script refuses a workbook whose cell A1 does not stamp `caiq_version` 4.1.0
and CCM 4.1.1. To rebuild the first generation instead, for comparison:

```bash
./parse_caiq.py --input ../CAIQv4.1.0-star_security_questionnaire-generated_at_2026_01_13.xlsx \
    --ccm-json ../../../ccm/4.1.0/ccm-4.1.0.json --expect-ccm-version 4.1.0 --output /tmp/caiq-4.1.0-jan.json
```

That reproduces the replaced extraction exactly, apart from the
`source_workbook` key added on 2026-10-23.
