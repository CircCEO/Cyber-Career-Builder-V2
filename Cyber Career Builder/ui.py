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

# Radar: 8 axes (top clockwise) — clone colors and placement from reference
RADAR_8_LABELS = [
    "Analyze",
    "Protect & Defend",
    "Securely Provision",
    "Oversee & Govern",
    "Operate & Maintain",
    "Investigate",
    "Govern",
    "Collect & Operate",
]
RADAR_8_NICE_MAP = [CATEGORY_AN, CATEGORY_PR, CATEGORY_SP, CATEGORY_OV, CATEGORY_OM, CATEGORY_IN, CATEGORY_OV, CATEGORY_CO]
# Target Readiness (Project A) — from reference: 75, 78, 65, 70, 55, 50, 70, 75
TARGET_READINESS_VALUES = [75, 78, 65, 70, 55, 50, 70, 75]
# Exact colors from reference (clone identically)
RADAR_CYAN = "#61D9EE"   # light blue-green/cyan: grid, axis labels, "You" series
RADAR_GREEN = "#7CEB8D"  # vibrant lime green: "Target Readiness (Project A)" dashed line


def build_ares_radar_figure(category_scores: Dict[str, float]):
    """
    Radar clone: 8 axes, dark background. #61D9EE light blue-green (grid + "You"), #7CEB8D lime green ("Target Readiness" dashed). Scale 0–100 in white.
    """
    try:
        import plotly.graph_objects as go
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Plotly is required to render the Ares radar.") from exc

    # "You" — 8 values from 7 NICE scores (Govern = OV repeated)
    you_values = [
        max(0.0, min(100.0, float(category_scores.get(code, 0.0))))
        for code in RADAR_8_NICE_MAP
    ]
    m = max(you_values) if you_values else 0.0
    if m < 1.0 and m >= 0:
        you_values = [max(10.0, v * 100.0) if v > 0 else 10.0 for v in you_values]
    you_loop = you_values + [you_values[0]]
    target_loop = TARGET_READINESS_VALUES + [TARGET_READINESS_VALUES[0]]
    labels_loop = RADAR_8_LABELS + [RADAR_8_LABELS[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=you_loop,
                theta=labels_loop,
                fill="toself",
                name="You",
                line=dict(color=RADAR_CYAN, width=2),
                fillcolor="rgba(97, 217, 238, 0.12)",
                marker=dict(size=7, color=RADAR_CYAN, symbol="circle", line=dict(width=0)),
            ),
            go.Scatterpolar(
                r=target_loop,
                theta=labels_loop,
                fill="toself",
                name="Target Readiness (Project A)",
                line=dict(color=RADAR_GREEN, width=2.5, dash="dash"),
                fillcolor="rgba(124, 235, 141, 0.06)",
                marker=dict(size=7, color=RADAR_GREEN, symbol="circle", line=dict(width=0)),
            ),
        ]
    )

    fig.update_layout(
        polar=dict(
            bgcolor="#1a1a1a",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickfont=dict(color="#ffffff", size=11, family="'Share Tech Mono', 'JetBrains Mono', monospace"),
                gridcolor=RADAR_CYAN,
                linecolor=RADAR_CYAN,
                showgrid=True,
                dtick=20,
            ),
            angularaxis=dict(
                tickfont=dict(color=RADAR_CYAN, size=10, family="'Share Tech Mono', 'JetBrains Mono', monospace"),
                gridcolor=RADAR_CYAN,
                linecolor=RADAR_CYAN,
                showgrid=True,
            ),
        ),
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
            font=dict(family="'Share Tech Mono', monospace", color=RADAR_CYAN, size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=40, b=40, l=40, r=40),
        height=420,
        font=dict(family="'Share Tech Mono', monospace", color="#ffffff"),
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
