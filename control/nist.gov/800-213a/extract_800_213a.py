#!/usr/bin/env python3
"""Parse NIST SP 800-213A (IoT Device Cybersecurity Capability Catalog) into CSV/JSON.

800-213A organizes IoT cybersecurity capabilities as a two-level hierarchy:

  Capability (DI, DC, DP, LA, SU) — device cybersecurity capabilities
    Sub-capability (e.g., DI:IMS, DI:AID) — refines a capability
      Requirements (numbered, sometimes with letter sub-items)

  Plus non-technical supporting capabilities (DO, CT, EI, AS, IS) with the
  same shape (sub-capabilities containing requirements).

Each sub-capability section in the markdown looks like:

    #### **(IMS) Identifier Management Support**

    Description: Ability for device identification.

    Discussion: ...

    Related SP 800-53 Rev. 5 Controls: IA-3, IA-4

    *Requirements that may be necessary:*

    - 1. Ability to uniquely identify the IoT device logically.
    - 2. Ability to uniquely identify a remote IoT device.
      - a. ...

Output (one row per requirement) at 800-213a-requirements.{csv,json}:
    capability_id, capability_name,
    subcapability_id, subcapability_name,
    subcapability_description, subcapability_discussion,
    related_800_53_controls,
    requirement_id, requirement_text
"""
import csv
import json
import re
from pathlib import Path


CAPABILITY_RE = re.compile(
    r"^#+\s+(?:<span[^>]*></span>)?\*\*([A-Z]{2})\s*-\s*([A-Z][A-Z\s]+?)\*\*\s*$",
    re.MULTILINE,
)
SUBCAPABILITY_RE = re.compile(
    r"^#+\s+(?:<span[^>]*></span>)?\*\*\(([A-Z]+)\)\s+(.+?)\*\*\s*$",
    re.MULTILINE,
)
DESCRIPTION_RE = re.compile(r"^Description:\s*(.+?)$", re.MULTILINE)
DISCUSSION_RE = re.compile(r"^Discussion:\s*(.+?)$", re.MULTILINE)
RELATED_RE = re.compile(
    r"^(?:#+\s*)?Related SP 800-53(?:\s*Rev\.\s*5)? Controls?:\s*(.+?)$",
    re.MULTILINE,
)
# Requirement lines: "- 1. text" (top-level) or "  - a. text" (sub-item)
TOP_REQ_RE = re.compile(r"^-\s+(\d+)\.\s+(.+?)$")
SUB_REQ_RE = re.compile(r"^\s+-\s+([a-z])\.\s+(.+?)$")
PARENT_AS_INTRO_RE = re.compile(r"^-\s+(\d+)\.\s+(.+:\s*)$")
END_OF_REQS_RE = re.compile(r"^(#+\s+|\{[\d]+\}|\*[A-Z])", re.MULTILINE)


def normalize(s: str) -> str:
    s = re.sub(r"\\([\[\]\(\)_*.\-])", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_requirements(block: str):
    """Yield (req_id, text) pairs from a block of bulleted requirements."""
    current_top = None
    current_top_text = ""
    pending_sub = []

    def flush_top():
        nonlocal current_top, current_top_text, pending_sub
        if current_top is not None:
            yield current_top, current_top_text
            for letter, text in pending_sub:
                yield f"{current_top}.{letter}", text
        current_top = None
        current_top_text = ""
        pending_sub = []

    out = []
    for line in block.splitlines():
        if not line.strip():
            continue
        m_top = TOP_REQ_RE.match(line)
        if m_top:
            out.extend(flush_top())
            current_top = m_top.group(1)
            current_top_text = normalize(m_top.group(2))
            continue
        m_sub = SUB_REQ_RE.match(line)
        if m_sub and current_top is not None:
            pending_sub.append((m_sub.group(1), normalize(m_sub.group(2))))
            continue
        # Continuation of current requirement — append to current_top_text
        if current_top is not None and not line.startswith("#"):
            stripped = line.strip()
            if stripped:
                current_top_text = (current_top_text + " " + normalize(stripped)).strip()
    out.extend(flush_top())
    return list(out)


def main():
    here = Path(__file__).parent
    md = (here / "800-213a.md").read_text(encoding="utf-8")

    # Anchor capability heading positions
    cap_positions = list(CAPABILITY_RE.finditer(md))
    # Pre-build sub-capability headings list to assign each to its capability.
    sub_positions = list(SUBCAPABILITY_RE.finditer(md))

    # Filter cap_positions to those that actually start a capability section.
    # The catalog begins after "Device Cybersecurity Capability Catalog" heading;
    # find that anchor and clip the cap_positions.
    catalog_anchor = re.search(r"Device Cybersecurity Capability Catalog", md)
    catalog_start = catalog_anchor.start() if catalog_anchor else 0
    cap_positions = [m for m in cap_positions if m.start() >= catalog_start]

    if not cap_positions:
        raise SystemExit("Could not find any capability headings")

    # For each sub-capability, slice the body from its heading to the next
    # sub-capability heading OR next capability heading OR EOF.
    all_anchors = sorted(
        [(m.start(), "cap", m) for m in cap_positions]
        + [(m.start(), "sub", m) for m in sub_positions if m.start() >= catalog_start]
    )

    rows = []
    current_cap_id = None
    current_cap_name = None

    for i, (pos, kind, m) in enumerate(all_anchors):
        if kind == "cap":
            current_cap_id = m.group(1)
            current_cap_name = " ".join(w.capitalize() for w in m.group(2).split())
            continue
        # kind == "sub"
        sub_id = m.group(1)
        sub_name = m.group(2).strip()
        body_start = m.end()
        body_end = all_anchors[i + 1][0] if i + 1 < len(all_anchors) else len(md)
        body = md[body_start:body_end]

        desc_m = DESCRIPTION_RE.search(body)
        disc_m = DISCUSSION_RE.search(body)
        rel_m = RELATED_RE.search(body)

        description = normalize(desc_m.group(1)) if desc_m else ""
        discussion = normalize(disc_m.group(1)) if disc_m else ""
        related = normalize(rel_m.group(1)) if rel_m else ""

        # Requirements come after the Related Controls line (or after the
        # discussion if no related controls).
        req_anchor = (rel_m or disc_m or desc_m)
        if req_anchor:
            req_block = body[req_anchor.end():]
        else:
            req_block = body

        reqs = parse_requirements(req_block)
        if not reqs:
            # Sub-capability with no requirements — still emit one row to record
            # the sub-capability itself (e.g., PID in DI just has Description).
            rows.append({
                "capability_id": current_cap_id,
                "capability_name": current_cap_name,
                "subcapability_id": sub_id,
                "subcapability_name": sub_name,
                "subcapability_description": description,
                "subcapability_discussion": discussion,
                "related_800_53_controls": related,
                "requirement_id": "",
                "requirement_text": "",
            })
            continue
        for rid, rtext in reqs:
            rows.append({
                "capability_id": current_cap_id,
                "capability_name": current_cap_name,
                "subcapability_id": sub_id,
                "subcapability_name": sub_name,
                "subcapability_description": description,
                "subcapability_discussion": discussion,
                "related_800_53_controls": related,
                "requirement_id": rid,
                "requirement_text": rtext,
            })

    csv_path = here / "800-213a-requirements.csv"
    json_path = here / "800-213a-requirements.json"
    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_caps = len({r["capability_id"] for r in rows})
    n_subs = len({(r["capability_id"], r["subcapability_id"]) for r in rows})
    print(f"Capabilities: {n_caps}")
    print(f"Sub-capabilities: {n_subs}")
    print(f"Requirement rows: {len(rows)}")
    print(f"Wrote {csv_path.name} and {json_path.name}")


if __name__ == "__main__":
    main()
