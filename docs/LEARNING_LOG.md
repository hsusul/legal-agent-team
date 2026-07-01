# Learning Log

Use this file to track what you learn while rebuilding the project.

## Entries

### 2026-07-01

- The app is currently a single Streamlit script, which makes import and smoke tests the first useful quality gate.
- `phidata` provides the `phi.*` imports used by the app; the separate `phi` package conflicts with those imports.
- `phi.tools.duckduckgo` requires the `duckduckgo-search` package at import time.
- Early tests should avoid OpenAI, Anthropic, Qdrant, and web-search calls.

## Template

### YYYY-MM-DD

- What I changed:
- What I learned:
- What broke:
- How I verified it:
- Follow-up:
