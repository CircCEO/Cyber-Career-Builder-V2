"""
Proving Grounds content: TKS Validation pool and Calibration (20 Personality + 10 Core = 30 questions).
Aligned to NIST NICE Task/Knowledge/Skill statements. Used by Proving Grounds and scoring.
"""

import random
from typing import Dict, List, Optional, Any

from .nice_framework import (
    CATEGORY_SP,
    CATEGORY_PR,
    CATEGORY_AN,
    CATEGORY_CO,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
)
from .questions import Question, Choice, get_explorer_instinct_questions, get_technical_questions


def _w(*pairs: Any) -> Dict[str, float]:
    d: Dict[str, float] = {}
    for i in range(0, len(pairs), 2):
        d[str(pairs[i])] = float(pairs[i + 1])
    return d


# 25-question Validation: NICE pool — TKS-aligned (Task, Knowledge, Skill). 3 choices each.
TKS_VALIDATION_PROMPTS: List[str] = [
    "RMF Step 1 (Categorize) requires:",
    "Incident triage prioritization should be based on:",
    "A Security Control Assessor validates controls using:",
    "Contingency plan testing should include:",
    "Vulnerability remediation tracking is most effective when:",
    "Authority to Operate (ATO) is granted by:",
    "Security awareness training content should be:",
    "As IR coordinator, your first step after declaration is:",
    "A security architecture review should address:",
    "SIEM use cases should be:",
    "Supply chain risk (OG-WRL-017) management includes:",
    "Secure development (TKS) integrates:",
    "Board security reporting should emphasize:",
    "Identity governance (2026) includes:",
    "Zero Trust architecture assumes:",
    "Threat intelligence (TKS) is used to:",
    "Digital forensics (IN) chain of custody requires:",
    "Security orchestration (SOAR) automates:",
    "Cloud security posture management (CSPM) focuses on:",
    "Penetration testing scope is defined by:",
    "Security metrics (KPI) should align with:",
    "Incident post-mortem should produce:",
    "Vendor risk assessment should cover:",
    "Red team exercises should:",
    "Security operations center (SOC) tiering supports:",
]

# 25 rows × 3 choices: each row is [weights_choice0, weights_choice1, weights_choice2]
TKS_VALIDATION_WEIGHTS: List[List[Dict[str, float]]] = [
    [_w(CATEGORY_SP, 0.6, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_CO, 0.2), _w(CATEGORY_PR, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_CO, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_CO, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.4), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.3)],
    [_w(CATEGORY_AN, 0.6, CATEGORY_IN, 0.25), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_IN, 0.6, CATEGORY_AN, 0.25), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_SP, 0.3)],
    [_w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.4), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_PR, 0.5, CATEGORY_IN, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_SP, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_PR, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
]

# 25 × 3 choice texts (correct / best answer first per row for scoring)
TKS_VALIDATION_CHOICES: List[List[str]] = [
    ["System boundary and impact level per FIPS 199/200.", "Only hardware inventory.", "Skip categorization."],
    ["Impact to CIA and alignment with IR plan.", "Ticket arrival order only.", "System hostname only."],
    ["NIST SP 800-53A assessment procedures and evidence.", "Checklist only.", "Vendor attestation only."],
    ["Backup/restore tests and RTO/RPO alignment.", "Documentation only.", "No testing."],
    ["Risk-ranked findings, assigned owners, and closure tracking.", "Ad-hoc patching.", "Ignore findings."],
    ["The Authorizing Official based on risk acceptance.", "The system owner only.", "No formal decision."],
    ["Role-based, measured by behavior and knowledge.", "Single annual video only.", "Optional."],
    ["Activate IR plan, assign roles, establish comms, preserve evidence.", "Wait for management.", "Image all systems first."],
    ["Data flows, trust boundaries, authn/authz, and requirements.", "Vendor reputation only.", "UI only."],
    ["Tied to threats and controls; tuned; reviewed for coverage.", "Defaults only.", "Post-breach only."],
    ["Due diligence, contracts, continuous monitoring, offboarding.", "One-time assessment.", "No lifecycle."],
    ["IDE and pipeline; training and reviews.", "Optional guidelines.", "Not adopted."],
    ["Risk posture, metrics, regulatory alignment.", "Technical jargon only.", "Incident-only."],
    ["Lifecycle, access reviews, least privilege.", "Provisioning only.", "No governance."],
    ["Verify explicitly; assume breach; identity and context.", "Trust internal network.", "Single login."],
    ["Inform detection, response, and strategy.", "Ignore.", "Archive only."],
    ["Documented handling, integrity, and continuity.", "No documentation.", "Copy only."],
    ["Playbook execution and analyst workflow.", "Manual only.", "No automation."],
    ["Misconfigurations and compliance drift.", "On-prem only.", "Ignore cloud."],
    ["Rules of engagement and authorized scope.", "No scope.", "Unlimited scope."],
    ["Business and regulatory objectives.", "Technical only.", "No alignment."],
    ["Lessons learned and actionable improvements.", "Blame only.", "No report."],
    ["Security posture and contract requirements.", "NDA only.", "No assessment."],
    ["Real adversaries; detection and response.", "Isolated tests only.", "Avoid disruption."],
    ["Escalation paths and analyst specialization.", "No tiering.", "Single tier."],
]


def get_tks_validation_pool(lang: Optional[str] = None) -> List[Question]:
    """Return the full 25-question Validation: NICE pool. Shuffle order when used for a run."""
    pool: List[Question] = []
    for i in range(min(len(TKS_VALIDATION_PROMPTS), len(TKS_VALIDATION_WEIGHTS), len(TKS_VALIDATION_CHOICES))):
        prompt = TKS_VALIDATION_PROMPTS[i]
        choices_raw = TKS_VALIDATION_CHOICES[i]
        weights_list = TKS_VALIDATION_WEIGHTS[i]
        choices = [
            Choice(choices_raw[j], weights_list[j] if j < len(weights_list) else weights_list[0])
            for j in range(len(choices_raw))
        ]
        pool.append(Question(prompt=prompt, choices=choices, correct_index=0))
    return pool


def get_tks_validation_questions(lang: Optional[str] = None, n: int = 25, shuffle: bool = True) -> List[Question]:
    """Return n questions from the TKS Validation pool (default 25). Optionally shuffle."""
    pool = get_tks_validation_pool(lang)
    if shuffle:
        pool = list(pool)
        random.shuffle(pool)
    return pool[:n]


# ─── Calibration: 20 Personality + 10 Core = 30 questions (replaces 25-question block) ───
CALIBRATION_PERSONALITY_COUNT = 20
CALIBRATION_CORE_COUNT = 10
CALIBRATION_TOTAL = CALIBRATION_PERSONALITY_COUNT + CALIBRATION_CORE_COUNT  # 30


def get_calibration_questions(lang: Optional[str] = None, shuffle_personality: bool = True) -> List[Question]:
    """
    Return exactly 30 questions for Proving Ground Calibration:
    - 20 Personality Scenarios (NIST TKS/Work Role mapping): 10 Explorer Instinct + 10 from TKS Validation pool.
    - 10 Core Technical Scenarios.
    Order: 20 personality first, then 10 core. Personality block can be shuffled.
    """
    personality: List[Question] = []
    # 10 from Explorer Instinct (personality)
    instinct = get_explorer_instinct_questions(lang)
    personality.extend(instinct[:10])
    # 10 more from TKS Validation pool (scenario/personality-style)
    tks_pool = list(get_tks_validation_pool(lang))
    if shuffle_personality:
        random.shuffle(tks_pool)
    for q in tks_pool:
        if len(personality) >= CALIBRATION_PERSONALITY_COUNT:
            break
        personality.append(q)
    personality = personality[:CALIBRATION_PERSONALITY_COUNT]

    core = get_technical_questions(lang)[:CALIBRATION_CORE_COUNT]
    return personality + core
