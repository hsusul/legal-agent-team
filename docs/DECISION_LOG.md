# Decision Log

Record technical decisions here so the rebuild remains intentional and reviewable.

## Decisions

### 2026-07-01: Start With Importability Before Architecture Changes

Status: Accepted

Context: The app could not be imported from a clean dependency install because the dependency list was incomplete and included a conflicting package.

Decision: Keep the first code change small: fix dependencies and add an import smoke test before refactoring the app.

Consequences:

- The repo gets a fast validation baseline.
- Larger architecture work is deferred until the current behavior is reproducible.
- Tests remain free of external API calls.

### 2026-07-01: Keep Legal Safety Framing in Planning Docs First

Status: Accepted

Context: The project needs legal-safety framing, but rewriting prompts and UI copy is broader than the first runnable baseline.

Decision: Document safety constraints in the PRD now and defer app prompt/UI wording changes to Phase 2.

Consequences:

- The first PR stays small.
- Safety work is explicitly planned rather than forgotten.
- Future prompt changes can be reviewed as a focused safety PR.

## Template

### YYYY-MM-DD: Title

Status: Proposed | Accepted | Rejected | Superseded

Context:

Decision:

Consequences:
