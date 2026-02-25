"""
Scoring module — rebuilt from Project Ares NIST NICE Guide v1.0.0 and Gemini Prompts.

- NICE-Ares Master Dictionary: 52 NIST Work Roles → Project Ares Mission IDs and Battle Rooms.
- Weighted Attribution Matrix & ScoreState: category_scores at 0.1 baseline, add_mission_telemetry().
- Deployment Engine: get_ares_recommendations() returns Ares Mission ID, Title, Relevance for 2 lowest categories.
- Reflex State-Lock Foundation: reflex_complete = False at init; prepared for st.rerun() to reveal Ares nodes.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List, Tuple

from nice_framework import (
    CATEGORY_SP,
    CATEGORY_PR,
    CATEGORY_AN,
    CATEGORY_CO,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
    ALL_CATEGORIES,
    ALL_ROLE_IDS,
    ROLE_CATEGORY_WEIGHTS,
    KNOWLEDGE_LEVEL_0,
    KNOWLEDGE_LEVEL_1,
)


# ─── Reflex State-Lock Foundation ───────────────────────────────────────────
# Hard-code default so Mission Node Map and Recommended Training Deployments
# only render after Reflex loop completes. main.py sets st.session_state.reflex_complete = False
# at initialization; st.rerun() after the 10-threat Reflex loop sets reflex_complete = True
# to instantly reveal the Ares nodes.
REFLEX_COMPLETE_DEFAULT = False


# ─── Always-Live Radar: baseline pulse for all 7 NIST categories ──────────────
INITIAL_CATEGORY_BASELINE = 0.1


# ─── Weighted Attribution Matrix: category name/code normalization ─────────
QuestionWeights = Dict[str, float]

CATEGORY_NAME_TO_CODE: Dict[str, str] = {
    "Securely Provision": CATEGORY_SP,
    "Protect and Defend": CATEGORY_PR,
    "Protect & Defend": CATEGORY_PR,
    "Collect and Operate": CATEGORY_CO,
    "Collect & Operate": CATEGORY_CO,
    "Analyze": CATEGORY_AN,
    "Investigate": CATEGORY_IN,
    "Operate and Maintain": CATEGORY_OM,
    "Oversee and Govern": CATEGORY_OV,
    "Oversee & Govern": CATEGORY_OV,
}


def normalize_question_weights(weights: QuestionWeights) -> Dict[str, float]:
    """Convert weight keys to NICE category codes (SP, PR, AN, CO, IN, OM, OV)."""
    out: Dict[str, float] = {}
    for key, value in weights.items():
        code = CATEGORY_NAME_TO_CODE.get(key, key)
        if code in ALL_CATEGORIES:
            out[code] = out.get(code, 0.0) + value
    return out


# ─── NICE-Ares Master Dictionary (Project Ares NIST NICE Guide v1.0.0, Page 47 and full guide) ─
# Maps NIST Work Role IDs (and app IDs e.g. PR-CDA-001, AN-TWA-001) to Project Ares Battle Room / Mission IDs.
# Example: PR-CDA-001 → PD-WRL-001 (Defensive Cybersecurity) → BR1, BR8, M4E, ...; AN-TWA-001 → PD-WRL-006 (Threat Analysis) → BR2, BR8, BR5, ...
NICE_ARES_MASTER: Dict[str, List[str]] = {
    # App role IDs (PR-CDA-001 style) and NICE PD-WRL / IO-WRL / IN-WRL
    "PR-CDA-001": ["BR8", "M4E", "M10E", "M5E", "BR11", "BR2"],
    "PD-WRL-001": ["BR8", "M4E", "M10E", "M5E", "BR11", "BR2"],
    "PD-WRL-002": ["BR9", "M4E", "M5E", "M10E", "M8E", "BR1001", "BR1003"],
    "PD-WRL-003": ["M10E", "M4E", "M5E", "M8E", "BR8", "BR2", "BR11", "M1E"],
    "PD-WRL-004": ["BR6", "BR21", "BR1004", "M8E", "M10E"],
    "AN-TWA-001": ["BR2", "BR8", "BR5", "M4E", "M5E", "M10E"],
    "PD-WRL-006": ["BR2", "BR8", "BR5", "M4E", "M5E", "M10E"],
    "PD-WRL-007": ["BR1", "BR8", "M8E", "M5E", "M10E", "M3E"],
    "IO-WRL-004": ["BR1004", "BR2", "BR8", "BR6", "M4E", "M8E"],
    "IO-WRL-005": ["BR1001", "BR1002", "BR1003", "BR1004", "BR6", "BR21", "BR10"],
    "IO-WRL-006": ["BR11", "BR21", "BR1004", "M8E", "M10E"],
    "IN-WRL-001": ["BR9", "BR2", "M4E", "M5E", "M10E", "M2E", "M1E"],
    "IN-WRL-002": ["BR9", "BR1001", "M2E", "M4E", "M5E", "BR1003", "BR1004"],
    "IN-CLI-001": ["BR9", "BR2", "M4E", "M5E", "M10E", "M2E", "M1E"],
}

# NIST category → Ares scenario IDs for Deployment Engine (2 lowest categories)
NIST_CATEGORY_TO_ARES_SCENARIOS: Dict[str, List[str]] = {
    CATEGORY_PR: ["BR8", "M4E", "M10E", "M5E", "BR11", "BR2"],
    CATEGORY_SP: ["BR1", "BR8", "M8E", "M5E", "M10E", "M3E"],
    CATEGORY_AN: ["BR2", "BR8", "BR5", "M4E", "M5E", "M10E"],
    CATEGORY_CO: ["BR1001", "BR1002", "BR1003", "BR1004", "BR6", "BR21", "BR10"],
    CATEGORY_IN: ["BR9", "BR2", "M4E", "M5E", "M10E", "M2E", "M1E"],
    CATEGORY_OM: ["BR1004", "BR2", "BR8", "BR6", "M4E", "M8E"],
    CATEGORY_OV: ["BR8", "M4E", "M10E", "M5E", "BR11", "BR2"],
}


# ─── ScoreState: Weighted Attribution Matrix & Always-Live Radar ─────────────
@dataclass
class ScoreState:
    """
    Manages st.session_state-backed category_scores (via the score object stored in session).
    All 7 NIST categories initialize at INITIAL_CATEGORY_BASELINE (0.1) so the Always-Live
    Radar has a baseline pulse. add_mission_telemetry(weights) aggregates fractional points
    (e.g. {'Analyze': 0.7, 'Investigate': 0.3}) into the global state.
    """

    category_scores: Dict[str, float] = field(
        default_factory=lambda: {c: INITIAL_CATEGORY_BASELINE for c in ALL_CATEGORIES}
    )
    technical_correct: int = 0
    technical_total: int = 0

    def add_mission_telemetry(self, weights: QuestionWeights) -> None:
        """
        Aggregate fractional points from a mission/question into category_scores.
        Keys may be category codes (SP, PR, AN, ...) or names (Analyze, Investigate, ...).
        Example: add_mission_telemetry({'Analyze': 0.7, 'Investigate': 0.3})
        """
        normalized = normalize_question_weights(weights)
        for cat, value in normalized.items():
            if cat in self.category_scores:
                self.category_scores[cat] = self.category_scores.get(cat, INITIAL_CATEGORY_BASELINE) + value

    def add_weights(self, weights: QuestionWeights) -> None:
        """Alias for add_mission_telemetry for backward compatibility."""
        self.add_mission_telemetry(weights)

    def add_question_weights(self, weights: QuestionWeights) -> None:
        """Alias for add_mission_telemetry."""
        self.add_mission_telemetry(weights)

    def add_technical_result(self, correct: bool) -> None:
        self.technical_total += 1
        if correct:
            self.technical_correct += 1

    def get_category_scores(self) -> Dict[str, float]:
        """Return current raw category scores (aggregated fractional points)."""
        return dict(self.category_scores)

    def get_dominant_aptitude(self) -> str:
        """Return the dominant NICE category."""
        if not self.category_scores:
            return CATEGORY_SP
        return max(self.category_scores.items(), key=lambda x: x[1])[0]

    def get_archetype(self) -> str:
        """
        Archetype Logic Engine: analyze ScoreState and return one of four core Archetypes.
        - The Guardian (High PR / CO)
        - The Analyst (High AN / OV)
        - The Ghost (High IN)
        - The Architect (High SP / OM)
        """
        _id, _title, _desc = self.get_reveal_archetype()
        return _id

    def get_reveal_archetype(self) -> Tuple[str, str, str]:
        """
        High-Fidelity Reveal: assign one of four core Archetypes from highest-weighted NIST categories.
        Returns (archetype_id, title, description).
        """
        dominant = self.get_dominant_aptitude()
        if dominant in (CATEGORY_PR, CATEGORY_CO):
            return (
                "guardian",
                "The Guardian",
                "You protect and defend. Your profile aligns with Protect & Defend and Collect & Operate—monitoring, incident response, and securing systems at the edge.",
            )
        if dominant == CATEGORY_IN:
            return (
                "ghost",
                "The Ghost",
                "You investigate and operate in the shadows. Your profile aligns with Investigate—digital forensics, evidence analysis, and cybercrime investigation.",
            )
        if dominant in (CATEGORY_SP, CATEGORY_OM):
            return (
                "architect",
                "The Architect",
                "You build and maintain secure systems. Your profile aligns with Securely Provision and Operate & Maintain—designing defenses, hardening infrastructure, and keeping operations secure.",
            )
        if dominant in (CATEGORY_AN, CATEGORY_OV):
            return (
                "analyst",
                "The Analyst",
                "You analyze and govern. Your profile aligns with Analyze and Oversee & Govern—threat intelligence, risk assessment, and strategic security leadership.",
            )
        return (
            "guardian",
            "The Guardian",
            "Your profile aligns with defensive cybersecurity and operational readiness.",
        )

    def get_knowledge_level(self) -> int:
        """Knowledge Level 0 or 1 based on technical correct ratio."""
        if self.technical_total == 0:
            return KNOWLEDGE_LEVEL_0
        if self.technical_correct >= (self.technical_total + 1) // 2:
            return KNOWLEDGE_LEVEL_1
        return KNOWLEDGE_LEVEL_0

    def get_normalized_radar_scores(self) -> Dict[str, float]:
        """
        Scores scaled to 0–100 for the radar (relative to max).
        When max is 0, returns INITIAL_CATEGORY_BASELINE per category (Always-Live Radar pulse).
        """
        raw = self.get_category_scores()
        m = max(raw.values()) if raw else 0.0
        if m <= 0:
            return {c: INITIAL_CATEGORY_BASELINE for c in ALL_CATEGORIES}
        return {k: min(100.0, (v / m) * 100.0) for k, v in raw.items()}

    def get_top_role_match_pct(self) -> float:
        """Best work-role match percentage (0–100)."""
        probs = self.get_role_probabilities()
        return max(probs.values()) if probs else 0.0

    def get_role_probabilities(self) -> Dict[str, float]:
        """Role match percentages from category_scores and ROLE_CATEGORY_WEIGHTS."""
        raw = self.get_category_scores()
        role_scores: Dict[str, float] = {}
        for role_id in ALL_ROLE_IDS:
            weights = ROLE_CATEGORY_WEIGHTS.get(role_id, {})
            score = 0.0
            for cat, w in weights.items():
                score += raw.get(cat, 0.0) * w
            role_scores[role_id] = max(0.0, score)
        m = max(role_scores.values()) if role_scores else 1.0
        if m <= 0:
            m = 1.0
        return {rid: min(100.0, (s / m) * 100.0) for rid, s in role_scores.items()}


# ─── Deployment Engine: 2 lowest NIST categories → Ares Mission ID, Title, Relevance ─
def get_ares_recommendations(
    score_state: Any,
    max_per_category: int = 4,
) -> List[Dict[str, str]]:
    """
    Identify the 2 lowest NIST categories and return the corresponding Ares Mission ID,
    Title, and Relevance description (from Project Ares NIST NICE Guide v1.0.0 PDF text).
    Relevance is the 'Training Value' text from the guide.
    """
    from project_ares import ARES_SCENARIOS

    raw = score_state.get_category_scores()
    if not raw:
        return []

    # Two lowest categories by score (ascending)
    sorted_cats = sorted(raw.items(), key=lambda x: x[1])
    lowest_two = [sorted_cats[0][0], sorted_cats[1][0]] if len(sorted_cats) >= 2 else [sorted_cats[0][0]]

    result: List[Dict[str, str]] = []
    seen: set = set()
    for cat in lowest_two:
        scenario_ids = NIST_CATEGORY_TO_ARES_SCENARIOS.get(cat, [])
        for sid in scenario_ids[:max_per_category]:
            if sid in seen:
                continue
            seen.add(sid)
            info = ARES_SCENARIOS.get(sid)
            if not info:
                continue
            result.append({
                "mission_id": sid,
                "title": info.get("title", sid),
                "relevance": info.get("training_value", ""),
            })
    return result


# ─── XP and Agent Ranking ───────────────────────────────────────────────────
XP_PER_REFLEX_CORRECT = 5
XP_PER_INSTINCT_CHOICE = 8
XP_PER_TECHNICAL_CORRECT = 12
XP_EXPLORER_COMPLETE = 50
XP_SPECIALIST_COMPLETE = 100
XP_OPERATOR_COMPLETE = 75
XP_REFLEX_LAB_COMPLETE = 40

AGENT_RANK_THRESHOLDS = [
    (0, "Security Initiate"),
    (50, "Apprentice"),
    (150, "Agent"),
    (300, "Specialist"),
    (500, "Operator"),
]


def xp_to_rank(xp: int) -> str:
    """Return Agent Rank label for given XP total."""
    for threshold, rank in reversed(AGENT_RANK_THRESHOLDS):
        if xp >= threshold:
            return rank
    return "Security Initiate"

COMPETENCY_RAW_THRESHOLD = 2.0
