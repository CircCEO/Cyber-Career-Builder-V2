"""
Compatibility shim for absolute imports.

Allows both:
- `from nice_framework import ...` when running modules as top-level scripts inside
  the `cyber_career_compass` directory, and
- `from cyber_career_compass.nice_framework import ...` when using the package
  from the Streamlit app (`main.py`).
"""

from cyber_career_compass.nice_framework import *  # noqa: F401,F403

