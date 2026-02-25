#!/usr/bin/env python3
"""
Cyber Career Compass — Structural Foundation. Single Streamlit entry point.
Run: streamlit run main.py

- Entry point: Initializes ScoreState (scoring.py), manages global navigation flow.
- State: st.session_state keeps NIST scores across pages; Always-Live Radar in sidebar.
- UI: st.radio for mission questions, st.progress for diagnostic completion.
- Theme: Dark Mode Hacker (#0a0a0b background, Cyber-Blue / Neon-Cyan #00f2ff).
"""

import sys
import html
import time
from typing import Optional, List, Any, Dict

import streamlit as st

# Module synchronization: questions.py drives content; scoring.py consumes results.
from cyber_career_compass.questions import (
    get_instinct_questions,
    get_technical_questions,
    get_explorer_questions,
    get_specialist_questions,
    get_operator_questions,
    Question,
    Choice,
)
from cyber_career_compass.scoring import (
    ScoreState,
    xp_to_rank,
    XP_PER_REFLEX_CORRECT,
    XP_PER_INSTINCT_CHOICE,
    XP_PER_TECHNICAL_CORRECT,
    XP_EXPLORER_COMPLETE,
    XP_SPECIALIST_COMPLETE,
    XP_OPERATOR_COMPLETE,
    XP_REFLEX_LAB_COMPLETE,
    COMPETENCY_RAW_THRESHOLD,
)
from cyber_career_compass.results import (
    render_radar_chart,
    render_radar_chart_compact,
    render_dossier,
    render_dossier_explorer,
    render_dossier_operator,
)
from cyber_career_compass.nice_framework import (
    ALL_CATEGORIES,
    ALL_ROLE_IDS,
    CATEGORY_PR,
    CATEGORY_SP,
    CATEGORY_AN,
    CATEGORY_IN,
)
from cyber_career_compass.reflex_drill import REFLEX_THREATS
from cyber_career_compass.content import get_calibration_questions, CALIBRATION_TOTAL
from cyber_career_compass.translations import (
    SUPPORTED_LANGUAGES,
    LANGUAGE_LABELS,
    get_ui,
    get_category_labels,
    get_role_display,
)

if __name__ == "__main__" and "--demo" in sys.argv:
    from cyber_career_compass.game import run_with_answers
    run_with_answers(["a", "b", "c", "a", "b"], ["a"] * 10)
    sys.exit(0)

st.set_page_config(page_title="Cyber Career Compass", layout="wide")

# ─── Phase 1: Canonical session keys and defaults. Score preserved across navigation. ─
# mission_tier: None | "explorer" | "specialist" | "operator"
# mission_total: 0 until start_mission(tier) sets 20 | 50 | 10
# mission_active: False until start_mission(tier) sets True
PHASE_1_DEFAULTS = {
    "score": None,
    "current_question_index": 0,
    "responses": [],
    "nav_page": "mission_hub",
    "reflex_complete": False,
    "lang": "en",
    "language": "en",
    "reflex_drill_index": 0,
    "questions": None,
    "mission_tier": None,
    "mission_total": 0,
    "mission_active": False,
    "xp": 0,
    "agent_rank": "Security Initiate",
}

# Router config: tier → (mission_total, question pool loader). Used by switch_mission_path().
def _load_explorer(): return list(get_explorer_questions(_get_lang()))
def _load_specialist(): return list(get_specialist_questions(_get_lang()))
def _load_operator(): return list(REFLEX_THREATS)
MISSION_PATH_CONFIG = {
    "explorer": (20, _load_explorer),
    "specialist": (50, _load_specialist),
    "operator": (10, _load_operator),
}


def switch_mission_path(tier: str) -> None:
    """
    Router: set mission_tier, load the correct question pool, reset indices, set mission_total.
    tier must be "explorer" | "specialist" | "operator". Does not clear score — Sidebar Radar intact.
    """
    if tier not in MISSION_PATH_CONFIG:
        return
    mission_total, get_questions = MISSION_PATH_CONFIG[tier]
    st.session_state.mission_tier = tier
    st.session_state.mission_total = mission_total
    st.session_state.questions = get_questions()
    st.session_state.current_question_index = 0
    st.session_state.reflex_drill_index = 0
    st.session_state.mission_active = True
    if tier == "operator":
        st.session_state.operator_prior_choices = []


def start_mission(tier: str) -> None:
    """
    Start a mission: set tier, reset question_index to 0, set mission_total (Explorer=20, Specialist=50, Operator=10),
    load question pool, and set mission_active=True. Does not clear score — Sidebar Radar intact.
    """
    switch_mission_path(tier)


def _get_lang() -> str:
    return st.session_state.get("language", st.session_state.get("lang", "en"))


def _init_session() -> None:
    """
    Initialize session state once. ScoreState in st.session_state.score is never reset
    when navigating between Mission Hub, Proving Ground, and Cyber Archetype — Always-Live Radar.
    """
    if "score" not in st.session_state:
        st.session_state.score = ScoreState()
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = PHASE_1_DEFAULTS["current_question_index"]
    if "responses" not in st.session_state:
        st.session_state.responses = list(PHASE_1_DEFAULTS["responses"])
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = PHASE_1_DEFAULTS["nav_page"]
    if "reflex_complete" not in st.session_state:
        st.session_state.reflex_complete = PHASE_1_DEFAULTS["reflex_complete"]
    if "lang" not in st.session_state:
        st.session_state.lang = PHASE_1_DEFAULTS["lang"]
    if "language" not in st.session_state:
        st.session_state.language = PHASE_1_DEFAULTS["language"]
    if "reflex_drill_index" not in st.session_state:
        st.session_state.reflex_drill_index = PHASE_1_DEFAULTS["reflex_drill_index"]
    if "questions" not in st.session_state or not st.session_state.questions:
        st.session_state.questions = list(REFLEX_THREATS)
    if "mission_tier" not in st.session_state:
        st.session_state.mission_tier = PHASE_1_DEFAULTS["mission_tier"]
    if "mission_total" not in st.session_state:
        st.session_state.mission_total = PHASE_1_DEFAULTS["mission_total"]
    if "mission_active" not in st.session_state:
        st.session_state.mission_active = PHASE_1_DEFAULTS["mission_active"]
    if "xp" not in st.session_state:
        st.session_state.xp = PHASE_1_DEFAULTS.get("xp", 0)
    if "agent_rank" not in st.session_state:
        st.session_state.agent_rank = PHASE_1_DEFAULTS.get("agent_rank", "Security Initiate")
    if "proving_ground_reflex_index" not in st.session_state:
        st.session_state.proving_ground_reflex_index = 0


# ─── Dark Mode Hacker theme: deep black #0a0a0b, Neon-Cyan #00f2ff ─
MODULE_METADATA_STR = "SYS_REF: 800-181 // AUTH: DISA_CSSP"

DASHBOARD_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
    /* ═══ Zero-Box Aesthetic Force: global background #0a0a0b, 3% Scanline/CRT, Asymmetric Cyan Brackets at viewport corners ═══ */
    html, body, .stApp, .main, section.main,
    [data-testid="stVerticalBlock"] > div:first-child {
        background: #0a0a0b !important;
    }
    /* ═══ Total DOM Takeover: Vacuum Reset ═══ */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0b !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stHeader"] {
        display: none !important;
    }
    header, footer {
        display: none !important;
    }
    /* stAppViewContainer overrides: strip Streamlit identity, void-black, no default padding */
    [data-testid="stAppViewContainer"] {
        background: #0a0a0b !important;
        padding: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stAppViewContainer"] > section {
        background: #0a0a0b !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .main .block-container {
        padding: 0 !important;
        margin: 0 auto !important;
        max-width: 1200px !important;
    }
    header, footer, [data-testid="stHeader"], #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    /* ═══ Zero-Box HUD Reset (Gemini Prompts Page 18) ═══ */
    /* Container Deletion: remove standard Streamlit blue containers and default padding */
    .main .block-container,
    [data-testid="stVerticalBlock"] > div:first-child,
    section.main [data-testid="stVerticalBlock"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    /* Replace default blocks with Glass-Card treatment for content blocks */
    .main [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(10, 10, 11, 0.4) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.15) !important;
        border-radius: 8px;
        padding: 1rem !important;
    }
    /* Asymmetric Cyan Brackets: top-left and bottom-right of main viewport (CSS fallback; st.html wrapper adds DOM brackets) */
    [data-testid="stAppViewContainer"] {
        position: relative;
    }
    /* Diegetic: Scanline texture — global repeating-linear-gradient at 3% opacity (CRT) */
    body::before,
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 0, 0, 0.08) 2px,
            rgba(0, 0, 0, 0.08) 4px
        );
        pointer-events: none;
        z-index: 9998;
        opacity: 0.03;
        animation: crt-flicker 8s ease-in-out infinite;
    }
    @keyframes crt-flicker {
        0%, 90%, 100% { opacity: 0.03; }
        92% { opacity: 0.025; }
        94% { opacity: 0.035; }
        96% { opacity: 0.028; }
        98% { opacity: 0.032; }
    }
    /* Tactical Summary header: Bold White Monospace */
    .tactical-summary-header {
        font-family: 'Share Tech Mono', monospace !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }
    /* Status text: Tactical Green #00FF00 */
    .tactical-status {
        color: #00FF00 !important;
        text-shadow: 0 0 8px #00FF00;
        font-family: 'Share Tech Mono', monospace !important;
    }
    /* Floating Sidebar: Live Biometric HUD panel */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(10, 10, 11, 0.88) !important;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 242, 255, 0.35) !important;
        border-radius: 10px;
        box-shadow: 0 0 32px rgba(0, 242, 255, 0.12), inset 0 1px 0 rgba(255,255,255,0.03);
        margin: 10px 0 10px 10px !important;
        padding: 1rem !important;
    }
    [data-testid="stSidebar"] .tactical-summary-header { font-size: 1rem; margin-bottom: 0.5rem; }
    [data-testid="stSidebar"] .tactical-status { font-size: 0.85rem; }
    /* Sidebar: static grain overlay (diegetic HUD) */
    [data-testid="stSidebar"] { position: relative; }
    [data-testid="stSidebar"]::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 1;
        opacity: 0.14;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        border-radius: 10px;
    }
    /* Ares Perimeter Radar — .radar-hud-frame: marker div before each chart; next sibling block gets The Ares Line (Neon-Cyan glowing ring) */
    .radar-hud-frame {
        display: block;
        height: 0;
        margin: 0;
        padding: 0;
        overflow: visible;
        position: relative;
    }
    .radar-hud-frame + div {
        position: relative;
    }
    .radar-hud-frame + div::before {
        content: "";
        position: absolute;
        inset: -8px;
        border: 2px solid #00f2ff;
        border-radius: 50%;
        box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.3), 0 0 24px rgba(0, 242, 255, 0.6), 0 0 48px 6px rgba(0, 242, 255, 0.25);
        pointer-events: none;
        z-index: 1;
    }
    /* Ares Perimeter Radar — legacy per-chart ring (keep for sidebar) */
    .ares-perimeter-outer,
    .ares-perimeter,
    .ares-perimeter [data-testid="stPlotlyChart"],
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"],
    [data-testid="stPlotlyChart"] {
        border: 2px solid #00f2ff !important;
        border-radius: 50% !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.25), 0 0 20px rgba(0, 242, 255, 0.5), 0 0 40px 4px rgba(0, 242, 255, 0.25) !important;
        filter: drop-shadow(0 0 2px rgba(0, 242, 255, 0.6));
    }
    .ares-perimeter-outer {
        display: inline-block;
        padding: 8px;
        margin: 0 auto;
    }
    /* Sidebar Live Biometric radar: circular frame + pulse */
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"] {
        overflow: hidden;
        padding: 8px !important;
        animation: tech-ring-pulse 4s ease-in-out infinite;
    }
    @keyframes tech-ring-pulse {
        0%, 100% { box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.25), 0 0 20px rgba(0, 242, 255, 0.5), 0 0 40px 4px rgba(0, 242, 255, 0.25); }
        50% { box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.4), 0 0 28px rgba(0, 242, 255, 0.7), 0 0 50px 6px rgba(0, 242, 255, 0.35); }
    }

    /* Tactical Obsidian / Zero-Box Mandate: Pure Black #0a0a0b everywhere (exclude chart paper so radar stays visible) */
    html, body {
        font-size: 14px !important;
    }
    html, body, .stApp, [data-testid="stAppViewContainer"], .main .block-container,
    section[data-testid="stSidebar"] + section.main,
    [data-testid="stHeader"],
    .archetype-reveal-section {
        background: #0a0a0b !important;
    }
    .stApp, [data-testid="stAppViewContainer"], .main .block-container {
        color: #e0e0e0 !important;
        position: relative;
    }
    /* Hide sidebar collapse icon text bug */
    div[data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span {
        display: none !important;
    }
    *, body, h1, h2, h3, .stMarkdown, p, label, span, .stRadio label, .stCaption,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stButton > button {
        font-family: 'Share Tech Mono', monospace !important;
        color: #e0e0e0 !important;
    }
    /* .glitch-text — neon cyan #00f2ff, 4s pulsing glow */
    .glitch-text {
        font-family: 'Share Tech Mono', monospace !important;
        font-weight: 700;
        color: #00f2ff;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        animation: glitch-glow 4s infinite;
    }
    @keyframes glitch-glow {
        0%, 90%, 100% { text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff; transform: translate(0); }
        92% { text-shadow: -2px 0 #00f2ff, 2px 0 #b026ff; transform: translate(-1px, 1px); }
        94% { text-shadow: 2px 0 #b026ff, -2px 0 #00f2ff; transform: translate(1px, -1px); }
        96% { text-shadow: -1px 1px #00f2ff, 1px -1px #b026ff; transform: translate(0); }
        98% { text-shadow: 1px -1px #b026ff, -1px 1px #00f2ff; transform: translate(-1px, 0); }
    }
    /* Base buttons: cyan border, no reticle (reticle only in .main-cta) */
    .stButton > button {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        background: transparent !important;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        border-color: rgba(0, 242, 255, 0.8) !important;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.4);
        background: rgba(0, 242, 255, 0.08) !important;
    }
    /* Main content CTAs: [ ENGAGE ] reticle + Tactical Amber (#ffbf00) on hover. Calibration tiles keep their label + amber hover. */
    .main-cta .stButton > button,
    .main .mission-hub-zerobox .stButton > button,
    .main .targeting-reticle .stButton > button {
        position: relative !important;
    }
    .main-cta .stButton > button span,
    .main .mission-hub-zerobox .stButton > button span,
    .main .targeting-reticle .stButton > button span {
        visibility: hidden !important;
    }
    .main-cta .stButton > button::before,
    .main .mission-hub-zerobox .stButton > button::before,
    .main .targeting-reticle .stButton > button::before {
        content: "[ ENGAGE ]" !important;
        visibility: visible !important;
        display: inline-block !important;
        position: absolute !important;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        white-space: nowrap;
    }
    .main-cta .stButton > button:hover,
    .main .mission-hub-zerobox .stButton > button:hover,
    .main .targeting-reticle .stButton > button:hover {
        border-color: #ffbf00 !important;
        box-shadow: 0 0 20px rgba(255, 191, 0, 0.6) !important;
        color: #0a0a0b !important;
        background: #ffbf00 !important;
        animation: btn-glitch 0.4s ease;
    }
    .main .calibration-bracket-wrap .stButton > button:hover {
        border-color: #ffbf00 !important;
        box-shadow: 0 0 20px rgba(255, 191, 0, 0.4) !important;
        color: #e0e0e0 !important;
        background: rgba(255, 191, 0, 0.06) !important;
    }
    @keyframes btn-glitch {
        0%, 100% { filter: none; }
        50% { text-shadow: -1px 0 #00f2ff, 1px 0 rgba(176, 38, 255, 0.8); filter: drop-shadow(0 0 6px #00f2ff); }
    }
    /* Sidebar: clean cyan-bordered buttons, no [ ] reticle — original labels visible */
    [data-testid="stSidebar"] .stButton > button {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        background: transparent !important;
        transition: all 0.25s ease;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: rgba(0, 242, 255, 0.9) !important;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.4);
        background: rgba(0, 242, 255, 0.1) !important;
        color: #e0e0e0 !important;
    }
    .neon-cyan { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; }
    .neon-green { color: #39FF14 !important; text-shadow: 0 0 10px #39FF14; }
    /* Progress bars: Neon-Cyan #00f2ff (tactical theme) */
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #00f2ff, rgba(0, 242, 255, 0.7)) !important;
        box-shadow: 0 0 12px rgba(0, 242, 255, 0.5);
    }
    .skill-heat-bar { height: 8px; border-radius: 4px; margin: 4px 0; transition: width 0.5s ease; }
    /* Typing engine: threat descriptions as live terminal feed */
    .threat-terminal-feed {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem;
        font-weight: 600;
        color: #00f2ff !important;
        text-shadow: 0 0 12px rgba(0, 242, 255, 0.9);
        margin: 1rem 0 1.25rem 0;
        padding: 0.75rem 1rem;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 4px;
        animation: terminal-fade-in 0.6s ease-out;
        position: relative;
    }
    .threat-terminal-feed::after {
        content: "▌";
        animation: cursor-blink 1s step-end infinite;
        color: #00f2ff;
        margin-left: 2px;
    }
    @keyframes terminal-fade-in {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes cursor-blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    /* Card fidelity: Explorer/Specialist/Operator — Frosted Glass + bottom-aligned buttons */
    .tier-card {
        background: rgba(10, 10, 11, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.45);
        border-radius: 10px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        font-family: 'Share Tech Mono', monospace !important;
        color: #e0e0e0;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.12), inset 0 0 30px rgba(0, 242, 255, 0.03);
        display: flex;
        flex-direction: column;
    }
    .tier-card .stButton { margin-top: auto; align-self: flex-end; }
    /* Mission Hub three-path cards — Targeting Reticles: frosted glass + 1px neon border pulse on hover */
    .mission-hub-zerobox { background: transparent; padding: 0 0 1rem 0; }
    /* Center column: Asymmetric Cyan Brackets frame entire center column (World-Class Page 18) — target column by order */
    section.main [data-testid="column"]:nth-child(2) {
        position: relative;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 8px;
        padding: 1.5rem 2rem 1.5rem 2.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 0 24px rgba(0, 242, 255, 0.12), inset 0 0 24px rgba(0, 242, 255, 0.03);
    }
    section.main [data-testid="column"]:nth-child(2)::before {
        content: "[ ";
        position: absolute;
        left: 0.6rem;
        top: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1.2rem;
        text-shadow: 0 0 12px #00f2ff;
    }
    section.main [data-testid="column"]:nth-child(2)::after {
        content: " ]";
        position: absolute;
        right: 0.6rem;
        bottom: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1.2rem;
        text-shadow: 0 0 12px #00f2ff;
    }
    .mission-hub-center-column {
        /* Kept for semantic wrapper; visual frame applied to column above */
    }
    /* Mission cards: fixed height 500px, buttons pixel-perfect aligned on horizontal line */
    .mission-hub-card {
        height: 500px !important;
        display: flex !important;
        flex-direction: column !important;
        min-height: 500px !important;
    }
    .mission-hub-card .stButton {
        margin-top: auto !important;
        align-self: flex-end;
    }
    /* Holographic Toggle: iridescent glow + subtle animation for language selector */
    .holographic-toggle {
        background: linear-gradient(135deg, rgba(0, 242, 255, 0.08), rgba(176, 38, 255, 0.05)) !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.35), 0 0 40px rgba(176, 38, 255, 0.15), inset 0 0 20px rgba(0, 242, 255, 0.06) !important;
        animation: holographic-shift 6s ease-in-out infinite;
    }
    @keyframes holographic-shift {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 242, 255, 0.35), 0 0 40px rgba(176, 38, 255, 0.15), inset 0 0 20px rgba(0, 242, 255, 0.06); }
        50% { box-shadow: 0 0 28px rgba(0, 242, 255, 0.5), 0 0 55px rgba(176, 38, 255, 0.22), inset 0 0 24px rgba(0, 242, 255, 0.08); }
    }
    /* Sidebar Language block: cyan separator + Tactical Green monospace labels */
    .sidebar-language-block {
        border: 1px solid rgba(0, 242, 255, 0.35);
        border-radius: 6px;
        margin: 0.5rem 0 0.25rem;
        padding: 0.5rem 0.75rem 0.35rem 0.75rem;
    }
    /* Sidebar Console (upper-left anchor): Language first — 1px #00f2ff glow-border, Tactical Green monospace */
    .sidebar-language-console {
        border: 1px solid #00f2ff;
        border-radius: 6px;
        margin: 0 0 0.5rem 0;
        padding: 0.5rem 0.75rem 0.35rem 0.75rem;
        box-shadow: 0 0 14px rgba(0, 242, 255, 0.55);
    }
    .sidebar-language-console .sidebar-language-label,
    [data-testid="stSidebar"] .sidebar-language-console ~ div .stRadio label,
    [data-testid="stSidebar"] .sidebar-language-console ~ div .stRadio span {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.6);
        font-size: 12px;
    }
    .sidebar-language-console .sidebar-language-label { margin: 0; }
    /* Mission Hub Landing: vertical centering of Mission + Language block within Zero-Box */
    .mission-hub-landing-marker + div {
        min-height: 75vh;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    /* Language selector: Asymmetric Cyan Brackets (same HUD as calibration) + Tactical Monospace Neon-Cyan */
    .language-selector-bracket {
        position: relative;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        padding: 1rem 1.25rem 1rem 2rem;
        margin: 1.5rem 0 0;
        box-shadow: 0 0 16px rgba(0, 242, 255, 0.15), inset 0 0 20px rgba(0, 242, 255, 0.03);
        font-family: 'Share Tech Mono', monospace !important;
    }
    .language-selector-bracket::before {
        content: "[ ";
        position: absolute;
        left: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        color: #00f2ff;
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 0 8px #00f2ff;
    }
    .language-selector-bracket::after {
        content: " ]";
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        color: #00f2ff;
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 0 8px #00f2ff;
    }
    .language-selector-bracket .stRadio label,
    .language-selector-bracket .stRadio span,
    .language-selector-bracket p {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00f2ff !important;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
    }
    .language-selector-bracket .stRadio label span {
        color: #00f2ff !important;
    }
    .language-selector-bracket + div .stRadio label,
    .language-selector-bracket + div .stRadio span {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00f2ff !important;
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
    }
    .language-selector-bracket .language-selector-label {
        margin: 0 0 0.25rem 0;
        font-size: 0.9rem;
    }
    /* Mission Hub / Proving Ground [ ENGAGE ] — keep Tactical Amber hover; base border from global reticle */
    .mission-hub-zerobox .stButton > button,
    .targeting-reticle .stButton > button {
        width: 100% !important;
        max-width: 100% !important;
        color: rgba(255, 191, 0, 0.9) !important;
        border: 1px solid #00f2ff !important;
        background: transparent !important;
        letter-spacing: 0.12em !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        box-shadow: none;
        transition: box-shadow 0.25s ease, color 0.25s ease, border-color 0.25s ease;
    }
    .mission-hub-zerobox .stButton > button:hover,
    .targeting-reticle .stButton > button:hover {
        border-color: #ffbf00 !important;
        box-shadow: 0 0 20px #ffbf00, 0 0 40px rgba(255, 191, 0, 0.25) !important;
        color: #ffbf00 !important;
        background: rgba(255, 191, 0, 0.06) !important;
    }
    .mission-hub-card {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        font-family: 'Share Tech Mono', monospace !important;
        color: #e0e0e0;
        box-shadow: none;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        min-height: 340px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    .mission-hub-card:hover {
        border-color: rgba(0, 242, 255, 0.6);
        animation: neon-border-pulse 1.5s ease-in-out infinite;
    }
    @keyframes neon-border-pulse {
        0%, 100% { box-shadow: 0 0 12px rgba(0, 242, 255, 0.25), inset 0 0 20px rgba(0, 242, 255, 0.04); }
        50% { box-shadow: 0 0 24px rgba(0, 242, 255, 0.5), inset 0 0 24px rgba(0, 242, 255, 0.08); }
    }
    /* Card metadata overlay: top-right corner, Tactical Green, 10px monospace */
    .card-metadata-overlay,
    .mission-hub-card .card-metadata-overlay {
        position: absolute !important;
        top: 8px !important;
        right: 10px !important;
        font-size: 10px !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        pointer-events: none;
        z-index: 2;
        letter-spacing: 0.02em;
    }
    .mission-hub-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        opacity: 0;
        transition: opacity 0.25s ease;
        pointer-events: none;
        z-index: 0;
    }
    .mission-hub-card:has(.mission-meta:hover)::before { opacity: 1; }
    .mission-hub-card { border-left: 1px solid transparent !important; transition: border-color 0.25s ease, box-shadow 0.25s ease; }
    .mission-hub-card:has(.mission-meta:hover) {
        border-left-color: #00f2ff !important;
        box-shadow: -4px 0 20px rgba(0, 242, 255, 0.25), inset 1px 0 0 rgba(0, 242, 255, 0.15) !important;
    }
    .mission-hub-card > * { position: relative; z-index: 1; }
    .mission-hub-card .mission-meta { cursor: default; }
    .mission-hub-card:hover { box-shadow: none; }
    .mission-hub-card h4 { color: #00f2ff !important; text-shadow: 0 0 14px #00f2ff; margin-bottom: 0.5rem; }
    .mission-hub-card .mission-goal { font-size: 0.85rem; color: #00f2ff; font-weight: 600; margin: 0.35rem 0; text-shadow: 0 0 8px rgba(0, 242, 255, 0.8); }
    .mission-hub-card .mission-meta { font-size: 0.7rem; color: rgba(0, 242, 255, 0.5); margin-bottom: 0.25rem; letter-spacing: 0.02em; }
    .mission-hub-card .mission-status { font-size: 0.65rem; color: #39FF14; margin-bottom: 0.5rem; }
    .mission-hub-card .mission-tlevel { font-size: 0.75rem; margin-top: auto; }
    .mission-hub-card .mission-tlevel.tier-yellow { color: #ffcc00; text-shadow: 0 0 8px rgba(255, 204, 0, 0.6); }
    .mission-hub-card .mission-tlevel.tier-orange { color: #ff9900; text-shadow: 0 0 8px rgba(255, 153, 0, 0.6); }
    .mission-hub-card .mission-tlevel.tier-red { color: #ff4444; text-shadow: 0 0 8px rgba(255, 68, 68, 0.6); }
    .mission-hub-card .stButton {
        margin-top: auto !important;
        width: 100% !important;
    }
    .mission-hub-card .stButton > button {
        width: 100% !important;
        letter-spacing: 0.08em;
        margin-top: auto !important;
    }
    .mission-hub-card .stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 24px rgba(255, 191, 0, 0.5); }
    .tier-card h4 {
        color: #00f2ff !important;
        text-shadow: 0 0 12px #00f2ff, 0 0 24px rgba(0, 242, 255, 0.4);
    }
    .tier-card .stButton > button {
        letter-spacing: 0.08em;
    }
    .tier-card .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 24px rgba(0, 242, 255, 0.6), 0 0 48px rgba(0, 242, 255, 0.2);
    }
    /* Glassmorphism: semi-transparent cards with blur and neon border */
    .glass-card {
        position: relative;
        background: rgba(10, 10, 11, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 0 24px rgba(0, 242, 255, 0.08), inset 0 1px 0 rgba(255,255,255,0.04);
        font-family: 'Share Tech Mono', monospace !important;
        color: #e0e0e0;
    }
    .glass-card .threat-terminal-feed { margin: 0.5rem 0; }
    /* Ares Zero-Box: Asymmetric Cyan Brackets + Tactical Green (#00FF00) mission objectives (HUD style) */
    .ares-hud-wrap {
        position: relative;
        padding: 0.75rem 1rem 0.75rem 1.25rem;
        border: 1px solid rgba(0, 242, 255, 0.45);
        border-radius: 4px;
        margin: 0.5rem 0;
        font-family: 'Share Tech Mono', monospace !important;
    }
    .ares-hud-wrap::before {
        content: "[ ";
        position: absolute;
        left: 0.5rem;
        top: 0.5rem;
        color: #00f2ff;
        font-weight: 700;
        text-shadow: 0 0 8px #00f2ff;
    }
    .ares-hud-wrap::after {
        content: " ]";
        position: absolute;
        right: 0.5rem;
        bottom: 0.5rem;
        color: #00f2ff;
        font-weight: 700;
        text-shadow: 0 0 8px #00f2ff;
    }
    .ares-tactical-green {
        color: #00FF00 !important;
        text-shadow: 0 0 10px #00FF00;
        font-weight: 600;
    }
    .ares-bridge-card {
        background: rgba(10, 10, 11, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        position: relative;
        display: flex;
        flex-direction: column;
        font-family: 'Share Tech Mono', monospace !important;
    }
    .ares-bridge-card::before {
        content: "[ ";
        position: absolute;
        left: 0.5rem;
        top: 0.5rem;
        color: #00f2ff;
        font-weight: 700;
    }
    .ares-bridge-card::after {
        content: " ]";
        position: absolute;
        right: 0.5rem;
        bottom: 0.5rem;
        color: #00f2ff;
        font-weight: 700;
    }
    .ares-bridge-card-title { color: #00f2ff !important; font-weight: 600; margin: 0.35rem 0; }
    .ares-bridge-card-value { color: #00FF00 !important; text-shadow: 0 0 8px #00FF00; margin-top: 0.5rem; }
    .ares-node {
        display: inline-block;
        vertical-align: top;
        margin: 0.5rem 0.5rem 0.5rem 0;
        padding: 0.5rem 0.75rem;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 4px;
        position: relative;
        font-family: 'Share Tech Mono', monospace !important;
    }
    .ares-node::before { content: "[ "; color: #00f2ff; font-weight: 700; }
    .ares-node::after { content: " ]"; color: #00f2ff; font-weight: 700; }
    .ares-node-code { color: #00f2ff !important; font-weight: 700; }
    .ares-node-title { color: #e0e0e0 !important; }
    .ares-node-path { color: #00FF00 !important; text-shadow: 0 0 6px #00FF00; font-size: 0.85em; }
    .ares-roadmap-summary { margin: 0.75rem 0; }
    /* Dedicated tactical frame for Mission Node Map (Ares logic) */
    .ares-tactical-frame {
        position: relative;
        border: 1px solid rgba(0, 242, 255, 0.5);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        background: rgba(10, 10, 11, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 0 24px rgba(0, 242, 255, 0.15), inset 0 1px 0 rgba(0, 242, 255, 0.1);
        font-family: 'Share Tech Mono', monospace !important;
    }
    .ares-tactical-frame .card-metadata-overlay { top: 6px; right: 10px; }
    /* Independent panel scrolling (Gemini/Game Prompts): sidebar fixed, main scrolls */
    [data-testid="stSidebar"] {
        height: 100vh !important;
        overflow-y: auto !important;
        position: relative !important;
    }
    section.main {
        max-height: 100vh !important;
        overflow-y: auto !important;
    }
    /* Industrial metadata: VECTOR_ID // THREAT_MODEL — Tactical Green #00FF00 monospace */
    .module-metadata,
    .card-metadata-overlay,
    .reveal-metadata,
    .mission-meta {
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        font-family: 'Share Tech Mono', monospace !important;
    }
    /* Sidebar Radar: force Ares Line glow-ring using ::before on Plotly container */
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"] {
        position: relative !important;
        border-radius: 50% !important;
        overflow: visible !important;
    }
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"]::before {
        content: "";
        position: absolute;
        inset: -8px;
        border-radius: 50%;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.3), 0 0 24px rgba(0, 242, 255, 0.7), 0 0 48px 6px rgba(0, 242, 255, 0.3);
        pointer-events: none;
        z-index: 2;
    }
    .module-metadata {
        position: fixed !important;
        top: 8px !important;
        right: 12px !important;
        z-index: 9999 !important;
        font-size: 10px !important;
        font-family: 'Share Tech Mono', monospace !important;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        pointer-events: none;
    }
    /* High-Fidelity Proving Ground: Calibration sequence + terminal log + bracket wrap */
    .calibration-sequence-header {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.7);
        letter-spacing: 0.06em;
        margin-bottom: 0.5rem;
    }
    .pg-terminal-log {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.8rem !important;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 4px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }
    .calibration-bracket-wrap {
        position: relative;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        padding: 1rem 1.25rem 1rem 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 16px rgba(0, 242, 255, 0.15), inset 0 0 20px rgba(0, 242, 255, 0.03);
    }
    .calibration-bracket-wrap::before {
        content: "[ ";
        position: absolute;
        left: 0.5rem;
        top: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 0 8px #00f2ff;
    }
    .calibration-bracket-wrap::after {
        content: " ]";
        position: absolute;
        right: 0.5rem;
        bottom: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 0 8px #00f2ff;
    }
    .pg-scenario-text {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #00FF00 !important;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.6);
        margin: 0.5rem 0 1rem 0;
        line-height: 1.4;
    }
    .ares-bridge-status .stStatus label { font-family: 'Share Tech Mono', monospace !important; color: #00f2ff !important; }
    /* Reveal page: asymmetric brackets + Tactical Green monospace */
    .reveal-bracket-wrap {
        position: relative;
        border: 1px solid rgba(0, 242, 255, 0.45);
        border-radius: 8px;
        padding: 1.25rem 1.5rem 1.25rem 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2), inset 0 0 24px rgba(0, 242, 255, 0.04);
    }
    .reveal-bracket-wrap::before {
        content: "[ ";
        position: absolute;
        left: 0.6rem;
        top: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1.1rem;
        text-shadow: 0 0 10px #00f2ff;
    }
    .reveal-bracket-wrap::after {
        content: " ]";
        position: absolute;
        right: 0.6rem;
        bottom: 0.75rem;
        color: #00f2ff;
        font-weight: 700;
        font-size: 1.1rem;
        text-shadow: 0 0 10px #00f2ff;
    }
    .reveal-metadata, .reveal-bracket-wrap .reveal-metadata {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 10px !important;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
    }
    .reveal-bracket-wrap .reveal-title {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #00FF00 !important;
        text-shadow: 0 0 12px rgba(0, 255, 0, 0.6);
        margin: 0.5rem 0 0.75rem 0;
    }
    .reveal-bracket-wrap .reveal-desc {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem !important;
        color: #00FF00 !important;
        text-shadow: 0 0 8px rgba(0, 255, 0, 0.4);
        line-height: 1.5;
        margin: 0;
    }
    .reveal-glitch-settle {
        animation: glitch-glow 4s ease-out forwards;
    }
    /* Archetype Synthesis: Skill Fingerprint radar — Project Ares Perimeter Ring (biometric scan) */
    .skill-fingerprint-radar-wrap {
        display: inline-block;
        border: 2px solid #00f2ff !important;
        border-radius: 50% !important;
        padding: 12px !important;
        margin: 1rem 0 !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.2), 0 0 24px rgba(0, 242, 255, 0.5), 0 0 48px 4px rgba(0, 242, 255, 0.2) !important;
        filter: drop-shadow(0 0 4px rgba(0, 242, 255, 0.5));
    }
    .skill-fingerprint-radar-wrap [data-testid="stPlotlyChart"] {
        border-radius: 50% !important;
    }
    .archetype-reveal-section {
        background: #0a0a0b !important;
        position: relative;
    }
    /* Proving Ground Calibration: Custom Action Tiles — Tactical Amber hover */
    .calibration-action-tile {
        display: block;
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        background: rgba(10, 10, 11, 0.6);
        color: #e0e0e0;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem;
        cursor: pointer;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    .calibration-action-tile:hover {
        border-color: #ffbf00 !important;
        box-shadow: 0 0 16px rgba(255, 191, 0, 0.4) !important;
        background: rgba(255, 191, 0, 0.06) !important;
    }
    /* Apply tile styling to buttons inside calibration bracket */
    .calibration-bracket-wrap button {
        display: block;
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 242, 255, 0.4);
        border-radius: 6px;
        background: rgba(10, 10, 11, 0.6);
        color: #e0e0e0;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem;
        cursor: pointer;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    .calibration-bracket-wrap button:hover {
        border-color: #ffbf00 !important;
        box-shadow: 0 0 16px rgba(255, 191, 0, 0.4) !important;
        background: rgba(255, 191, 0, 0.06) !important;
    }
    /* Calibration counter: top-right, Tactical Green #00FF00 monospace */
    .calibration-counter {
        position: absolute;
        top: 8px;
        right: 12px;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 11px;
        color: #00FF00 !important;
        text-shadow: 0 0 6px rgba(0, 255, 0, 0.5);
        letter-spacing: 0.04em;
        z-index: 2;
    }
    /* Ares Bridge full-screen overlay */
    .ares-bridge-overlay {
        position: fixed;
        inset: 0;
        background: #0a0a0b;
        z-index: 10001;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    .ares-bridge-terminal {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem;
        color: #00FF00;
        text-shadow: 0 0 8px rgba(0, 255, 0, 0.6);
        letter-spacing: 0.08em;
        animation: terminal-blink 1s step-end infinite;
    }
    @keyframes terminal-blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.4; }
    }
</style>
"""
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

# Persistent UI wrapper: Fixed Asymmetric Cyan Brackets at all four viewport corners + module metadata
def _render_zerobox_wrapper() -> None:
    html_str = f"""
    <div id="zerobox-bracket-tl" style="position:fixed;top:0;left:0;width:120px;height:120px;border-top:2px solid #00f2ff;border-left:2px solid #00f2ff;pointer-events:none;z-index:10000;box-shadow:0 0 12px rgba(0,242,255,0.4);"></div>
    <div id="zerobox-bracket-tr" style="position:fixed;top:0;right:0;width:100px;height:100px;border-top:2px solid #00f2ff;border-right:2px solid #00f2ff;pointer-events:none;z-index:10000;box-shadow:0 0 12px rgba(0,242,255,0.4);"></div>
    <div id="zerobox-bracket-bl" style="position:fixed;bottom:0;left:0;width:100px;height:100px;border-bottom:2px solid #00f2ff;border-left:2px solid #00f2ff;pointer-events:none;z-index:10000;box-shadow:0 0 12px rgba(0,242,255,0.4);"></div>
    <div id="zerobox-bracket-br" style="position:fixed;bottom:0;right:0;width:120px;height:120px;border-bottom:2px solid #00f2ff;border-right:2px solid #00f2ff;pointer-events:none;z-index:10000;box-shadow:0 0 12px rgba(0,242,255,0.4);"></div>
    <div class="module-metadata">{html.escape(MODULE_METADATA_STR)}</div>
    """
    st.html(html_str)

_render_zerobox_wrapper()

# One-time Zero-Box refresh after CSS injection to clear broken cache (e.g. after syntax fix)
if not st.session_state.get("zerobox_css_refreshed", False):
    st.session_state.zerobox_css_refreshed = True
    st.rerun()
def _record_proving_ground_reflex(choice: str, correct_action: str, nice_category: str) -> None:
    """Proving Ground Reflex Lab only: update score and XP; do not advance Mission Hub index."""
    if choice == correct_action and nice_category:
        score_state = st.session_state.get("score")
        if score_state is not None:
            score_state.add_weights({nice_category: 0.1})
        st.session_state.xp = st.session_state.get("xp", 0) + XP_PER_REFLEX_CORRECT
        st.session_state.agent_rank = xp_to_rank(st.session_state.get("xp", 0))


def _record_pg_validation_choice(choice_index: int, question: Question) -> Optional[str]:
    """
    Proving Ground Calibration (30-step: 20 Personality + 10 Core) only: add weights to score, do not touch mission index.
    Returns terminal-style log string for TKS feedback.
    """
    if not question.choices or choice_index >= len(question.choices):
        return None
    score_state = st.session_state.get("score")
    if score_state is None:
        return None
    w = question.choices[choice_index].weights
    score_state.add_weights(w)
    sorted_cats = sorted(w.items(), key=lambda x: -x[1])
    cat_labels = get_category_labels(_get_lang())
    names = [cat_labels.get(c, c).upper() for c, _ in sorted_cats[:2]]
    cat_str = ", ".join(f"[{n}]" for n in names) if names else "[NIST]"
    return f"[SYSTEM] TKS METADATA EXTRACTED... CATEGORY: {cat_str} UPDATED."


def _record_reflex_choice(choice: str, correct_action: str, nice_category: str) -> None:
    """Scoring: weighted attribution. Specialist/Operator use 0.2 and 2× XP (multiplier logic)."""
    st.session_state.responses.append(choice)
    tier = st.session_state.get("mission_tier", "")
    use_double = tier in ["specialist", "operator"]
    weight = 0.2 if use_double else 0.1
    if choice == correct_action and nice_category:
        score_state = st.session_state.get("score")
        if score_state is not None:
            score_state.add_weights({nice_category: weight})
        xp_delta = XP_PER_REFLEX_CORRECT * 2 if use_double else XP_PER_REFLEX_CORRECT
        st.session_state.xp = st.session_state.get("xp", 0) + xp_delta
        st.session_state.agent_rank = xp_to_rank(st.session_state.get("xp", 0))
    st.session_state.current_question_index = st.session_state.get("current_question_index", 0) + 1
    idx_next = st.session_state.current_question_index
    if idx_next >= len(st.session_state.get("questions", [])):
        st.session_state.reflex_complete = True
    st.session_state.reflex_drill_index = idx_next


def _record_instinct_choice(choice_index: int, question: Question) -> None:
    """Scoring: weighted matrix from choice. Specialist/Operator use double weights and 2× XP."""
    st.session_state.responses.append(["NEUTRALIZE", "DROP", "FREEZE"][choice_index] if choice_index < 3 else "")
    tier = st.session_state.get("mission_tier", "")
    use_double = tier in ["specialist", "operator"]
    if question.choices and choice_index < len(question.choices):
        score_state = st.session_state.get("score")
        if score_state is not None:
            w = question.choices[choice_index].weights
            score_state.add_weights(w)
            if use_double:
                score_state.add_weights(w)
        xp_delta = XP_PER_INSTINCT_CHOICE * 2 if use_double else XP_PER_INSTINCT_CHOICE
        st.session_state.xp = st.session_state.get("xp", 0) + xp_delta
        correct = getattr(question, "correct_index", None) is not None and question.correct_index == choice_index
        if correct:
            bonus = (XP_PER_TECHNICAL_CORRECT - XP_PER_INSTINCT_CHOICE) * (2 if use_double else 1)
            st.session_state.xp = st.session_state.get("xp", 0) + bonus
        st.session_state.agent_rank = xp_to_rank(st.session_state.get("xp", 0))
    st.session_state.current_question_index = st.session_state.get("current_question_index", 0) + 1
    idx_next = st.session_state.current_question_index
    if idx_next >= len(st.session_state.get("questions", [])):
        st.session_state.reflex_complete = True
    st.session_state.reflex_drill_index = idx_next


def render_mission_hub() -> None:
    """Three-Path Mission Hub: Explorer (20), Specialist (50), Operator (10). Cards when mission_active is False."""
    _init_session()
    ui = get_ui(_get_lang())
    mission_active = st.session_state.get("mission_active", False)

    # ─── Landing: Centered vertical stack — st.columns([1, 4, 1]); center = title → Language (Holographic) → 3 cards; asymmetric brackets frame ─
    if not mission_active:
        st.markdown('<div class="mission-hub-landing-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
        col_left, col_center, col_right = st.columns([1, 4, 1])
        with col_center:
            st.markdown(
                '<p class="glitch-text" style="font-size:1.25rem;margin-bottom:0.25rem;">' + html.escape(ui.get("mission_hub_title", "Mission Hub")) + '</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="neon-cyan" style="font-size:0.95rem;margin-bottom:0.75rem;">Select a path to begin. Each path loads a distinct question pool and feeds the Live Biometric radar.</p>',
                unsafe_allow_html=True,
            )
            # Nested 3-column container for Mission Cards
            st.markdown('<div class="main-cta mission-hub-zerobox">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    '<div class="mission-hub-card targeting-reticle-card">'
                    '<div class="card-metadata-overlay">VECTOR_ID: EXP-20 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div>'
                    '<div class="mission-meta">VECTOR_ID: EXP-20 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div class="mission-status">SYSTEM STATUS: NOMINAL</div>'
                    '<h4>' + html.escape(ui.get("mode_explorer", "The Explorer")) + '</h4>'
                    '<p class="mission-goal">Goal: Baseline NIST orientation.</p>'
                    '<p style="margin:0.35rem 0;font-size:0.85rem;">20 scenarios. Find your Cyber Archetype and align with NICE work roles. Standard weight.</p>'
                    '</div>'
                    '<p class="mission-tlevel tier-yellow">T-LEVEL: YELLOW · Standard weight</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button("[ ENGAGE ]", key="tier_explorer"):
                    start_mission("explorer")
                    st.rerun()
            with c2:
                st.markdown(
                    '<div class="mission-hub-card targeting-reticle-card">'
                    '<div class="card-metadata-overlay">VECTOR_ID: TKS-50 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div>'
                    '<div class="mission-meta">VECTOR_ID: TKS-50 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div class="mission-status">SYSTEM STATUS: NOMINAL</div>'
                    '<h4>' + html.escape(ui.get("mode_specialist", "The Specialist")) + '</h4>'
                    '<p class="mission-goal">Goal: Deep-dive into technical TKS (Tasks, Knowledge, Skills).</p>'
                    '<p style="margin:0.35rem 0;font-size:0.85rem;">50 scenarios. Full NIST TKS gap analysis. 2× weight and XP.</p>'
                    '</div>'
                    '<p class="mission-tlevel tier-orange">T-LEVEL: ORANGE · 2× weight</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button("[ ENGAGE ]", key="tier_specialist"):
                    start_mission("specialist")
                    st.rerun()
            with c3:
                st.markdown(
                    '<div class="mission-hub-card targeting-reticle-card">'
                    '<div class="card-metadata-overlay">VECTOR_ID: OP-10 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div>'
                    '<div class="mission-meta">VECTOR_ID: OP-10 // THREAT_MODEL: 2026_STANDARD</div>'
                    '<div class="mission-status">SYSTEM STATUS: NOMINAL</div>'
                    '<h4>' + html.escape(ui.get("mode_operator", "The Operator")) + '</h4>'
                    '<p class="mission-goal">Goal: Rapid decision-making under pressure.</p>'
                    '<p style="margin:0.35rem 0;font-size:0.85rem;">10 threats. NEUTRALIZE / DROP / FREEZE. Rapid-fire reflex. 2× weight.</p>'
                    '</div>'
                    '<p class="mission-tlevel tier-red">T-LEVEL: RED · 2× weight</p>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                if st.button("[ ENGAGE ]", key="tier_operator"):
                    start_mission("operator")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        return

    # ─── Drill: mission active — show questions ─
    st.markdown("---")
    questions = st.session_state.questions
    idx = st.session_state.get("current_question_index", 0)
    total = len(questions)
    if total == 0:
        total = st.session_state.get("mission_total", 10)
        st.session_state.questions = list(REFLEX_THREATS)
        questions = st.session_state.questions
        total = len(questions)
    ui = get_ui(_get_lang())

    # Diagnostic completion progress (Always-Live: strict safety — float 0.0–1.0 only)
    mission_total = st.session_state.get("mission_total", 0)
    question_index = st.session_state.get("current_question_index", 0)
    progress_pct = 0.0
    if mission_total > 0:
        progress_pct = float(question_index) / float(mission_total)
    progress_pct = max(0.0, min(1.0, float(progress_pct)))
    try:
        st.progress(progress_pct, key="mission_diagnostic_progress")
    except (ValueError, TypeError):
        st.caption(f"Progress: {question_index} of {mission_total} ({int(progress_pct * 100)}%)")
    display_total = total if total > 0 else mission_total
    st.caption(f"{ui.get('question_count', 'Question')} {min(idx + 1, display_total)} {ui.get('of', 'of')} {display_total}")

    # Back to Mission Hub (Game Prompts / Gemini: button on every question page)
    if st.button("← " + ui.get("back_to_hub", "Back to Mission Hub"), key="back_to_hub_drill"):
        st.session_state.mission_tier = None
        st.session_state.mission_active = False
        st.rerun()

    if idx >= total:
        st.session_state.reflex_complete = True
        # Tier completion XP
        tier = st.session_state.get("mission_tier", "")
        if tier == "explorer":
            st.session_state.xp = st.session_state.get("xp", 0) + XP_EXPLORER_COMPLETE
        elif tier == "specialist":
            st.session_state.xp = st.session_state.get("xp", 0) + XP_SPECIALIST_COMPLETE
        elif tier == "operator":
            st.session_state.xp = st.session_state.get("xp", 0) + XP_OPERATOR_COMPLETE
        st.session_state.agent_rank = xp_to_rank(st.session_state.get("xp", 0))
        st.markdown(
            '<div style="font-family:\'Share Tech Mono\',monospace;font-weight:700;color:#39FF14;'
            'text-shadow:0 0 14px #39FF14;">SYSTEM SCAN COMPLETE</div>',
            unsafe_allow_html=True,
        )
        st.caption(ui.get("reflex_system_nominal", "System Nominal"))
        return

    # Central display: current scenario (Explorer/Specialist = Question objects; Operator = 10 reflex tuples)
    mission_tier = st.session_state.get("mission_tier", "")
    current = questions[idx]
    is_reflex_tuple = isinstance(current, (list, tuple)) and len(current) >= 3
    if is_reflex_tuple:
        threat_text, correct_action, nice_category = current[0], current[1], current[2]
        st.markdown(
            '<div class="threat-terminal-feed" style="font-family:\'Share Tech Mono\',monospace;'
            'font-size:1rem;font-weight:600;color:#00f2ff !important;text-shadow:0 0 12px rgba(0,242,255,0.9);'
            'margin:1rem 0 1.25rem 0;padding:0.75rem;border:1px solid rgba(0,242,255,0.4);border-radius:4px;">'
            f'{html.escape(threat_text)}</div>',
            unsafe_allow_html=True,
        )
        # Monospace button array → Phase 1 _record_reflex_choice
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(" [ NEUTRALIZE ] ", key="mh_neutralize"):
                _record_reflex_choice("NEUTRALIZE", correct_action, nice_category)
                st.rerun()
        with c2:
            if st.button(" [ DROP ] ", key="mh_drop"):
                _record_reflex_choice("DROP", correct_action, nice_category)
                st.rerun()
        with c3:
            if st.button(" [ FREEZE ] ", key="mh_freeze"):
                _record_reflex_choice("FREEZE", correct_action, nice_category)
                st.rerun()
    else:
        # Explorer / Specialist / Operator: Question with .prompt and .choices → st.radio (Modern Web UI)
        q = current
        prompt_text = getattr(q, "prompt", str(q))
        st.markdown(
            '<div class="threat-terminal-feed" style="font-family:\'Share Tech Mono\',monospace;'
            'font-size:1rem;font-weight:600;color:#00f2ff !important;text-shadow:0 0 12px rgba(0,242,255,0.9);'
            'margin:1rem 0 1.25rem 0;padding:0.75rem;border:1px solid rgba(0,242,255,0.4);border-radius:4px;">'
            f'{html.escape(prompt_text)}</div>',
            unsafe_allow_html=True,
        )
        choices = getattr(q, "choices", [])
        if not choices:
            st.caption("No choices for this question.")
            return
        option_labels = [getattr(c, "text", str(c)) for c in choices]
        selected = st.radio(
            ui.get("select_response", "Select your response"),
            option_labels,
            key=f"mh_radio_{idx}",
            index=None,
        )
        if st.button(ui.get("submit_next", "Submit & Next"), key=f"mh_submit_{idx}"):
            if selected is not None:
                choice_index = option_labels.index(selected)
                _record_instinct_choice(choice_index, q)
                st.rerun()
            else:
                st.warning(ui.get("please_select", "Please select an option."))


def render_archetype() -> None:
    """High-Fidelity Reveal: Archetype Synthesis, glitch-title, large Skill Fingerprint radar, bracket-framed portrait, Mission Node Map (3 BRs to Level Up)."""
    ui = get_ui(_get_lang())
    score_state = st.session_state.get("score")
    if score_state is None:
        st.markdown('<p class="neon-green">Complete the Mission Hub to unlock your Cyber Archetype.</p>', unsafe_allow_html=True)
        return
    lang = _get_lang()
    raw_scores = score_state.get_category_scores()
    raw_max = max(raw_scores.values()) if raw_scores else 0.0
    # 65% competency threshold: below baseline → Capability Gap screen (Game Prompts / Gemini)
    if raw_max < COMPETENCY_RAW_THRESHOLD:
        st.markdown(
            f'<div class="glass-card">'
            f'<div class="card-metadata-overlay">VECTOR_ID: GAP // THREAT_MODEL: 2026_STANDARD</div>'
            f'<h3 class="neon-cyan">{html.escape(ui.get("capability_gap_title", "Capability Gap Detected"))}</h3>'
            f'<p>{html.escape(ui.get("capability_gap_message", "You have not met the baseline for specialized roles."))}</p>'
            f'<p class="neon-green">{html.escape(ui.get("suggest_explorer_path", "We suggest the Explorer path for foundational upskilling."))}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(" [ " + ui.get("nav_mission_hub", "Mission Hub") + " ] ", key="gap_go_hub"):
            st.session_state.nav_page = "mission_hub"
            st.rerun()
        return
    archetype_id, archetype_title, archetype_desc = score_state.get_reveal_archetype()
    radar = score_state.get_normalized_radar_scores()
    category_labels = get_category_labels(lang)
    verification_hash = str(hash(str(raw_scores)))[:12].replace("-", "0")
    mission_tier = st.session_state.get("mission_tier", "")
    tier_badge = mission_tier.capitalize() if mission_tier else "—"
    match_pct = score_state.get_top_role_match_pct()
    archetype_match_str = f"{min(99.9, max(85.0, match_pct)):.1f}%" if match_pct else "98.4%"

    # Diegetic Reveal: st.html glitch-text entrance for Archetype name
    st.html(
        f'<div class="archetype-reveal-section">'
        f'<p class="glitch-text reveal-glitch-settle" style="font-size:1.75rem;margin-bottom:0.5rem;">{html.escape(archetype_title)}</p>'
        f'</div>'
    )
    # Industrial metadata — Tactical Green (#00FF00)
    st.markdown(
        f'<p class="reveal-metadata" style="margin-top:0;color:#00FF00 !important;">SUBJECT_ID: VERIFIED // ARCHETYPE_MATCH: {html.escape(archetype_match_str)}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="reveal-metadata" style="font-size:11px;margin-bottom:0.25rem;">SKILL FINGERPRINT // NIST NICE 7-CATEGORY</p>',
        unsafe_allow_html=True,
    )
    # Large-Scale Radar (2x sidebar height=440): Project Ares Perimeter Ring applied via global CSS to stPlotlyChart
    render_radar_chart_compact(radar, category_labels, height=440, accent_color="#00f2ff", fill_color="rgba(0, 242, 255, 0.2)")
    st.markdown("---")
    st.markdown(
        f'<div class="reveal-bracket-wrap">'
        f'<p class="reveal-metadata">VECTOR_ID: ARCHETYPE // ARCHETYPE_ID: {html.escape(archetype_id.upper())} // THREAT_MODEL: 2026_STANDARD</p>'
        f'<p class="reveal-metadata">VERIFICATION_HASH // {html.escape(verification_hash)} &nbsp; OPERATOR_TIER // {html.escape(tier_badge)}</p>'
        f'<p class="reveal-title">{html.escape(archetype_title)}</p>'
        f'<p class="reveal-desc">{html.escape(archetype_desc)}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    from cyber_career_compass.scoring import get_ares_recommendations
    from cyber_career_compass.project_ares import ARES_SCENARIOS
    from cyber_career_compass.results import render_ares_roadmap_summary
    ares_recs = get_ares_recommendations(score_state, max_per_category=4)
    br_only = [r for r in ares_recs if r.get("mission_id", "").startswith("BR")][:3]
    level_up_deployments = []
    for r in br_only:
        sid = r.get("mission_id", "")
        info = ARES_SCENARIOS.get(sid, {})
        relevance = r.get("relevance", info.get("training_value", ""))
        level_up_deployments.append({
            "id": sid,
            "title": r.get("title", info.get("title", sid)),
            "learning_path": relevance,
            "type": "BR",
        })
    if level_up_deployments:
        st.markdown(
            '<p class="reveal-metadata" style="font-size:11px;margin:1rem 0 0.5rem 0;">LEVEL UP // BATTLE ROOMS TO MASTER (PROJECT ARES NICE GUIDE v1.0.0)</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="reveal-bracket-wrap ares-deployment-bracket">'
            '<p class="reveal-metadata" style="margin-bottom:0.5rem;">ARES DEPLOYMENT ROADMAP // 3 RECOMMENDED MISSIONS</p>',
            unsafe_allow_html=True,
        )
        render_ares_roadmap_summary(
            level_up_deployments,
            lang,
            tactical_frame=False,
            metadata_str=None,
            skip_anchor_nodes=True,
            title_override="Mission Node Map",
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    # Dossier by tier: Explorer → light report; Specialist → full High-Security Dossier; Operator → Mission Complete summary
    mission_tier = st.session_state.get("mission_tier", "")
    if mission_tier == "explorer":
        render_dossier_explorer(score_state, lang)
    elif mission_tier == "specialist":
        render_dossier(score_state, lang)
    elif mission_tier == "operator":
        render_dossier_operator(score_state, lang)
    else:
        render_dossier(score_state, lang)
    st.markdown("---")
    # 2026 Job Role Dossier: top 3 matched roles with exact DNA descriptions (Cyber Defense Analyst, Security Architect, Incident Responder)
    st.markdown("#### " + ui.get("recommended_roles_2026_title", "2026 Job Role Dossier — Top 3 Matched Roles"))
    role_scores = score_state.get_role_probabilities()
    top_roles = sorted(
        [(rid, role_scores.get(rid, 0.0)) for rid in ALL_ROLE_IDS if role_scores.get(rid, 0.0) > 0],
        key=lambda x: -x[1],
    )[:3]
    # DNA: exact 2026 role descriptions for primary roles
    ROLE_2026_DESCRIPTIONS = {
        "PR-CDA": "Cyber Defense Analyst — Monitors and analyzes events to protect systems and respond to incidents. NICE PR category.",
        "SP-ARC": "Security Architect — Designs and builds secure systems, networks, and architectures. NICE SP category.",
        "PR-IR": "Incident Responder — Investigates and mitigates security incidents and coordinates response activities. NICE PR category.",
        "SP-SSE": "Secure Software Assessor — Assesses the security of software and systems through testing and analysis. NICE SP category.",
        "AN-TWA": "Threat/Warning Analyst — Analyzes threat data and produces assessments and warnings for decision makers. NICE AN category.",
        "IN-CLI": "Cyber Crime Investigator — Investigates cyber crimes and compiles evidence for legal proceedings. NICE IN category.",
    }
    for i, (role_id, score_val) in enumerate(top_roles, 1):
        display = get_role_display(lang, role_id)
        rtitle = display.get("title", role_id) if display else role_id
        rdef = display.get("definition", "") if display else ""
        dna_desc = ROLE_2026_DESCRIPTIONS.get(role_id, rdef or f"{rtitle} — NIST NICE work role.")
        st.markdown(f'<p class="neon-cyan">**{i}. {html.escape(rtitle)}** · {html.escape(role_id)} ({score_val:.0f}% match)</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;color:#e0e0e0;font-size:0.9rem;">{html.escape(dna_desc)}</p>', unsafe_allow_html=True)
    if not top_roles:
        st.caption(ui.get("no_roles_yet", "Complete Mission Hub to get role recommendations."))


def _render_sidebar_agent() -> None:
    """Floating Biometric HUD: Language first (upper-left anchor), nav, status, radar with Ares Line."""
    _init_session()
    ui = get_ui(_get_lang())
    with st.sidebar:
        # Sidebar Console: Language Selection at absolute top (first element operator sees)
        with st.container():
            st.markdown(
                '<div class="sidebar-language-console">'
                '<p class="sidebar-language-label">' + html.escape(ui.get("language_label", "Language")) + '</p>'
                '</div>',
                unsafe_allow_html=True,
            )
            current_lang = _get_lang()
            lang_index = min(SUPPORTED_LANGUAGES.index(current_lang), len(SUPPORTED_LANGUAGES) - 1) if current_lang in SUPPORTED_LANGUAGES else 0
            new_lang = st.radio(
                ui.get("language_label", "Language"),
                options=SUPPORTED_LANGUAGES,
                format_func=lambda x: LANGUAGE_LABELS[x],
                index=lang_index,
                key="sidebar_lang_radio",
                horizontal=False,
                label_visibility="collapsed",
            )
            if new_lang != current_lang:
                st.session_state.lang = new_lang
                st.session_state.language = new_lang
                st.rerun()
        st.markdown("---")
        if st.button(ui.get("nav_mission_hub", "Mission Hub"), key="nav_mission_hub_btn"):
            st.session_state.nav_page = "mission_hub"
            st.rerun()
        if st.button(ui.get("nav_proving_ground", "Proving Ground"), key="nav_proving_ground_btn"):
            st.session_state.nav_page = "proving_ground"
            st.rerun()
        if st.button(ui.get("nav_archetype", "Cyber Archetype"), key="nav_archetype_btn"):
            st.session_state.nav_page = "archetype"
            st.rerun()
        st.markdown("---")
        st.markdown(
            '<p class="tactical-summary-header">' + html.escape(ui.get("sidebar_title", "Tactical Summary")) + '</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        reflex_idx = st.session_state.get("reflex_drill_index", 0)
        mission_tier = st.session_state.get("mission_tier")
        mission_total = st.session_state.get("mission_total", 10)
        if mission_tier == "explorer":
            mode_label = "Explorer"
        elif mission_tier == "specialist":
            mode_label = "Specialist"
        elif mission_tier == "operator":
            mode_label = "Operator"
        else:
            mode_label = ui.get("status_idle", "Idle")
        total = mission_total
        question_num = min(reflex_idx + 1, total) if total else reflex_idx + 1
        st.markdown(
            f'<p class="tactical-status"><strong>{html.escape(ui.get("sidebar_status", "Status"))}:</strong> {html.escape(mode_label)}</p>'
            f'<p class="tactical-status"><strong>XP:</strong> {st.session_state.get("xp", 0)} · <strong>Rank:</strong> {html.escape(st.session_state.get("agent_rank", "Security Initiate"))}</p>'
            f'<p class="tactical-status"><strong>Question count:</strong> {question_num} of {total}</p>'
            f'<p class="tactical-status"><strong>Progress:</strong> {reflex_idx} of {total} {html.escape(ui.get("answered", "answered"))}</p>',
            unsafe_allow_html=True,
        )
        st.progress(reflex_idx / total if total else 0)
        # Proving Ground 30-Step Calibration status in sidebar
        st.markdown(
            '<p class="tactical-status" style="font-size:0.7rem;">[ CALIBRATION_SEQ: 30_UNITS_ACTIVE ]</p>',
            unsafe_allow_html=True,
        )
        score_state = st.session_state.get("score")
        if score_state is not None:
            try:
                radar = score_state.get_normalized_radar_scores()
                cat_labels = get_category_labels(_get_lang())
                if radar and cat_labels:
                    st.markdown('<p class="tactical-summary-header">' + html.escape(ui.get("live_biometric_title", "Live Biometric")) + '</p>', unsafe_allow_html=True)
                    render_radar_chart_compact(radar, cat_labels, height=220, accent_color="#00f2ff", fill_color="rgba(0, 242, 255, 0.2)")
                    st.markdown('<p class="tactical-summary-header">' + html.escape(ui.get("skill_heatmap_title", "Skill Heatmap")) + '</p>', unsafe_allow_html=True)
                    for cat in ALL_CATEGORIES:
                        if cat not in radar:
                            continue
                        v = max(0, min(100, radar[cat]))
                        r = int(34 + (239 - 34) * v / 100)
                        g = int(197 + (68 - 197) * v / 100)
                        b = int(94 + (68 - 94) * v / 100)
                        label = cat_labels.get(cat, cat)
                        st.markdown(
                            f'<div class="tactical-status" style="font-size:0.75rem;margin:2px 0;">{html.escape(label)}</div>'
                            f'<div class="skill-heat-bar" style="width:100%;background:rgba(60,60,60,0.6);">'
                            f'<div class="skill-heat-bar" style="width:{v}%;background:rgb({r},{g},{b});"></div></div>',
                            unsafe_allow_html=True,
                        )
            except Exception:
                pass
        st.markdown('<p class="tactical-status" style="font-size:0.7rem;">' + html.escape(ui.get("sidebar_footer", "NIST NICE · Cyber Career Compass")) + '</p>', unsafe_allow_html=True)


def _page_mission_hub() -> None:
    render_mission_hub()


def _page_proving_ground() -> None:
    """Proving Grounds — Reflex: Hygiene (10 threats), Validation: NICE, Live-Fire: Breach (Game Prompts module branding)."""
    _init_session()
    ui = get_ui(_get_lang())
    st.markdown(
        '<div style="position:relative;">'
        '<p class="glitch-text">' + html.escape(ui.get("nav_proving_ground", "The Proving Grounds")) + '</p>'
        '<div class="card-metadata-overlay" style="top:0;right:0;">REFLEX_MODULE // THREAT_MODEL: 2026_STANDARD</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.session_state.get("reflex_complete", False):
        score_state = st.session_state.get("score")
        primary_archetype = score_state.get_archetype() if score_state else "agent"
        archetype_label = primary_archetype.capitalize()
        st.markdown(
            f'<div class="threat-terminal-feed" style="color:#39FF14 !important;">'
            f'<strong>REFLEX LAB COMPLETE</strong> — Your primary archetype: <span class="neon-cyan">{html.escape(archetype_label)}</span>. '
            f'Proceed to Cyber Archetype for full Dossier.</div>',
            unsafe_allow_html=True,
        )
        return
    # Module branding: Reflex: Hygiene — 60-second sprint (correct +2s, wrong -5s)
    st.markdown(f'<p class="neon-cyan" style="font-size:1.05rem;">**{html.escape(ui.get("pg_reflex_hygiene", "Reflex: Hygiene"))}**</p>', unsafe_allow_html=True)
    st.caption(ui.get("pg_reflex_desc", "10 NIST-mapped threats. 60s sprint: correct +2s, wrong -5s."))
    if st.session_state.get("pg_sprint_active", False):
        end_ts = st.session_state.get("pg_sprint_end_ts", 0)
        sprint_idx = st.session_state.get("pg_sprint_index", 0)
        sprint_correct = st.session_state.get("pg_sprint_correct", 0)
        remaining = max(0.0, end_ts - time.time())
        if remaining <= 0 or sprint_idx >= len(REFLEX_THREATS):
            st.session_state.pg_sprint_active = False
            st.markdown(
                f'<div class="glass-card"><p class="neon-green">SPRINT OVER</p>'
                f'<p>Correct: {sprint_correct} of {sprint_idx}</p></div>',
                unsafe_allow_html=True,
            )
            if sprint_idx >= len(REFLEX_THREATS):
                st.session_state.reflex_complete = True
                st.session_state.xp = st.session_state.get("xp", 0) + XP_REFLEX_LAB_COMPLETE
                st.session_state.agent_rank = xp_to_rank(st.session_state.get("xp", 0))
            # Auto-Trigger Deployment: rerun so Mission Node Map and Recommended Training Deployments populate instantly
            st.rerun()
            return
        st.markdown(
            f'<p style="font-size:2rem;font-weight:700;color:#ff4444;text-shadow:0 0 20px #ff4444;">{int(remaining)}s</p>',
            unsafe_allow_html=True,
        )
        threat_text, correct_action, nice_category = REFLEX_THREATS[sprint_idx]
        st.markdown(
            '<div class="threat-terminal-feed" style="font-family:\'Share Tech Mono\',monospace;'
            'font-size:1rem;font-weight:600;color:#00f2ff !important;">'
            f'{html.escape(threat_text)}</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(" [ NEUTRALIZE ] ", key="pg_sprint_neutralize"):
                _record_proving_ground_reflex("NEUTRALIZE", correct_action, nice_category)
                st.session_state.pg_sprint_index = sprint_idx + 1
                if correct_action == "NEUTRALIZE":
                    st.session_state.pg_sprint_correct = sprint_correct + 1
                    st.session_state.pg_sprint_end_ts = end_ts + 2
                else:
                    st.session_state.pg_sprint_end_ts = end_ts - 5
                st.rerun()
        with c2:
            if st.button(" [ DROP ] ", key="pg_sprint_drop"):
                _record_proving_ground_reflex("DROP", correct_action, nice_category)
                st.session_state.pg_sprint_index = sprint_idx + 1
                if correct_action == "DROP":
                    st.session_state.pg_sprint_correct = sprint_correct + 1
                    st.session_state.pg_sprint_end_ts = end_ts + 2
                else:
                    st.session_state.pg_sprint_end_ts = end_ts - 5
                st.rerun()
        with c3:
            if st.button(" [ FREEZE ] ", key="pg_sprint_freeze"):
                _record_proving_ground_reflex("FREEZE", correct_action, nice_category)
                st.session_state.pg_sprint_index = sprint_idx + 1
                if correct_action == "FREEZE":
                    st.session_state.pg_sprint_correct = sprint_correct + 1
                    st.session_state.pg_sprint_end_ts = end_ts + 2
                else:
                    st.session_state.pg_sprint_end_ts = end_ts - 5
                st.rerun()
    else:
        st.markdown('<div class="targeting-reticle">', unsafe_allow_html=True)
        if st.button(" [ ENGAGE 60s SPRINT ] ", key="pg_start_sprint"):
            st.session_state.pg_sprint_active = True
            st.session_state.pg_sprint_end_ts = time.time() + 60
            st.session_state.pg_sprint_index = 0
            st.session_state.pg_sprint_correct = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    # 30-Step Calibration: 20 Personality + 10 Core (World-Class Page 18)
    st.markdown(
        '<p class="neon-cyan" style="font-size:0.95rem;">'
        '<strong>[ STATUS: 30-STEP CALIBRATION INITIALIZED ]</strong></p>'
        '<p class="tactical-status" style="font-size:0.8rem;margin-top:0.25rem;">20 Personality (NIST TKS/Work Roles) + 10 Core Technical</p>',
        unsafe_allow_html=True,
    )
    # Ares Bridge: show full-screen overlay when calibration just completed (before checking pg_validation_active)
    if st.session_state.get("pg_ares_bridge_show", False):
        st.html(
            '<div class="ares-bridge-overlay">'
            '<p class="ares-bridge-terminal">EXTRACTING TKS METADATA... ANALYZING NIST WORK ROLE GAPS...</p>'
            '<p class="ares-bridge-terminal" style="margin-top:1rem;">REDIRECTING TO CYBER ARCHETYPE REVEAL...</p>'
            '</div>'
        )
        st.session_state.pg_ares_bridge_show = False
        st.session_state.nav_page = "archetype"
        time.sleep(2.2)
        st.rerun()
        return
    if st.session_state.get("pg_validation_active", False):
        val_questions = st.session_state.get("pg_validation_questions", [])
        val_idx = st.session_state.get("pg_validation_index", 0)
        val_total = len(val_questions)
        if val_idx >= val_total or not val_questions:
            # Trigger Ares Bridge on next rerun
            st.session_state.pg_validation_active = False
            st.session_state.reflex_complete = True
            if "pg_last_tks_log" in st.session_state:
                del st.session_state["pg_last_tks_log"]
            st.session_state.pg_ares_bridge_show = True
            st.rerun()
            return
        score_state = st.session_state.get("score")
        cat_labels = get_category_labels(_get_lang())
        seq_num = val_idx + 1
        # Calibration counter: top-right, Tactical Green [n / 30]
        st.markdown(
            f'<p class="calibration-counter">CALIBRATION: [{seq_num} / {CALIBRATION_TOTAL}]</p>',
            unsafe_allow_html=True,
        )
        # Asymmetric Cyan Brackets frame around calibration area
        st.markdown('<div class="calibration-bracket-wrap" style="position:relative;margin-top:2rem;">', unsafe_allow_html=True)
        # Center: NIST Radar (real-time pulse — updates each rerun after answer)
        if score_state is not None and cat_labels:
            radar = score_state.get_normalized_radar_scores()
            if radar:
                st.markdown('<p class="tactical-summary-header" style="font-size:0.9rem;margin-bottom:0.5rem;">SKILL FINGERPRINT // LIVE TKS PROFILE</p>', unsafe_allow_html=True)
                render_radar_chart_compact(radar, cat_labels, height=320, accent_color="#00f2ff", fill_color="rgba(0, 242, 255, 0.2)")
        st.markdown("---", unsafe_allow_html=False)
        if val_idx > 0 and st.session_state.get("pg_last_tks_log"):
            st.markdown(
                f'<div class="pg-terminal-log">{html.escape(st.session_state.pg_last_tks_log)}</div>',
                unsafe_allow_html=True,
            )
        q = val_questions[val_idx]
        prompt_text = getattr(q, "prompt", str(q))
        st.markdown(f'<p class="pg-scenario-text">{html.escape(prompt_text)}</p>', unsafe_allow_html=True)
        choices = getattr(q, "choices", [])
        option_labels = [getattr(c, "text", str(c)) for c in choices]
        # Custom Action Tiles (replace radio): one button per choice, Tactical Amber hover via CSS
        for ci, label in enumerate(option_labels):
            if st.button(
                label,
                key=f"pg_val_tile_{val_idx}_{ci}",
                use_container_width=True,
            ):
                tks_log = _record_pg_validation_choice(ci, q)
                if tks_log:
                    st.session_state.pg_last_tks_log = tks_log
                st.session_state.pg_validation_index = val_idx + 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="targeting-reticle">', unsafe_allow_html=True)
        if st.button(" [ ENGAGE VALIDATION ] ", key="pg_start_validation"):
            st.session_state.pg_validation_active = True
            st.session_state.pg_validation_questions = get_calibration_questions(_get_lang(), shuffle_personality=True)
            st.session_state.pg_validation_index = 0
            st.session_state.pg_ares_bridge_show = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<p class="neon-cyan" style="font-size:0.95rem;">**{html.escape(ui.get("pg_livefire_breach", "Live-Fire: Breach"))}**</p>', unsafe_allow_html=True)
    st.caption("MITRE ATT&CK scenario. Coming soon.")


def _page_archetype() -> None:
    st.markdown(f'<p class="glitch-text">{html.escape(get_ui(_get_lang()).get("nav_archetype", "Cyber Archetype"))}</p>', unsafe_allow_html=True)
    st.markdown("---")
    render_archetype()


# ─── Entry point: init session (scores persist across nav), sidebar (Always-Live Radar), then route ─
_init_session()
_render_sidebar_agent()

nav_page = st.session_state.get("nav_page", "mission_hub")
if nav_page == "mission_hub":
    _page_mission_hub()
elif nav_page == "archetype":
    _page_archetype()
else:
    _page_proving_ground()
