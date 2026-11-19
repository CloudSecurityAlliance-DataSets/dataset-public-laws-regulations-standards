---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-16"
cwe_id: "CWE-16"
entry_type: category
name: "Configuration"
status: Obsolete
mapping_usage: Prohibited
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/16.html"
---

# CWE-16: Configuration

> **Obsolete.** MITRE marks this category as obsolete: kept for reference, no longer maintained.

## Summary

Weaknesses in this category are typically introduced during the configuration of the software.

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| WASC | 14 | Server Misconfiguration |
| WASC | 15 | Application Misconfiguration |

## References

- [REF-1287] MITRE. "Supplemental Details - 2022 CWE Top 25". Details of Problematic Mappings. 2022-06-28. <https://cwe.mitre.org/top25/archive/2022/2022_cwe_top25_supplemental.html#problematicMappingDetails> (URL validated: 2024-11-17).

## Mapping Notes

- **Usage:** Prohibited
- **Rationale:** This entry is a Category. Using categories for mapping has been discouraged since 2019. Categories are informal organizational groupings of weaknesses that can help CWE users with data aggregation, navigation, and browsing. However, they are not weaknesses in themselves [REF-1287]. This CWE entry may have become widely-used because of NIST's usage in NVD from 2008 to 2016 (see CWE-635 view, updated to the CWE-1003 view in 2016). Mapping is also Prohibited because this entry's status is Obsolete.
- **Comments:** As of CWE 4.9, "Configuration" is beginning to be treated as an aspect of the SDLC in which a product is directed (by a human or automated process) to perform an insecure behavior. CWE mapping should be conducted by analyzing the weakness in the behavior that has been set by the configuration, such as those related to access control (descendants of CWE-284) or resource management (CWE-400), etc.
- **Reasons:** Category, Frequent Misuse

## Notes

- **Maintenance**: Further discussion about this category was held over the CWE Research mailing list in early 2020. No definitive action has been decided.

- **Maintenance**: This entry is a Category, but various sources map to it anyway, despite CWE guidance that Categories should not be mapped. In this case, there are no clear CWE Weaknesses that can be utilized. "Inappropriate Configuration" sounds more like a Weakness in CWE's style, but it still does not indicate actual behavior of the product. Further research is still required, however, as a "configuration weakness" might be Primary to many other CWEs, i.e., it might be better described in terms of chaining relationships.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | CWE Community |  | CWE Draft 3, 2006-07-19 | Submitted by members of the CWE community to extend early CWE versions |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Taxonomy_Mappings |
| Modification | 2013-07-17 | CWE Content Team | MITRE | CWE 2.5, 2013-07-17 | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Detection_Factors |
| Modification | 2015-12-07 | CWE Content Team | MITRE | CWE 2.9, 2015-12-07 | updated Relationships |
| Modification | 2017-01-19 | CWE Content Team | MITRE | CWE 2.10, 2017-01-19 | updated Maintenance_Notes, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Detection_Factors |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated Relationships |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Maintenance_Notes, Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Maintenance_Notes, References |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Relationships |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Mapping_Notes |

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
