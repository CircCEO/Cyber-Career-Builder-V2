"""
Original Ares Geometry — 7-axis Plotly radar for Cyber Career Compass.

This module exposes a radar builder that can be embedded in Streamlit or other
front-ends while keeping the visual shape aligned to the Ares / NIST NICE spec.
"""

from typing import Dict

from nice_framework import (
    CATEGORY_AN,
    CATEGORY_CO,
    CATEGORY_IN,
    CATEGORY_OM,
    CATEGORY_OV,
    CATEGORY_PR,
    CATEGORY_SP,
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
    Build a 7-axis Plotly radar using the NIST NICE categories in fixed order:
    Analyze, Collect & Operate, Investigate, Operate & Maintain,
    Oversee & Govern, Protect & Defend, Securely Provision.
    """
    try:
        import plotly.graph_objects as go
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Plotly is required to render the Ares radar.") from exc

    values = [max(0.0, min(100.0, float(category_scores.get(code, 0.0)))) for code in NICE_CATEGORY_ORDER]
    values_loop = values + [values[0]]
    labels_loop = NICE_CATEGORY_LABELS + [NICE_CATEGORY_LABELS[0]]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_loop,
            theta=labels_loop,
            fill="toself",
            line=dict(color="#00f2ff", width=2),
            fillcolor="rgba(0, 242, 255, 0.10)",  # 10% Neon-Cyan opacity
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#00FF00", size=11, family="'Share Tech Mono', monospace"),
                gridcolor="#333333",
                linecolor="#333333",
                showgrid=True,
            ),
            angularaxis=dict(
                tickfont=dict(color="#00FF00", size=11, family="'Share Tech Mono', monospace"),
                gridcolor="#333333",
                linecolor="#333333",
                showgrid=True,
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # Float on Zero-Box #0a0a0b
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=420,
        font=dict(family="'Share Tech Mono', monospace", color="#e0e0e0"),
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
