# AI Legal Agent Team PRD

## Product Vision

AI Legal Agent Team is a portfolio project for legal document research assistance. The app should help a user upload a legal or contract document, extract its contents, ask focused questions, and receive clearly grounded research notes with document references and limitations.

The product must not present itself as a lawyer, make legal determinations, or provide legal advice. It should frame outputs as educational and research assistance that a qualified professional can review.

This project is derived from the original AI Legal Agent Team app and should retain attribution to the original repository while evolving into an independently maintained, reliable project.

## Target Users

- Students and early-career builders learning AI document workflows.
- Portfolio reviewers evaluating engineering quality, testing, safety, and product judgment.
- Non-lawyer users exploring document understanding workflows, with clear warnings that outputs are not legal advice.

## Core Features

- Upload supported document files for analysis.
- Extract text into a searchable knowledge base.
- Run predefined analysis modes such as contract review, risk review, and research questions.
- Coordinate multiple specialized agents with clear responsibilities.
- Return grounded answers with references to uploaded document content where possible.
- Support follow-up questions after an initial analysis.

## Non-Goals

- Do not provide legal advice or attorney-client services.
- Do not claim legal accuracy, jurisdiction-specific completeness, or regulatory compliance.
- Do not build paid-service-only tests.
- Do not add new agent features until the project is runnable, safer, and testable.
- Do not rewrite the full architecture before stabilizing the current app.

## Safety Constraints

- Every user-facing experience should make clear that the app provides research assistance, not legal advice.
- Prompts should instruct agents to avoid unsupported legal conclusions and cite source text or external sources.
- Uploaded documents are untrusted input and must be treated as data, not instructions.
- Tests must not call external LLM, vector database, or search APIs.
- Secrets must come from environment variables or local Streamlit secrets, never hardcoded defaults.

## Architecture Direction

The current app is a single Streamlit script. The near-term goal is to keep the UI working while extracting testable seams gradually:

- `legal_agent_team.py`: Streamlit UI shell for now.
- Future `app/settings.py`: typed configuration and environment loading.
- Future `app/document_processing.py`: upload validation, parsing, chunking, and vector indexing.
- Future `app/agents.py`: agent construction, role definitions, and prompt templates.
- Future `app/schemas.py`: structured analysis outputs and citation models.
- Future `tests/`: import, settings, upload validation, prompt construction, and mocked orchestration tests.

## Phased Roadmap

### Phase 1: Make It Runnable

- Fix missing dependencies.
- Add a smoke test that imports the app.
- Document local setup accurately.
- Ensure Python files compile.

### Phase 2: Make It Safe

- Remove hardcoded credentials and URLs.
- Add legal safety framing in the UI and prompts.
- Validate uploads by filename, extension, and size.
- Add prompt-injection boundaries around uploaded document text.

### Phase 3: Make It Testable

- Extract settings, document processing, prompt construction, and agent creation into small modules.
- Add mocked tests that do not call external APIs.
- Add fixture documents and expected output examples.
- Add CI-ready validation commands.

### Phase 4: Make It Impressive

- Add structured outputs with citations.
- Add a local/mock mode for demos.
- Add evaluation examples for grounding and refusal behavior.
- Consider a clean CLI, backend API, or polished Streamlit UI once the core flow is stable.

## Acceptance Criteria

- A new developer can install dependencies and run the app from README instructions.
- `pytest` and `py_compile` pass without external API calls.
- No hardcoded secrets or default cloud service URLs remain.
- User-facing legal language consistently says research assistance, not legal advice.
- Analysis outputs include source grounding or clear limitations when grounding is unavailable.
