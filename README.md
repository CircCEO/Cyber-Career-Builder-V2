# Cyber Career Compass

A **Streamlit web app** (and optional terminal game) that uses the **NIST NICE Framework** as its logic engine. Answer Instinct, Technical, and Deep-Scenario questions to get a **NICE Career Dossier**: work role, strengths, a **radar chart** across five NICE categories, and a **certification roadmap** with clickable links.

## Features

- **Weighted scoring** — Choices contribute to multiple NICE categories (e.g., 80% Protect and Defend, 20% Investigate).
- **5 Instinct + 10 Technical + 5 Deep-Scenario questions** — Deep scenarios cover 2026 trends: AI Security, Supply Chain Risk, Cloud Governance.
- **Five NICE categories** — SP (Securely Provision), PR (Protect and Defend), AN (Analyze), IN (Investigate), OM (Operate and Maintain).
- **Career Dossier** — Work role, strengths, **radar chart** (Plotly), and **recommended certifications with links** (e.g., Security+, GCIH, CISSP).
- **Dark Mode Hacker Theme** — Neon-blue accents and monospace font via custom CSS.

## How to Run (Streamlit — recommended)

1. **Create a virtual environment (recommended):**
   ```bash
   cd "/Users/mikemoniz/Cusor Project"
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Streamlit app:**
   ```bash
   streamlit run main.py
   ```

   This opens the app in your browser. Use the sidebar for **Agent Status** and the main area for questions; at the end you get the dossier with radar chart and certification links.

## Terminal game (optional)

After activating the same venv, you can run the terminal version (Instinct + Technical only):

```bash
python -m cyber_career_compass.game
```

Or with preset answers:

```bash
python main.py --demo
```

(Note: `main.py` is built for Streamlit; the `--demo` path still uses the legacy terminal flow if you keep a small CLI branch in `main.py`. For demo-only terminal, use `python -m cyber_career_compass.game` with your own harness.)

## Project Layout

```
Cusor Project/
├── main.py                 # Streamlit entry point — run with: streamlit run main.py
├── requirements.txt        # rich, streamlit, plotly
├── README.md
└── cyber_career_compass/
    ├── __init__.py
    ├── nice_framework.py   # NICE categories, work roles, certifications (with URLs)
    ├── questions.py        # Instinct, Technical, Deep-Scenario (weighted choices)
    ├── scoring.py          # Weighted category scores, knowledge level
    ├── results.py          # Radar chart + dossier for Streamlit
    ├── ui.py               # Rich terminal UI (for terminal game)
    └── game.py             # Terminal game flow
```

## Scoring

- **Weighted matrix:** Each choice adds fractional scores to one or more NICE categories (SP, PR, AN, IN, OM). The **dominant** category drives your work role.
- **Knowledge:** Technical questions have one correct answer each. ≥50% correct → Level 1; otherwise Level 0.
- **Dossier:** Dominant category + knowledge level select a NICE work role and two certifications (with links).

## Requirements

- Python 3.9+
- See `requirements.txt`: `rich`, `streamlit`, `plotly`
