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

# 3. Mission API: from local questions.py (root folder)
from questions import (
    get_explorer_questions,   # 20-item profile: 10 Instinct + 10 NIST Foundations
    get_specialist_questions, # 50-item gap analysis
    get_operator_questions,   # 12 mission scenarios
)
from cyber_career_compass.scoring import ScoreState
from ui import build_ares_radar_figure
import game  # reuse mission logic: question flow + dossier rendering


def _init_session_state() -> None:
    """Ensure shared game state mirrors game.py expectations."""
    if "game_page" not in st.session_state:
        st.session_state.game_page = "mission_hub"
    if "score" not in st.session_state:
        st.session_state.score = ScoreState()
    if "all_questions" not in st.session_state:
        st.session_state.all_questions = []
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "mission_tier" not in st.session_state:
        st.session_state.mission_tier = None  # "explorer" | "specialist" | "operator"


def _inject_global_hud_css() -> None:
    """C3S Environmental HUD: #05070a background, Share Tech Mono global, radar-pulse on sidebar, tactical framing, 8-cell neural bar, ENGAGE reticles."""
    st.set_page_config(
        page_title="Circadence Cyber Career Simulator (C3S)",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    css = """<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
/* 1. Environmental HUD */
    :root { --ares-neon: #00f6ff; }
    * { font-family: "Share Tech Mono", "JetBrains Mono", monospace !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp,
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background: #000000 !important;
        border-right: 1px solid rgba(0, 246, 255, 0.25);
    }
    /* Zero-Box Global: strip Streamlit background boxes and borders so cards float on #05070a */
    [data-testid="stVerticalBlock"], [data-testid="column"], [data-testid="stHorizontalBlock"],
    .stContainer, [class*="st-emotion-cache"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    .block-container { max-width: 1300px; padding-top: 1rem; padding-bottom: 1rem; background: none !important; border: none !important; }
    [data-testid="stHeader"] { border-bottom: none !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; }
    button[title="Collapse sidebar"], button[title="Expand sidebar"],
    svg[data-testid="baseIcon-keyboardDoubleArrowRight"] { display: none !important; }
    [data-testid="stSidebar"] .stMarkdown { font-family: "Share Tech Mono", "JetBrains Mono", monospace !important; }

    /* Glitch / chromatic aberration: white + cyan + magenta offsets */
    @keyframes cyber-glow {
        0%, 100% { color: #00f6ff; text-shadow: 2px 0 #00f6ff, -2px 0 #ff00ff, 0 0 0.1em #fff, 0 0 0.35em #00f6ff; }
        50% { color: #00b8c4; text-shadow: 2px 0 #00b8c4, -2px 0 #ff00ff, 0 0 0.1em #fff, 0 0 0.2em #00b8c4; }
    }
    .c3s-main-title {
        font-size: 1.8rem;
        letter-spacing: 0.12em;
        font-weight: 700;
        color: #00f6ff;
        margin: 0 0 0.15rem 0;
        text-shadow: 2px 0 #00f6ff, -2px 0 #ff00ff, 0 0 0.1em #fff;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
        animation: cyber-glow 2.8s ease-in-out infinite;
    }
    .c3s-subtitle {
        font-size: 1.35rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 1rem 0;
        text-shadow: 1px 0 #00f6ff, -1px 0 #ff00ff;
        font-family: "Share Tech Mono", "JetBrains Mono", monospace !important;
    }
    .connecting-status { position: absolute; top: 0; right: 0; font-size: 0.7rem; letter-spacing: 0.2em; color: #00f6ff; }

    /* World Class 16:30 — Fixed Geometry Lock: mission cards 480px; Zero-Box diegetic framing */
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
    /* Forced Geometry: column 540px so 480px card + [ ENGAGE ] align on one horizontal line */
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
    [data-testid="stSidebar"] [data-testid="stPlotlyChart"] {
        border: none !important;
        box-shadow: 0 0 0 2px #00FF00;
        animation: ares-radar-pulse 2s ease-in-out infinite;
    }
    @keyframes ares-radar-pulse {
        0%, 100% { box-shadow: 0 0 0 2px #00FF00, 0 0 12px rgba(0, 255, 0, 0.4); }
        50% { box-shadow: 0 0 0 3px #00FF00, 0 0 20px rgba(0, 255, 0, 0.7); }
    }
    /* Sidebar nav: asymmetric cyan brackets (#00f6ff) tl+br + padlock per item */
    .hud-mono { letter-spacing: 0.18em; text-transform: uppercase; font-size: 0.7rem; color: #00f6ff; }
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
    .ares-nav-block.active::after { content: " ]"; color: #00f6ff; }
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
    </style>
    """
    # Inject CSS as raw HTML so it is applied, not displayed as text (st.markdown can render <style> content as code)
    try:
        st.html(css)
    except AttributeError:
        st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def _render_sidebar() -> None:
    """Agent Status: NAVIGATION (active Mission Hub or Dossier wrapped in [ ] via CSS), 8-cell neural-link, Live Biometric radar in holographic well."""
    score_state: ScoreState = st.session_state.score
    current_idx = st.session_state.question_index
    total = len(st.session_state.all_questions) or 1
    progress = min(1.0, current_idx / total) if total else 0.0
    num_lit = min(8, int(round(progress * 8)))  # 8-cell row: first num_lit cells get .lit (neon cyan)
    page = st.session_state.game_page
    mission_hub_active = page == "mission_hub"
    proving_active = False  # placeholder until Proving Grounds route exists
    archetype_active = page == "dossier"

    with st.sidebar:
        st.markdown('<div class="hud-mono" style="margin-bottom:0.4rem;">STRAT-COM</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="ares-nav-block{" active" if mission_hub_active else ""}">'
            '<span class="nav-corner nav-corner-tl"></span><span class="nav-corner nav-corner-br"></span>'
            '<span class="nav-lock" aria-hidden="true">&#128274;</span>Mission Hub</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ares-nav-block{" active" if proving_active else ""}">'
            '<span class="nav-corner nav-corner-tl"></span><span class="nav-corner nav-corner-br"></span>'
            '<span class="nav-lock" aria-hidden="true">&#128274;</span>Proving Grounds</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ares-nav-block{" active" if archetype_active else ""}">'
            '<span class="nav-corner nav-corner-tl"></span><span class="nav-corner nav-corner-br"></span>'
            '<span class="nav-lock" aria-hidden="true">&#128274;</span>Cyber Archetype</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="hud-mono" style="margin-top:0.25rem;font-size:0.6rem;">SYNC_LEVEL // %</div>', unsafe_allow_html=True)
        st.markdown('<div class="hud-mono" style="margin-top:0.5rem;font-size:0.6rem;">LIVE-FIRE // RANGE // PERS-INTEL</div>', unsafe_allow_html=True)
        st.selectbox("Language", ["English"], key="lang")
        st.markdown("---")

        st.markdown('<div class="hud-mono">[ NEURAL-LINK ]</div>', unsafe_allow_html=True)
        st.markdown('<div class="hud-mono" style="font-size:0.6rem;margin-top:0.15rem;">OPERATOR ID: [ GUARDIAN ]</div>', unsafe_allow_html=True)
        st.markdown('<div class="hud-mono" style="margin-top:0.5rem;">SYNC_LEVEL // %</div>', unsafe_allow_html=True)
        cells_html = "".join(
            f'<div class="ares-neural-cell{" lit" if i < num_lit else ""}"></div>' for i in range(8)
        )
        st.markdown(f'<div class="ares-neural-row">{cells_html}</div>', unsafe_allow_html=True)
        st.caption(f"Progress: {current_idx}/{total} answered")
        st.caption("SYNC_LEVEL // %")

        st.markdown('<div class="hud-mono" style="margin-top:1rem;">Live Biometric</div>', unsafe_allow_html=True)
        st.markdown('<div class="ares-radar-well">', unsafe_allow_html=True)
        radar_scores = score_state.get_normalized_radar_scores()
        fig = build_ares_radar_figure(radar_scores)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=dict(displayModeBar=False),
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="skill-heatmap-label">Skill Heatmap</div>', unsafe_allow_html=True)
        st.markdown('<div class="hud-mono" style="font-size:0.6rem;">Securely Provision</div>', unsafe_allow_html=True)


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
    """Circadence C3S — Project Ares Tactical Mission Hub (carbon copy of reference)."""
    st.markdown(
        '<div style="position:relative; display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">'
        '<div><h1 class="c3s-main-title">Circadence Cyber Career Simulator (C3S)</h1>'
        '<p class="c3s-subtitle">Project Ares Tactical Mission Hub</p></div>'
        '<span class="connecting-status">••• CONNECTING</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # Explorer – Foundational (20 items)
    with col1:
        st.markdown(
            """
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0x7F2A</span>
                <div class="mission-status">SYSTEM STATUS: NOMINAL</div>
                <div class="mission-title">The Explorer (Foundational)</div>
                <div class="mission-metadata">VECTOR_ID: EXP-28</div>
                <div class="mission-metadata">THREAT_MODEL: 2026_STANDARD</div>
                <div class="mission-directive">Operational Directive: Assess foundational alignment with NICE work roles. 20-item profile.</div>
                <div class="mission-footnote">TRK_LOCK // 0x7F2A</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("[ ENGAGE ]", key="engage_explorer"):
            _start_mission("explorer")

    # Specialist – Elite (50 items)
    with col2:
        st.markdown(
            """
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0x83C1</span>
                <div class="mission-status">SYSTEM STATUS: NOMINAL</div>
                <div class="mission-title">The Specialist (Elite)</div>
                <div class="mission-metadata">VECTOR_ID: TRS-58</div>
                <div class="mission-metadata">THREAT_MODEL: 2026_STANDARD</div>
                <div class="mission-directive">Operational Directive: Full TKS assessment against NIST 2026 framework. 50-item gap analysis.</div>
                <div class="mission-footnote">TRK_LOCK // 0x83C1</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("[ ENGAGE ]", key="engage_specialist"):
            _start_mission("specialist")

    # Operator – Tier 1 (12 vectors)
    with col3:
        st.markdown(
            """
            <div class="mission-card">
                <span class="corner-bracket corner-tl"></span>
                <span class="corner-bracket corner-br"></span>
                <span class="mission-hex-tl">0xEB4D</span>
                <div class="mission-status">SYSTEM STATUS: NOMINAL</div>
                <div class="mission-title">The Operator (Tier 1)</div>
                <div class="mission-metadata">VECTOR_ID: OP-12</div>
                <div class="mission-metadata">THREAT_MODEL: 2026_STANDARD</div>
                <div class="mission-directive">Operational Directive: Assess readiness for Critical Infrastructure Protection (ICS/SCADA) and Ransomware Mitigation. 12 missions aligned to Project Ares Advanced Learning Paths.</div>
                <div class="mission-footnote">TRK_LOCK // 0xE04D</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("[ ENGAGE ]", key="engage_operator"):
            _start_mission("operator")


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
    elif st.session_state.game_page == "questions":
        # Reuse shared mission logic from game.py
        game._render_questions(st.session_state.score)  # type: ignore[attr-defined]
    else:  # "dossier"
        game._render_dossier(st.session_state.score)  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
