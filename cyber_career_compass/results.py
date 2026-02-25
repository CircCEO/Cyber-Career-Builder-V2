"""
High-fidelity results: dashboard layout, 7-category radar, Role Probability radar, PDF export.
"""

from typing import Dict, List, Optional, Any, Tuple

from .nice_framework import (
    get_work_role,
    get_certifications,
    ALL_CATEGORIES,
    ALL_ROLE_IDS,
)

# Reflex Telemetry Guard: default the Reflex drill state to False until
# the drill explicitly flips it, so downstream rendering logic can safely
# rely on st.session_state.reflex_complete.
try:  # pragma: no cover
    import streamlit as st  # type: ignore

    if "reflex_complete" not in st.session_state:
        st.session_state.reflex_complete = False
except Exception:
    # Safe no-op when imported outside a Streamlit session.
    pass

# Professional baseline (0–100) per category for Skill Gap comparison
PROFESSIONAL_BASELINE: Dict[str, float] = {c: 70.0 for c in ALL_CATEGORIES}
READINESS_THRESHOLD = 70.0  # Below this = show Professional Development Roadmap
ELITE_BASELINE = 70.0

# Credential mapping: category gap -> 1–2 certs that address the weakness
GAP_CERT_RECOMMENDATIONS: Dict[str, List[Tuple[str, str]]] = {
    "SP": [("Certified Secure Software Lifecycle Professional (CSSLP)", "ISC²"), ("GIAC Secure Software Programmer (GSSP)", "GIAC")],
    "PR": [("GIAC Certified Incident Handler (GCIH)", "GIAC"), ("Certified Incident Handler (ECIH)", "EC-Council")],
    "AN": [("GIAC Cyber Threat Intelligence (GCTI)", "GIAC"), ("CompTIA Cybersecurity Analyst (CySA+)", "CompTIA")],
    "CO": [("GIAC Security Essentials (GSEC)", "GIAC"), ("CompTIA Security+", "CompTIA")],
    "IN": [("GIAC Certified Forensic Analyst (GCFA)", "GIAC"), ("Certified Cyber Forensics Professional (CCFP)", "ISC²")],
    "OM": [("CompTIA Security+", "CompTIA"), ("GIAC Cloud Security Automation (GCSA)", "GIAC")],
    "OV": [("CISSP", "ISC²"), ("CompTIA Security+", "CompTIA")],
}


def get_top_gaps(
    user_scores: Dict[str, float],
    baseline: Optional[Dict[str, float]] = None,
    n: int = 3,
) -> List[Tuple[str, float, str]]:
    """Return top n (category, gap_size, category_label) where gap = baseline - user (largest gaps first)."""
    base = baseline if baseline is not None else PROFESSIONAL_BASELINE
    gaps: List[Tuple[str, float, str]] = []
    for c in ALL_CATEGORIES:
        u = user_scores.get(c, 0.0)
        b = base.get(c, ELITE_BASELINE)
        gap = max(0.0, b - u)
        if gap > 0:
            gaps.append((c, gap, c))
    gaps.sort(key=lambda x: -x[1])
    return gaps[:n]


def render_path_to_readiness_chart(
    user_scores: Dict[str, float],
    category_labels: Dict[str, str],
    baseline: Optional[Dict[str, float]] = None,
    lang: Optional[str] = None,
) -> None:
    """Bar chart: Path to Readiness — current score vs Elite baseline, gap in warning color (orange/red)."""
    try:
        import plotly.graph_objects as go
        import streamlit as st
        from .translations import get_ui
    except ImportError:
        return
    lang_key = lang or "en"
    ui = get_ui(lang_key)
    legend_you = ui.get("path_legend_you", "You")
    legend_gap = ui.get("path_legend_gap", "Gap to Elite")
    base = baseline if baseline is not None else PROFESSIONAL_BASELINE
    cats = list(ALL_CATEGORIES)
    labels = [category_labels.get(c, c) for c in cats]
    user_vals = [user_scores.get(c, 0) for c in cats]
    base_vals = [base.get(c, ELITE_BASELINE) for c in cats]
    gap_vals = [max(0, b - u) for u, b in zip(user_vals, base_vals)]
    fig = go.Figure()
    fig.add_trace(go.Bar(name=legend_you, y=labels, x=user_vals, orientation="h", marker_color="#00f2ff", text=[f"{v:.0f}" for v in user_vals], textposition="inside"))
    fig.add_trace(go.Bar(name=legend_gap, y=labels, x=gap_vals, orientation="h", marker_color="#ef4444", base=user_vals, text=[f"+{g:.0f}" if g > 0 else "" for g in gap_vals], textposition="inside"))
    fig.update_layout(
        barmode="stack",
        margin=dict(t=24, b=24, l=120, r=80),
        height=320,
        xaxis=dict(range=[0, 105], title="Score (0–100)", tickfont=dict(color="#a0a0a0")),
        yaxis=dict(tickfont=dict(color="#e0e0e0")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="#e0e0e0")),
        font=dict(family="'Share Tech Mono', sans-serif", color="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))


def _html_escape(s: str) -> str:
    """Escape for safe HTML."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_ares_deployment_cards(
    deployments: List[Dict[str, str]],
    lang: Optional[str] = None,
) -> None:
    """Render Project Ares Battle Room / Mission cards with neon-green pulsing border and logo."""
    import streamlit as st
    from .translations import get_ui

    if not deployments:
        return
    lang_key = lang or "en"
    ui = get_ui(lang_key)
    label_br = ui.get("ares_battle_room", "Battle Room")
    label_mission = ui.get("ares_mission", "Mission")
    label_path = ui.get("ares_learning_path", "Learning Path")
    label_value = ui.get("ares_training_value", "Training Value")

    # Project Ares logo: simple SVG shield + text (inline so no external asset)
    logo_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="1.5" width="28" height="28" style="vertical-align:middle;margin-right:6px;">'
        '<path d="M12 2L4 6v6c0 5.5 3.5 10 8 12 4.5-2 8-6.5 8-12V6l-8-4z"/>'
        '</svg>'
    )

    for d in deployments:
        typ = d.get("type", "BR")
        type_label = label_mission if typ == "M" else label_br
        title = _html_escape(d.get("title", ""))
        training_value = _html_escape(d.get("training_value", ""))
        learning_path = _html_escape(d.get("learning_path", ""))
        sid = _html_escape(d.get("id", ""))
        st.markdown(
            f'<div class="ares-bridge-card">'
            f'<div class="ares-bridge-card-header">'
            f'{logo_svg}'
            f'<span class="ares-bridge-card-badge">{type_label} {sid}</span>'
            f'</div>'
            f'<div class="ares-bridge-card-title">{title}</div>'
            f'<div class="ares-bridge-card-meta"><strong>{label_path}:</strong> {learning_path}</div>'
            f'<div class="ares-bridge-card-value ares-tactical-green"><strong>{label_value}:</strong> {training_value}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_ares_roadmap_summary(
    deployments: List[Dict[str, str]],
    lang: Optional[str] = None,
    tactical_frame: bool = False,
    metadata_str: Optional[str] = None,
    skip_anchor_nodes: bool = False,
    title_override: Optional[str] = None,
) -> None:
    """Horizontal Mission Node Map with BR1 and BR8 connections (cyan HUD nodes).
    If tactical_frame=True, wrap in .ares-tactical-frame with optional metadata overlay.
    If skip_anchor_nodes=True, only render the provided deployments (e.g. 3 BRs for Reveal Level Up)."""
    import streamlit as st
    from .translations import get_ui, get_ares_scenario_title
    from .project_ares import ARES_SCENARIOS

    lang_key = lang or "en"
    ui = get_ui(lang_key)
    node_map_title = title_override if title_override is not None else ui.get("ares_node_map_title", "Mission Node Map")

    seen: set = set()
    ordered: List[Dict[str, str]] = []
    if not skip_anchor_nodes:
        for sid in ("BR1", "BR8"):
            if sid in seen:
                continue
            seen.add(sid)
            info = ARES_SCENARIOS.get(sid)
            if info:
                title = get_ares_scenario_title(lang_key, sid) or info.get("title", sid)
                tv = info.get("training_value", "")
                ordered.append({
                    "id": sid,
                    "title": title,
                    "learning_path": (tv[:60] + "…") if len(tv) > 60 else tv,
                    "type": "BR",
                })
    for d in deployments:
        sid = d.get("id", "")
        if sid in seen:
            continue
        seen.add(sid)
        ordered.append({
            "id": sid,
            "title": d.get("title", ""),
            "learning_path": d.get("learning_path", ""),
            "type": d.get("type", "BR"),
        })

    if not ordered:
        return
    nodes_html = []
    for n in ordered:
        sid = _html_escape(n.get("id", ""))
        title = _html_escape(n.get("title", ""))
        path = _html_escape(n.get("learning_path", ""))
        nodes_html.append(
            f'<div class="ares-node">'
            f'<div class="ares-node-code">{sid}</div>'
            f'<div class="ares-node-title">{title}</div>'
            f'<div class="ares-node-path">{path}</div>'
            f'</div>'
        )
    roadmap_html = (
        f'<p style="font-weight:700;margin-bottom:0.5rem;">{_html_escape(node_map_title)}</p>'
        f'<div class="ares-roadmap-summary">{"".join(nodes_html)}</div>'
    )
    if tactical_frame:
        meta = f'<div class="card-metadata-overlay">{_html_escape(metadata_str or "SYS_REF: 800-181 // AUTH: DISA_CSSP")}</div>' if metadata_str else ""
        full_html = f'<div class="ares-tactical-frame">{meta}{roadmap_html}</div>'
        st.markdown(full_html, unsafe_allow_html=True)
    else:
        st.markdown("**" + node_map_title + "**")
        st.markdown(
            f'<div class="ares-roadmap-summary">{"".join(nodes_html)}</div>',
            unsafe_allow_html=True,
        )


def render_development_roadmap(score_state: Any, lang: Optional[str] = None) -> bool:
    """
    Reflex-gated Professional Development Roadmap.
    Only renders once Reflex telemetry is complete and NIST scores are non-zero:
    - Header + Mission Node Map
    - Recommended Training Deployments
    - Top 3 Gaps + Credential Mapping
    """
    import streamlit as st
    from .translations import get_ui, get_category_labels, get_learning_objectives
    from .project_ares import COMPETENCY_THRESHOLD, get_recommended_deployments, get_recommended_deployments_by_top_category

    lang_key = lang or "en"
    ui = get_ui(lang_key)
    category_labels = get_category_labels(lang_key)
    learning_objectives = get_learning_objectives(lang_key)
    user_scores = score_state.get_normalized_radar_scores()
    baseline = PROFESSIONAL_BASELINE

    # Require at least one category below readiness threshold for roadmap relevance.
    below = [c for c in ALL_CATEGORIES if user_scores.get(c, 0) < READINESS_THRESHOLD]
    if not below:
        return False

    avg_score = sum(user_scores.get(c, 0) for c in ALL_CATEGORIES) / len(ALL_CATEGORIES)
    # Reflex Telemetry State-Lock: Mission Node Map and Recommended Training Deployments ONLY when reflex_complete
    if not st.session_state.get("reflex_complete", False):
        return False
    if avg_score <= 0:
        return False

    st.markdown("---")
    st.markdown("#### " + ui.get("roadmap_title", "Professional Development Roadmap"))
    st.caption(ui.get("ares_guide_ref", "Battle Room descriptions (BR1, BR8, etc.) from Project Ares NIST NICE Guide, Page 47."))

    # Zone C: Mission Node Map + Recommended Training Deployments (state-locked behind reflex_complete)
    if st.session_state.get("reflex_complete", False):
        # Ares Logic Synchronization: Mission Node Map driven by get_ares_recommendations() (2 lowest NIST categories → BR8, etc.)
        from .scoring import get_ares_recommendations

        ares_deployments = get_ares_recommendations(score_state, max_per_category=4)
        # Convert to roadmap summary format: id, title, learning_path, type
        deployments_for_node_map: List[Dict[str, str]] = []
        for r in ares_deployments:
            sid = r.get("mission_id", "")
            relevance = r.get("relevance", "")
            deployments_for_node_map.append({
                "id": sid,
                "title": r.get("title", sid),
                "learning_path": (relevance[:60] + "…") if len(relevance) > 60 else relevance,
                "type": "M" if sid.startswith("M") else "BR",
            })
        # Render Mission Node Map inside dedicated tactical frame with real Ares data
        render_ares_roadmap_summary(
            deployments_for_node_map,
            lang_key,
            tactical_frame=True,
            metadata_str="SYS_REF: 800-181 // AUTH: DISA_CSSP",
        )

        deployments = get_recommended_deployments(score_state, lang=lang_key, max_cards=4) if avg_score < COMPETENCY_THRESHOLD else []

        if deployments:
            st.markdown("**" + ui.get("ares_deployments_title", "Recommended Training Deployments") + "**")
            render_ares_deployment_cards(deployments, lang_key)
            st.markdown("")

        # Project Ares by highest NIST category (strength-based, dynamic)
        top_category_deployments = get_recommended_deployments_by_top_category(score_state, lang=lang_key, max_cards=4)
        if top_category_deployments:
            st.markdown("**" + ui.get("ares_top_category_title", "Recommended for your top category") + "**")
            st.caption(ui.get("ares_top_category_caption", "Training aligned with your strongest NIST category."))
            render_ares_deployment_cards(top_category_deployments, lang_key)
            st.markdown("")

    # Top 3 NIST K/S gaps + credential mapping.
    top_gaps = get_top_gaps(user_scores, baseline, n=3)
    if top_gaps:
        st.markdown("**" + ui.get("gap_identification_title", "Top 3 NIST K/S Gaps") + "**")
        for cat, gap_size, _ in top_gaps:
            label = category_labels.get(cat, cat)
            objs = learning_objectives.get(cat, [])
            obj_text = objs[0] if objs else ""
            st.markdown(f"- **{label}** (gap: {gap_size:.0f}) → *{obj_text}*")
            if len(objs) > 1:
                st.caption("  " + "; ".join(objs[1:3]))
        st.markdown("")

        st.markdown("**" + ui.get("credential_mapping_title", "Credential Mapping") + "**")
        seen: set = set()
        for cat, _, _ in top_gaps:
            for cert_name, issuer in GAP_CERT_RECOMMENDATIONS.get(cat, [])[:2]:
                if cert_name not in seen:
                    seen.add(cert_name)
                    st.markdown(f"- **{cert_name}** — {issuer}")
        st.markdown("")

    return True


def render_radar_chart(
    category_scores: Dict[str, float],
    category_labels: Dict[str, str],
    accent_color: str = "#00f2ff",
    fill_color: str = "rgba(0, 242, 255, 0.12)",
    neon_glow: bool = True,
    ghost: bool = False,
    hud_style: bool = True,
) -> None:
    """Plotly radar: HUD style = transparent cyan fill + pure white stroke, grid hidden. Otherwise neon (#00f2ff)."""
    try:
        import plotly.graph_objects as go
        import streamlit as st
    except ImportError:
        return
    cats = [c for c in ALL_CATEGORIES if c in category_scores]
    if not cats:
        cats = list(category_scores.keys())
    values = [category_scores.get(c, 0) for c in cats]
    labels = [category_labels.get(c, c) for c in cats]
    values_loop = values + [values[0]]
    labels_loop = labels + [labels[0]]
    line_color = "#ffffff" if hud_style else accent_color
    fill = fill_color if not hud_style else "rgba(0, 242, 255, 0.12)"
    line_width = 3 if neon_glow else 2
    grid_color = "rgba(0,0,0,0)" if hud_style else ("rgba(0, 242, 255, 0.35)" if ghost else "rgba(0, 242, 255, 0.15)")
    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_loop,
            theta=labels_loop,
            fill="toself",
            line=dict(color=line_color, width=line_width),
            fillcolor=fill,
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#a0a0a0"),
                gridcolor=grid_color,
                showgrid=not hud_style,
            ),
            angularaxis=dict(
                tickfont=dict(color="#00FF00", size=11, family="'Share Tech Mono', monospace"),
                gridcolor=grid_color,
                showgrid=not hud_style,
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=30, b=30, l=50, r=50),
        height=420,
        font=dict(family="'Share Tech Mono', 'Inter', 'Hiragino Sans', sans-serif", color="#e0e0e0"),
    )
    if neon_glow:
        fig.update_traces(
            line=dict(width=line_width, color=line_color),
            selector=dict(type="scatterpolar"),
        )
    st.markdown('<div class="radar-hud-frame" aria-hidden="true"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=True))


def render_radar_chart_compact(
    category_scores: Dict[str, float],
    category_labels: Dict[str, str],
    height: int = 220,
    accent_color: str = "#00f2ff",
    fill_color: str = "rgba(0, 242, 255, 0.12)",
    hud_style: bool = True,
) -> None:
    """Compact Plotly radar: HUD style = transparent cyan fill + pure white stroke, grid hidden. For sidebar and Proving Ground."""
    try:
        import plotly.graph_objects as go
        import streamlit as st
    except ImportError:
        return
    cats = [c for c in ALL_CATEGORIES if c in category_scores]
    if not cats:
        cats = list(category_scores.keys())
    values = [category_scores.get(c, 0) for c in cats]
    labels = [category_labels.get(c, c) for c in cats]
    values_loop = values + [values[0]]
    labels_loop = labels + [labels[0]]
    line_color = "#ffffff" if hud_style else accent_color
    fill = fill_color if not hud_style else "rgba(0, 242, 255, 0.12)"
    grid_color = "rgba(0,0,0,0)" if hud_style else "rgba(0, 242, 255, 0.15)"
    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_loop,
            theta=labels_loop,
            fill="toself",
            line=dict(color=line_color, width=2),
            fillcolor=fill,
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=8, color="#a0a0a0"),
                gridcolor=grid_color,
                showgrid=not hud_style,
            ),
            angularaxis=dict(
                tickfont=dict(color="#00FF00", size=9, family="'Share Tech Mono', monospace"),
                gridcolor=grid_color,
                showgrid=not hud_style,
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=20, b=20, l=30, r=30),
        height=height,
        font=dict(family="'Share Tech Mono', sans-serif", color="#e0e0e0", size=10),
    )
    st.markdown('<div class="radar-hud-frame" aria-hidden="true"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))


def render_skill_gap_radar(
    user_scores: Dict[str, float],
    category_labels: Dict[str, str],
    baseline_scores: Optional[Dict[str, float]] = None,
    user_color: str = "#00f2ff",
    baseline_color: str = "rgba(255, 180, 0, 0.8)",
    lang: Optional[str] = None,
) -> None:
    """Plotly radar: User vs Professional baseline (transparent bg, neon user fill, dashed baseline)."""
    try:
        import plotly.graph_objects as go
        import streamlit as st
        from .translations import get_ui
    except ImportError:
        return
    lang_key = lang or "en"
    ui = get_ui(lang_key)
    legend_you = ui.get("path_legend_you", "You")
    legend_baseline = ui.get("radar_legend_baseline", "Professional baseline")
    baseline = baseline_scores if baseline_scores is not None else PROFESSIONAL_BASELINE
    cats = [c for c in ALL_CATEGORIES if c in user_scores or c in baseline]
    if not cats:
        cats = list(ALL_CATEGORIES)
    labels = [category_labels.get(c, c) for c in cats]
    user_vals = [user_scores.get(c, 0) for c in cats] + [user_scores.get(cats[0], 0)]
    base_vals = [baseline.get(c, 70) for c in cats] + [baseline.get(cats[0], 70)]
    labels_loop = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=user_vals,
            theta=labels_loop,
            name=legend_you,
            fill="toself",
            line=dict(color=user_color, width=3),
            fillcolor="rgba(0, 242, 255, 0.25)",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=base_vals,
            theta=labels_loop,
            name=legend_baseline,
            line=dict(color=baseline_color, width=2, dash="dash"),
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#a0a0a0"), gridcolor="rgba(0, 242, 255, 0.15)"),
            angularaxis=dict(tickfont=dict(color=user_color, size=11), gridcolor="rgba(0, 242, 255, 0.15)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="#e0e0e0")),
        margin=dict(t=40, b=30, l=50, r=50),
        height=420,
        font=dict(family="'Share Tech Mono', 'Inter', 'Hiragino Sans', sans-serif", color="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=True))


def render_role_probability_radar(
    role_scores: Dict[str, float],
    role_labels: Dict[str, str],
    accent_color: str = "#00f2ff",
    fill_color: str = "rgba(0, 242, 255, 0.2)",
) -> None:
    """Interactive Plotly radar: Role Probability with neon #00f2ff and transparent background."""
    try:
        import plotly.graph_objects as go
        import streamlit as st
    except ImportError:
        return
    roles = [r for r in ALL_ROLE_IDS if r in role_scores]
    if not roles:
        roles = list(role_scores.keys())
    values = [role_scores.get(r, 0) for r in roles]
    labels = [role_labels.get(r, r) for r in roles]
    values_loop = values + [values[0]]
    labels_loop = labels + [labels[0]]
    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_loop,
            theta=labels_loop,
            fill="toself",
            line=dict(color=accent_color, width=3),
            fillcolor=fill_color,
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#a0a0a0"),
                gridcolor="rgba(0, 242, 255, 0.15)",
            ),
            angularaxis=dict(
                tickfont=dict(color=accent_color, size=11),
                gridcolor="rgba(0, 242, 255, 0.15)",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=30, b=30, l=50, r=50),
        height=420,
        font=dict(family="'Share Tech Mono', 'Inter', 'Hiragino Sans', sans-serif", color="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=True))


def build_dossier_pdf(score_state: Any, lang: Optional[str] = None) -> Optional[bytes]:
    """Build Career Dossier as PDF bytes for download. Returns None if fpdf2 not available."""
    try:
        from fpdf import FPDF
    except ImportError:
        return None
    from .translations import get_ui, get_category_labels
    ui = get_ui(lang or "en")
    labels = get_category_labels(lang or "en")
    dominant = score_state.get_dominant_aptitude()
    knowledge_level = score_state.get_knowledge_level()
    role = get_work_role(dominant, knowledge_level)
    certs = get_certifications(dominant, knowledge_level)
    radar = score_state.get_normalized_radar_scores()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, ui.get("pdf_title", "NICE Career Dossier"), ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{ui.get('pdf_work_role', 'Work Role')}: {role.title} ({role.id})", ln=True)
    pdf.cell(0, 8, f"{ui.get('pdf_category', 'Category')}: {role.category}", ln=True)
    pdf.ln(4)
    pdf.multi_cell(0, 6, role.definition)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, ui.get("pdf_strengths", "Your Strengths"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, role.strengths_summary)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, ui.get("pdf_category_profile", "Category Profile (normalized 0-100)"), ln=True)
    pdf.set_font("Helvetica", "", 9)
    for c in ALL_CATEGORIES:
        if c in radar:
            pdf.cell(0, 6, f"  {labels.get(c, c)}: {radar[c]:.0f}", ln=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, ui.get("pdf_certs", "Recommended Certifications"), ln=True)
    pdf.set_font("Helvetica", "", 10)
    for cert in certs:
        pdf.cell(0, 6, f"  - {cert.name} ({cert.issuer}, {cert.level})", ln=True)
    return bytes(pdf.output())


def render_dossier_explorer(score_state: Any, lang: Optional[str] = None) -> None:
    """Render Explorer results: report engine ONLY after Question 10 (reflex_complete)."""
    import streamlit as st
    from .translations import get_ui, get_category_labels

    lang_key = lang or "en"
    ui = get_ui(lang_key)
    # Telemetry Guard: strictly gate Archetype (The Reveal) behind reflex_complete
    if not st.session_state.get("reflex_complete", False):
        st.markdown("#### " + ui.get("explorer_results_title", "Your Cyber Archetype"))
        st.markdown(
            f'<p style="font-family:\'Share Tech Mono\',monospace;color:#39ff14;">'
            f'{_html_escape(ui.get("archetype_await_telemetry", "Complete Proving Grounds (10 NIST-mapped questions) to unlock your Cyber Archetype report."))}</p>',
            unsafe_allow_html=True,
        )
        return

    archetype = score_state.get_archetype()
    radar_scores = score_state.get_normalized_radar_scores()
    category_labels = get_category_labels(lang_key)

    arch_title_key = f"archetype_{archetype}"
    arch_desc_key = f"archetype_{archetype}_desc"
    arch_title = ui.get(arch_title_key, archetype.title())
    arch_desc = ui.get(arch_desc_key, "")

    # Zone 2: Asymmetric Cyan Brackets (#00ffff) and Neon Green only — no standard boxes
    desc_block = f'<p class="archetype-tactical-green" style="font-size:0.9rem;">{_html_escape(arch_desc)}</p>' if arch_desc else ""
    st.markdown(
        f'<div class="archetype-hud-frame">'
        f'<div class="archetype-title-cyan">{_html_escape(ui.get("explorer_results_title", "Your Cyber Archetype"))}</div>'
        f'<div class="archetype-title-cyan" style="font-size:1.1rem; margin:0.35rem 0;">{_html_escape(arch_title)}</div>'
        f'{desc_block}'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f'<p class="archetype-title-cyan">{_html_escape(ui["category_fit"])}</p>', unsafe_allow_html=True)
        render_radar_chart(
            radar_scores,
            category_labels,
            accent_color="#00f2ff",
            fill_color="rgba(0, 242, 255, 0.2)",
            neon_glow=True,
        )
    st.markdown("---")
    render_development_roadmap(score_state, lang)


def render_dossier_operator(score_state: Any, lang: Optional[str] = None) -> None:
    """Render Operator mission complete: Mission Summary + category radar + top role match."""
    import streamlit as st
    from .translations import get_ui, get_category_labels, get_role_display
    from .nice_framework import get_work_role

    lang_key = lang or "en"
    ui = get_ui(lang_key)
    radar_scores = score_state.get_normalized_radar_scores()
    category_labels = get_category_labels(lang_key)
    dominant = score_state.get_dominant_aptitude()
    role = get_work_role(dominant, 0)
    role_display = get_role_display(lang_key, role.id)

    title = role_display["title"] if role_display else role.title
    definition = role_display["definition"] if role_display else role.definition

    st.markdown("#### " + ui.get("operator_results_title", "Mission Complete"))
    st.markdown(
        f'<p style="font-family:\'Share Tech Mono\',monospace;color:#39ff14;">{_html_escape(ui.get("align_success", "Align your path with the NICE Framework."))}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("#### " + ui["category_fit"])
    render_radar_chart(
        radar_scores,
        category_labels,
        accent_color="#00f2ff",
        fill_color="rgba(0, 242, 255, 0.2)",
        neon_glow=True,
    )
    st.markdown("---")
    render_development_roadmap(score_state, lang)
    st.markdown("---")
    st.markdown("#### " + ui["work_role"])
    st.markdown(f"**{title}** · {role.id}")
    st.caption(definition)
    st.markdown("---")


def render_dossier(score_state: Any, lang: Optional[str] = None) -> None:
    """Render Specialist High-Security Dossier: Work Role, NIST 2026, Skill Gap Radar, PDF."""
    import streamlit as st
    from .translations import get_ui, get_category_labels, get_role_labels, get_role_display

    lang_key = lang or "en"
    ui = get_ui(lang_key)
    dominant = score_state.get_dominant_aptitude()
    knowledge_level = score_state.get_knowledge_level()
    role = get_work_role(dominant, knowledge_level)
    certs = get_certifications(dominant, knowledge_level)
    radar_scores = score_state.get_normalized_radar_scores()
    category_labels = get_category_labels(lang_key)
    role_scores = score_state.get_role_probabilities()
    role_labels = get_role_labels(lang_key)
    role_display = get_role_display(lang_key, role.id)

    title = role_display["title"] if role_display else role.title
    definition = role_display["definition"] if role_display else role.definition
    strengths = role_display["strengths"] if role_display else role.strengths_summary
    category_display = role_display["category"] if role_display else role.category

    nist_id = f"{role.id}-001"

    st.markdown("#### " + ui.get("high_security_dossier_title", "High-Security Dossier"))
    st.caption(ui.get("specialist_results_title", "50-Question TKS Assessment · NIST NICE 2026 (OG-WRL-017, NF-COM-008)"))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### " + ui["work_role"])
        st.markdown(f"**{title}**")
        st.caption(f"{category_display} · {role.id}")
        st.markdown("**" + ui.get("nist_role_id", "NIST Work Role ID") + ":** `" + nist_id + "`")
        st.write(definition)
        st.markdown("**" + ui["your_strengths"] + "**")
        if strengths:
            st.markdown(
                f"<p style=\"font-family:'Share Tech Mono',monospace;color:#39ff14;font-size:0.9rem;\">{_html_escape(strengths)}</p>",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("#### " + ui["category_fit"])
        render_radar_chart(
            radar_scores,
            category_labels,
            accent_color="#00f2ff",
            fill_color="rgba(0, 242, 255, 0.25)",
            neon_glow=True,
        )

    st.markdown("---")
    st.markdown("#### " + ui.get("skill_gap_radar_title", "Skill Gap Radar (You vs Professional Baseline)"))
    render_skill_gap_radar(radar_scores, category_labels, baseline_scores=PROFESSIONAL_BASELINE, lang=lang_key)

    render_development_roadmap(score_state, lang)

    st.markdown("---")
    st.markdown("#### " + ui["role_probability"])
    render_role_probability_radar(
        role_scores,
        role_labels,
        accent_color="#00f2ff",
        fill_color="rgba(0, 242, 255, 0.2)",
    )

    st.markdown("---")
    st.markdown("#### " + ui.get("salary_roadmap_2026", "2026 Salary & Certification Roadmap"))
    st.caption(ui.get("salary_range", "Typical salary range (2026):") + " **$90K – $180K+** (varies by role, region, level).")
    st.markdown("**" + ui.get("cert_roadmap", "Certification path:") + "**")
    road_col1, road_col2 = st.columns(2)
    certs_left = certs[0::2]
    certs_right = certs[1::2]
    with road_col1:
        for c in certs_left:
            url = getattr(c, "url", None)
            if url:
                st.markdown(f"- **[{c.name}]({url})** — {c.issuer} · {c.level}")
            else:
                st.markdown(f"- **{c.name}** — {c.issuer} · {c.level}")
    with road_col2:
        for c in certs_right:
            url = getattr(c, "url", None)
            if url:
                st.markdown(f"- **[{c.name}]({url})** — {c.issuer} · {c.level}")
            else:
                st.markdown(f"- **{c.name}** — {c.issuer} · {c.level}")

    st.markdown("---")
    st.markdown("#### " + ui.get("download_dossier", "Download PDF"))
    pdf_bytes = build_dossier_pdf(score_state, lang)
    if pdf_bytes is not None:
        st.download_button(
            label=ui.get("download_pdf", "Download High-Security Dossier (PDF)"),
            data=pdf_bytes,
            file_name="high_security_dossier.pdf",
            mime="application/pdf",
            type="primary",
        )
    else:
        st.caption(ui.get("install_fpdf2", "Install fpdf2 for PDF download: pip install fpdf2"))
    st.markdown("---")
