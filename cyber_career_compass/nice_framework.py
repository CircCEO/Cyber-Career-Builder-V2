"""
NIST NICE Framework logic engine for Cyber Career Compass.
Maps weighted category scores (SP, PR, AN, IN, OM) to work roles and certifications.
"""

from dataclasses import dataclass
from typing import List, Optional

# Seven NIST NICE categories for radar chart and weighted attribution
CATEGORY_SP = "SP"  # Securely Provision
CATEGORY_PR = "PR"  # Protect and Defend
CATEGORY_AN = "AN"  # Analyze
CATEGORY_CO = "CO"  # Collect and Operate
CATEGORY_IN = "IN"  # Investigate
CATEGORY_OM = "OM"  # Operate and Maintain
CATEGORY_OV = "OV"  # Oversee and Govern

ALL_CATEGORIES: List[str] = [
    CATEGORY_SP, CATEGORY_PR, CATEGORY_AN, CATEGORY_CO,
    CATEGORY_IN, CATEGORY_OM, CATEGORY_OV,
]

# Legacy aptitude mapping: dominant category -> work role key
APTITUDE_BUILDER = "Builder"   # SP, OM, OV
APTITUDE_GUARDIAN = "Guardian"  # PR, CO
APTITUDE_INVESTIGATOR = "Investigator"  # AN, IN

KNOWLEDGE_LEVEL_0 = 0  # Entry / foundational
KNOWLEDGE_LEVEL_1 = 1  # Intermediate


def _category_to_aptitude(category: str) -> str:
    """Map dominant NICE category to legacy aptitude for work role lookup."""
    if category in (CATEGORY_SP, CATEGORY_OM, CATEGORY_OV):
        return APTITUDE_BUILDER
    if category in (CATEGORY_PR, CATEGORY_CO):
        return APTITUDE_GUARDIAN
    return APTITUDE_INVESTIGATOR


@dataclass
class WorkRole:
    """NICE Framework work role."""
    id: str
    title: str
    category: str
    definition: str
    strengths_summary: str


@dataclass
class Certification:
    """Certification recommendation with optional URL for roadmap links."""
    name: str
    issuer: str
    level: str  # "Entry" or "Intermediate"
    url: Optional[str] = None


# Work roles by (legacy_aptitude, knowledge_level)
WORK_ROLES: dict = {
    (APTITUDE_BUILDER, KNOWLEDGE_LEVEL_0): WorkRole(
        id="SP-SSE",
        title="Secure Software Assessor",
        category="Securely Provision (SP)",
        definition="Assesses the security of software and systems through testing and analysis.",
        strengths_summary="You excel at structured assessment and building security into the development lifecycle.",
    ),
    (APTITUDE_BUILDER, KNOWLEDGE_LEVEL_1): WorkRole(
        id="SP-ARC",
        title="Security Architect",
        category="Securely Provision (SP)",
        definition="Designs and builds secure systems, networks, and architectures.",
        strengths_summary="You combine design thinking with security principles to create resilient systems.",
    ),
    (APTITUDE_GUARDIAN, KNOWLEDGE_LEVEL_0): WorkRole(
        id="PR-CDA",
        title="Cyber Defense Analyst",
        category="Protect and Defend (PR)",
        definition="Monitors and analyzes events to protect systems and respond to incidents.",
        strengths_summary="You thrive in defending systems and responding to threats in real time.",
    ),
    (APTITUDE_GUARDIAN, KNOWLEDGE_LEVEL_1): WorkRole(
        id="PR-IR",
        title="Incident Responder",
        category="Protect and Defend (PR)",
        definition="Investigates and mitigates security incidents and coordinates response activities.",
        strengths_summary="You lead under pressure and coordinate teams to contain and remediate incidents.",
    ),
    (APTITUDE_INVESTIGATOR, KNOWLEDGE_LEVEL_0): WorkRole(
        id="AN-TWA",
        title="Threat/Warning Analyst",
        category="Analyze (AN)",
        definition="Analyzes threat data and produces assessments and warnings for decision makers.",
        strengths_summary="You connect dots across data to surface threats and inform strategy.",
    ),
    (APTITUDE_INVESTIGATOR, KNOWLEDGE_LEVEL_1): WorkRole(
        id="IN-CLI",
        title="Cyber Crime Investigator",
        category="Investigate (IN)",
        definition="Investigates cyber crimes and compiles evidence for legal proceedings.",
        strengths_summary="You pursue leads methodically and build cases that stand up to scrutiny.",
    ),
}

# Certification URLs for recommended roadmap (official or info pages)
CERT_URLS: dict = {
    "CompTIA Security+": "https://www.comptia.org/certifications/security",
    "GIAC Secure Software Programmer (GSSP)": "https://www.giac.org/certifications/secure-software-programmer-gssp",
    "Certified Secure Software Lifecycle Professional (CSSLP)": "https://www.isc2.org/certifications/csslp",
    "GIAC Cloud Security Automation (GCSA)": "https://www.giac.org/certifications/cloud-security-automation-gcsa",
    "GIAC Security Essentials (GSEC)": "https://www.giac.org/certifications/security-essentials-gsec",
    "GIAC Certified Incident Handler (GCIH)": "https://www.giac.org/certifications/certified-incident-handler-gcih",
    "Certified Incident Handler (ECIH)": "https://www.eccouncil.org/certifications/certified-incident-handler-ecih/",
    "CompTIA Cybersecurity Analyst (CySA+)": "https://www.comptia.org/certifications/cybersecurity-analyst",
    "GIAC Cyber Threat Intelligence (GCTI)": "https://www.giac.org/certifications/cyber-threat-intelligence-gcti",
    "GIAC Certified Forensic Analyst (GCFA)": "https://www.giac.org/certifications/certified-forensic-analyst-gcfa",
    "Certified Cyber Forensics Professional (CCFP)": "https://www.isc2.org/certifications/ccfp",
    "CISSP": "https://www.isc2.org/certifications/cissp",
}

# Certifications by (aptitude, knowledge_level)
CERTIFICATIONS: dict = {
    (APTITUDE_BUILDER, KNOWLEDGE_LEVEL_0): [
        Certification("CompTIA Security+", "CompTIA", "Entry", CERT_URLS.get("CompTIA Security+")),
        Certification("GIAC Secure Software Programmer (GSSP)", "GIAC", "Entry", CERT_URLS.get("GIAC Secure Software Programmer (GSSP)")),
    ],
    (APTITUDE_BUILDER, KNOWLEDGE_LEVEL_1): [
        Certification("Certified Secure Software Lifecycle Professional (CSSLP)", "ISC²", "Intermediate", CERT_URLS.get("Certified Secure Software Lifecycle Professional (CSSLP)")),
        Certification("GIAC Cloud Security Automation (GCSA)", "GIAC", "Intermediate", CERT_URLS.get("GIAC Cloud Security Automation (GCSA)")),
    ],
    (APTITUDE_GUARDIAN, KNOWLEDGE_LEVEL_0): [
        Certification("CompTIA Security+", "CompTIA", "Entry", CERT_URLS.get("CompTIA Security+")),
        Certification("GIAC Security Essentials (GSEC)", "GIAC", "Entry", CERT_URLS.get("GIAC Security Essentials (GSEC)")),
    ],
    (APTITUDE_GUARDIAN, KNOWLEDGE_LEVEL_1): [
        Certification("GIAC Certified Incident Handler (GCIH)", "GIAC", "Intermediate", CERT_URLS.get("GIAC Certified Incident Handler (GCIH)")),
        Certification("Certified Incident Handler (ECIH)", "EC-Council", "Intermediate", CERT_URLS.get("Certified Incident Handler (ECIH)")),
    ],
    (APTITUDE_INVESTIGATOR, KNOWLEDGE_LEVEL_0): [
        Certification("CompTIA Cybersecurity Analyst (CySA+)", "CompTIA", "Entry", CERT_URLS.get("CompTIA Cybersecurity Analyst (CySA+)")),
        Certification("GIAC Cyber Threat Intelligence (GCTI)", "GIAC", "Entry", CERT_URLS.get("GIAC Cyber Threat Intelligence (GCTI)")),
    ],
    (APTITUDE_INVESTIGATOR, KNOWLEDGE_LEVEL_1): [
        Certification("GIAC Certified Forensic Analyst (GCFA)", "GIAC", "Intermediate", CERT_URLS.get("GIAC Certified Forensic Analyst (GCFA)")),
        Certification("Certified Cyber Forensics Professional (CCFP)", "ISC²", "Intermediate", CERT_URLS.get("Certified Cyber Forensics Professional (CCFP)")),
    ],
}


def get_work_role(dominant_category: str, knowledge_level: int) -> WorkRole:
    """Return the NICE work role for the given dominant category and knowledge level."""
    aptitude = _category_to_aptitude(dominant_category)
    key = (aptitude, knowledge_level)
    if key not in WORK_ROLES:
        key = (aptitude, KNOWLEDGE_LEVEL_0)
    return WORK_ROLES[key]


def get_certifications(dominant_category: str, knowledge_level: int) -> List[Certification]:
    """Return the first two certifications for the roadmap (with URLs)."""
    aptitude = _category_to_aptitude(dominant_category)
    key = (aptitude, knowledge_level)
    if key not in CERTIFICATIONS:
        key = (aptitude, KNOWLEDGE_LEVEL_0)
    return CERTIFICATIONS[key][:2]


# Work role IDs including 2026 NIST NICE (OG-WRL-017 Supply Chain, NF-COM-008 DevSecOps)
ALL_ROLE_IDS: List[str] = [
    "SP-SSE", "SP-ARC", "PR-CDA", "PR-IR", "AN-TWA", "IN-CLI",
    "OG-WRL-017", "NF-COM-008",
]

# Weighted match: each role gets a score from category contributions (percentages)
ROLE_CATEGORY_WEIGHTS: dict = {
    "SP-SSE": {CATEGORY_SP: 0.55, CATEGORY_OM: 0.30, CATEGORY_OV: 0.15},
    "SP-ARC": {CATEGORY_SP: 0.60, CATEGORY_OM: 0.25, CATEGORY_OV: 0.15},
    "PR-CDA": {CATEGORY_PR: 0.60, CATEGORY_CO: 0.30, CATEGORY_AN: 0.10},
    "PR-IR": {CATEGORY_PR: 0.55, CATEGORY_CO: 0.25, CATEGORY_IN: 0.20},
    "AN-TWA": {CATEGORY_AN: 0.60, CATEGORY_IN: 0.25, CATEGORY_OV: 0.15},
    "IN-CLI": {CATEGORY_IN: 0.60, CATEGORY_AN: 0.25, CATEGORY_OV: 0.15},
    "OG-WRL-017": {CATEGORY_OV: 0.50, CATEGORY_AN: 0.25, CATEGORY_PR: 0.25},
    "NF-COM-008": {CATEGORY_SP: 0.50, CATEGORY_OM: 0.35, CATEGORY_CO: 0.15},
}


def get_category_label(cat_id: str) -> str:
    """Human-readable label for radar chart (7 NIST NICE categories)."""
    labels = {
        CATEGORY_SP: "Securely Provision",
        CATEGORY_PR: "Protect & Defend",
        CATEGORY_AN: "Analyze",
        CATEGORY_CO: "Collect & Operate",
        CATEGORY_IN: "Investigate",
        CATEGORY_OM: "Operate & Maintain",
        CATEGORY_OV: "Oversee & Govern",
    }
    return labels.get(cat_id, cat_id)
