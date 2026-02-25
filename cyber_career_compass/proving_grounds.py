"""
Proving Ground — 30-Step Calibration (20 Personality / 10 Core Technical), Reflex Lab, and future labs.
Calibration uses get_calibration_questions() from content.py (20 NIST TKS/Work Role personality + 10 Core Technical).
Lab UI and state live in main.py (_page_proving_ground). This module is reserved for
future lab expansions (e.g. live-fire scenarios, Project Ares deployments).
"""

# Re-export 30-step calibration constants for single source of truth (content.py implements the split)
from content import CALIBRATION_TOTAL, get_calibration_questions

__all__ = ["CALIBRATION_TOTAL", "get_calibration_questions"]
