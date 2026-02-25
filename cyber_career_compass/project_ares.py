"""
Project Ares NIST NICE Guide v1.0.0 — direct training pipeline.
Source: Project Ares NIST NICE Guide v1.0.0 (Circadence). Learning Path, Battle Room,
and Mission mappings to NIST NICE v1.0.0 work roles.
Maps skill gaps (below 65% competency) to NIST Work Roles and Project Ares
Battle Rooms (BR) / Missions (M) with Training Value from the official guide.
Capability Gap Engine: competency baseline per work role, calculate_gaps(), and
Recommended Training Deployments linked to Ares Battle Rooms.
"""

from typing import Any, Dict, List, Optional, Tuple

# Competency threshold: below this we show Recommended Training Deployments (Project Ares)
COMPETENCY_THRESHOLD = 65.0

# ─── Competency Baseline: per Work Role (e.g. 65%) ───────────────────────────
# Default baseline for TKS areas (NICE categories) and for work roles when not overridden.
DEFAULT_COMPETENCY_BASELINE = 65.0

# Competency baseline (0–100) per NICE work role ID. Below this = gap for that role.
# Work role IDs from Project Ares NIST NICE Guide v1.0.0 (PDF).
COMPETENCY_BASELINE_PER_WORK_ROLE: Dict[str, float] = {
    "PD-WRL-001": 65.0,  # Defensive Cybersecurity
    "PD-WRL-002": 65.0,  # Digital Forensics
    "PD-WRL-003": 65.0,  # Incident Response
    "PD-WRL-004": 65.0,  # Infrastructure Support
    "PD-WRL-006": 65.0,  # Threat Analysis
    "PD-WRL-007": 65.0,  # Vulnerability Analysis
    "IO-WRL-004": 65.0,  # Network Operations
    "IO-WRL-005": 65.0,  # Systems Administration
    "IO-WRL-006": 65.0,  # Systems Security Analysis
    "IN-WRL-001": 65.0,  # Cybercrime Investigation
    "IN-WRL-002": 65.0,  # Digital Evidence Analysis
}
# App work role IDs use the same default unless mapped to a NICE role with a custom baseline
COMPETENCY_BASELINE_PER_APP_ROLE: Dict[str, float] = {
    "SP-SSE": 65.0,
    "SP-ARC": 65.0,
    "PR-CDA": 65.0,
    "PR-IR": 65.0,
    "AN-TWA": 65.0,
    "IN-CLI": 65.0,
    "OG-WRL-017": 65.0,
    "NF-COM-008": 65.0,
}

# App work role ID → NIST NICE v1.0.0 work role ID (from Project Ares guide)
APP_ROLE_TO_NICE_ID: Dict[str, str] = {
    "PR-CDA": "PD-WRL-001",   # Cyber Defense Analyst / Defensive Cybersecurity
    "PR-IR": "PD-WRL-003",    # Incident Responder / Incident Response
    "SP-SSE": "PD-WRL-007",   # Secure Software Assessor → Vulnerability Analysis
    "SP-ARC": "PD-WRL-007",   # Security Architect → Vulnerability / Defensive
    "AN-TWA": "PD-WRL-006",   # Threat/Warning Analyst → Threat Analysis
    "IN-CLI": "IN-WRL-001",   # Cyber Crime Investigator
    "OG-WRL-017": "PD-WRL-001",
    "NF-COM-008": "IO-WRL-005",
}

# NIST NICE v1.0.0 role ID → learning path key (per Project Ares NIST NICE Guide v1.0.0 PDF)
NICE_ROLE_TO_LEARNING_PATH_KEY: Dict[str, str] = {
    "PD-WRL-001": "endpoint_security",           # Defensive Cybersecurity
    "PD-WRL-002": "endpoint_security",           # Digital Forensics
    "PD-WRL-003": "advanced_networking",        # Incident Response
    "PD-WRL-004": "windows_fundamentals",        # Infrastructure Support (BR6, BR21, BR1004)
    "PD-WRL-006": "advanced_networking",        # Threat Analysis
    "PD-WRL-007": "computer_networking",        # Vulnerability Analysis
    "IO-WRL-004": "computer_networking",        # Network Operations
    "IO-WRL-005": "windows_fundamentals",        # Systems Administration
    "IO-WRL-006": "intermediate_endpoint_security",  # Systems Security Analysis
    "IN-WRL-001": "advanced_networking",        # Cybercrime Investigation
    "IN-WRL-002": "advanced_networking",        # Digital Evidence Analysis
}

# Battle Room / Mission ID → title and Training Value excerpt (from PDF)
ARES_SCENARIOS: Dict[str, Dict[str, str]] = {
    "BR1": {
        "title": "System Integrator",
        "training_value": "Vulnerability scanning, reconnaissance, and firewall analysis. Aligns with Defensive Cybersecurity and Vulnerability Analysis roles.",
    },
    "BR2": {
        "title": "Network Analyst",
        "training_value": "Configuring Snort, analyzing packet captures with Wireshark/tcpdump. Directly supports Network Operations, Incident Response, and Defensive Cybersecurity.",
    },
    "BR5": {
        "title": "Intel Analyst",
        "training_value": "All-Source and Cyber Intelligence Planning. Supports threat analysis and target network analysis.",
    },
    "BR6": {
        "title": "Linux Basics",
        "training_value": "File management, permissions, process monitoring. Essential for Systems Administration and Technical Support.",
    },
    "BR8": {
        "title": "Network Traffic Analysis",
        "training_value": "Packet analysis for incident response and digital forensics. Critical for Network Operations, Defensive Cybersecurity, and Threat Analysis.",
    },
    "BR9": {
        "title": "Forensics",
        "training_value": "Digital evidence analysis and forensic investigation techniques. Aligns with Digital Forensics and Cybercrime Investigation roles.",
    },
    "BR10": {
        "title": "Python Scripting Fundamentals",
        "training_value": "Automation and analysis scripts for security and system administration. Supports Secure Software Development and Systems Administration.",
    },
    "BR11": {
        "title": "System Security Analyst",
        "training_value": "Systems monitoring, configuration, and security analysis. Aligns with Systems Security Analysis, Incident Response, and Defensive Cybersecurity.",
    },
    "BR21": {
        "title": "PowerShell Fundamentals",
        "training_value": "Command-line scripting and automation for system and network management. Supports Systems Administration and Incident Response.",
    },
    "BR1001": {
        "title": "Windows Fundamentals 1: File System",
        "training_value": "File system management and security controls. Foundation for Systems Administration and Digital Evidence Analysis.",
    },
    "BR1002": {
        "title": "Windows Fundamentals 2: Services",
        "training_value": "Managing processes, services, and scheduled tasks. Essential for Systems Administration and Incident Response.",
    },
    "BR1003": {
        "title": "Windows Fundamentals 3: Registry",
        "training_value": "Registry management and forensic analysis. Supports Systems Security, Digital Forensics, and Incident Response.",
    },
    "BR1004": {
        "title": "Windows Fundamentals 4: Networking",
        "training_value": "Network settings, troubleshooting, and connectivity. Aligns with Network Operations and Systems Administration.",
    },
    "M1E": {
        "title": "Disable Botnet",
        "training_value": "Incident response and cyberspace operations to take down C2 infrastructure. Aligns with Incident Response and Digital Forensics.",
    },
    "M2E": {
        "title": "Stop Terrorist Financing",
        "training_value": "Digital evidence analysis, cybercrime investigation, and threat assessment. Supports multi-role investigative operations.",
    },
    "M3E": {
        "title": "Intercept Attack Plans",
        "training_value": "Vulnerability analysis and penetration testing. Supports Exploitation Analysis and Target Network Analysis.",
    },
    "M4E": {
        "title": "Stop Malicious Processes",
        "training_value": "Incident response, digital forensics, and stopping data exfiltration. Critical for Incident Response and Defensive Cybersecurity.",
    },
    "M5E": {
        "title": "Protect Financial Institution",
        "training_value": "Malware response, digital forensics, and defensive cybersecurity. Aligns with Incident Response and Defensive Cybersecurity.",
    },
    "M8E": {
        "title": "Defend ICS/SCADA System",
        "training_value": "Incident response and defense of critical infrastructure. Essential for ICS/SCADA security and Defensive Cybersecurity.",
    },
    "M9E": {
        "title": "Manipulate Industrial Control System",
        "training_value": "Cyberspace operations and vulnerability analysis for industrial systems. Supports Exploitation Analysis and ICS security.",
    },
    "M10E": {
        "title": "Ransomware",
        "training_value": "Incident response, digital forensics, and defending against ransomware. Critical for Defensive Cybersecurity and Incident Response.",
    },
}

# NIST role ID → recommended scenario IDs (BR/M) that address that role's gaps (from PDF)
NICE_ROLE_TO_SCENARIOS: Dict[str, List[str]] = {
    "PD-WRL-001": ["BR8", "M4E", "M10E", "M5E", "BR11", "BR2"],
    "PD-WRL-002": ["BR9", "M4E", "M5E", "M10E", "M8E", "BR1001", "BR1003"],
    "PD-WRL-003": ["M10E", "M4E", "M5E", "M8E", "BR8", "BR2", "BR11", "M1E"],
    "PD-WRL-004": ["BR6", "BR21", "BR1004", "M8E", "M10E"],
    "PD-WRL-006": ["BR2", "BR8", "BR5", "M4E", "M5E", "M10E"],
    "PD-WRL-007": ["BR1", "BR8", "M8E", "M5E", "M10E", "M3E"],
    "IO-WRL-004": ["BR1004", "BR2", "BR8", "BR6", "M4E", "M8E"],
    "IO-WRL-005": ["BR1001", "BR1002", "BR1003", "BR1004", "BR6", "BR21", "BR10"],
    "IO-WRL-006": ["BR11", "BR21", "BR1004", "M8E", "M10E"],
    "IN-WRL-001": ["BR9", "BR2", "M4E", "M5E", "M10E", "M2E", "M1E"],
    "IN-WRL-002": ["BR9", "BR1001", "M2E", "M4E", "M5E", "BR1003", "BR1004"],
}

# NIST category (highest-scoring) → primary NICE role for strength-based Project Ares recommendations
NIST_CATEGORY_TO_NICE_ROLE: Dict[str, str] = {
    "PR": "PD-WRL-001",   # Protect and Defend → Cyber Defense Analyst
    "CO": "IO-WRL-005",   # Collect and Operate → Windows/systems
    "SP": "PD-WRL-007",   # Securely Provision → Vulnerability / Defensive
    "AN": "PD-WRL-006",   # Analyze → Threat/Warning Analyst
    "IN": "IN-WRL-001",   # Investigate → Cyber Crime Investigator
    "OM": "IO-WRL-004",   # Operate and Maintain → Network/sysadmin
    "OV": "PD-WRL-001",   # Oversee and Govern → Defensive/oversight
}


def get_closest_nice_role_id(role_id: str) -> str:
    """Return NIST NICE v1.0.0 role ID for the app's work role."""
    return APP_ROLE_TO_NICE_ID.get(role_id, "PD-WRL-001")


def get_learning_path_key_for_role(nice_role_id: str) -> str:
    """Return Project Ares learning path key for the NICE role. Localize with get_ares_learning_path(lang, key)."""
    return NICE_ROLE_TO_LEARNING_PATH_KEY.get(nice_role_id, "computer_networking")


def get_baseline_for_work_role(nice_role_id: str) -> float:
    """Return the competency baseline (0–100) for a NICE work role ID."""
    return COMPETENCY_BASELINE_PER_WORK_ROLE.get(nice_role_id, DEFAULT_COMPETENCY_BASELINE)


def get_baseline_for_app_role(app_role_id: str) -> float:
    """Return the competency baseline (0–100) for an app work role ID (e.g. PR-CDA)."""
    return COMPETENCY_BASELINE_PER_APP_ROLE.get(app_role_id, DEFAULT_COMPETENCY_BASELINE)


def calculate_gaps(
    score_state: Any,
    lang: Optional[str] = None,
    tks_baseline: Optional[float] = None,
    max_deployments: int = 8,
) -> Dict[str, Any]:
    """
    Capability Gap Engine: identify TKS areas and work roles below competency baseline,
    and generate Recommended Training Deployments linked to Ares Battle Rooms.

    Returns a dict with:
      - tks_areas_below: List of (category_id, user_score, baseline) for categories below threshold
      - work_roles_below: List of (role_id, match_pct, baseline) for roles below threshold
      - recommended_training_deployments: List of deployment dicts (id, title, training_value, learning_path, type)
        linked to Ares Battle Rooms / Missions for the identified gaps.
    """
    from .nice_framework import ALL_CATEGORIES, ALL_ROLE_IDS
    from .translations import get_ares_learning_path, get_ares_scenario_title

    lang_key = lang or "en"
    baseline = tks_baseline if tks_baseline is not None else DEFAULT_COMPETENCY_BASELINE

    user_scores = score_state.get_normalized_radar_scores()
    role_probs = score_state.get_role_probabilities()

    # 1) TKS areas (NICE categories) below threshold
    tks_areas_below: List[Tuple[str, float, float]] = []
    for cat in ALL_CATEGORIES:
        score = user_scores.get(cat, 0.0)
        if score < baseline:
            tks_areas_below.append((cat, score, baseline))
    tks_areas_below.sort(key=lambda x: x[1])  # smallest score first (largest gap)

    # 2) Work roles below their competency baseline
    work_roles_below: List[Tuple[str, float, float]] = []
    for role_id in ALL_ROLE_IDS:
        match_pct = role_probs.get(role_id, 0.0)
        role_baseline = get_baseline_for_app_role(role_id)
        if match_pct < role_baseline:
            work_roles_below.append((role_id, match_pct, role_baseline))
    work_roles_below.sort(key=lambda x: x[1])  # smallest match first

    # 3) Recommended Training Deployments: Ares BR/M for roles below baseline (and for gap categories)
    seen_sids: set = set()
    deployments: List[Dict[str, str]] = []

    # Collect NICE role IDs that need training (from app roles below baseline)
    nice_roles_to_fill: List[str] = []
    for role_id, _, _ in work_roles_below:
        nice_id = get_closest_nice_role_id(role_id)
        if nice_id not in nice_roles_to_fill:
            nice_roles_to_fill.append(nice_id)

    # If no roles below baseline, still recommend by dominant role or by TKS gaps (map category to NICE role)
    if not nice_roles_to_fill and tks_areas_below:
        for cat, _, _ in tks_areas_below:
            nice_id = NIST_CATEGORY_TO_NICE_ROLE.get(cat)
            if nice_id and nice_id not in nice_roles_to_fill:
                nice_roles_to_fill.append(nice_id)

    if not nice_roles_to_fill:
        dominant = score_state.get_dominant_aptitude()
        nice_id = NIST_CATEGORY_TO_NICE_ROLE.get(dominant, "PD-WRL-001")
        nice_roles_to_fill = [nice_id]

    for nice_id in nice_roles_to_fill:
        if len(deployments) >= max_deployments:
            break
        scenario_ids = NICE_ROLE_TO_SCENARIOS.get(nice_id, ["BR8", "M10E", "M4E", "BR9"])
        learning_path_key = get_learning_path_key_for_role(nice_id)
        learning_path = get_ares_learning_path(lang_key, learning_path_key)
        for sid in scenario_ids:
            if len(deployments) >= max_deployments:
                break
            if sid in seen_sids:
                continue
            info = ARES_SCENARIOS.get(sid)
            if not info:
                continue
            seen_sids.add(sid)
            title = get_ares_scenario_title(lang_key, sid)
            deployments.append({
                "id": sid,
                "title": title,
                "training_value": info["training_value"],
                "learning_path": learning_path,
                "learning_path_key": learning_path_key,
                "type": "M" if sid.startswith("M") else "BR",
            })

    return {
        "tks_areas_below": tks_areas_below,
        "work_roles_below": work_roles_below,
        "recommended_training_deployments": deployments,
    }


def get_recommended_deployments(
    score_state: Any,
    lang: Optional[str] = None,
    max_cards: int = 4,
) -> List[Dict[str, str]]:
    """
    When user is below COMPETENCY_THRESHOLD, return recommended Project Ares
    Battle Room / Mission deployments for their closest NIST Work Role.
    Each item: { "id", "title", "training_value", "learning_path", "learning_path_key", "type" } (type = "BR" or "M").
    title and learning_path are localized when lang is provided.
    """
    from .nice_framework import get_work_role, ALL_CATEGORIES
    from .translations import get_ares_learning_path, get_ares_scenario_title

    lang_key = lang or "en"
    user_scores = score_state.get_normalized_radar_scores()
    avg = sum(user_scores.get(c, 0) for c in ALL_CATEGORIES) / len(ALL_CATEGORIES) if ALL_CATEGORIES else 0
    if avg >= COMPETENCY_THRESHOLD:
        return []

    dominant = score_state.get_dominant_aptitude()
    knowledge_level = score_state.get_knowledge_level()
    role = get_work_role(dominant, knowledge_level)
    nice_id = get_closest_nice_role_id(role.id)
    learning_path_key = get_learning_path_key_for_role(nice_id)
    learning_path = get_ares_learning_path(lang_key, learning_path_key)
    scenario_ids = NICE_ROLE_TO_SCENARIOS.get(nice_id, ["BR8", "M10E", "M4E", "BR9"])

    deployments: List[Dict[str, str]] = []
    for sid in scenario_ids:
        if len(deployments) >= max_cards:
            break
        info = ARES_SCENARIOS.get(sid)
        if not info:
            continue
        title = get_ares_scenario_title(lang_key, sid)
        deployments.append({
            "id": sid,
            "title": title,
            "training_value": info["training_value"],
            "learning_path": learning_path,
            "learning_path_key": learning_path_key,
            "type": "M" if sid.startswith("M") else "BR",
        })
    return deployments


def get_recommended_deployments_by_top_category(
    score_state: Any,
    lang: Optional[str] = None,
    max_cards: int = 4,
) -> List[Dict[str, str]]:
    """
    Project Ares recommendations based on the user's highest-scoring NIST category (strength-based).
    Each item: { "id", "title", "training_value", "learning_path", "learning_path_key", "type" }.
    """
    from .nice_framework import ALL_CATEGORIES
    from .translations import get_ares_learning_path, get_ares_scenario_title

    lang_key = lang or "en"
    user_scores = score_state.get_normalized_radar_scores()
    if not user_scores:
        return []
    top_category = max(user_scores.items(), key=lambda x: x[1])[0]
    nice_id = NIST_CATEGORY_TO_NICE_ROLE.get(top_category, "PD-WRL-001")
    learning_path_key = get_learning_path_key_for_role(nice_id)
    learning_path = get_ares_learning_path(lang_key, learning_path_key)
    scenario_ids = NICE_ROLE_TO_SCENARIOS.get(nice_id, ["BR8", "M10E", "M4E", "BR9"])

    deployments: List[Dict[str, str]] = []
    for sid in scenario_ids:
        if len(deployments) >= max_cards:
            break
        info = ARES_SCENARIOS.get(sid)
        if not info:
            continue
        title = get_ares_scenario_title(lang_key, sid)
        deployments.append({
            "id": sid,
            "title": title,
            "training_value": info["training_value"],
            "learning_path": learning_path,
            "learning_path_key": learning_path_key,
            "type": "M" if sid.startswith("M") else "BR",
        })
    return deployments
