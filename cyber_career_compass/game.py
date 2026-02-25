"""
Game flow: questions, input handling, scoring, and dossier.
"""

from rich.text import Text

from questions import get_instinct_questions, get_technical_questions, get_deep_scenario_questions, Question, Choice
from scoring import ScoreState
from ui import (
    console,
    print_banner,
    print_section_title,
    print_question,
    print_choices,
    print_dossier,
    print_farewell,
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
