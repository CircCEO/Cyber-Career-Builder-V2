"""
Compatibility shim for absolute imports.

Allows `from translations import ...` to resolve to the core
`cyber_career_compass.translations` module when code is running as part
of the Streamlit app (`main.py`) or other package-based entrypoints.
"""

from cyber_career_compass.translations import *  # noqa: F401,F403

