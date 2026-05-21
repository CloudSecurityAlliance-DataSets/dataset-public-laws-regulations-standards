#!/usr/bin/env python3
"""
Extract the ENISA Glossary of Terms.

Source: https://www.enisa.europa.eu/media/media-press-kits/enisa-glossary

The ENISA glossary page renders terms as `<strong>TERM</strong>: definition`
fragments inside `<p>` blocks (and occasional inline runs), grouped under
`<h3>` letter-section headers. There are no per-term HTML anchors, so the
`source_anchor` column emits the letter-section header (e.g. "A", "B"),
which is the only granularity the source supports.

This script:
  1. Fetches the live page
  2. Parses out (term, definition) tuples from `<strong>` runs
  3. Writes:
       - enisa-glossary.md           Markdown rendering of the glossary
       - enisa-glossary-terms.csv    Header: term,definition,source_anchor,notes
       - enisa-glossary-terms.json   Same data as a list of objects

If the network is unavailable or the page structure has changed beyond the
parser's tolerance, the script falls back to an embedded snapshot captured
from the live page on 2026-05-21 so the extraction is always reproducible.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

SOURCE_URL = "https://www.enisa.europa.eu/media/media-press-kits/enisa-glossary"
OUT_DIR = Path(__file__).resolve().parent

# --- Embedded fallback snapshot ------------------------------------------------
# Captured from the live page 2026-05-21 via WebFetch. Order matches source
# (alphabetical by term/acronym, case-insensitive). Tuple is (term, definition).
SNAPSHOT: list[tuple[str, str]] = [
    ("ABAC", "Accrual-based accounting"),
    ("AD", "Administrator"),
    ("AG", "Advisory Group"),
    ("AHWG", "Ad-hoc Working Group"),
    ("AI", "Artificial intelligence"),
    ("APF", "Annual privacy forum"),
    ("APT", "Advanced Persistent Threat. This term is commonly used to refer to cyber threats, in particular that of Internet-enabled espionage using a variety of intelligence gathering techniques."),
    ("APWG", "Anti-Phishing Working Group. Non-profit global pan-industrial and law enforcement association focused on eliminating the fraud, crime and identity theft that result from phishing, pharming, malware and email spoofing."),
    ("ARET", "Awareness Raising and Education Team"),
    ("AST", "Assistant(s)"),
    ("Awareness raising", "Awareness is the 'what' component of the education strategy of an organisation which tries to change the behaviour and patterns in how targeted audience uses technology and the Internet."),
    ("BEREC", "Body of European Regulators of Electronic Communications"),
    ("CA (Contract)", "Contract agent"),
    ("CA (Certification)", "Certification Authority. An authority that carries out certain management actions related to digital certificates, e.g. issuing, suspending, revoking etc."),
    ("CBU", "Capacity Building Unit"),
    ("CE", "Cyber Europe exercises. The Cyber Europe exercises are simulations of large-scale cybersecurity incidents that escalate to become cyber crises."),
    ("CEN", "European Committee for Standardisation"),
    ("Cenelec", "European Committee for Electrotechnical Standardisation"),
    ("CEP", "Cyber exercise platform. Set of machines and networks that provide the possibility of training technical skills and practise the participants' knowledge in an online way."),
    ("CERT", "Computer emergency response team. CERT, refers to a group of IT security experts, that provide reactive and proactive IT security services to its customers."),
    ("CERT-EU", "Computer Emergency Response Team for the EU institutions, bodies and agencies"),
    ("CII", "Critical Information Infrastructures. Information infrastructure (like networks, hardware, software, etc.) that is critical to the functioning of a nation or country."),
    ("CIIP", "Critical information-infrastructure protection"),
    ("CISO", "Chief Information Security Officer. Manages information security implications within the organization, specific program, or other area of responsibility."),
    ("Cloud Computing", "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services)."),
    ("CoA", "Court of Auditors"),
    ("COM", "European Commission"),
    ("CSA", "Cybersecurity Act"),
    ("CSCG", "ETSI CEN-CENELEC cybersecurity Security coordination group. It is the only joint group of the three officially recognised European Standardisation Organisations with a mandate for coordinating Cyber Security standards."),
    ("CSIRT", "Computer-security and incident-response team. Computer Security and Incident Response Team. Other term for CERT."),
    ("Cyber crisis", "Critical situation that involves information and telecommunication structures or facilities and can damage them and provoke a reduction or the discharge of the services they provide."),
    ("CyCLONe", "Cyber Crisis Liaison Organisation Network"),
    ("Data Protection", "Laws and regulations that make it illegal to store or share some types of information about people without their knowledge or permission."),
    ("DG", "Directorate-general. An organisational unit within the European Commission."),
    ("DG CONNECT", "Directorate General for Communications Networks, Content and Technology. An organisational unit within the European Commission."),
    ("DPA", "Data protection authorities. Independent body which is charge of monitoring the processing of personal data within its jurisdiction."),
    ("DPO", "Data protection officer"),
    ("DSM", "Digital single market"),
    ("EATA", "European Automotive Telecom Alliance"),
    ("EB", "Executive board"),
    ("EC", "European Union Commission. Other term for COM. The European Commission is the EU's executive body and represents the interests of Europe as a whole."),
    ("ECB", "European Central Bank"),
    ("EC3", "European cybercrime centre, Europol"),
    ("ECA", "European Court of Auditors"),
    ("ECCG", "European Cybersecurity Certification Group"),
    ("ECSC", "European cybersecurity challenge"),
    ("ECSM", "European cybersecurity month"),
    ("ECSO", "European cybersecurity organisation"),
    ("ED", "Executive Director. The senior manager and legal representative of the European Union Agency for Cybersecurity."),
    ("EDA", "European Defence Agency"),
    ("EDO", "Executive Director's Office"),
    ("EDPS", "European Data Protection Supervisor. An independent supervisory authority devoted to protecting personal data and privacy and promoting good practice in the EU institutions and bodies."),
    ("EEAS", "European External Action Service"),
    ("EECC", "EU electronic communications code"),
    ("EFTA", "European Free Trade Association (Stockholm Convention) (Iceland, Liechtenstein, Norway and Switzerland)"),
    ("eID", "Electronic Identity. Identity of a physical person in the digital world. It provides personal information about a person that can be accessible through digital services."),
    ("eIDAS", "Regulation on electronic identification and trusted services for electronic transactions in the internal market"),
    ("Electronic Seal", "Data in electronic form which are attached to or logically associated with other electronic data to ensure the origin and the integrity of the associated data."),
    ("ENISA", "European Union Agency for Cybersecurity (formly known as the European Union Network and Information Security Agency)"),
    ("ERA", "European Railway Agency"),
    ("ETSI", "European Telecommunications Standards Institute"),
    ("EU", "European Union"),
    ("EUIBAs", "EU institutions, bodies and agencies"),
    ("Europol", "European Union Agency for Law Enforcement Cooperation"),
    ("eu-LISA", "European Union Agency for the Operational Management of Large-Scale IT Systems in the Area of Freedom, Security and Justice"),
    ("FIRST", "Forum of incident-response and security teams"),
    ("GDPR", "General data protection regulation"),
    ("H2020", "Horizon 2020"),
    ("HoU", "Head of Unit. The mid-manager who is in charge of an organisational unit within ENISA."),
    ("IaaS", "Infrastructure as a Service. In Cloud computing, IaaS incorporates the capability to abstract resources (or not) as well as deliver physical and logical connectivity to those resources."),
    ("IAS", "Internal Audit Service"),
    ("ICC", "International Cybersecurity Challenge. ENISA, together with other regional and international organisations, decided to design and host for the first time the International Cybersecurity Challenge (ICC) in 2022."),
    ("ICS", "Industrial control systems. Control systems used in industrial production like SCADA or distributed control systems."),
    ("ICT", "Information and communication technology"),
    ("Information society", "The information society is the society, where low-cost information and data storage and transmission technologies are in general use."),
    ("INT", "International Cooperation Team"),
    ("IoT", "Internet of things"),
    ("IPR", "Intellectual property rights"),
    ("IS", "Information systems. Combination of information technology and people's activities that support operations, management and decision making."),
    ("ISAC", "Information Sharing & Analysis Centre. Trusted and specific entity which collects analyses and disseminates alerts and incident reports, as well as it shares and provides analytical support."),
    ("ISO", "International Organization for Standardization. The International Organization for Standardization develops and publishes International Standards."),
    ("ISO (Security)", "Information Security Officer (See CISO)"),
    ("ISP", "Internet Service Providers. A company that provides use of the Internet, allows you to use email, and gives you space on the Internet to show documents."),
    ("IT", "Information technology"),
    ("ITU", "International Telecommunication Union. The International Telecommunication Union is the United Nations specialised agency for information and communication technologies."),
    ("IXP", "Internet exchange point. Physical infrastructure through which Internet service providers (ISPs) exchange Internet traffic between their networks."),
    ("JRC", "Joint Research Centre. Directorate of the European Commission"),
    ("KIT", "Knowledge and Information Team"),
    ("LEA", "Law Enforcement Agency"),
    ("M2M", "Machine to machine"),
    ("MB", "Management Board"),
    ("MCS", "Market, Certification and Standardization Unit"),
    ("MEP", "Member of the European Parliament"),
    ("MoU", "Memorandum of understanding"),
    ("MS", "Member State"),
    ("NAPAC", "National public authority representatives committee"),
    ("NATO", "North Atlantic Treaty Organisation"),
    ("NCSS", "National Cybersecurity Strategies"),
    ("NGO", "Non-governmental organisation"),
    ("n/g CERT", "National / Governmental CERT. The term 'national / governmental CERT' subsumes all 'flavours' of national CERTs, governmental CERTs, national points of contacts."),
    ("NIS", "Network and Information Security. A term used by the European Commission to refer to issues related to IT security, security of hard- and software, etc."),
    ("NISD", "NIS directive"),
    ("NIS CG", "NIS Cooperation Group"),
    ("NLO", "National liaison officer"),
    ("NRA", "National regulatory authority"),
    ("OCU", "Operational Cooperation Unit"),
    ("OECD", "Organisation for Economic Co-operation and Development"),
    ("OSCE", "Organization for Security and Co-operation in Europe"),
    ("PaaS", "Platform as a Service. In Cloud computing, PaaS is a layer of integration with application development frameworks, middleware capabilities."),
    ("PDI", "Policy Development and Implementation Unit"),
    ("Personal data", "Any information relating to an identified or identifiable natural person hereinafter referred to as 'data subject'."),
    ("PETs", "Privacy-enhancing technologies"),
    ("PKI", "Public Key Infrastructure. The architecture, organization, techniques, practices, and procedures that collectively support the implementation and operation of a certificate-based public key cryptographic system."),
    ("PPP", "Public-private partnership. An arrangement where a government and a profit-making company invest in and work on an activity together."),
    ("Privacy", "The right of a person to not be subjected to arbitrary interference with his private life, family, home or correspondence nor to attacks upon his honour and reputation."),
    ("Privacy Seal", "A recognisable trust mark displayed by a web site which verifies the site implements certain security requirements as stated in its privacy policy."),
    ("PSD", "Payment services directive"),
    ("PSG", "Permanent stakeholders group"),
    ("R&D", "Research and Development"),
    ("Resilience", "The ability to recover from faults in addition to the ability to provide and maintain."),
    ("Risk assessment", "The process of finding out how much risk is involved in doing something."),
    ("SaaS", "Software as a Service. In Cloud computing, SaaS provides a self-contained operating environment used to deliver the entire user experience."),
    ("SB", "Supervisory Body"),
    ("SCADA", "Supervisory Control and Data Acquisition. SCADA systems are highly distributed systems used to control geographically dispersed assets, often scattered over thousands of square kilometers."),
    ("SCCG", "Stakeholder Cybersecurity Certification Group"),
    ("Security Incident", "An occurrence that harms integrity, accessibility, confidentiality or authenticity of a computer (or other device) or a network."),
    ("SLA", "Service-level agreement"),
    ("Smart Grid", "It generally refers to a class of technology people are using to bring utility electricity delivery systems into the 21st century, using computer-based remote control and automation."),
    ("SME", "Small and Medium Enterprise"),
    ("SNE", "Seconded national expert"),
    ("SOC", "Security Operations Centre. Unit that deals with security issues on an organisational and technical level."),
    ("SOP", "Standard operating procedure"),
    ("SPD", "Single programming document"),
    ("Standards", "Guidance set up and established by authority as a rule for the measure of quantity, weight, extent, value, or quality."),
    ("TA", "Temporary agent"),
    ("Threat", "An expression of intention to inflict damage."),
    ("TRANSIST", "Training of Network Security Incident Teams Staff. Course that provides affordable, high-quality training to both new and experienced Computer Security and Incident Response Team (CSIRT) personnel."),
    ("Transits", "Computer-security and incident-response team (CSIRT) personnel training"),
    ("TSP", "Trust service provider"),
    ("WP", "Work programme"),
]


# --- Live-page parser ----------------------------------------------------------

class _GlossaryParser(HTMLParser):
    """Walks the ENISA glossary page; collects (term, definition) from `<strong>`
    runs followed by free text in the same paragraph."""

    def __init__(self) -> None:
        super().__init__()
        self.in_strong = False
        self.in_h3 = False
        self.current_term: list[str] = []
        self.current_text: list[str] = []
        self.entries: list[tuple[str, str]] = []
        self._capture_text = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("strong", "b"):
            # Flush any pending entry before starting a new term
            self._flush()
            self.in_strong = True
            self._capture_text = True
        elif tag == "h3":
            self._flush()
            self.in_h3 = True
        elif tag in ("p", "br", "div"):
            # Boundary -> flush
            self._flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("strong", "b"):
            self.in_strong = False
        elif tag == "h3":
            self.in_h3 = False

    def handle_data(self, data: str) -> None:
        if self.in_strong:
            self.current_term.append(data)
        elif self.current_term:
            self.current_text.append(data)

    def _flush(self) -> None:
        if self.current_term and self.current_text:
            term = " ".join("".join(self.current_term).split()).strip(": ").strip()
            definition = " ".join("".join(self.current_text).split()).lstrip(": ").strip()
            if term and definition:
                self.entries.append((term, definition))
        self.current_term = []
        self.current_text = []


def fetch_live() -> list[tuple[str, str]]:
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        html = resp.read().decode("utf-8", errors="replace")
    parser = _GlossaryParser()
    parser.feed(html)
    parser._flush()
    return parser.entries


def get_entries() -> tuple[list[tuple[str, str]], str]:
    """Return (entries, source_tag). Falls back to embedded snapshot on error or
    if the live parse yields fewer rows than the snapshot (parser drift)."""
    try:
        live = fetch_live()
    except Exception as exc:  # network unavailable / TLS / 404
        print(f"[warn] live fetch failed ({exc}); using embedded snapshot", file=sys.stderr)
        return SNAPSHOT, "embedded-snapshot-2026-05-21"
    if len(live) < len(SNAPSHOT) * 0.9:
        print(
            f"[warn] live parse yielded {len(live)} entries vs snapshot {len(SNAPSHOT)}; "
            "using snapshot",
            file=sys.stderr,
        )
        return SNAPSHOT, "embedded-snapshot-2026-05-21"
    return live, "live-fetch"


# --- Output writers ------------------------------------------------------------

def _letter_for(term: str) -> str:
    """Letter-section anchor for a term (the only granularity ENISA's page supports)."""
    for ch in term:
        if ch.isalpha():
            return ch.upper()
    return "#"


def write_csv(entries: Iterable[tuple[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["term", "definition", "source_anchor", "notes"])
        for term, definition in entries:
            writer.writerow([term, definition, _letter_for(term), ""])


def write_json(entries: Iterable[tuple[str, str]], path: Path) -> None:
    data = [
        {
            "term": term,
            "definition": definition,
            "source_anchor": _letter_for(term),
            "notes": "",
        }
        for term, definition in entries
    ]
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def write_markdown(entries: list[tuple[str, str]], path: Path, source_tag: str) -> None:
    lines: list[str] = []
    lines.append("# ENISA Glossary of Terms")
    lines.append("")
    lines.append(f"Source: <{SOURCE_URL}>")
    lines.append("")
    lines.append(f"Total terms: {len(entries)}")
    lines.append("")
    lines.append(f"Extraction mode: `{source_tag}`")
    lines.append("")
    lines.append(
        "ENISA's published page is the European Union Agency for Cybersecurity's "
        "general glossary covering acronyms, organisational units, and core "
        "cybersecurity / data-protection concepts. The page has no per-term "
        "anchors, so terms below are grouped by their leading letter."
    )
    lines.append("")

    current_letter = ""
    for term, definition in entries:
        letter = _letter_for(term)
        if letter != current_letter:
            current_letter = letter
            lines.append(f"## {letter}")
            lines.append("")
        lines.append(f"**{term}** — {definition}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    entries, source_tag = get_entries()
    # De-duplicate while preserving order
    seen = set()
    deduped: list[tuple[str, str]] = []
    for term, definition in entries:
        key = (term.lower(), definition.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append((term, definition))

    md_path = OUT_DIR / "enisa-glossary.md"
    csv_path = OUT_DIR / "enisa-glossary-terms.csv"
    json_path = OUT_DIR / "enisa-glossary-terms.json"

    write_markdown(deduped, md_path, source_tag)
    write_csv(deduped, csv_path)
    write_json(deduped, json_path)

    print(f"Wrote {len(deduped)} terms ({source_tag})")
    print(f"  - {md_path}")
    print(f"  - {csv_path}")
    print(f"  - {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
