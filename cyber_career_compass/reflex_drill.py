"""
Reflex Drill — Architectural Reset. Single-focus stream, no columns.
One NIST-mapped threat at a time; binary accuracy gate (chromatic glitch + 1s lockout on wrong).
Center-aligned container (max-width 800px), asymmetric cyan brackets, scrolling header.
"""

import html as html_module
import time
from typing import Optional, List, Tuple

from .nice_framework import (
    CATEGORY_PR,
    CATEGORY_CO,
    CATEGORY_SP,
    CATEGORY_AN,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
)
from .scoring import ScoreState
from .translations import get_ui


# 10 NIST-mapped threats: (threat_text, correct_action_key, nice_category).
# Action = "NEUTRALIZE" | "DROP" | "FREEZE". Telemetry maps each to one NICE category.
REFLEX_THREATS: List[Tuple[str, str, str]] = [
    ("DETECTED: MFA_BYPASS req=0x7f", "NEUTRALIZE", CATEGORY_PR),   # 1 Protect and Defend
    ("DETECTED: DORMANT_USER_LOGIN uid=admin", "NEUTRALIZE", CATEGORY_CO),  # 2 Collect and Operate
    ("DETECTED: Unauthorized SMB/445 Egress", "DROP", CATEGORY_PR),  # 3
    ("DETECTED: Unauthorized Telnet/23 Egress", "DROP", CATEGORY_OM),  # 4 Operate and Maintain
    ("DETECTED: SHA256 MISMATCH /usr/bin/sudo", "FREEZE", CATEGORY_SP),  # 5 Securely Provision
    ("DETECTED: Unauthorized registry shift HKLM\\System", "FREEZE", CATEGORY_IN),  # 6 Investigate
    ("DETECTED: PHISH_C2 beacon outbound 443", "DROP", CATEGORY_AN),  # 7 Analyze
    ("DETECTED: Suspicious lateral movement SMB", "NEUTRALIZE", CATEGORY_PR),  # 8
    ("DETECTED: Policy violation — unsigned script execution", "FREEZE", CATEGORY_OV),  # 9 Oversee and Govern
    ("DETECTED: Data exfil over DNS tunnel", "DROP", CATEGORY_CO),  # 10
]

REFLEX_HEADER_TEXT = "REACTION_TIME_VALIDATION // NIST_800-53_SYNC"

REFLEX_CANVAS_CSS = """
<style>
/* Center-aligned single container, max-width 800px */
.reflex-single-container {
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    padding: 1rem 1.2rem;
    background: transparent !important;
    border: none !important;
}
.reflex-single-container::before {
    content: ""; position: absolute; top: 0; left: 0; width: 24px; height: 24px;
    border-left: 2px solid rgba(0, 242, 255, 0.9); border-top: 2px solid rgba(0, 242, 255, 0.9);
    pointer-events: none; z-index: 1;
}
.reflex-single-container::after {
    content: ""; position: absolute; bottom: 0; right: 0; width: 24px; height: 24px;
    border-right: 2px solid rgba(0, 242, 255, 0.9); border-bottom: 2px solid rgba(0, 242, 255, 0.9);
    pointer-events: none; z-index: 1;
}
.reflex-scrolling-header {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 0.14em;
    color: rgba(0, 242, 255, 0.95);
    margin-bottom: 1rem;
    overflow: hidden;
    white-space: nowrap;
    animation: reflexHeaderScroll 15s linear infinite;
}
@keyframes reflexHeaderScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%%); }
}
.reflex-threat-line {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem;
    font-weight: 600;
    color: #00f2ff;
    text-shadow: 0 0 12px rgba(0, 242, 255, 0.8);
    margin: 1rem 0 1.25rem 0;
    line-height: 1.4;
}
.reflex-workstation-glitch-shake {
    animation: reflexGlitchShake 0.5s ease-in-out;
}
@keyframes reflexGlitchShake {
    0%%, 100% { transform: translate(0); }
    15% { transform: translate(-4px, 0); }
    30% { transform: translate(4px, 0); }
    45% { transform: translate(-2px, 0); }
    60% { transform: translate(2px, 0); }
    75% { transform: translate(-1px, 0); }
}
.reflex-system-health-wrap { margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
.reflex-system-health-ring {
    width: 52px; height: 52px;
    border-radius: 50%;
    background: conic-gradient(rgba(0, 242, 255, 0.9) calc(var(--pct, 0) * 1%), rgba(40, 40, 45, 0.9) 0);
    display: inline-flex; align-items: center; justify-content: center;
    box-shadow: 0 0 calc(6px + (var(--pct, 0) / 100) * 12px) rgba(0, 255, 255, 0.5);
}
.reflex-system-health-inner {
    width: 40px; height: 40px; border-radius: 50%;
    background: #0a0a0b;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px; color: rgba(0, 242, 255, 0.9);
}
.reflex-divider { margin: 0.5rem 0 !important; }
/* Targeting Reticle — Tactical Amber hover */
.reflex-reticle-wrap .stButton > button {
    background: transparent !important; border: none !important; box-shadow: none !important;
    color: rgba(0, 242, 255, 0.95) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.12em;
    position: relative;
    padding: 0.4rem 0.8rem !important;
    transition: color 0.2s ease, padding 0.2s ease !important;
}
.reflex-reticle-wrap .stButton > button::before {
    content: "[ "; position: absolute; left: 0.25rem; top: 50%%; transform: translateY(-50%%);
    color: inherit; transition: left 0.2s ease, color 0.2s ease;
}
.reflex-reticle-wrap .stButton > button::after {
    content: " ]"; position: absolute; right: 0.25rem; top: 50%%; transform: translateY(-50%%);
    color: inherit; transition: right 0.2s ease, color 0.2s ease;
}
.reflex-reticle-wrap .stButton > button:hover {
    color: #ffbf00 !important;
    text-shadow: 0 0 14px #ffbf00, 0 0 28px rgba(255, 191, 0, 0.55);
}
.reflex-reticle-wrap .stButton > button:hover::before { left: 0.5rem; color: #ffbf00; }
.reflex-reticle-wrap .stButton > button:hover::after { right: 0.5rem; color: #ffbf00; }
.reflex-reticle-wrap .stButton > button:disabled { opacity: 0.4; cursor: not-allowed; }
.reflex-complete-section { margin-top: 1rem !important; }
.reflex-complete-btn-wrap.nominal .stButton > button {
    background: transparent !important; border: none !important; box-shadow: none !important;
    color: #00f2ff !important; font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.12em; position: relative;
}
.reflex-complete-btn-wrap.nominal .stButton > button::before { content: "["; position: absolute; left: 0.25rem; top: 50%%; transform: translateY(-50%%); color: #00f2ff; }
.reflex-complete-btn-wrap.nominal .stButton > button::after { content: "]"; position: absolute; right: 0.25rem; top: 50%%; transform: translateY(-50%%); color: #00f2ff; }
.reflex-complete-btn-wrap.nominal .stButton > button:hover { color: #ffbf00 !important; }
</style>
"""


def _apply_reflex_drill_weights(score_state: Optional[ScoreState]) -> None:
    """Apply final completion bonus after 10th threat (all 10 NIST-mapped)."""
    if score_state is None:
        return
    score_state.add_weights({CATEGORY_PR: 0.15, CATEGORY_CO: 0.15})


def _set_pulse_amber() -> None:
    import streamlit as st
    st.session_state.reflex_pulse_amber = True
    st.session_state.power_cell_just_filled = True


def _trigger_fail_state() -> None:
    """Incorrect click: 0.5s chromatic glitch + 1s UI lockout."""
    import streamlit as st
    st.session_state.reflex_chromatic_glitch_until = time.time() + 0.5
    st.session_state.reflex_ui_lockout_until = time.time() + 1.0


def render_reflex_drill_page() -> None:
    import streamlit as st

    lang = st.session_state.get("language", st.session_state.get("lang", "en"))
    ui = get_ui(lang)
    score_state: Optional[ScoreState] = st.session_state.get("score")

    if "reflex_drill_index" not in st.session_state:
        st.session_state.reflex_drill_index = 0

    idx = st.session_state.reflex_drill_index
    total_threats = len(REFLEX_THREATS)
    completed = idx
    st.session_state.checks_cleared = completed
    lockout_until = st.session_state.get("reflex_ui_lockout_until", 0)
    if time.time() >= lockout_until and lockout_until > 0:
        st.session_state.pop("reflex_ui_lockout_until", None)
    locked = time.time() < lockout_until
    glitch_active = st.session_state.get("reflex_chromatic_glitch_until", 0) > time.time()
    workstation_class = "reflex-workstation-glitch-shake" if glitch_active else ""

    st.markdown(REFLEX_CANVAS_CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="reflex-unified-workstation {workstation_class}">'
        f'<div class="reflex-single-container">'
        f'<div class="reflex-scrolling-header">{html_module.escape(REFLEX_HEADER_TEXT)}</div>',
        unsafe_allow_html=True,
    )

    pct = (completed / total_threats * 100) if total_threats else 0
    health_label = ui.get("reflex_system_health_label", "SYSTEM HEALTH")
    st.markdown(
        f'<div class="reflex-system-health-wrap">'
        f'<div class="reflex-system-health-ring" style="--pct: {pct};">'
        f'<div class="reflex-system-health-inner">{completed}/{total_threats}</div></div>'
        f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:10px;color:rgba(0,242,255,0.9);">{html_module.escape(health_label)}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="reflex-divider"/>', unsafe_allow_html=True)

    if idx >= total_threats:
        st.markdown("</div>", unsafe_allow_html=True)
        nominal_label = ui.get("reflex_system_nominal", "System Nominal")
        complete_label = ui.get("reflex_complete_btn", "Complete drill")
        st.caption(nominal_label)
        st.markdown(f'<div class="reflex-complete-section reflex-complete-btn-wrap nominal">', unsafe_allow_html=True)
        if st.button(complete_label, key="reflex_complete_btn", type="primary"):
            _apply_reflex_drill_weights(score_state)
            st.session_state.sync_level = 100
            st.session_state.reflex_complete = True
            st.session_state.proving_grounds_module = None
            for k in ("reflex_drill_index", "checks_cleared", "reflex_chromatic_glitch_until", "reflex_ui_lockout_until"):
                st.session_state.pop(k, None)
            st.markdown(
                f'<p style="font-family:\'Share Tech Mono\',monospace;color:#39ff14;">'
                f'{html_module.escape(ui.get("pg_scores_synced", "Scores synced to C3S radar. Your NICE alignment has been updated."))}</p>',
                unsafe_allow_html=True,
            )
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
        return

    threat_text, correct_action, nice_category = REFLEX_THREATS[idx]
    neutralize_btn = ui.get("reflex_neutralize", "NEUTRALIZE")
    drop_btn = ui.get("reflex_drop", "DROP")
    freeze_btn = ui.get("reflex_freeze", "FREEZE")
    action_labels = {"NEUTRALIZE": neutralize_btn, "DROP": drop_btn, "FREEZE": freeze_btn}

    # Per-question NIST telemetry weight (0.1 per correct answer for this threat's category)
    question_weight = {nice_category: 0.1}

    current_display = idx + 1
    st.markdown(
        f'<div class="reflex-single-container">'
        f'<div class="reflex-system-health-wrap">'
        f'<div class="reflex-system-health-ring" style="--pct: {pct};">'
        f'<div class="reflex-system-health-inner">{current_display}/10</div></div></div>'
        f'<p class="reflex-threat-line">{html_module.escape(threat_text)}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="reflex-reticle-wrap">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f" [ {neutralize_btn} ] ", key="reflex_act_neutralize", type="secondary", disabled=locked):
            if correct_action == "NEUTRALIZE":
                st.session_state.reflex_drill_index = idx + 1
                _set_pulse_amber()
                if score_state is not None:
                    score_state.add_weights(question_weight)
                st.rerun()
            else:
                _trigger_fail_state()
                st.markdown(
                    f'<p style="font-family:\'Share Tech Mono\',monospace;color:#00f2ff;">[ {html_module.escape(ui.get("reflex_incorrect_try", "Incorrect."))} ]</p>',
                    unsafe_allow_html=True,
                )
    with c2:
        if st.button(f" [ {drop_btn} ] ", key="reflex_act_drop", type="secondary", disabled=locked):
            if correct_action == "DROP":
                st.session_state.reflex_drill_index = idx + 1
                _set_pulse_amber()
                if score_state is not None:
                    score_state.add_weights(question_weight)
                st.rerun()
            else:
                _trigger_fail_state()
                st.markdown(
                    f'<p style="font-family:\'Share Tech Mono\',monospace;color:#00f2ff;">[ {html_module.escape(ui.get("reflex_incorrect_try", "Incorrect."))} ]</p>',
                    unsafe_allow_html=True,
                )
    with c3:
        if st.button(f" [ {freeze_btn} ] ", key="reflex_act_freeze", type="secondary", disabled=locked):
            if correct_action == "FREEZE":
                st.session_state.reflex_drill_index = idx + 1
                _set_pulse_amber()
                if score_state is not None:
                    score_state.add_weights(question_weight)
                st.rerun()
            else:
                _trigger_fail_state()
                st.markdown(
                    f'<p style="font-family:\'Share Tech Mono\',monospace;color:#00f2ff;">[ {html_module.escape(ui.get("reflex_incorrect_try", "Incorrect."))} ]</p>',
                    unsafe_allow_html=True,
                )
    st.markdown("</div></div></div>", unsafe_allow_html=True)
