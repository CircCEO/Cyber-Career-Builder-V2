"""
Compatibility shim for absolute imports.

Ensures `from project_ares import ...` resolves to the
`cyber_career_compass.project_ares` module when running the
Streamlit app or other package-based entrypoints.
"""

from cyber_career_compass.project_ares import *  # noqa: F401,F403

