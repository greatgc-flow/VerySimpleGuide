# Lifecycle Value Stream

## Purpose and limits
Solve measurable problems for users and organizations while reducing lifetime safety, support, transition and maintenance costs. Conformity scores are a means, not the outcome.

The twelve stages form a **logical coverage view**, not a mandatory sequential waterfall. Activities may overlap, iterate, shrink or be omitted with a recorded reason. Analyze each relevant stage using **Outcome → Inputs → Decision/Owner → Outputs/Evidence → Acceptance → Next/Revisit**. Before building, compare **build / buy / reuse / do nothing**; planned retirement is a valid decision, not automatically a failure.

Security, quality, reliability, data, finance and user value are cross-cutting concerns, not the exclusive responsibilities of one stage. UI, CLI, library, API, event-only, embedded, offline, critical-control, cloud, AI-assisted and data-only projects are in scope. No single language, database, CI, vendor or infrastructure pattern is mandated; legal or operational constraints can strengthen project-local obligations.

## Decision strength
- If user value is unknown, revisit discovery before declaring an implementation complete.
- If pre/post measurements are unavailable, design the measurement method or approve a scoped exception.
- Scale the required evidence with expected impact and risk, not the number of project artifacts.
- New technology is a hypothesis to evaluate, not a trend to obey.

## Stage transitions
The machine authority is [`03_LIFECYCLE/lifecycle-matrix.json`](../03_LIFECYCLE/lifecycle-matrix.json), which specifies twelve stages, ten concerns, normal `next_stages` and uncertainty/failure `revisit_stages`. Learning from retirement may inform a new discovery without falsifying the historical closure record. `N_A` requires applicability rationale; `DEFERRED` requires an owner and trigger; `PASS` requires exact evidence for the declared scope and candidate.

**Design closure** means lifecycle coverage, ownership, transitions, schemas and negative tests are defined. **Operational closure** additionally requires field evidence, post-release outcomes, and retirement/data/access obligations as applicable. The General package can assert only the former for its examples.

## Lightweight evaluation of the 12×10 space
A project records 12 stage decisions and 10 concern decisions (22 entries). Combine these into review prompts; use `cell_overrides` for exceptional stage–concern intersections. `FOCUS`/`CONSIDER` are not mandatory actions. Avoid promoting an intersection to `PASS` merely because its stage and concern each have broad PASS; the exact cell requires its own applicable evidence. If decisions conflict, retain `REQUIRED` or `DEFERRED` until justified.
