"""
CYBER-OPS // Tactical Interface — Streamlit entry point.
Ares Tactical Standard: #05070a (Deep-Space Black), #00f6ff (Neon Cyan).

Path & Mission logic:
- sys.path priority loads local questions.py (app root first; parent re-appended for cyber_career_compass).
- Explorer Mission: 20-item profile (10 Instinct + 10 NIST Foundations) via get_explorer_questions().
- Specialist: 50-item; Operator: 12-item.
"""
import sys
import textwrap
from pathlib import Path

# ─── Strict path isolation: load local questions.py only ─────────────────────
# 1. Purge search path: current folder must be sys.path[0]
_app_dir = Path(__file__).resolve().parent
_app_dir_str = str(_app_dir)
while _app_dir_str in sys.path:
    sys.path.remove(_app_dir_str)
sys.path.insert(0, _app_dir_str)

# 2. Block parent loading: remove parent directory so shadow questions.py is never used
_parent = _app_dir.parent
_parent_str = str(_parent)
while _parent_str in sys.path:
    sys.path.remove(_parent_str)
# Re-add parent only after app dir so cyber_career_compass can still be imported
sys.path.append(_parent_str)

import streamlit as st
import time
import hashlib
import random

# 3. Mission API: from local questions.py (root folder)
from questions import (
    get_explorer_questions,   # 20-item profile: 10 Instinct + 10 NIST Foundations
    get_specialist_questions, # 50-item gap analysis
    get_operator_questions,   # 12 mission scenarios
)
from cyber_career_compass.scoring import ScoreState, NIST_CATEGORY_TO_ARES_SCENARIOS
from cyber_career_compass.nice_framework import (
    get_category_label,
    get_work_role,
    get_certifications,
    ALL_CATEGORIES,
    CATEGORY_AN,
    CATEGORY_PR,
)
from ui import build_ares_radar_figure
import game  # reuse mission logic: question flow + dossier rendering

# ─── Global Operator Suite: centralized LANG_MAP for reactive i18n ─────────────────────────
LANG_OPTIONS_DISPLAY = ["日本語", "繁體中文", "English"]
LANG_VALUE_MAP = {"日本語": "ja", "繁體中文": "zh-TW", "English": "en"}

LANG_MAP = {
    "en": {
        "headline": "CIRCADENCE CYBER CAREER SIMULATOR (C3S)",
        "subtitle": "Project Ares Tactical Mission Hub",
        "system_status": "SYSTEM STATUS: NOMINAL",
        "operational_directive_exp": "Operational Directive: Assess foundational alignment with NICE work roles. 20-item profile.",
        "operational_directive_spec": "Operational Directive: Full TKS assessment against NIST 2026 framework. 50-item gap analysis.",
        "operational_directive_op": "Operational Directive: Assess readiness for Critical Infrastructure Protection (ICS/SCADA) and Ransomware Mitigation. 12 missions aligned to Project Ares Advanced Learning Paths.",
        "mission_title_explorer": "The Explorer (Foundational)",
        "mission_title_specialist": "The Specialist (Elite)",
        "mission_title_operator": "The Operator (Tier 1)",
        "vector_id_exp": "VECTOR_ID: EXP-28",
        "vector_id_spec": "VECTOR_ID: TRS-58",
        "vector_id_op": "VECTOR_ID: OP-12",
        "threat_model": "THREAT_MODEL: 2026_STANDARD",
        "trk_lock_exp": "TRK_LOCK // 0x7F2A",
        "trk_lock_spec": "TRK_LOCK // 0x83C1",
        "trk_lock_op": "TRK_LOCK // 0xE04D",
        "engage": "[ ENGAGE ]",
        "nav_mission_hub": "Mission Hub",
        "nav_proving_grounds": "Proving Grounds",
        "nav_cyber_archetype": "Cyber Archetype",
        "secure_link_mode_hub": "SECURE_LINK // MISSION_HUB",
        "secure_link_proving": "SECURE_LINK // PROVING_GROUNDS",
        "secure_link_archetype": "SECURE_LINK // CYBER_ARCHETYPE",
        "connecting": "••• CONNECTING",
        "strat_com": "STRAT-COM",
        "sync_level": "SYNC_LEVEL // %",
        "live_fire": "LIVE-FIRE // RANGE // PERS-INTEL",
        "neural_link": "[ NEURAL-LINK ]",
        "operator_id": "OPERATOR ID: [ GUARDIAN ]",
        "live_biometric": "Live Biometric",
        "skill_heatmap": "Skill Heatmap",
        "securely_provision": "Securely Provision",
        "back_to_hub": "← Back to Mission Hub",
        "breadcrumb_proving": "< SYS // PROVING_GROUNDS",
        "breadcrumb_archetype": "< SYS // CYBER_ARCHETYPE",
        "archetype_drift": "Archetype Drift // Latency + Intel Usage →",
        "validated": "VALIDATED",
        "status_active": "STATUS: ACTIVE",
        "identity": "Identity",
        "boundary": "Boundary",
        "integrity": "Integrity",
        "log_stream_analysis": "Log-stream analysis",
        "identify_event_type": "Identify event type in the stream below.",
        "traffic_monitor": "Traffic monitor",
        "select_critical_finding": "Select the critical egress finding.",
        "hash_verification": "Hash verification",
        "select_valid_sha256": "Select the valid SHA256 for policy.conf.",
        "select_reject_mismatch": "Select the line to REJECT (SHA256 mismatch).",
        "submit": "Submit",
        "gap_analysis_radar": "Gap Analysis Radar // NICE 2026 Baseline",
        "neural_career_paths": "Neural-Link career paths (cyan filaments)",
        "project_ares_bridge": "Project Ares Bridge — Mission Node Map (top 3 gaps → Battle Rooms)",
        "primary_mission_role": "Primary Mission Role",
        "recommended_certs": "Recommended certifications",
        "archetype_root": "Archetype Root",
        "language": "Language",
        "progress_answered": "Progress",
        "identity_strike": "[ IDENTITY_STRIKE ]",
        "boundary_purge": "[ BOUNDARY_PURGE ]",
        "integrity_sync": "[ INTEGRITY_SYNC ]",
        "identity_strike_instruction": "Neutralize threat strings in the 0xHEX log feed. Click the line containing MFA_BYPASS, DORMANT_USER, or NTLM_RELAY.",
        "boundary_purge_instruction": "Drop packets beaconing to rogue ports (4444, 6667, 445). Speed of drop vs proximity to Internal Network drives Archetype Drift.",
        "integrity_sync_instruction": "Two SHA256 hashes in the Holographic Scanner. Click VALIDATE if identical, REJECT if mismatch. Validating a mismatch triggers SYSTEM_STALL.",
        "neutralize": "Neutralize",
        "drop": "Drop",
        "validate": "VALIDATE",
        "reject": "REJECT",
        "system_stall": "SYSTEM_STALL",
        "system_stall_countdown": "KSA frozen — ",
        "power_cell": "Power Cell",
        "internal_network": "Internal Network",
        "packet_beaconing": "Packet beaconing to port",
        "position_to_egress": "Position",
        "to_egress": "to egress",
        "holographic_scanner": "Holographic Scanner",
        "hash_expected": "Expected",
        "hash_computed": "Computed",
        "neutralization_success": "Threat neutralized.",
        "wrong_target": "Wrong target — Chromatic Glitch.",
        "drop_recorded": "Packet dropped.",
        "module_complete": "Module complete.",
        "next_module": "Next",
    },
    "ja": {
        "headline": "CIRCADENCE CYBER CAREER SIMULATOR (C3S)",
        "subtitle": "プロジェクト・アレス 戦術ミッション Hub",
        "system_status": "SYSTEM STATUS: NOMINAL",
        "operational_directive_exp": "作戦指示: NICE ワークロールとの基礎的整合性を評価。20項目プロファイル。",
        "operational_directive_spec": "作戦指示: NIST 2026 フレームワークに基づく完全TKS評価。50項目ギャップ分析。",
        "operational_directive_op": "作戦指示: 重要インフラ保護(ICS/SCADA)およびランサムウェア対策の準備を評価。12ミッション。",
        "mission_title_explorer": "The Explorer (基礎)",
        "mission_title_specialist": "The Specialist (エリート)",
        "mission_title_operator": "The Operator (Tier 1)",
        "vector_id_exp": "VECTOR_ID: EXP-28",
        "vector_id_spec": "VECTOR_ID: TRS-58",
        "vector_id_op": "VECTOR_ID: OP-12",
        "threat_model": "THREAT_MODEL: 2026_STANDARD",
        "trk_lock_exp": "TRK_LOCK // 0x7F2A",
        "trk_lock_spec": "TRK_LOCK // 0x83C1",
        "trk_lock_op": "TRK_LOCK // 0xE04D",
        "engage": "[ ENGAGE ]",
        "nav_mission_hub": "Mission Hub",
        "nav_proving_grounds": "Proving Grounds",
        "nav_cyber_archetype": "Cyber Archetype",
        "secure_link_mode_hub": "SECURE_LINK // MISSION_HUB",
        "secure_link_proving": "SECURE_LINK // PROVING_GROUNDS",
        "secure_link_archetype": "SECURE_LINK // CYBER_ARCHETYPE",
        "connecting": "••• CONNECTING",
        "strat_com": "STRAT-COM",
        "sync_level": "SYNC_LEVEL // %",
        "live_fire": "LIVE-FIRE // RANGE // PERS-INTEL",
        "neural_link": "[ NEURAL-LINK ]",
        "operator_id": "OPERATOR ID: [ GUARDIAN ]",
        "live_biometric": "Live Biometric",
        "skill_heatmap": "Skill Heatmap",
        "securely_provision": "Securely Provision",
        "back_to_hub": "← Mission Hub に戻る",
        "breadcrumb_proving": "< SYS // PROVING_GROUNDS",
        "breadcrumb_archetype": "< SYS // CYBER_ARCHETYPE",
        "archetype_drift": "Archetype Drift // Latency + Intel Usage →",
        "validated": "VALIDATED",
        "status_active": "STATUS: ACTIVE",
        "identity": "Identity",
        "boundary": "Boundary",
        "integrity": "Integrity",
        "log_stream_analysis": "Log-stream analysis",
        "identify_event_type": "Identify event type in the stream below.",
        "traffic_monitor": "Traffic monitor",
        "select_critical_finding": "Select the critical egress finding.",
        "hash_verification": "Hash verification",
        "select_valid_sha256": "Select the valid SHA256 for policy.conf.",
        "select_reject_mismatch": "不一致の行を REJECT で選択。",
        "submit": "Submit",
        "gap_analysis_radar": "Gap Analysis Radar // NICE 2026 Baseline",
        "neural_career_paths": "Neural-Link career paths (cyan filaments)",
        "project_ares_bridge": "Project Ares Bridge — Mission Node Map",
        "primary_mission_role": "Primary Mission Role",
        "recommended_certs": "Recommended certifications",
        "archetype_root": "Archetype Root",
        "language": "言語",
        "progress_answered": "進捗",
    },
    "zh-TW": {
        "headline": "CIRCADENCE CYBER CAREER SIMULATOR (C3S)",
        "subtitle": "Project Ares 戰術任務中心",
        "system_status": "SYSTEM STATUS: NOMINAL",
        "operational_directive_exp": "作戰指令：評估與 NICE 職能之基礎對齊。20 項側寫。",
        "operational_directive_spec": "作戰指令：依 NIST 2026 框架進行完整 TKS 評估。50 項差距分析。",
        "operational_directive_op": "作戰指令：評估關鍵基礎設施保護(ICS/SCADA)與勒索軟體緩解準備度。12 項任務。",
        "mission_title_explorer": "The Explorer (基礎)",
        "mission_title_specialist": "The Specialist (菁英)",
        "mission_title_operator": "The Operator (Tier 1)",
        "vector_id_exp": "VECTOR_ID: EXP-28",
        "vector_id_spec": "VECTOR_ID: TRS-58",
        "vector_id_op": "VECTOR_ID: OP-12",
        "threat_model": "THREAT_MODEL: 2026_STANDARD",
        "trk_lock_exp": "TRK_LOCK // 0x7F2A",
        "trk_lock_spec": "TRK_LOCK // 0x83C1",
        "trk_lock_op": "TRK_LOCK // 0xE04D",
        "engage": "[ ENGAGE ]",
        "nav_mission_hub": "Mission Hub",
        "nav_proving_grounds": "Proving Grounds",
        "nav_cyber_archetype": "Cyber Archetype",
        "secure_link_mode_hub": "SECURE_LINK // MISSION_HUB",
        "secure_link_proving": "SECURE_LINK // PROVING_GROUNDS",
        "secure_link_archetype": "SECURE_LINK // CYBER_ARCHETYPE",
        "connecting": "••• CONNECTING",
        "strat_com": "STRAT-COM",
        "sync_level": "SYNC_LEVEL // %",
        "live_fire": "LIVE-FIRE // RANGE // PERS-INTEL",
        "neural_link": "[ NEURAL-LINK ]",
        "operator_id": "OPERATOR ID: [ GUARDIAN ]",
        "live_biometric": "Live Biometric",
        "skill_heatmap": "Skill Heatmap",
        "securely_provision": "Securely Provision",
        "back_to_hub": "← 返回 Mission Hub",
        "breadcrumb_proving": "< SYS // PROVING_GROUNDS",
        "breadcrumb_archetype": "< SYS // CYBER_ARCHETYPE",
        "archetype_drift": "Archetype Drift // Latency + Intel Usage →",
        "validated": "VALIDATED",
        "status_active": "STATUS: ACTIVE",
        "identity": "Identity",
        "boundary": "Boundary",
        "integrity": "Integrity",
        "log_stream_analysis": "Log-stream analysis",
        "identify_event_type": "Identify event type in the stream below.",
        "traffic_monitor": "Traffic monitor",
        "select_critical_finding": "Select the critical egress finding.",
        "hash_verification": "Hash verification",
        "select_valid_sha256": "Select the valid SHA256 for policy.conf.",
        "select_reject_mismatch": "選取要 REJECT 的 SHA256 不一致行。",
        "submit": "Submit",
        "gap_analysis_radar": "Gap Analysis Radar // NICE 2026 Baseline",
        "neural_career_paths": "Neural-Link career paths (cyan filaments)",
        "project_ares_bridge": "Project Ares Bridge — Mission Node Map",
        "primary_mission_role": "Primary Mission Role",
        "recommended_certs": "Recommended certifications",
        "archetype_root": "Archetype Root",
        "language": "語言",
        "progress_answered": "進度",
        "identity_strike": "[ IDENTITY_STRIKE ]",
        "boundary_purge": "[ BOUNDARY_PURGE ]",
        "integrity_sync": "[ INTEGRITY_SYNC ]",
        "identity_strike_instruction": "在 0xHEX 日誌中 Neutralize 威脅字串：MFA_BYPASS、DORMANT_USER、NTLM_RELAY。點擊該行。",
        "boundary_purge_instruction": "Drop 通往流氓埠 (4444, 6667, 445) 的封包。Drop 速度與距 Internal Network 距離決定 Archetype Drift。",
        "integrity_sync_instruction": "Holographic Scanner 中兩組 SHA256。相同則 VALIDATE，不同則 REJECT。對不一致按 VALIDATE 會觸發 SYSTEM_STALL。",
        "neutralize": "Neutralize",
        "drop": "Drop",
        "validate": "VALIDATE",
        "reject": "REJECT",
        "system_stall": "SYSTEM_STALL",
        "system_stall_countdown": "KSA 凍結 — ",
        "power_cell": "Power Cell",
        "internal_network": "Internal Network",
        "packet_beaconing": "封包 beaconing 至埠",
        "position_to_egress": "Position",
        "to_egress": "to egress",
        "holographic_scanner": "Holographic Scanner",
        "hash_expected": "Expected",
        "hash_computed": "Computed",
        "neutralization_success": "Threat neutralized.",
        "wrong_target": "Wrong target — Chromatic Glitch.",
        "drop_recorded": "Packet dropped.",
        "module_complete": "Module complete.",
        "next_module": "Next",
    },
}


def t(key: str) -> str:
    """Reactive i18n: return string for current language from LANG_MAP."""
    lang = st.session_state.get("lang", "en")
    return LANG_MAP.get(lang, LANG_MAP["en"]).get(key, LANG_MAP["en"].get(key, key))


def _init_session_state() -> None:
    """Ensure shared game state mirrors game.py expectations."""
    if "game_page" not in st.session_state:
        st.session_state.game_page = "mission_hub"
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if "score" not in st.session_state:
        st.session_state.score = ScoreState()
    if "all_questions" not in st.session_state:
        st.session_state.all_questions = []
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "mission_tier" not in st.session_state:
        st.session_state.mission_tier = None
    if "proving_drill_start" not in st.session_state:
        st.session_state.proving_drill_start = None  # set on first Proving Grounds render
    if "proving_identity_done" not in st.session_state:
        st.session_state.proving_identity_done = False
    if "proving_boundary_done" not in st.session_state:
        st.session_state.proving_boundary_done = False
    if "proving_integrity_done" not in st.session_state:
        st.session_state.proving_integrity_done = False
    if "proving_question_index" not in st.session_state:
        st.session_state.proving_question_index = 0
    if "proving_question_start" not in st.session_state:
        st.session_state.proving_question_start = None
    if "proving_total_start" not in st.session_state:
        st.session_state.proving_total_start = None
    if "proving_module" not in st.session_state:
        st.session_state.proving_module = "identity_strike"
    if "proving_identity_round" not in st.session_state:
        st.session_state.proving_identity_round = 0
    if "proving_boundary_round" not in st.session_state:
        st.session_state.proving_boundary_round = 0
    if "proving_integrity_round" not in st.session_state:
        st.session_state.proving_integrity_round = 0
    if "power_cell_pulses" not in st.session_state:
        st.session_state.power_cell_pulses = 0
    if "system_stall_until" not in st.session_state:
        st.session_state.system_stall_until = 0.0
    if "proving_boundary_shown_at" not in st.session_state:
        st.session_state.proving_boundary_shown_at = None
    if "chromatic_glitch_trigger" not in st.session_state:
        st.session_state.chromatic_glitch_trigger = False
    if "proving_current_round_key" not in st.session_state:
        st.session_state.proving_current_round_key = ""
    if "proving_round_started_at" not in st.session_state:
        st.session_state.proving_round_started_at = None
    if "proving_used_intel_this_round" not in st.session_state:
        st.session_state.proving_used_intel_this_round = False
    if "proving_any_intel_used" not in st.session_state:
        st.session_state.proving_any_intel_used = False
    if "proving_correct_count" not in st.session_state:
        st.session_state.proving_correct_count = 0
    if "proving_total_count" not in st.session_state:
        st.session_state.proving_total_count = 0
    if "proving_module" not in st.session_state:
        st.session_state.proving_module = "identity_strike"
    if "proving_identity_round" not in st.session_state:
        st.session_state.proving_identity_round = 0
    if "proving_boundary_round" not in st.session_state:
        st.session_state.proving_boundary_round = 0
    if "proving_integrity_round" not in st.session_state:
        st.session_state.proving_integrity_round = 0
    if "power_cell_pulses" not in st.session_state:
        st.session_state.power_cell_pulses = 0
    if "system_stall_until" not in st.session_state:
        st.session_state.system_stall_until = 0.0
    if "proving_boundary_shown_at" not in st.session_state:
        st.session_state.proving_boundary_shown_at = None
    if "chromatic_glitch_trigger" not in st.session_state:
        st.session_state.chromatic_glitch_trigger = False


def _inject_global_hud_css() -> None:
    """C3S Environmental HUD: #05070a background, Share Tech Mono global, radar-pulse on sidebar, tactical framing, 8-cell neural bar, ENGAGE reticles."""
    st.set_page_config(
        page_title="Circadence Cyber Career Simulator (C3S)",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    css = """<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* Zero-Box: absolute HUD dominance — background #05070a, strip all Streamlit borders/grey */
    :root { --ares-neon: #00f6ff; --ares-amber: #ffbf00; }
    html, body, [data-testid="stAppViewContainer"], .stApp,
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: #05070a !important;
        color: #ffffff !important;
    }
    * { font-family: "Share Tech Mono", "JetBrains Mono", monospace !important; }
    [data-testid="stSidebar"] {
        background: transparent !important;
        border-right: 1px solid rgba(0, 246, 255, 0.2);
    }
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
    .stContainer, [class*="st-emotion-cache"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="column"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stVerticalBlock"] > div { border: none !important; background: none !important; }
    section[data-testid="stSidebar"] > div { background: transparent !important; border: none !important; }
    .stMarkdown hr { display: none !important; }
    .block-container { max-width: 1300px; padding: 0 !important; padding-bottom: 1rem; background: none !important; border: none !important; }
    [data-testid="stHeader"] { border-bottom: none !important; background: transparent !important; padding: 0 !important; margin: 0 !important; min-height: 0 !important; }
    main { padding: 0 !important; padding-top: 0 !important; }
    hr { border: none !important; background: none !important; height: 0 !important; margin: 0 !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; }
    button[title="Collapse sidebar"], button[title="Expand sidebar"],
    svg[data-testid="baseIcon-keyboardDoubleArrowRight"] { display: none !important; }
    [data-testid="stSidebar"] .stMarkdown { font-family: "Share Tech Mono", "JetBrains Mono", monospace !important; }

    /* Mission Hub only: Billboard — 0.8rem max, Pure White #FFFFFF, top-left zero padding + heartbeat cyan 1.5s */
    .c3s-main-title {
        font-size: 0.8rem !important;
        letter-spacing: 0.15em;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: left;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        animation: cyber-glitch-pulse 1.5s ease-in-out infinite;
    }
    @keyframes cyber-glitch-pulse {
        0%, 100% { text-shadow: 0 0 6px #00f6ff, 0 0 12px rgba(0, 246, 255, 0.5); opacity: 1; }
        15% { text-shadow: -1px 0 #00f6ff, 1px 0 rgba(0, 246, 255, 0.7), 0 0 10px #00f6ff; opacity: 0.97; }
        30% { text-shadow: 0 0 8px #00f6ff; opacity: 1; }
        50% { text-shadow: 1px 0 #00f6ff, -1px 0 rgba(0, 246, 255, 0.4), 0 0 14px #00f6ff; opacity: 0.98; }
        70% { text-shadow: 0 0 8px #00f6ff; opacity: 1; }
        85% { text-shadow: -1px 0 #00f6ff, 0 0 10px #00f6ff; opacity: 0.99; }
    }
    /* Sub-Headers: 0.7rem Cyan #00f6ff (e.g. Project Ares Tactical Mission Hub) */
    .c3s-subtitle {
        font-size: 0.7rem !important;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
        color: #00f6ff !important;
        margin: 0 0 1rem 0;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
    }
    .connecting-status { position: absolute; top: 0; right: 0; font-size: 0.7rem; letter-spacing: 0.2em; color: #00f6ff; }
    /* Sub-pages: technical breadcrumb only */
    .sys-breadcrumb {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        color: #00FF00;
        margin: 0 0 1rem 0;
        text-align: left;
    }

    /* Page 1 Mission cards: 480px height lock for horizontal [ ENGAGE ] line */
    .mission-card {
        position: relative;
        min-height: 480px !important;
        height: 480px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 1.5rem 1.75rem 1.75rem 2rem;
        overflow: visible;
    }
    .mission-card .corner-bracket {
        position: absolute;
        width: 18px;
        height: 18px;
        border-color: #00f6ff;
        border-style: solid;
        border-width: 0;
        pointer-events: none;
    }
    .mission-card .corner-tl { top: 0; left: 0; border-top-width: 2px; border-left-width: 2px; }
    .mission-card .corner-br { bottom: 0; right: 0; border-bottom-width: 2px; border-right-width: 2px; }
    /* Diegetic: ONLY asymmetric cyan brackets (#00f6ff) tl+br; Zero-Box: no background, border, shadow */
    /* Hex anchor: 0.6 opacity cyan in top-left bracket of each card (e.g. 0xE04D, 0x7F2A, 0x8B3C) */
    .mission-hex-tl {
        position: absolute;
        top: 4px;
        left: 6px;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.6rem;
        font-weight: 700;
        color: #00f6ff;
        opacity: 0.6;
        letter-spacing: 0.08em;
    }
    /* Metadata: SYSTEM STATUS Tactical Green #00FF00; TRK_LOCK + hex Pure White #FFFFFF */
    .mission-status {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-weight: 700;
        font-size: 0.62rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #00FF00;
        margin-bottom: 0.5rem;
        padding-top: 1.25rem;
    }
    /* Typography: Larger Bold White mission titles (Clone.jpg reference) */
    .mission-title {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-weight: 700;
        font-size: 1.35rem;
        letter-spacing: 0.08em;
        color: #FFFFFF;
    }
    .mission-metadata {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #FFFFFF;
    }
    .mission-directive {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-weight: 700;
        font-size: 0.85rem;
        line-height: 1.5;
        color: rgba(255,255,255,0.85);
        margin-top: 0.5rem;
    }
    .mission-footnote {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #FFFFFF;
        margin-top: auto;
    }
    /* Column geometry: 480px card + [ ENGAGE ] aligned */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: 540px !important;
    }
    [data-testid="column"] .stButton { margin-top: auto; padding-top: 1rem; display: flex; justify-content: center; }
    .stButton > button {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 1.75rem;
        border: 1px solid #00f6ff;
        border-radius: 0;
        background: transparent;
        cursor: pointer;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.85rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #ffffff;
        transition: box-shadow 0.18s, transform 0.18s;
    }
    .stButton > button:hover, .stButton > button:focus-visible {
        outline: none;
        transform: translateY(-1px);
        box-shadow: 0 0 12px rgba(0, 246, 255, 0.5);
    }
    /* 4. Sidebar: 8-block Neural-Link with #00f6ff neon-glow; Green Pulse on radar container */
    .ares-neural-row { display: flex; gap: 4px; margin: 0.5rem 0 0.75rem 0; flex-wrap: wrap; }
    .ares-neural-cell {
        width: 20px; height: 20px;
        background: transparent;
        border: 1px solid rgba(0, 246, 255, 0.3);
        transition: background 0.2s, box-shadow 0.2s;
    }
    .ares-neural-cell.lit {
        background: #00f6ff;
        box-shadow: 0 0 12px #00f6ff, inset 0 0 6px rgba(255,255,255,0.25);
        border-color: #00f6ff;
    }
    .ares-radar-well { background: transparent !important; border: none !important; }
    /* Live Biometric radar: green pulsing overlay (#00FF00), 2s breathing 0.2–0.5 opacity */
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"] {
        position: relative !important;
        border: none !important;
        box-shadow: 0 0 0 2px #00FF00;
        animation: ares-radar-pulse 2s ease-in-out infinite;
    }
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"]::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at center, #00FF00 0%, transparent 70%);
        pointer-events: none;
        animation: ares-radar-overlay-pulse 2s ease-in-out infinite;
    }
    @keyframes ares-radar-overlay-pulse {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 0.5; }
    }
    @keyframes ares-radar-pulse {
        0%, 100% { box-shadow: 0 0 0 2px #00FF00, 0 0 12px rgba(0, 255, 0, 0.4); }
        50% { box-shadow: 0 0 0 3px #00FF00, 0 0 20px rgba(0, 255, 0, 0.7); }
    }
    /* Tactical Navigation Nodes: asymmetric cyan brackets only, transparent, glow on hover + SECURE_LINK */
    .hud-mono { letter-spacing: 0.18em; text-transform: uppercase; font-size: 0.7rem; color: #00f6ff; }
    .tactical-nav-node {
        position: relative;
        display: block;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.4rem;
        background: transparent !important;
        border: none !important;
        border-top: 2px solid #00f6ff;
        border-left: 2px solid #00f6ff;
        border-bottom: none;
        border-right: none;
        border-radius: 0;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85);
        cursor: pointer;
        transition: color 0.2s, box-shadow 0.2s, text-shadow 0.2s;
    }
    .tactical-nav-node::before { content: ""; position: absolute; bottom: 0; right: 0; width: 12px; height: 12px; border-bottom: 2px solid #00f6ff; border-right: 2px solid #00f6ff; }
    .tactical-nav-node:hover {
        color: #00f6ff;
        box-shadow: 0 0 16px rgba(0, 246, 255, 0.4);
        text-shadow: 0 0 8px #00f6ff;
    }
    .tactical-nav-node:hover .nav-node-meta { opacity: 1; }
    .nav-node-meta { font-size: 7px; letter-spacing: 0.2em; color: #00f6ff; opacity: 0; transition: opacity 0.2s; margin-top: 0.2rem; }
    .ares-nav-block {
        position: relative;
        display: block;
        padding: 0.5rem 0.5rem 0.5rem 1rem;
        margin-bottom: 0.35rem;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.9);
    }
    .ares-nav-block .nav-corner { position: absolute; width: 12px; height: 12px; border-color: #00f6ff; border-style: solid; border-width: 0; pointer-events: none; }
    .ares-nav-block .nav-corner-tl { top: 0; left: 0; border-top-width: 1px; border-left-width: 1px; }
    .ares-nav-block .nav-corner-br { bottom: 0; right: 0; border-bottom-width: 1px; border-right-width: 1px; }
    .ares-nav-block .nav-lock { margin-right: 0.35rem; opacity: 0.9; }
    .ares-nav-block.active { color: #00f6ff; }
    .ares-nav-block.active::before { content: "[ "; color: #00f6ff; }
    /* Sidebar: first 3 buttons = Tactical Nav Nodes (asymmetric brackets, transparent, hover glow) */
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(1) button,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(2) button,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(3) button {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.85) !important;
        background: transparent !important;
        border: none !important;
        border-top: 2px solid #00f6ff !important;
        border-left: 2px solid #00f6ff !important;
        border-bottom: none !important;
        border-right: none !important;
        border-radius: 0 !important;
        padding: 0.5rem 0.75rem !important;
        text-align: left !important;
        width: 100%;
        position: relative;
    }
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(1) button::after,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(2) button::after,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(3) button::after {
        content: ""; position: absolute; bottom: 0; right: 0; width: 12px; height: 12px;
        border-bottom: 2px solid #00f6ff; border-right: 2px solid #00f6ff;
    }
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(1) button:hover,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(2) button:hover,
    [data-testid="stSidebar"] > div > div .stButton:nth-of-type(3) button:hover {
        color: #ffbf00 !important;
        box-shadow: 0 0 18px rgba(255, 191, 0, 0.5) !important;
        text-shadow: 0 0 8px #ffbf00 !important;
    }
    .nav-node-meta { font-size: 7px; letter-spacing: 0.2em; color: rgba(0, 246, 255, 0.8); margin-top: 0.2rem; transition: opacity 0.2s; }
    .ares-nav-item {
        display: block;
        padding: 0.4rem 0;
        border-left: 2px solid rgba(0, 246, 255, 0.3);
        padding-left: 0.75rem;
        margin-bottom: 0.2rem;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85);
        transition: border-color 0.2s, color 0.2s, box-shadow 0.2s;
    }
    .ares-nav-item:hover { border-left-color: #00f6ff; color: #00f6ff; }
    .ares-nav-item.active {
        border-left-color: #00f6ff;
        color: #00f6ff;
        box-shadow: 0 0 10px rgba(0, 246, 255, 0.4);
    }
    .ares-nav-item.active::before { content: "[ "; color: #00f6ff; }
    .ares-nav-item.active::after { content: " ]"; color: #00f6ff; }
    .skill-heatmap-label { font-size: 0.65rem; letter-spacing: 0.15em; color: #00f6ff; margin-top: 1rem; margin-bottom: 0.35rem; text-transform: uppercase; }
    /* Proving Grounds: KSA progress bars — Tactical Green strength, Caution Orange gap */
    .ares-ksa-label { font-family: "Share Tech Mono", monospace !important; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: #ffffff; margin-bottom: 0.25rem; }
    .ares-ksa-bar-wrap { margin-bottom: 1rem; }
    .ares-ksa-bar { height: 12px; border-radius: 0; overflow: hidden; background: rgba(255,165,0,0.2); }
    .ares-ksa-bar .fill { height: 100%; transition: width 0.4s ease; }
    .ares-ksa-bar .fill.strength { background: #00FF00 !important; }
    .ares-ksa-bar .fill.gap { background: #FFA500 !important; }
    .ares-archetype-card { background: transparent; border: 1px solid rgba(0, 246, 255, 0.3); padding: 1.25rem; margin-bottom: 1rem; }
    .ares-tri-vector-title { font-size: 0.8rem; letter-spacing: 0.15em; color: #00f6ff; margin-bottom: 0.5rem; text-transform: uppercase; }
    /* Tactical page headers (sub-pages): sharp, left-aligned — Tactical Green #00FF00 */
    .tactical-page-header {
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        color: #00FF00;
        margin: 0 0 1rem 0;
        text-align: left;
    }
    /* Lab cards: 400px height lock, asymmetric cyan brackets */
    .ares-lab-card {
        position: relative;
        min-height: 400px !important;
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: transparent !important;
        border: none !important;
        padding: 1.25rem 1.5rem;
        overflow: visible;
    }
    .ares-lab-card .corner-bracket { position: absolute; width: 14px; height: 14px; border-color: #00f6ff; border-style: solid; border-width: 0; pointer-events: none; }
    .ares-lab-card .corner-tl { top: 0; left: 0; border-top-width: 2px; border-left-width: 2px; }
    .ares-lab-card .corner-br { bottom: 0; right: 0; border-bottom-width: 2px; border-right-width: 2px; }
    .ares-lab-status { font-size: 0.65rem; letter-spacing: 0.18em; text-transform: uppercase; color: #00FF00; margin-bottom: 0.5rem; }
    /* Archetype page frame: asymmetric cyan brackets */
    .ares-archetype-frame { position: relative; padding: 1.5rem 2rem; margin-bottom: 1rem; }
    .ares-archetype-frame .frame-tl { position: absolute; top: 0; left: 0; width: 24px; height: 24px; border-top: 2px solid #00f6ff; border-left: 2px solid #00f6ff; }
    .ares-archetype-frame .frame-br { position: absolute; bottom: 0; right: 0; width: 24px; height: 24px; border-bottom: 2px solid #00f6ff; border-right: 2px solid #00f6ff; }
    .ares-node-map-row { font-family: "Share Tech Mono", monospace !important; font-size: 0.75rem; color: #00FF00; margin-bottom: 0.5rem; }
    /* Proving Grounds tactical: Chromatic Glitch (wrong click), Power Cell, Traffic Pulse, Holographic Scanner, SYSTEM_STALL */
    .proving-glitch-pulse { animation: chromatic-glitch 0.6s ease-out; }
    @keyframes chromatic-glitch {
        0% { filter: hue-rotate(0deg) saturate(1.5); box-shadow: 0 0 30px #ff00ff, 0 0 60px rgba(255,0,255,0.5); }
        25% { filter: hue-rotate(90deg) saturate(2); box-shadow: 0 0 40px #00ffff, 0 0 80px rgba(0,255,255,0.6); }
        50% { filter: hue-rotate(-60deg) saturate(2); box-shadow: 0 0 35px #ff6600, 0 0 70px rgba(255,102,0,0.5); }
        75% { filter: hue-rotate(60deg) saturate(1.8); }
        100% { filter: hue-rotate(0deg) saturate(1); box-shadow: none; }
    }
    .power-cell-pulse { box-shadow: 0 0 16px #00f6ff, inset 0 0 8px rgba(0, 246, 255, 0.4) !important; background: rgba(0, 246, 255, 0.25) !important; }
    .traffic-pulse-line { height: 4px; background: linear-gradient(90deg, #00f6ff 0%, transparent 50%, #00f6ff 100%); background-size: 200% 100%; animation: traffic-pulse-move 2s linear infinite; margin: 0.5rem 0; }
    @keyframes traffic-pulse-move { 0% { background-position: 0% 0; } 100% { background-position: 200% 0; } }
    .holographic-scanner { border: 1px solid #00f6ff; box-shadow: 0 0 20px rgba(0, 246, 255, 0.5), inset 0 0 20px rgba(0, 246, 255, 0.1); padding: 1rem 1.25rem; margin: 0.75rem 0; background: rgba(0, 246, 255, 0.05); font-family: "Share Tech Mono", monospace !important; font-size: 0.7rem; letter-spacing: 0.1em; color: #00f6ff; word-break: break-all; }
    .system-stall-overlay { position: fixed; inset: 0; background: rgba(120, 0, 0, 0.85) !important; z-index: 9999; display: flex; align-items: center; justify-content: center; pointer-events: none; }
    .system-stall-overlay .stall-text { font-size: 1.5rem; font-weight: 700; letter-spacing: 0.3em; color: #ff4444; text-shadow: 0 0 20px #ff0000; animation: stall-pulse 1s ease-in-out infinite; }
    @keyframes stall-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
    .proving-frame { position: relative; padding: 1rem 1.25rem; margin: 0.5rem 0; background: transparent !important; border: none !important; }
    .proving-frame .frame-tl { position: absolute; top: 0; left: 0; width: 20px; height: 20px; border-top: 2px solid #00f6ff; border-left: 2px solid #00f6ff; }
    .proving-frame .frame-br { position: absolute; bottom: 0; right: 0; width: 20px; height: 20px; border-bottom: 2px solid #00f6ff; border-right: 2px solid #00f6ff; }
    .hex-log-line { font-family: "Share Tech Mono", monospace !important; font-size: 0.72rem; color: #00FF00; margin: 0.2rem 0; padding: 0.35rem 0.5rem; border-left: 2px solid rgba(0, 246, 255, 0.4); background: rgba(0, 0, 0, 0.3); display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
    </style>
    """
    # Inject CSS as raw HTML so it is applied, not displayed as text (st.markdown can render <style> content as code)
    try:
        st.html(css)
    except AttributeError:
        st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def _render_sidebar() -> None:
    """Tactical Navigation Nodes: asymmetric cyan brackets only, transparent, glow on hover."""
    score_state: ScoreState = st.session_state.score
    current_idx = st.session_state.question_index
    total = len(st.session_state.all_questions) or 1
    progress = min(1.0, current_idx / total) if total else 0.0
    num_lit = min(8, int(round(progress * 8)))
    page = st.session_state.game_page

    with st.sidebar:
        st.markdown(f'<div class="hud-mono" style="margin-bottom:0.4rem;">{t("strat_com")}</div>', unsafe_allow_html=True)
        if st.button(t("nav_mission_hub"), key="nav_mission_hub", use_container_width=True):
            st.session_state.game_page = "mission_hub"
            st.rerun()
        st.markdown(f'<div class="nav-node-meta" style="font-size:7px;letter-spacing:0.15em;margin-top:-0.2rem;margin-bottom:0.35rem;">{t("secure_link_mode_hub")}</div>', unsafe_allow_html=True)
        if st.button(t("nav_proving_grounds"), key="nav_proving_grounds", use_container_width=True):
            st.session_state.game_page = "proving_grounds"
            st.session_state.proving_module = "identity_strike"
            st.session_state.proving_identity_round = 0
            st.session_state.proving_boundary_round = 0
            st.session_state.proving_integrity_round = 0
            st.session_state.proving_total_start = None
            st.session_state.proving_boundary_shown_at = None
            st.rerun()
        st.markdown(f'<div class="nav-node-meta" style="font-size:7px;letter-spacing:0.15em;margin-top:-0.2rem;margin-bottom:0.35rem;">{t("secure_link_proving")}</div>', unsafe_allow_html=True)
        if st.button(t("nav_cyber_archetype"), key="nav_archetype", use_container_width=True):
            st.session_state.game_page = "dossier"
            st.rerun()
        st.markdown(f'<div class="nav-node-meta" style="font-size:7px;letter-spacing:0.15em;margin-top:-0.2rem;margin-bottom:0.35rem;">{t("secure_link_archetype")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-mono" style="margin-top:0.25rem;font-size:0.6rem;">{t("sync_level")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-mono" style="margin-top:0.5rem;font-size:0.6rem;">{t("live_fire")}</div>', unsafe_allow_html=True)
        lang_display = st.selectbox(
            t("language"),
            LANG_OPTIONS_DISPLAY,
            index={"ja": 0, "zh-TW": 1, "en": 2}.get(st.session_state.lang, 2),
            key="lang_select",
        )
        st.session_state.lang = LANG_VALUE_MAP.get(lang_display, "en")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="hud-mono">[ NEURAL-LINK ]</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-mono" style="font-size:0.6rem;margin-top:0.15rem;">{t("operator_id")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-mono" style="margin-top:0.5rem;">{t("sync_level")}</div>', unsafe_allow_html=True)
        cells_html = "".join(
            f'<div class="ares-neural-cell{" lit" if i < num_lit else ""}"></div>' for i in range(8)
        )
        st.markdown(f'<div class="ares-neural-row">{cells_html}</div>', unsafe_allow_html=True)
        if page == "proving_grounds":
            power_pulses = st.session_state.get("power_cell_pulses", 0)
            power_cells_html = "".join(
                f'<div class="ares-neural-cell{" lit power-cell-pulse" if i < power_pulses else ""}"></div>' for i in range(8)
            )
            st.markdown(f'<div class="hud-mono" style="font-size:0.6rem;margin-top:0.35rem;">{t("power_cell")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ares-neural-row">{power_cells_html}</div>', unsafe_allow_html=True)
        st.caption(f"{t('progress_answered')}: {current_idx}/{total} answered")
        st.caption(t("sync_level"))

        st.markdown(f'<div class="hud-mono" style="margin-top:1rem;">{t("live_biometric")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="ares-radar-well">', unsafe_allow_html=True)
        radar_scores = score_state.get_normalized_radar_scores()
        fig = build_ares_radar_figure(radar_scores)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=dict(displayModeBar=False),
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="skill-heatmap-label">{t("skill_heatmap")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hud-mono" style="font-size:0.6rem;">{t("securely_provision")}</div>', unsafe_allow_html=True)


def _start_mission(mission: str) -> None:
    """Load mission-specific question bank and jump into shared flow."""
    st.session_state.score = ScoreState()
    st.session_state.question_index = 0
    st.session_state.mission_tier = mission

    if mission == "explorer":
        # 20-item profile: 10 Instinct + 10 NIST Foundations (Explorer only)
        st.session_state.all_questions = get_explorer_questions()
    elif mission == "specialist":
        st.session_state.all_questions = get_specialist_questions()
    else:
        st.session_state.all_questions = get_operator_questions()

    st.session_state.game_page = "questions"
    st.rerun()


def _render_mission_hub() -> None:
    """Mission Hub: C3S headline (0.8rem, heartbeat glitch). All strings from LANG_MAP."""
    st.markdown(
        '<div style="position:relative; display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">'
        f'<div><h1 class="c3s-main-title">' + t("headline") + '</h1>'
        f'<p class="c3s-subtitle">' + t("subtitle") + '</p></div>'
        f'<span class="connecting-status">' + t("connecting") + '</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'''
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0x7F2A</span>
                <div class="mission-status">''' + t("system_status") + '''</div>
                <div class="mission-title">''' + t("mission_title_explorer") + '''</div>
                <div class="mission-metadata">''' + t("vector_id_exp") + '''</div>
                <div class="mission-metadata">''' + t("threat_model") + '''</div>
                <div class="mission-directive">''' + t("operational_directive_exp") + '''</div>
                <div class="mission-footnote">''' + t("trk_lock_exp") + '''</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        if st.button(t("engage"), key="engage_explorer"):
            _start_mission("explorer")

    with col2:
        st.markdown(
            f'''
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0x83C1</span>
                <div class="mission-status">''' + t("system_status") + '''</div>
                <div class="mission-title">''' + t("mission_title_specialist") + '''</div>
                <div class="mission-metadata">''' + t("vector_id_spec") + '''</div>
                <div class="mission-metadata">''' + t("threat_model") + '''</div>
                <div class="mission-directive">''' + t("operational_directive_spec") + '''</div>
                <div class="mission-footnote">''' + t("trk_lock_spec") + '''</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        if st.button(t("engage"), key="engage_specialist"):
            _start_mission("specialist")

    with col3:
        st.markdown(
            f'''
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0xEB4D</span>
                <div class="mission-status">''' + t("system_status") + '''</div>
                <div class="mission-title">''' + t("mission_title_operator") + '''</div>
                <div class="mission-metadata">''' + t("vector_id_op") + '''</div>
                <div class="mission-metadata">''' + t("threat_model") + '''</div>
                <div class="mission-directive">''' + t("operational_directive_op") + '''</div>
                <div class="mission-footnote">''' + t("trk_lock_op") + '''</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        if st.button(t("engage"), key="engage_operator"):
            _start_mission("operator")


# Role ID → display title for Tri-Vector recommendation (NICE work roles)
_ROLE_ID_TO_TITLE = {
    "SP-SSE": "Secure Software Assessor",
    "SP-ARC": "Security Architect",
    "PR-CDA": "Cyber Defense Analyst",
    "PR-IR": "Incident Responder",
    "AN-TWA": "Threat/Warning Analyst",
    "IN-CLI": "Cyber Crime Investigator",
    "OG-WRL-017": "Supply Chain Risk Manager",
    "NF-COM-008": "DevSecOps Engineer",
}


def _get_tri_vector_career_paths(score_state: ScoreState) -> list[tuple[str, float]]:
    """Top 3 career paths by Nobel-inspired weighting (role probabilities). Returns [(title, pct), ...]."""
    probs = score_state.get_role_probabilities()
    sorted_roles = sorted(probs.items(), key=lambda x: -x[1])[:3]
    return [
        (_ROLE_ID_TO_TITLE.get(rid, rid), round(pct, 1))
        for rid, pct in sorted_roles
    ]


def calculate_archetype_drift(base_ksa: float, is_correct: bool, time_taken: float, used_intel: bool) -> float:
    """
    Nobel Scoring Engine (Stockholm Math).

    Score = (Base_KSA * Accuracy) / (Time_Taken / 3.0)
    - Accuracy: 1.0 if correct else 0.0
    - Intel penalty: if [INTEL] brief used, cap mastery at 0.2x base_ksa
    - Latency threshold: responses > 3.0s get 'Sluggish Telemetry' penalty on mastery
    """
    if not is_correct:
        return 0.0

    accuracy = 1.0
    effective_time = max(time_taken, 0.1)
    score = (base_ksa * accuracy) / (effective_time / 3.0)

    # Intel brief penalty – cap mastery gain
    if used_intel:
        score = min(score, base_ksa * 0.2)

    # Sluggish Telemetry penalty for slow responses
    if effective_time > 3.0:
        score *= 0.6

    return max(0.0, score)


def _build_proving_identity_rounds() -> list[dict]:
    """Build [ IDENTITY_STRIKE ] rounds: 0xHEX log feed, one threat per round (MFA_BYPASS, DORMANT_USER, NTLM_RELAY)."""
    if "proving_questions_seed" not in st.session_state:
        st.session_state.proving_questions_seed = random.randint(0, 999999)
    rng = random.Random(st.session_state.proving_questions_seed)
    threats = ["MFA_BYPASS", "DORMANT_USER", "NTLM_RELAY"]
    benign = ["LOGIN_OK", "SESSION_ACTIVE", "AUTH_OK"]
    rounds_list = []
    # 4 rounds → contributes to 10-question triad loop (4/3/3)
    for _ in range(4):
        threat = rng.choice(threats)
        log_lines = []
        threat_idx = rng.randint(0, 5)
        for i in range(6):
            hex_ts = f"0x{rng.randint(0x1A2B3C4D, 0xE5F6A7B8):08X}"
            ip = f"10.0.0.{rng.randint(1, 50)}"
            log_lines.append(f"0x{rng.randint(0, 0xFFFF):04X} {hex_ts} AUTH_EVENT {threat if i == threat_idx else rng.choice(benign)} {ip}")
        rng.shuffle(log_lines)
        correct_idx = next(i for i, line in enumerate(log_lines) if any(t in line for t in threats))
        rounds_list.append({"log_lines": log_lines, "correct_line_index": correct_idx})
    return rounds_list


def _build_proving_boundary_rounds() -> list[dict]:
    """Build [ BOUNDARY_PURGE ] rounds: packet position % and rogue port (4444, 6667, 445)."""
    if "proving_questions_seed" not in st.session_state:
        st.session_state.proving_questions_seed = random.randint(0, 999999)
    rng = random.Random(st.session_state.proving_questions_seed + 1)
    rogue_ports = [4444, 6667, 445]
    # 3 rounds
    return [
        {"port": rng.choice(rogue_ports), "position_pct": rng.randint(25, 95)}
        for _ in range(3)
    ]


def _build_proving_integrity_rounds() -> list[dict]:
    """Build [ INTEGRITY_SYNC ] rounds: two 64-char SHA256, match or mismatch."""
    if "proving_questions_seed" not in st.session_state:
        st.session_state.proving_questions_seed = random.randint(0, 999999)
    rng = random.Random(st.session_state.proving_questions_seed + 2)
    canonical = hashlib.sha256(b"Project Ares policy v1.0\nIntegrity check.").hexdigest()
    wrong = hashlib.sha256(b"tampered").hexdigest()
    rounds_list = []
    # 3 rounds
    for _ in range(3):
        match = rng.choice([True, False])
        if match:
            h1 = h2 = canonical
        else:
            h1, h2 = canonical, wrong
        rounds_list.append({"hash_a": h1, "hash_b": h2, "match": match})
    return rounds_list


def _build_proving_questions() -> list[dict]:
    """Legacy: kept for any refs; new Proving Grounds uses _build_proving_*_rounds()."""
    return []


def _render_proving_grounds() -> None:
    """Proving Grounds: Kinetic Triad with Stockholm Nobel math and 10-step loop (4/3/3)."""
    score_state: ScoreState = st.session_state.score
    now = time.time()

    # SYSTEM_STALL: 5s red HUD, KSA frozen
    if now < st.session_state.get("system_stall_until", 0):
        remaining = max(0, st.session_state.system_stall_until - now)
        st.markdown(
            f'<div class="system-stall-overlay"><span class="stall-text">'
            f'{t("system_stall")} — {t("system_stall_countdown")}{remaining:.1f}s</span></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)
        st.rerun()
        return

    # Init on first entry for this run
    if st.session_state.get("proving_total_start") is None:
        st.session_state.proving_total_start = now
        st.session_state.proving_correct_count = 0
        st.session_state.proving_total_count = 0
        st.session_state.proving_any_intel_used = False

    if st.session_state.get("proving_module") is None:
        st.session_state.proving_module = "identity_strike"
        st.session_state.proving_identity_round = 0
        st.session_state.proving_boundary_round = 0
        st.session_state.proving_integrity_round = 0
        st.session_state.power_cell_pulses = 0
        st.session_state.proving_current_round_key = ""
        st.session_state.proving_round_started_at = None

    # Chromatic glitch: trigger one-time glitch class then clear
    glitch_class = " proving-glitch-pulse" if st.session_state.pop("chromatic_glitch_trigger", False) else ""

    # Header: tiny 0.8rem white pulsing (same as Mission Hub), breadcrumb, asymmetric frame only
    st.markdown(
        f'<h1 class="c3s-main-title" style="margin-bottom:0.25rem;">{t("headline")}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="sys-breadcrumb">{t("breadcrumb_proving")}</p>', unsafe_allow_html=True)

    module = st.session_state.proving_module

    # Helper to init a round key + timer and reset INTEL usage
    def _ensure_round_started(key: str) -> None:
        if st.session_state.proving_current_round_key != key:
            st.session_state.proving_current_round_key = key
            st.session_state.proving_round_started_at = time.time()
            st.session_state.proving_used_intel_this_round = False

    # ---------- [ IDENTITY_STRIKE ] ----------
    if module == "identity_strike":
        identity_rounds = _build_proving_identity_rounds()
        r = st.session_state.proving_identity_round
        if r >= len(identity_rounds):
            st.session_state.proving_module = "boundary_purge"
            st.session_state.proving_boundary_round = 0
            st.session_state.proving_boundary_shown_at = None
            st.session_state.proving_current_round_key = ""
            st.session_state.proving_round_started_at = None
            st.rerun()
            return

        _ensure_round_started(f"identity_{r}")
        round_data = identity_rounds[r]
        log_lines = round_data["log_lines"]
        correct_idx = round_data["correct_line_index"]

        st.markdown(
            f'<div class="proving-frame{glitch_class}" style="margin-bottom:0.75rem;">'
            '<span class="frame-tl"></span><span class="frame-br"></span>'
            f'<div class="ares-lab-status">{t("identity_strike")} — {r + 1}/{len(identity_rounds)}</div>'
            f'<p style="font-size:0.7rem;color:rgba(255,255,255,0.9);margin-bottom:0.5rem;">{t("identity_strike_instruction")}</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Optional INTEL brief (penalizes mastery if used)
        if st.button("[ INTEL ]", key=f"pg_id_intel_{r}"):
            st.session_state.proving_used_intel_this_round = True
            st.session_state.proving_any_intel_used = True

        # Vertical 0xHEX log feed: each line with [ Neutralize ] button (no columns)
        for i, line in enumerate(log_lines):
            st.markdown(f'<div class="hex-log-line">{line}</div>', unsafe_allow_html=True)
            if st.button(f"  {t('neutralize')}  ", key=f"pg_id_r{r}_line{i}"):
                is_correct = i == correct_idx
                st.session_state.proving_total_count += 1
                if is_correct:
                    st.session_state.proving_correct_count += 1
                time_taken = time.time() - (st.session_state.proving_round_started_at or now)
                delta = calculate_archetype_drift(
                    base_ksa=0.06,
                    is_correct=is_correct,
                    time_taken=time_taken,
                    used_intel=st.session_state.proving_used_intel_this_round,
                )
                if delta > 0:
                    st.session_state.power_cell_pulses = st.session_state.get("power_cell_pulses", 0) + 1
                    score_state.add_weights({CATEGORY_AN: delta, CATEGORY_PR: delta})

                if is_correct:
                    st.session_state.proving_identity_round = r + 1
                else:
                    st.session_state.chromatic_glitch_trigger = True
                st.session_state.proving_round_started_at = None
                st.rerun()
        return

    # ---------- [ BOUNDARY_PURGE ] ----------
    if module == "boundary_purge":
        boundary_rounds = _build_proving_boundary_rounds()
        r = st.session_state.proving_boundary_round
        if r >= len(boundary_rounds):
            st.session_state.proving_module = "integrity_sync"
            st.session_state.proving_integrity_round = 0
            st.session_state.proving_current_round_key = ""
            st.session_state.proving_round_started_at = None
            st.rerun()
            return

        _ensure_round_started(f"boundary_{r}")
        round_data = boundary_rounds[r]
        port = round_data["port"]
        position_pct = round_data["position_pct"]
        if st.session_state.proving_boundary_shown_at is None:
            st.session_state.proving_boundary_shown_at = time.time()

        st.markdown(
            f'<div class="proving-frame{glitch_class}">'
            '<span class="frame-tl"></span><span class="frame-br"></span>'
            f'<div class="ares-lab-status">{t("boundary_purge")} — {r + 1}/{len(boundary_rounds)}</div>'
            f'<p style="font-size:0.7rem;color:rgba(255,255,255,0.9);margin-bottom:0.5rem;">{t("boundary_purge_instruction")}</p>'
            f'<p style="font-size:0.75rem;color:#00f6ff;">{t("internal_network")} ← 0% ——————— {t("position_to_egress")} {position_pct}% {t("to_egress")} — 100%</p>'
            '<div class="traffic-pulse-line"></div>'
            f'<p style="font-size:0.75rem;color:#00FF00;">{t("packet_beaconing")} {port}</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(f"  {t('drop')}  ", key=f"pg_bd_r{r}"):
            is_correct = True  # dropping is always the defensive action here
            st.session_state.proving_total_count += 1
            st.session_state.proving_correct_count += 1
            latency = time.time() - st.session_state.proving_boundary_shown_at
            st.session_state.proving_boundary_shown_at = None
            time_taken = latency
            delta = calculate_archetype_drift(
                base_ksa=0.05,
                is_correct=is_correct,
                time_taken=time_taken,
                used_intel=st.session_state.proving_used_intel_this_round,
            )
            if delta > 0:
                # Proximity to internal network shapes underlying scoring via position_pct
                proximity_to_internal = 100 - position_pct
                geom_mult = max(0.4, min(1.0, proximity_to_internal / 100.0))
                delta *= geom_mult
                score_state.add_weights({CATEGORY_AN: delta, CATEGORY_PR: delta})
            st.session_state.proving_boundary_round = r + 1
            st.session_state.proving_round_started_at = None
            st.rerun()
        return

    # ---------- [ INTEGRITY_SYNC ] ----------
    if module == "integrity_sync":
        integrity_rounds = _build_proving_integrity_rounds()
        r = st.session_state.proving_integrity_round
        if r >= len(integrity_rounds):
            total_start = st.session_state.get("proving_total_start") or now
            elapsed = now - total_start
            total = st.session_state.proving_total_count or 1
            accuracy = st.session_state.proving_correct_count / total
            # Aggregate Nobel drift for the triad
            drift_score = calculate_archetype_drift(
                base_ksa=1.0,
                is_correct=True if accuracy > 0 else False,
                time_taken=max(elapsed, 0.1),
                used_intel=st.session_state.proving_any_intel_used,
            )
            drift_pct = max(0, min(100, round(drift_score * 100, 1)))

            st.markdown(
                f'<div class="proving-frame"><span class="frame-tl"></span><span class="frame-br"></span>'
                f'<div class="ares-lab-status" style="margin-bottom:0.75rem;">{t("archetype_drift")} {drift_pct}%</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            if st.button(t("back_to_hub"), key="proving_back"):
                st.session_state.game_page = "mission_hub"
                st.session_state.proving_module = "identity_strike"
                st.session_state.proving_identity_round = 0
                st.session_state.proving_boundary_round = 0
                st.session_state.proving_integrity_round = 0
                st.session_state.proving_total_start = None
                st.session_state.proving_boundary_shown_at = None
                st.session_state.power_cell_pulses = 0
                st.session_state.proving_current_round_key = ""
                st.session_state.proving_round_started_at = None
                st.session_state.proving_used_intel_this_round = False
                st.session_state.proving_any_intel_used = False
                st.session_state.proving_correct_count = 0
                st.session_state.proving_total_count = 0
                st.rerun()
            return

        _ensure_round_started(f"integrity_{r}")
        round_data = integrity_rounds[r]
        h_a, h_b = round_data["hash_a"], round_data["hash_b"]
        match = round_data["match"]

        st.markdown(
            f'<div class="proving-frame{glitch_class}">'
            '<span class="frame-tl"></span><span class="frame-br"></span>'
            f'<div class="ares-lab-status">{t("integrity_sync")} — {r + 1}/{len(integrity_rounds)}</div>'
            f'<p style="font-size:0.7rem;color:rgba(255,255,255,0.9);margin-bottom:0.5rem;">{t("integrity_sync_instruction")}</p>'
            f'<div class="holographic-scanner">'
            f'<div>{t("hash_expected")}: {h_a}</div>'
            f'<div style="margin-top:0.5rem;">{t("hash_computed")}: {h_b}</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(t("validate"), key=f"pg_int_v_r{r}"):
            is_correct = match
            st.session_state.proving_total_count += 1
            if is_correct:
                st.session_state.proving_correct_count += 1
            time_taken = time.time() - (st.session_state.proving_round_started_at or now)
            delta = calculate_archetype_drift(
                base_ksa=0.06,
                is_correct=is_correct,
                time_taken=time_taken,
                used_intel=st.session_state.proving_used_intel_this_round,
            )
            if is_correct and delta > 0:
                score_state.add_weights({CATEGORY_AN: delta, CATEGORY_PR: delta})
                st.session_state.proving_integrity_round = r + 1
            else:
                # Critical failure: validating bad hash triggers SYSTEM_STALL
                st.session_state.system_stall_until = time.time() + 5.0
            st.session_state.proving_round_started_at = None
            st.rerun()

        if st.button(t("reject"), key=f"pg_int_rej_r{r}"):
            is_correct = not match
            st.session_state.proving_total_count += 1
            if is_correct:
                st.session_state.proving_correct_count += 1
            time_taken = time.time() - (st.session_state.proving_round_started_at or now)
            delta = calculate_archetype_drift(
                base_ksa=0.06,
                is_correct=is_correct,
                time_taken=time_taken,
                used_intel=st.session_state.proving_used_intel_this_round,
            )
            if delta > 0:
                score_state.add_weights({CATEGORY_AN: delta, CATEGORY_PR: delta})
            st.session_state.proving_integrity_round = r + 1
            st.session_state.proving_round_started_at = None
            st.rerun()
        return

    st.rerun()


def _render_cyber_archetype() -> None:
    """Page 3: Cyber Archetype — NICE Synthesis, asymmetric frame, Nobel vector radar, Tri-Vector, Mission Node Map."""
    score_state: ScoreState = st.session_state.score
    radar_scores = score_state.get_normalized_radar_scores()
    tri_vector = _get_tri_vector_career_paths(score_state)
    dominant = score_state.get_dominant_aptitude()
    knowledge_level = score_state.get_knowledge_level()

    # Sub-page: technical breadcrumb only
    st.markdown(f'<p class="sys-breadcrumb">{t("breadcrumb_archetype")}</p>', unsafe_allow_html=True)

    # Neural-Link Career Map: hexagonal root + cyan filaments to 3 paths
    tri_vector = _get_tri_vector_career_paths(score_state)
    role = get_work_role(dominant, knowledge_level)
    st.markdown(
        '<div class="neural-map-container" style="position:relative;min-height:120px;margin-bottom:1rem;">'
        '<div class="neural-hex-root" style="margin:0 auto;width:72px;height:72px;border:2px solid #00f6ff;'
        'clip-path:polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);'
        'background:rgba(0,246,255,0.12);box-shadow:0 0 24px rgba(0,246,255,0.4);'
        'display:flex;align-items:center;justify-content:center;">'
        f'<span style="font-size:0.55rem;color:#00f6ff;text-align:center;padding:4px;">{role.title[:14]}</span></div>'
        f'<p style="font-size:0.65rem;color:#00f6ff;text-align:center;margin-top:0.35rem;">' + t("archetype_root") + '</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Floating hologram: Gap Analysis Radar at center-mass of page
    st.markdown(f'<div class="ares-lab-status" style="margin:0.5rem 0;">{t("gap_analysis_radar")}</div>', unsafe_allow_html=True)
    fig = build_ares_radar_figure(radar_scores)
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown(f'<div class="ares-tri-vector-title">{t("neural_career_paths")}</div>', unsafe_allow_html=True)
    for i, (title, pct) in enumerate(tri_vector, 1):
        st.markdown(
            f'<div class="ares-archetype-card">'
            f'<span class="mission-metadata">#{i}</span> '
            f'<span class="mission-title">{title}</span> '
            f'<span style="color:#00f6ff;">({pct}% fit)</span></div>',
            unsafe_allow_html=True,
        )

    # Project Ares Bridge: Mission Node Map — top 3 gaps → Battle Rooms
    raw = score_state.get_category_scores()
    sorted_cats = sorted(raw.items(), key=lambda x: x[1])[:3]  # lowest 3 = gaps
    st.markdown(f'<div class="ares-tri-vector-title">{t("project_ares_bridge")}</div>', unsafe_allow_html=True)
    for cat_code, _ in sorted_cats:
        label = get_category_label(cat_code)
        nodes = NIST_CATEGORY_TO_ARES_SCENARIOS.get(cat_code, [])[:5]
        nodes_str = ", ".join(nodes) if nodes else "—"
        st.markdown(
            f'<div class="ares-node-map-row">Gap: {label} → {nodes_str}</div>',
            unsafe_allow_html=True,
        )

    role = get_work_role(dominant, knowledge_level)
    certs = get_certifications(dominant, knowledge_level)
    st.markdown(f'<div class="ares-tri-vector-title">{t("primary_mission_role")}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="ares-archetype-card">'
        f'<span class="mission-title">{role.title}</span> '
        f'<span class="mission-metadata">({role.id})</span> — {role.category}<br>'
        f'<span style="color:rgba(255,255,255,0.85);">{role.definition}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ares-tri-vector-title">{t("recommended_certs")}</div>', unsafe_allow_html=True)
    for c in certs:
        st.markdown(f'- **{c.name}** — {c.issuer} ({c.level})', unsafe_allow_html=False)

    # Asymmetric cyan bracket frame (bottom-right corner)
    st.markdown(
        '<div class="ares-archetype-frame" style="min-height:40px; margin-top:1rem;">'
        '<span class="frame-br"></span></div>',
        unsafe_allow_html=True,
    )

    if st.button(t("back_to_hub"), key="archetype_back"):
        st.session_state.game_page = "mission_hub"
        st.rerun()


def main() -> None:
    """
    Entry point for the Streamlit Cyber-Ops interface.

    - Imports HUD geometry from ui.build_ares_radar_figure.
    - Imports mission / question logic from questions.py and game.py.
    - Presents three-tier Mission Hub (Explorer, Specialist, Operator).
    - Each [ ENGAGE ] routes into game.py's Streamlit question flow and dossier.
    """
    _inject_global_hud_css()
    _init_session_state()
    _render_sidebar()

    if st.session_state.game_page == "mission_hub":
        _render_mission_hub()
    elif st.session_state.game_page == "proving_grounds":
        _render_proving_grounds()
    elif st.session_state.game_page == "questions":
        game._render_questions(st.session_state.score)  # type: ignore[attr-defined]
    else:  # "dossier" — Cyber Archetype (synthesis)
        _render_cyber_archetype()


if __name__ == "__main__":
    main()
