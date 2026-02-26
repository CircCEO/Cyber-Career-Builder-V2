"""
Game flow: questions, input handling, scoring, and dossier.
Full Streamlit UI: Mission Hub → 30 questions (20 personality + 10 technical) → Final Dossier.
"""

import streamlit as st
from rich.text import Text

from questions import (
    get_instinct_questions,
    get_technical_questions,
    get_deep_scenario_questions,
    get_personality_scenarios_questions,
    Question,
    Choice,
)
from cyber_career_compass.scoring import ScoreState
from cyber_career_compass.nice_framework import get_work_role, get_certifications
from ui import (
    console,
    print_banner,
    print_section_title,
    print_question,
    print_choices,
    print_dossier,
    print_farewell,
    build_ares_radar_figure,
)

LETTERS = "abcdefghij"


def parse_choice_index(raw: str, num_choices: int) -> int | None:
    """Parse user input to 0-based choice index. Accepts a/b/c or 1/2/3."""
    raw = raw.strip().lower()
    if not raw:
        return None
    if raw in LETTERS:
        i = LETTERS.index(raw)
        return i if i < num_choices else None
    try:
        i = int(raw)
        return i - 1 if 1 <= i <= num_choices else None
    except ValueError:
        return None


def run_instinct_phase(score: ScoreState) -> None:
    """Run the 5 Instinct (Personality) questions and update aptitude scores."""
    questions = get_instinct_questions()
    for i, q in enumerate(questions, 1):
        print_question("Instinct", i, len(questions), q.prompt)
        print_choices(q.choices)
        while True:
            raw = console.input(Text("Your choice (a/b/c): ", style="#39ff14"))
            idx = parse_choice_index(raw, len(q.choices))
            if idx is not None:
                choice = q.choices[idx]
                score.add_weights(choice.weights)
                break
            console.print("[yellow]Please enter a valid letter or number.[/yellow]")
        console.print()


def run_technical_phase(score: ScoreState) -> None:
    """Run the 10 Technical (Triage) questions and update knowledge score."""
    questions = get_technical_questions()
    for i, q in enumerate(questions, 1):
        print_question("Technical", i, len(questions), q.prompt)
        print_choices(q.choices)
        while True:
            raw = console.input(Text("Your choice (a/b/c/d): ", style="#39ff14"))
            idx = parse_choice_index(raw, len(q.choices))
            if idx is not None:
                correct = q.correct_index is not None and idx == q.correct_index
                score.add_technical_result(correct)
                break
            console.print("[yellow]Please enter a valid letter or number.[/yellow]")
        console.print()


def run_with_answers(instinct_answers: list[str], technical_answers: list[str]) -> None:
    """Run the full flow using preset answers (for demo or testing)."""
    print_banner()
    score = ScoreState()
    instinct_q = get_instinct_questions()
    technical_q = get_technical_questions()

    print_section_title("Phase 1 — Instinct (Personality)")
    for i, q in enumerate(instinct_q, 1):
        print_question("Instinct", i, len(instinct_q), q.prompt)
        print_choices(q.choices)
        raw = instinct_answers[i - 1] if i <= len(instinct_answers) else "a"
        idx = parse_choice_index(raw, len(q.choices)) or 0
        choice = q.choices[idx]
        score.add_weights(choice.weights)
        console.print(Text(f"  >> {raw}\n", style="#39ff14"))

    print_section_title("Phase 2 — Technical (Triage)")
    for i, q in enumerate(technical_q, 1):
        print_question("Technical", i, len(technical_q), q.prompt)
        print_choices(q.choices)
        raw = technical_answers[i - 1] if i <= len(technical_answers) else "a"
        idx = parse_choice_index(raw, len(q.choices)) or 0
        correct = q.correct_index is not None and idx == q.correct_index
        score.add_technical_result(correct)
        console.print(Text(f"  >> {raw}\n", style="#39ff14"))

    dominant = score.get_dominant_aptitude()
    knowledge_level = score.get_knowledge_level()
    print_section_title("NICE Career Dossier")
    print_dossier(dominant, knowledge_level)
    print_farewell()


def run() -> None:
    """Run the full Cyber Career Compass flow (interactive)."""
    print_banner()
    score = ScoreState()

    print_section_title("Phase 1 — Instinct (Personality)")
    run_instinct_phase(score)

    print_section_title("Phase 2 — Technical (Triage)")
    run_technical_phase(score)

    dominant = score.get_dominant_aptitude()
    knowledge_level = score.get_knowledge_level()

    print_section_title("NICE Career Dossier")
    print_dossier(dominant, knowledge_level)
    print_farewell()


def main() -> None:
    """
    Full Streamlit game: Mission Hub (landing) → 30 questions → Final Dossier.
    """
    st.set_page_config(page_title="Cyber Career Compass", layout="wide")

    # ─── Dark theme: Pure Black #0a0a0b, Neon-Cyan / Tactical Green ───
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
        .stApp, [data-testid="stAppViewContainer"], main, .block-container {
            background-color: #0a0a0b !important;
            color: #e0e0e0 !important;
        }
        .stMarkdown, p, label, .stRadio label { color: #e0e0e0 !important; font-family: 'Share Tech Mono', monospace !important; }
        .ares-title { font-family: 'Share Tech Mono', monospace !important; font-weight: 700; color: #00f2ff; text-shadow: 0 0 12px #00f2ff; font-size: 1.8rem; }
        .ares-subtitle { color: #00ff00; font-family: 'Share Tech Mono', monospace !important; font-size: 1rem; margin-top: 0.5rem; }
        .ares-card { background: rgba(10, 10, 11, 0.6); border: 1px solid rgba(0, 242, 255, 0.4); border-radius: 10px; padding: 2rem; margin: 2rem auto; max-width: 640px; }
        .stButton > button { font-family: 'Share Tech Mono', monospace !important; color: #00f2ff !important; border: 1px solid #00f2ff !important; background: transparent !important; }
        .stButton > button:hover { border-color: #ffbf00 !important; color: #ffbf00 !important; background: rgba(255, 191, 0, 0.08) !important; box-shadow: 0 0 16px rgba(255, 191, 0, 0.3); }
        .dossier-heading { color: #00f2ff !important; font-family: 'Share Tech Mono', monospace !important; }
        .dossier-value { color: #00ff00 !important; font-family: 'Share Tech Mono', monospace !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ─── Session state: page, score, 30-question list, index ───
    if "game_page" not in st.session_state:
        st.session_state.game_page = "mission_hub"
    if "score" not in st.session_state:
        st.session_state.score = ScoreState()
    if "all_questions" not in st.session_state:
        st.session_state.all_questions = []
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    score_state = st.session_state.score

    # Sidebar: always show auth header + live radar
    st.sidebar.markdown("### [ AUTHENTICATION: GLOBAL ]")
    radar_scores = score_state.get_normalized_radar_scores()
    fig_sidebar = build_ares_radar_figure(radar_scores)
    st.sidebar.plotly_chart(fig_sidebar, use_container_width=True, config=dict(displayModeBar=False))

    # ─── Route by page ───
    if st.session_state.game_page == "mission_hub":
        _render_mission_hub()
    elif st.session_state.game_page == "questions":
        _render_questions(score_state)
    else:
        _render_dossier(score_state)


def _render_mission_hub() -> None:
    """Landing page: title, subtitle, [ ENGAGE ] to start 30-question sequence."""
    st.markdown('<p class="ares-title">ARES: Cyber Career Compass</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ares-subtitle">NIST NICE–driven assessment. 20 personality scenarios + 10 technical core. Your Career Dossier awaits.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="ares-card">', unsafe_allow_html=True)
        if st.button("**[ ENGAGE ]** — Start 30-Question Calibration", type="primary", use_container_width=True):
            st.session_state.all_questions = (
                get_personality_scenarios_questions() + get_technical_questions()
            )
            st.session_state.question_index = 0
            st.session_state.game_page = "questions"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def _render_questions(score_state: ScoreState) -> None:
    """30-question sequence: 20 personality (add_weights) + 10 technical (add_technical_result)."""
    questions = st.session_state.all_questions
    idx = st.session_state.question_index
    total = len(questions)

    if total == 0:
        st.warning("No questions loaded. Return to Mission Hub.")
        if st.button("Back to Mission Hub"):
            st.session_state.game_page = "mission_hub"
            st.rerun()
        return

    if idx >= total:
        st.session_state.game_page = "dossier"
        st.rerun()
        return

    # Progress
    st.progress((idx + 1) / total)
    phase = "Personality" if idx < 20 else "Technical"
    st.caption(f"Question {idx + 1} of {total} — {phase}")

    q = questions[idx]
    option_texts = [c.text for c in q.choices]
    is_technical = getattr(q, "correct_index", None) is not None

    st.subheader(q.prompt)
    selected = st.radio("Choose one:", option_texts, key=f"q_radio_{idx}", label_visibility="collapsed")

    if st.button("Submit & Next", key=f"q_submit_{idx}"):
        if selected is None:
            st.warning("Please select an option.")
        else:
            choice_index = option_texts.index(selected)
            choice = q.choices[choice_index]
            if is_technical:
                correct = choice_index == q.correct_index
                score_state.add_technical_result(correct)
            else:
                score_state.add_weights(choice.weights)
            st.session_state.question_index = idx + 1
            st.rerun()

    st.markdown("---")
    if st.button("← Back to Mission Hub"):
        st.session_state.game_page = "mission_hub"
        st.session_state.question_index = 0
        st.session_state.score = ScoreState()
        st.rerun()


def _render_dossier(score_state: ScoreState) -> None:
    """Final Dossier: work role, radar, strengths, certifications."""
    dominant = score_state.get_dominant_aptitude()
    knowledge_level = score_state.get_knowledge_level()
    role = get_work_role(dominant, knowledge_level)
    certs = get_certifications(dominant, knowledge_level)
    radar_scores = score_state.get_normalized_radar_scores()

    st.markdown("## NICE Career Dossier")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f'<p class="dossier-heading">Work Role</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="dossier-value">**{role.title}** ({role.id})</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#e0e0e0;">Category: {role.category}</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<p class="dossier-heading">Definition</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#e0e0e0;">{role.definition}</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<p class="dossier-heading">Your strengths</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#00ff00;">{role.strengths_summary}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="dossier-heading">Category fit (7-axis radar)</p>', unsafe_allow_html=True)
        fig = build_ares_radar_figure(radar_scores)
        st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

    st.markdown("---")
    st.markdown(f'<p class="dossier-heading">Recommended certifications</p>', unsafe_allow_html=True)
    for c in certs:
        st.markdown(f'- **{c.name}** — {c.issuer} ({c.level})', unsafe_allow_html=False)

    st.markdown("---")
    st.success("Scan complete. Align your path with the NICE Framework.")

    if st.button("← Back to Mission Hub"):
        st.session_state.game_page = "mission_hub"
        st.session_state.question_index = 0
        st.session_state.score = ScoreState()
        st.rerun()


if __name__ == "__main__":
    main()
