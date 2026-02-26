"""
Instinct (Personality), Technical (Triage), and Deep-Scenario questions for Cyber Career Compass.
Choices use a weighted matrix: each option contributes to multiple NIST NICE categories
(e.g., 80% Protect and Defend, 20% Investigate).

Mission-tier API (imported by main.py):
- get_explorer_questions()  → 20 items (10 Instinct + 10 NIST Foundations)
- get_specialist_questions() → 50 items (5 Instinct + 10 Technical + 16 Deep + 19 TKS)
- get_operator_questions()  → 12 items (mission scenarios)
All question text is sourced from cyber_career_compass.translations.
"""

# Public API: mission-tier functions first for clean importing
__all__ = [
    "get_explorer_questions",
    "get_specialist_questions",
    "get_operator_questions",
    "Question",
    "Choice",
    "get_instinct_questions",
    "get_technical_questions",
    "get_deep_scenario_questions",
    "get_personality_scenarios_questions",
    "get_operator_question_branch",
    "get_explorer_instinct_questions",
    "get_explorer_foundations_questions",
    "get_specialist_tks_questions",
    "get_all_questions_for_flow",
    "shuffle_choices_for_display",
]

import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Union, Tuple

from cyber_career_compass.nice_framework import (
    CATEGORY_SP,
    CATEGORY_PR,
    CATEGORY_AN,
    CATEGORY_CO,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
)

# Weights must sum to 1.0 per choice for consistency (optional but preferred)


@dataclass
class Choice:
    """Single answer choice with weighted contribution to NICE categories."""
    text: str
    weights: Dict[str, float]  # e.g. {"PR": 0.8, "IN": 0.2}
    knowledge: Optional[int] = None  # 0 or 1 for technical correctness (when correct_index is set)


@dataclass
class Question:
    """Question with choices and optional correct index for technical scoring."""
    prompt: str
    choices: List[Choice]
    correct_index: Optional[int] = None  # 0-based index of correct answer (technical/deep)


def _w(*pairs: Any) -> Dict[str, float]:
    """Helper: build weight dict from (cat, value), (cat, value), ..."""
    d: Dict[str, float] = {}
    for i in range(0, len(pairs), 2):
        d[str(pairs[i])] = float(pairs[i + 1])
    return d


# —— Instinct (Personality) — 5 questions ——
# Weights spread across SP, PR, AN, IN, OM as appropriate.
INSTINCT_QUESTIONS: List[Question] = [
    Question(
        prompt="When something breaks in production, your first instinct is to:",
        choices=[
            Choice("Design a fix and improve the system so it doesn't happen again.", _w(CATEGORY_SP, 0.85, CATEGORY_OM, 0.15)),
            Choice("Contain the impact and protect users while others fix it.", _w(CATEGORY_PR, 0.8, CATEGORY_IN, 0.2)),
            Choice("Trace the root cause and document what happened before changing anything.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5)),
        ],
    ),
    Question(
        prompt="You're most energized when:",
        choices=[
            Choice("Creating or improving a secure product or architecture.", _w(CATEGORY_SP, 0.9, CATEGORY_OM, 0.1)),
            Choice("Stopping an attack or defending a critical asset.", _w(CATEGORY_PR, 0.9, CATEGORY_IN, 0.1)),
            Choice("Uncovering how an attacker got in or what they were after.", _w(CATEGORY_IN, 0.6, CATEGORY_AN, 0.4)),
        ],
    ),
    Question(
        prompt="In a team crisis, you naturally:",
        choices=[
            Choice("Propose a new process or tool to prevent recurrence.", _w(CATEGORY_SP, 0.7, CATEGORY_OM, 0.3)),
            Choice("Take charge of communication and containment.", _w(CATEGORY_PR, 0.8, CATEGORY_OM, 0.2)),
            Choice("Gather evidence and timeline before assigning blame.", _w(CATEGORY_IN, 0.6, CATEGORY_AN, 0.4)),
        ],
    ),
    Question(
        prompt="Your ideal project is one where you:",
        choices=[
            Choice("Build something that stays secure by design.", _w(CATEGORY_SP, 0.9, CATEGORY_OM, 0.1)),
            Choice("Monitor and respond to real-world threats.", _w(CATEGORY_PR, 0.7, CATEGORY_AN, 0.3)),
            Choice("Analyze patterns and produce intelligence others act on.", _w(CATEGORY_AN, 0.8, CATEGORY_IN, 0.2)),
        ],
    ),
    Question(
        prompt="Feedback you value most is:",
        choices=[
            Choice("'The system you designed held up under stress.'", _w(CATEGORY_SP, 0.8, CATEGORY_OM, 0.2)),
            Choice("'Your response saved us from a major breach.'", _w(CATEGORY_PR, 0.9, CATEGORY_IN, 0.1)),
            Choice("'Your analysis changed how we see the threat landscape.'", _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)),
        ],
    ),
]

# —— Personality Scenarios — 20 grey-area cybersecurity dilemmas ——
# Archetype mapping: A = Analyze / Protect & Defend, B = Investigate / Collect & Operate, C = Oversee & Govern / Securely Provision
PERSONALITY_SCENARIOS: List[Question] = [
    Question(
        prompt="You detect a breach in a hospital network. Do you shut down the system immediately to stop the spread (risking patient lives) or keep it running while you hunt the intruder (risking data theft)?",
        choices=[
            Choice("Shut down affected systems immediately to contain the breach, then assess impact.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Keep systems up while you collect evidence and trace the intruder in real time.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Escalate to leadership and follow the documented incident response plan; let governance decide.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A zero-day is being exploited in critical infrastructure you help protect. Do you disclose publicly immediately to force patches, or work with the vendor privately first?",
        choices=[
            Choice("Assess impact and coordinate with the vendor under embargo; go public only if they delay.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Collect indicators and hunt for active exploitation while sharing privately with trusted partners.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow coordinated disclosure policy and ensure patches are ready before public disclosure.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="An employee is suspected of exfiltrating sensitive data. Do you confront them immediately or gather evidence first?",
        choices=[
            Choice("Analyze logs and risk; contain access quickly while building a clear picture before any confrontation.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Investigate silently: collect artifacts, trace data flows, and document the chain of evidence.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Escalate to HR and legal; follow policy on insider threat and let governance drive next steps.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="Ransomware has encrypted your payment systems. Paying the ransom could restore service in hours; refusing means days of recovery and lost revenue.",
        choices=[
            Choice("Assess business impact and legal guidance; prioritize containment and recovery over paying.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Preserve encrypted systems for forensics while restoring from backup; do not pay.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow the organization's ransomware playbook and get executive approval before any payment decision.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A researcher published a critical vulnerability in your product before contacting you. Do you treat them as hostile or try to partner?",
        choices=[
            Choice("Analyze the finding and impact; respond professionally and fix before it spreads.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Investigate how they found it and what else might be exposed; improve detection and response.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Enforce your disclosure policy and improve secure development so this does not recur.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A legacy system cannot be patched and runs critical operations. Do you keep it running with compensating controls or force an upgrade and accept business disruption?",
        choices=[
            Choice("Assess risk and document compensating controls; recommend a phased replacement timeline.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Monitor and segment it; collect telemetry to detect abuse while planning migration.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Govern through policy: require exception process, risk acceptance, and a funded remediation plan.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A key vendor had a breach and did not notify you for weeks. Do you terminate the contract or work with them to fix and monitor?",
        choices=[
            Choice("Evaluate impact to your environment and contractual obligations; contain then decide.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Investigate what was accessed and whether your data was affected; improve vendor monitoring.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Invoke contract terms and governance; require remediation and stronger security requirements going forward.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="You suspect an insider threat but narrowing the investigation could mean invading privacy of innocent staff. Do you monitor broadly or focus only on high-risk individuals?",
        choices=[
            Choice("Use risk-based criteria to scope the investigation and minimize unnecessary data access.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Collect and correlate evidence across systems to identify the source before restricting anyone.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Ensure all monitoring follows policy and legal review; get approval for any expanded scope.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="You have strong evidence of a nation-state campaign against your sector. Do you go public to raise awareness or stay quiet to protect an ongoing investigation?",
        choices=[
            Choice("Weigh public interest and investigation value; share with authorities and trusted peers first.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Continue investigating and collecting evidence; share indicators through trusted channels only.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow disclosure and classification policy; let leadership and legal decide on public statements.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A cloud misconfiguration exposed customer data. Do you notify all affected immediately or fix the exposure first and then notify?",
        choices=[
            Choice("Contain the exposure immediately and assess scope; notify as soon as impact is understood.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Preserve logs and fix the misconfiguration; determine exactly what was accessed before notification.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow incident and breach notification procedures; coordinate with legal and comms per policy.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="The CEO wants to skip security review for a critical product launch to meet a deadline. Do you comply or refuse and delay the launch?",
        choices=[
            Choice("Present the risk clearly and propose a time-boxed mitigation; let leadership accept or defer risk.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Document what would be skipped and what could go wrong; recommend a short review window.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Enforce the security gate; no launch without sign-off per policy.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A penetration test found critical issues days before an external audit. Do you fix quietly and pass the audit or document and report the findings (risking audit failure)?",
        choices=[
            Choice("Assess which findings the audit would catch; fix the worst and document the rest with timelines.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Preserve test evidence and remediate; be transparent with auditors about recent discovery.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow audit and remediation policy; report findings and request a realistic remediation plan.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="Law enforcement requests access to encrypted data in a criminal investigation. Your policy is unclear. Do you comply to support the investigation or refuse on principle?",
        choices=[
            Choice("Analyze the request against legal and policy; provide only what is legally required and documented.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Preserve evidence and chain of custody; ensure any handover is documented and lawful.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Escalate to legal and governance; no disclosure without clear authority and policy alignment.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="You discover a serious vulnerability in a competitor's product. Do you report it responsibly or consider using it for competitive advantage?",
        choices=[
            Choice("Assess the risk to the ecosystem and your reputation; report responsibly and document it.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Document the finding and share through a neutral channel; avoid any appearance of misuse.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow responsible disclosure and ethics policy; do not use for competitive gain.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A contractor has excessive access for convenience and the project is almost done. Do you revoke access now and slow delivery or leave it until the project ends?",
        choices=[
            Choice("Evaluate residual risk for the short remainder; restrict to minimum needed and monitor closely.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Audit what they have accessed; reduce scope and ensure no sensitive data remains in their hands.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Enforce access policy; no exception for convenience—reduce access and document the exception.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A partner organization suffered a breach that may have exposed your shared data. Do you disclose to your customers immediately or wait until impact is confirmed?",
        choices=[
            Choice("Assess likelihood and impact to your systems and data; notify customers when scope is clear.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Investigate what was shared with the partner and what could have been taken; then communicate.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow breach notification and contract obligations; coordinate with legal and the partner.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="The SIEM is overwhelming the team with alerts. Do you tune down to reduce noise (and risk missing real threats) or keep all alerts and push for more staff?",
        choices=[
            Choice("Prioritize by risk and business impact; tune to high-value alerts and document the residual risk.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Keep collection broad but improve correlation and automation so analysts focus on real incidents.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Govern through SLA and capacity; get approval for tuning changes and document coverage gaps.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A critical patch will break a legacy integration. Do you deploy the patch and fix the integration (operational pain) or delay the patch and accept the vulnerability?",
        choices=[
            Choice("Assess the exploitability of the vulnerability versus the impact of the break; recommend a timeline.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Deploy in a test environment and work with ops to fix the integration before production rollout.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow change and risk acceptance process; no long-term delay without formal exception and remediation plan.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="An internal whistleblower leaked details of security failures to the press. Do you treat it as a breach and investigate the leak or focus on fixing the failures and protecting the whistleblower?",
        choices=[
            Choice("Assess the damage from both the leak and the underlying failures; prioritize remediation and transparency.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Investigate how the information left and what else might be at risk; fix the root causes.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Follow whistleblower and incident policy; protect the individual and address the security gaps per governance.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
    Question(
        prompt="A subsidiary has weaker security posture. Do you enforce group standards (cost and resistance) or allow local control and accept higher risk?",
        choices=[
            Choice("Assess the actual risk to the group and critical assets; push for targeted improvements first.", _w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5)),
            Choice("Improve visibility and monitoring of the subsidiary; reduce risk through detection and response.", _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5)),
            Choice("Enforce group security policy and fund remediation; no permanent exception without board-level acceptance.", _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)),
        ],
    ),
]

# Canonical weights for Personality Scenarios (A=AN+PR, B=IN+CO, C=OV+SP) — for i18n
CANONICAL_PERSONALITY_SCENARIOS_WEIGHTS: List[List[Dict[str, float]]] = [
    [_w(CATEGORY_AN, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_IN, 0.5, CATEGORY_CO, 0.5), _w(CATEGORY_OV, 0.5, CATEGORY_SP, 0.5)]
] * 20

# —— Technical (Triage) — 10 questions ——
TECHNICAL_QUESTIONS: List[Question] = [
    Question(
        prompt="What does 'defense in depth' emphasize?",
        choices=[
            Choice("Multiple layers of security controls so one failure doesn't compromise the system.", _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), 1),
            Choice("A single strong firewall at the perimeter.", _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.4), 0),
            Choice("Encryption only.", _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.5), 0),
            Choice("Physical security only.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="Which best describes a zero-trust approach?",
        choices=[
            Choice("Never trust, always verify; assume breach.", _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), 1),
            Choice("Trust only the internal network.", _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.5), 0),
            Choice("Trust only after one login.", _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.6), 0),
            Choice("Trust only physical access.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What is the primary goal of an incident response plan?",
        choices=[
            Choice("Contain, eradicate, recover, and learn from security incidents.", _w(CATEGORY_PR, 0.7, CATEGORY_IN, 0.3), 1),
            Choice("Prevent all incidents from ever occurring.", _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), 0),
            Choice("Blame the right team.", _w(CATEGORY_IN, 0.5, CATEGORY_AN, 0.5), 0),
            Choice("Only document incidents.", _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What does 'phishing' typically rely on?",
        choices=[
            Choice("Social engineering and deceptive communication to steal credentials or data.", _w(CATEGORY_AN, 0.4, CATEGORY_PR, 0.6), 1),
            Choice("Only technical exploits in software.", _w(CATEGORY_SP, 0.5, CATEGORY_IN, 0.5), 0),
            Choice("Physical theft of devices.", _w(CATEGORY_OM, 0.5, CATEGORY_IN, 0.5), 0),
            Choice("Encryption weaknesses.", _w(CATEGORY_SP, 0.5, CATEGORY_AN, 0.5), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="Why is patch management important?",
        choices=[
            Choice("To fix known vulnerabilities and reduce attack surface.", _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.6), 1),
            Choice("Only to add new features.", _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4), 0),
            Choice("To slow down systems.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), 0),
            Choice("Only for compliance paperwork.", _w(CATEGORY_AN, 0.4, CATEGORY_OM, 0.6), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What is the role of multi-factor authentication (MFA)?",
        choices=[
            Choice("Require more than one proof of identity to reduce risk of credential compromise.", _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), 1),
            Choice("Replace passwords entirely with one factor.", _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4), 0),
            Choice("Only for high-level executives.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), 0),
            Choice("To simplify login.", _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What does 'least privilege' mean?",
        choices=[
            Choice("Users and processes get only the minimum access needed to do their job.", _w(CATEGORY_SP, 0.6, CATEGORY_PR, 0.4), 1),
            Choice("Everyone gets admin rights for convenience.", _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4), 0),
            Choice("Only one person has any access.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), 0),
            Choice("Privilege is based on job title only.", _w(CATEGORY_AN, 0.4, CATEGORY_OM, 0.6), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="Why is logging and monitoring important in security?",
        choices=[
            Choice("To detect anomalies, investigate incidents, and support accountability.", _w(CATEGORY_PR, 0.4, CATEGORY_AN, 0.4, CATEGORY_IN, 0.2), 1),
            Choice("Only for compliance audits.", _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5), 0),
            Choice("To slow down systems.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), 0),
            Choice("To replace firewalls.", _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What is a common goal of security awareness training?",
        choices=[
            Choice("Reduce human error and improve recognition of social engineering.", _w(CATEGORY_PR, 0.5, CATEGORY_AN, 0.5), 1),
            Choice("Replace all technical controls.", _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.5), 0),
            Choice("Only to satisfy auditors.", _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5), 0),
            Choice("To teach everyone to code.", _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4), 0),
        ],
        correct_index=0,
    ),
    Question(
        prompt="What does 'confidentiality, integrity, availability' (CIA triad) represent?",
        choices=[
            Choice("Core security objectives: protect secrecy, accuracy, and access to data/systems.", _w(CATEGORY_SP, 0.4, CATEGORY_PR, 0.4, CATEGORY_AN, 0.2), 1),
            Choice("A single tool that does everything.", _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4), 0),
            Choice("Only physical security.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), 0),
            Choice("A government agency.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5), 0),
        ],
        correct_index=0,
    ),
]

# —— Deep-Scenario: 16 total (5 trend + 10 NIST + 1 regional). Weights in CANONICAL_DEEP_WEIGHTS.
DEEP_SCENARIO_QUESTIONS: List[Question] = [
    # 5 trend
    Question(
        prompt="Your organization is rolling out an AI-powered threat detection tool. Your priority is to:",
        choices=[
            Choice("Define secure development and validation criteria so the model isn't poisoned or evaded.", _w(CATEGORY_SP, 0.8, CATEGORY_AN, 0.2)),
            Choice("Monitor live alerts and tune response playbooks when the AI flags incidents.", _w(CATEGORY_PR, 0.7, CATEGORY_OM, 0.3)),
            Choice("Audit the training data and model behavior to document risks and explainability.", _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)),
        ],
    ),
    Question(
        prompt="A critical vendor in your supply chain reports a breach. Your first focus is:",
        choices=[
            Choice("Harden procurement and vendor assessment so future contracts enforce security requirements.", _w(CATEGORY_SP, 0.6, CATEGORY_AN, 0.4)),
            Choice("Contain exposure: isolate affected systems and coordinate with the vendor on containment.", _w(CATEGORY_PR, 0.8, CATEGORY_IN, 0.2)),
            Choice("Map the vendor's access and data flows, then produce a risk assessment for leadership.", _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)),
        ],
    ),
    Question(
        prompt="Cloud governance is being centralized. You prefer to:",
        choices=[
            Choice("Design and implement guardrails (e.g., IaC policies, landing zones) so teams can move fast safely.", _w(CATEGORY_SP, 0.8, CATEGORY_OM, 0.2)),
            Choice("Operate and maintain the secure baseline: patch, monitor, and respond to misconfigurations.", _w(CATEGORY_OM, 0.7, CATEGORY_PR, 0.3)),
            Choice("Analyze cloud activity and compliance drift to report gaps and recommend controls.", _w(CATEGORY_AN, 0.6, CATEGORY_IN, 0.4)),
        ],
    ),
    Question(
        prompt="You discover a third-party library used in your app has a critical CVE. Your instinct is to:",
        choices=[
            Choice("Patch or replace the dependency and add SBOM and dependency checks to the pipeline.", _w(CATEGORY_SP, 0.7, CATEGORY_OM, 0.3)),
            Choice("Assess impact, apply mitigations, and coordinate with ops and dev for a fix.", _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.4)),
            Choice("Trace where the library is used and document the blast radius for incident and risk reports.", _w(CATEGORY_IN, 0.5, CATEGORY_AN, 0.5)),
        ],
    ),
    Question(
        prompt="Leadership asks how to prepare for AI-driven attacks (e.g., deepfakes, automated exploits). You emphasize:",
        choices=[
            Choice("Building security into AI systems and defenses (e.g., adversarial testing, model assurance).", _w(CATEGORY_SP, 0.8, CATEGORY_AN, 0.2)),
            Choice("Strengthening detection and response so we can recognize and contain novel attack patterns.", _w(CATEGORY_PR, 0.7, CATEGORY_AN, 0.3)),
            Choice("Investing in threat intelligence and forensics to understand and attribute AI-enabled campaigns.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5)),
        ],
    ),
    # 10 NIST (RMF, triage, SCA, contingency, vuln mgmt, ATO, awareness, IR coord, arch review, SIEM)
    Question(
        prompt="Your organization is implementing the Risk Management Framework (RMF). Your primary task is to:",
        choices=[
            Choice("Categorize the system, select and tailor NIST SP 800-53 controls, and document the security plan.", _w(CATEGORY_SP, 0.6, CATEGORY_OV, 0.3, CATEGORY_OM, 0.1)),
            Choice("Execute continuous monitoring and report control status to the authorizing official.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3, CATEGORY_OV, 0.1)),
            Choice("Conduct security assessments and produce the authorization package for the AO.", _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)),
        ],
    ),
    Question(
        prompt="During incident triage, you prioritize events by:",
        choices=[
            Choice("Impact to confidentiality, integrity, availability and alignment with the incident response plan.", _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3, CATEGORY_IN, 0.3)),
            Choice("Order of arrival so no ticket is left behind.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_OV, 0.2)),
            Choice("Which system generated the alert, regardless of business criticality.", _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3, CATEGORY_CO, 0.3)),
        ],
    ),
    Question(
        prompt="A security control assessment (SCA) is due. You focus on:",
        choices=[
            Choice("Testing controls per NIST SP 800-53A and documenting findings with evidence and remediation plans.", _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)),
            Choice("Running the scanning tools and forwarding reports to the assessment team.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2)),
            Choice("Drafting the system security plan and leaving testing to the assessor.", _w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3, CATEGORY_OM, 0.2)),
        ],
    ),
    Question(
        prompt="Contingency planning for a critical system requires:",
        choices=[
            Choice("Documented contingency plans, tested backup/restore, and alignment with recovery objectives (RTO/RPO).", _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3, CATEGORY_OV, 0.1)),
            Choice("Only maintaining backups; restoration is handled during an incident.", _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.4, CATEGORY_CO, 0.1)),
            Choice("A single annual tabletop exercise with no updates to the plan.", _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)),
        ],
    ),
    Question(
        prompt="Vulnerability management (scanning and remediation) is most effective when:",
        choices=[
            Choice("Scans are scheduled, results are risk-ranked and assigned to owners, and remediation is tracked to closure.", _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_OV, 0.2)),
            Choice("Scans run only after a major incident.", _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3, CATEGORY_CO, 0.1)),
            Choice("All findings are treated equally and patching is done only during maintenance windows.", _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.4, CATEGORY_IN, 0.2)),
        ],
    ),
    Question(
        prompt="To achieve Authority to Operate (ATO), you ensure:",
        choices=[
            Choice("The security assessment is complete, the authorization package is ready, and the AO can make a risk-based decision.", _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)),
            Choice("All controls are fully implemented with no exceptions before the assessment.", _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_OV, 0.2)),
            Choice("Only the system owner signs the authorization; no AO is required.", _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3, CATEGORY_CO, 0.3)),
        ],
    ),
    Question(
        prompt="Security awareness training is designed to support NICE tasks when:",
        choices=[
            Choice("Content is role-based, covers policy and threats (e.g., phishing), and is measured by behavior and knowledge checks.", _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_CO, 0.2)),
            Choice("Everyone watches the same annual video with no assessment.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2)),
            Choice("Training is optional and only for new hires.", _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3, CATEGORY_IN, 0.2)),
        ],
    ),
    Question(
        prompt="As incident response coordinator, your first steps after declaration are:",
        choices=[
            Choice("Activate the IR plan, assign roles, establish communication channels, and begin containment and evidence preservation.", _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2, CATEGORY_IN, 0.2)),
            Choice("Wait for management to decide whether to respond.", _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.4)),
            Choice("Start forensic imaging on all systems before containing the threat.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)),
        ],
    ),
    Question(
        prompt="A security architecture review of a new application should address:",
        choices=[
            Choice("Data flows, trust boundaries, authentication/authorization, and alignment with security requirements and standards.", _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.2, CATEGORY_OV, 0.2)),
            Choice("Only whether the vendor is reputable.", _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.4)),
            Choice("Only the look and feel of the login page.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)),
        ],
    ),
    Question(
        prompt="Security operations use cases (e.g., in a SIEM) should be:",
        choices=[
            Choice("Tied to threats and controls, tuned to reduce false positives, and reviewed for coverage and effectiveness.", _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2)),
            Choice("Left at default and never updated.", _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3, CATEGORY_CO, 0.2)),
            Choice("Defined only after a major breach.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)),
        ],
    ),
    # 1 regional (EN)
    Question(
        prompt="Your organization must align with a regional cybersecurity framework (e.g., NIST CSF, sector guidelines). You prioritize:",
        choices=[
            Choice("Mapping existing controls to the framework and closing gaps with a prioritized roadmap.", _w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3, CATEGORY_OM, 0.2)),
            Choice("Ensuring operations and monitoring support continuous compliance and evidence collection.", _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.4, CATEGORY_OM, 0.2)),
            Choice("Producing executive summaries and audit-ready reports for regulators and boards.", _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)),
        ],
    ),
]


# Canonical weights only (for i18n: text from translations, weights from here)
CANONICAL_INSTINCT_WEIGHTS: List[List[Dict[str, float]]] = [
    [_w(CATEGORY_SP, 0.85, CATEGORY_OM, 0.15), _w(CATEGORY_PR, 0.8, CATEGORY_IN, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5)],
    [_w(CATEGORY_SP, 0.9, CATEGORY_OM, 0.1), _w(CATEGORY_PR, 0.9, CATEGORY_IN, 0.1), _w(CATEGORY_IN, 0.6, CATEGORY_AN, 0.4)],
    [_w(CATEGORY_SP, 0.7, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.8, CATEGORY_OM, 0.2), _w(CATEGORY_IN, 0.6, CATEGORY_AN, 0.4)],
    [_w(CATEGORY_SP, 0.9, CATEGORY_OM, 0.1), _w(CATEGORY_PR, 0.7, CATEGORY_AN, 0.3), _w(CATEGORY_AN, 0.8, CATEGORY_IN, 0.2)],
    [_w(CATEGORY_SP, 0.8, CATEGORY_OM, 0.2), _w(CATEGORY_PR, 0.9, CATEGORY_IN, 0.1), _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)],
]

# Explorer path: 10 Instinct (5 above + 5 extra) — same weight style for extra 5
CANONICAL_EXPLORER_INSTINCT_WEIGHTS: List[List[Dict[str, float]]] = CANONICAL_INSTINCT_WEIGHTS + [
    [_w(CATEGORY_SP, 0.7, CATEGORY_OM, 0.2, CATEGORY_OV, 0.1), _w(CATEGORY_PR, 0.7, CATEGORY_OM, 0.2), _w(CATEGORY_AN, 0.6, CATEGORY_IN, 0.4)],
    [_w(CATEGORY_SP, 0.8, CATEGORY_OM, 0.2), _w(CATEGORY_PR, 0.8, CATEGORY_CO, 0.2), _w(CATEGORY_AN, 0.6, CATEGORY_OV, 0.4)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.6, CATEGORY_OV, 0.4)],
    [_w(CATEGORY_SP, 0.85, CATEGORY_OM, 0.15), _w(CATEGORY_PR, 0.8, CATEGORY_IN, 0.2), _w(CATEGORY_AN, 0.7, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_SP, 0.75, CATEGORY_OM, 0.25), _w(CATEGORY_PR, 0.7, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.6, CATEGORY_OV, 0.4)],
]

# Technical: 10 questions, 4 choices, correct_index 0
CANONICAL_TECHNICAL_WEIGHTS: List[List[Dict[str, float]]] = [
    [_w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.4), _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.5), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.5), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.6), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4)],
    [_w(CATEGORY_PR, 0.7, CATEGORY_IN, 0.3), _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_IN, 0.5, CATEGORY_AN, 0.5), _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5)],
    [_w(CATEGORY_AN, 0.4, CATEGORY_PR, 0.6), _w(CATEGORY_SP, 0.5, CATEGORY_IN, 0.5), _w(CATEGORY_OM, 0.5, CATEGORY_IN, 0.5), _w(CATEGORY_SP, 0.5, CATEGORY_AN, 0.5)],
    [_w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.6), _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), _w(CATEGORY_AN, 0.4, CATEGORY_OM, 0.6)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_PR, 0.4), _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_AN, 0.4, CATEGORY_OM, 0.6)],
    [_w(CATEGORY_PR, 0.4, CATEGORY_AN, 0.4, CATEGORY_IN, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.4), _w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.5)],
    [_w(CATEGORY_PR, 0.5, CATEGORY_AN, 0.5), _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.5), _w(CATEGORY_AN, 0.5, CATEGORY_OM, 0.5), _w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.4)],
    [_w(CATEGORY_SP, 0.4, CATEGORY_PR, 0.4, CATEGORY_AN, 0.2), _w(CATEGORY_OM, 0.6, CATEGORY_SP, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.5), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5)],
]
CANONICAL_TECHNICAL_CORRECT_INDEX: int = 0  # first choice is correct for all 10

# Deep: 16 questions, 3 choices each. 15 common (5 trend + 10 NIST) + 1 regional.
CANONICAL_DEEP_WEIGHTS: List[List[Dict[str, float]]] = [
    # 5 trend
    [_w(CATEGORY_SP, 0.8, CATEGORY_AN, 0.2), _w(CATEGORY_PR, 0.7, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_AN, 0.4), _w(CATEGORY_PR, 0.8, CATEGORY_IN, 0.2), _w(CATEGORY_AN, 0.7, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_SP, 0.8, CATEGORY_OM, 0.2), _w(CATEGORY_OM, 0.7, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.6, CATEGORY_IN, 0.4)],
    [_w(CATEGORY_SP, 0.7, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.4), _w(CATEGORY_IN, 0.5, CATEGORY_AN, 0.5)],
    [_w(CATEGORY_SP, 0.8, CATEGORY_AN, 0.2), _w(CATEGORY_PR, 0.7, CATEGORY_AN, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.5)],
    # 10 NIST (RMF, triage, SCA, contingency, vuln mgmt, ATO, awareness, IR coord, arch review, SIEM)
    [_w(CATEGORY_SP, 0.6, CATEGORY_OV, 0.3, CATEGORY_OM, 0.1), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3, CATEGORY_OV, 0.1), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)],
    [_w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3, CATEGORY_IN, 0.3), _w(CATEGORY_PR, 0.7, CATEGORY_OM, 0.2, CATEGORY_IN, 0.1), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_OV, 0.2)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2), _w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3, CATEGORY_OM, 0.2)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3, CATEGORY_OV, 0.1), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.4, CATEGORY_CO, 0.1), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_OV, 0.2), _w(CATEGORY_OM, 0.6, CATEGORY_PR, 0.3, CATEGORY_CO, 0.1), _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.4, CATEGORY_IN, 0.2)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4, CATEGORY_IN, 0.1), _w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_OV, 0.2), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3, CATEGORY_CO, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OM, 0.3, CATEGORY_CO, 0.2), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3, CATEGORY_IN, 0.2)],
    [_w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2, CATEGORY_IN, 0.2), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.4), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.2, CATEGORY_OV, 0.2), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.4), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)],
    [_w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3, CATEGORY_CO, 0.2), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3, CATEGORY_CO, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)],
    # 1 regional
    [_w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.3, CATEGORY_OM, 0.2), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.4, CATEGORY_OM, 0.2), _w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3, CATEGORY_OV, 0.2)],
]

# Specialist TKS (19 questions) — 2026 NIST TKS gap analysis; 3 choices each.
def _build_specialist_tks_weights() -> List[List[Dict[str, float]]]:
    return [
        [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3)],
        [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_OV, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
        [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_CO, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3)],
        [_w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3), _w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3)],
        [_w(CATEGORY_SP, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
        [_w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_OV, 0.4, CATEGORY_AN, 0.3)],
        [_w(CATEGORY_OV, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3)],
        [_w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
        [_w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
        [_w(CATEGORY_AN, 0.5, CATEGORY_IN, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_OV, 0.4, CATEGORY_AN, 0.3)],
        [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
        [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_OV, 0.3)],
        [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.2)],
        [_w(CATEGORY_OV, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
    ]
CANONICAL_SPECIALIST_TKS_WEIGHTS: List[List[Dict[str, float]]] = _build_specialist_tks_weights()

# Operator mission: 12 scenarios (AI/Supply Chain 2026); 3 choices each.
CANONICAL_OPERATOR_WEIGHTS: List[List[Dict[str, float]]] = [
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.5, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_PR, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3)],
    [_w(CATEGORY_SP, 0.6, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_SP, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_PR, 0.6, CATEGORY_OM, 0.2), _w(CATEGORY_OV, 0.4, CATEGORY_AN, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_AN, 0.4, CATEGORY_IN, 0.3)],
    [_w(CATEGORY_AN, 0.5, CATEGORY_OV, 0.4), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_OM, 0.5, CATEGORY_PR, 0.3)],
    [_w(CATEGORY_OV, 0.5, CATEGORY_AN, 0.3), _w(CATEGORY_SP, 0.4, CATEGORY_OM, 0.3), _w(CATEGORY_PR, 0.4, CATEGORY_CO, 0.2)],
]


def get_specialist_tks_questions(lang: Optional[str] = None) -> List[Question]:
    """19 TKS gap questions for Specialist path (2026 NIST)."""
    from cyber_career_compass.translations import get_specialist_tks_texts
    l = lang or "en"
    texts = get_specialist_tks_texts(l)
    out: List[Question] = []
    for i, t in enumerate(texts):
        weights = CANONICAL_SPECIALIST_TKS_WEIGHTS[i] if i < len(CANONICAL_SPECIALIST_TKS_WEIGHTS) else CANONICAL_SPECIALIST_TKS_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices))
    return out


def get_specialist_questions(lang: Optional[str] = None) -> List[Question]:
    """50 questions for Specialist path: 5 Instinct + 10 Technical + 16 Deep + 19 TKS.
    Explicitly defined and exported for main.py mission hub."""
    return (
        get_instinct_questions(lang)
        + get_technical_questions(lang)
        + get_deep_scenario_questions(lang)
        + get_specialist_tks_questions(lang)
    )


def get_operator_questions(lang: Optional[str] = None) -> List[Question]:
    """12 mission scenario questions for Operator path (2026 AI/Supply Chain).
    Explicitly defined and exported for main.py mission hub. Linear order; use get_operator_question_branch for branching."""
    from cyber_career_compass.translations import get_operator_texts
    l = lang or "en"
    texts = get_operator_texts(l)
    out: List[Question] = []
    for i, t in enumerate(texts):
        weights = CANONICAL_OPERATOR_WEIGHTS[i] if i < len(CANONICAL_OPERATOR_WEIGHTS) else CANONICAL_OPERATOR_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices))
    return out


def get_operator_question_branch(lang: Optional[str], index: int, choice_history: List[int]) -> Optional[Question]:
    """Return Operator question at index; for index 1 and 2 use branch variant from prior choice (decision tree)."""
    from cyber_career_compass.translations import get_operator_texts_branch
    l = lang or "en"
    prior = choice_history[index - 1] if index > 0 and index <= len(choice_history) else None
    if index in (1, 2):
        prior = choice_history[index - 1] if len(choice_history) >= index else None
    t = get_operator_texts_branch(l, index, prior)
    if not t:
        return None
    weights = CANONICAL_OPERATOR_WEIGHTS[index] if index < len(CANONICAL_OPERATOR_WEIGHTS) else CANONICAL_OPERATOR_WEIGHTS[0]
    choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
    return Question(prompt=t["prompt"], choices=choices)


def get_instinct_questions(lang: Optional[str] = None) -> List[Question]:
    """Return Instinct questions; text from translations if lang given, else built-in EN."""
    if lang is None:
        return INSTINCT_QUESTIONS
    from cyber_career_compass.translations import get_instinct_texts
    texts = get_instinct_texts(lang)
    out: List[Question] = []
    for i, t in enumerate(texts):
        weights = CANONICAL_INSTINCT_WEIGHTS[i] if i < len(CANONICAL_INSTINCT_WEIGHTS) else CANONICAL_INSTINCT_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices))
    return out


def get_personality_scenarios_questions(lang: Optional[str] = None) -> List[Question]:
    """Return 20 Personality Scenario questions (grey-area dilemmas). Compatible with i18n when translations add personality scenario texts."""
    return list(PERSONALITY_SCENARIOS)


def get_technical_questions(lang: Optional[str] = None) -> List[Question]:
    """Return Technical questions; text from translations if lang given."""
    if lang is None:
        return TECHNICAL_QUESTIONS
    from cyber_career_compass.translations import get_technical_texts
    texts = get_technical_texts(lang)
    out = []
    for i, t in enumerate(texts):
        weights = CANONICAL_TECHNICAL_WEIGHTS[i] if i < len(CANONICAL_TECHNICAL_WEIGHTS) else CANONICAL_TECHNICAL_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j], 1 if j == CANONICAL_TECHNICAL_CORRECT_INDEX else 0) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices, correct_index=CANONICAL_TECHNICAL_CORRECT_INDEX))
    return out


def get_deep_scenario_questions(lang: Optional[str] = None) -> List[Question]:
    """Return 16 Deep Scenario questions (5 trend + 10 NIST + 1 regional, e.g. METI for JA)."""
    if lang is None:
        return DEEP_SCENARIO_QUESTIONS
    from cyber_career_compass.translations import get_deep_texts
    texts = get_deep_texts(lang)
    out = []
    for i, t in enumerate(texts):
        weights = CANONICAL_DEEP_WEIGHTS[i] if i < len(CANONICAL_DEEP_WEIGHTS) else CANONICAL_DEEP_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices))
    return out


def get_explorer_instinct_questions(lang: Optional[str] = None) -> List[Question]:
    """10 Instinct questions for Explorer path (5 base + 5 extra). Text from cyber_career_compass.translations."""
    from cyber_career_compass.translations import get_explorer_instinct_texts
    l = lang or "en"
    texts = get_explorer_instinct_texts(l)
    out: List[Question] = []
    for i, t in enumerate(texts):
        weights = CANONICAL_EXPLORER_INSTINCT_WEIGHTS[i] if i < len(CANONICAL_EXPLORER_INSTINCT_WEIGHTS) else CANONICAL_EXPLORER_INSTINCT_WEIGHTS[0]
        choices = [Choice(t["choices"][j], weights[j]) for j in range(len(t["choices"]))]
        out.append(Question(prompt=t["prompt"], choices=choices))
    return out


def get_explorer_foundations_questions(lang: Optional[str] = None) -> List[Question]:
    """10 NIST Foundations questions for Explorer path (same content as Technical; text from cyber_career_compass.translations when lang set)."""
    return get_technical_questions(lang)


def get_explorer_questions(lang: Optional[str] = None) -> List[Question]:
    """Return exactly 20 foundational NIST questions: 10 Instinct + 10 NIST Foundations.
    Explicitly defined and exported for main.py mission hub. All text via cyber_career_compass.translations."""
    instinct = get_explorer_instinct_questions(lang)
    foundations = get_explorer_foundations_questions(lang)
    result = instinct + foundations
    assert len(result) == 20, f"Explorer path must be 20 questions, got {len(result)}"
    return result


def get_all_questions_for_flow(lang: Optional[str] = None) -> List[Question]:
    """Instinct + Technical + Deep Scenario for full flow (used for progress)."""
    return (
        get_instinct_questions(lang)
        + get_technical_questions(lang)
        + get_deep_scenario_questions(lang)
    )


def shuffle_choices_for_display(question: Question) -> Tuple[List[str], List[Choice]]:
    """
    Return (option_texts, choice_objects) with order randomized so the correct answer
    is not always on top. Call once per question and cache in session state for consistency.
    """
    pairs = list(zip([c.text for c in question.choices], list(question.choices)))
    random.shuffle(pairs)
    return ([p[0] for p in pairs], [p[1] for p in pairs])
