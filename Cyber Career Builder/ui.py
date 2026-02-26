"""
Original Ares Geometry — 7-axis Plotly radar for Cyber Career Compass.

This module exposes:
- A radar builder that can be embedded in Streamlit or other front-ends while
  keeping the visual shape aligned to the Ares / NIST NICE spec.
- Minimal CLI UI helpers (console + print_* functions) for the legacy terminal
  game flow in game.py.
"""

from typing import Dict, List

from rich.console import Console
from rich.text import Text

from cyber_career_compass.nice_framework import (
    CATEGORY_AN,
    CATEGORY_CO,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
    CATEGORY_PR,
    CATEGORY_SP,
    get_work_role,
    get_certifications,
)


NICE_CATEGORY_ORDER = [
    CATEGORY_AN,  # Analyze
    CATEGORY_CO,  # Collect & Operate
    CATEGORY_IN,  # Investigate
    CATEGORY_OM,  # Operate & Maintain
    CATEGORY_OV,  # Oversee & Govern
    CATEGORY_PR,  # Protect & Defend
    CATEGORY_SP,  # Securely Provision
]

NICE_CATEGORY_LABELS = [
    "Analyze",
    "Collect & Operate",
    "Investigate",
    "Operate & Maintain",
    "Oversee & Govern",
    "Protect & Defend",
    "Securely Provision",
]


def build_ares_radar_figure(category_scores: Dict[str, float]):
    """
    Ares Live Biometric Radar: 7 axes in NIST NICE order.
    Deep-space background (#05070a); cyan labels and fill.
    """
    try:
        import plotly.graph_objects as go
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Plotly is required to render the Ares radar.") from exc

    # Strict NIST NICE framework order (7 categories)
    values = [max(0.0, min(100.0, float(category_scores.get(code, 0.0)))) for code in NICE_CATEGORY_ORDER]
    m = max(values) if values else 0.0
    if m < 1.0 and m >= 0:
        values = [max(10.0, v * 100.0) if v > 0 else 10.0 for v in values]
    values_loop = values + [values[0]]
    labels_loop = NICE_CATEGORY_LABELS + [NICE_CATEGORY_LABELS[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values_loop,
                theta=labels_loop,
                fill="toself",
                showlegend=False,
                line=dict(color="rgba(0, 246, 255, 0.35)", width=5),
                fillcolor="rgba(0, 246, 255, 0.08)",
            ),
            go.Scatterpolar(
                r=values_loop,
                theta=labels_loop,
                fill="toself",
                name="You",
                line=dict(color="#00f6ff", width=2),
                fillcolor="rgba(0, 246, 255, 0.15)",
            ),
        ]
    )

    fig.update_layout(
        polar=dict(
            bgcolor="#05070a",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#00f6ff", size=11, family="'Share Tech Mono', 'JetBrains Mono', monospace"),
                gridcolor="rgba(0, 246, 255, 0.2)",
                linecolor="rgba(0, 246, 255, 0.4)",
                showgrid=True,
            ),
            angularaxis=dict(
                tickfont=dict(color="#00f6ff", size=11, family="'Share Tech Mono', 'JetBrains Mono', monospace"),
                gridcolor="rgba(0, 246, 255, 0.15)",
                linecolor="rgba(0, 246, 255, 0.35)",
                showgrid=True,
            ),
        ),
        paper_bgcolor="#05070a",
        plot_bgcolor="#05070a",
        showlegend=True,
        legend=dict(font=dict(family="'Share Tech Mono', monospace", color="#00f6ff", size=10), orientation="h", y=1.02),
        margin=dict(t=0, b=0, l=0, r=0),
        height=420,
        font=dict(family="'Share Tech Mono', monospace", color="#00f6ff"),
    )
    return fig


def render_ares_radar_streamlit(category_scores: Dict[str, float]) -> None:
    """
    Convenience wrapper: render the Original Ares radar directly in Streamlit,
    if Streamlit is available in the execution context.
    """
    try:
        import streamlit as st
    except Exception:  # pragma: no cover
        return
    fig = build_ares_radar_figure(category_scores)
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))


# ─── Legacy CLI UI: console + print helpers for game.py ────────────────────────

# Shared console for the terminal game flow.
console: Console = Console()


def print_banner() -> None:
    """Print the main banner for the terminal game."""
    title = Text("CYBER CAREER COMPASS", style="#00f2ff bold")
    subtitle = Text("NIST NICE–driven terminal assessment", style="#00ff00")
    console.rule(title)
    console.print(subtitle, justify="center")
    console.print()


def print_section_title(title: str) -> None:
    """Print a section title with a cyan divider."""
    console.rule(Text(title, style="#00f2ff"))


def print_question(phase: str, index: int, total: int, prompt: str) -> None:
    """Render a question header and prompt."""
    header = Text(f"[{phase}] Question {index} of {total}", style="#00f2ff bold")
    console.print()
    console.print(header)
    console.print(Text(prompt, style="#e0e0e0"))


def print_choices(choices: List[object]) -> None:
    """Render answer choices labelled a, b, c, ..."""
    letters = "abcdefghijklmnopqrstuvwxyz"
    for i, choice in enumerate(choices):
        label = letters[i]
        text = getattr(choice, "text", str(choice))
        console.print(Text(f"  ({label}) {text}", style="#00ff00"))


def print_dossier(dominant_category: str, knowledge_level: int) -> None:
    """
    Print a simple NICE work-role dossier for the terminal flow.
    Uses nice_framework.get_work_role() and get_certifications().
    """
    role = get_work_role(dominant_category, knowledge_level)
    certs = get_certifications(dominant_category, knowledge_level)

    console.print()
    console.rule(Text("NICE Career Dossier", style="#00f2ff bold"))
    console.print(Text(f"Work Role: {role.title} ({role.id})", style="#00ff00"))
    console.print(Text(f"Category: {role.category}", style="#e0e0e0"))
    console.print()
    console.print(Text("Definition:", style="#00f2ff"))
    console.print(Text(role.definition, style="#e0e0e0"))
    console.print()
    console.print(Text("Your strengths:", style="#00f2ff"))
    console.print(Text(role.strengths_summary, style="#e0e0e0"))
    if certs:
        console.print()
        console.print(Text("Recommended certifications:", style="#00f2ff"))
        for c in certs:
            console.print(Text(f"- {c.name} ({c.issuer}, {c.level})", style="#e0e0e0"))


def print_farewell() -> None:
    """Print closing message for the terminal game."""
    console.print()
    console.print(
        Text(
            "Scan complete. Align your path with the NICE Framework.",
            style="#00ff00",
        )
    )
    console.print()
