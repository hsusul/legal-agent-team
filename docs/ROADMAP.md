# Roadmap

## Phase 1: Make It Runnable

Goal: A new developer can install dependencies, import the app, and run basic validation without external API calls.

Tasks:

- Fix missing import dependencies.
- Remove dependency conflicts that prevent import.
- Add `pytest`.
- Add `tests/test_imports.py`.
- Ensure `legal_agent_team.py` and `config.py` compile.
- Update setup documentation in a later focused PR.

Acceptance criteria:

- `uv run --with-requirements requirements.txt pytest -q` passes.
- `uv run --with-requirements requirements.txt python -m py_compile legal_agent_team.py config.py` passes.

## Phase 2: Make It Safe

Goal: The app is clearly framed as research assistance and handles secrets and uploads responsibly.

Tasks:

- Remove hardcoded password autofill and default Qdrant Cloud URL.
- Add `.env.example` and standard environment variable names.
- Add legal safety copy to the UI and README.
- Add upload size, extension, and filename validation.
- Add prompt-injection boundaries for uploaded document content.

Acceptance criteria:

- No hardcoded credentials, passwords, or service URLs.
- User-facing copy says the app is not legal advice.
- Upload validation is covered by tests.

## Phase 3: Make It Testable

Goal: Core behavior can be tested without Streamlit or live services.

Tasks:

- Extract settings loading.
- Extract document processing.
- Extract agent role and prompt construction.
- Add mocked tests for settings, upload validation, prompt construction, and orchestration.
- Add fixture documents and expected output examples.

Acceptance criteria:

- Unit tests cover core modules without OpenAI, Anthropic, Qdrant, or DuckDuckGo calls.
- Streamlit remains a thin UI shell.

## Phase 4: Make It Impressive

Goal: The app demonstrates strong AI product engineering, not just a demo wrapper.

Tasks:

- Add structured analysis outputs.
- Add citation/source-grounding fields.
- Add local mock mode for demos and tests.
- Add evaluation examples for grounding, refusal, and safety behavior.
- Consider CLI, FastAPI, or a polished UI once the core flow is stable.

Acceptance criteria:

- Demo can run in a controlled mode without paid services.
- Outputs show citations or explicit limitations.
- Portfolio reviewers can understand architecture, safety choices, and test strategy.
