"""
Compatibility shim for absolute imports.

Ensures `from content import ...` resolves to the
`cyber_career_compass.content` module when imported from package-based
entrypoints like the Streamlit app (`main.py`).
"""

from cyber_career_compass.content import *  # noqa: F401,F403

