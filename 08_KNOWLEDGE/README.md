# Optional Engineering Guidance, Patterns and References

**Goal:** find the smallest relevant guidance, explain its applicability, compare alternatives, test its trade-offs and keep the option to reject it.

Adoption, provenance and source-status rules live in the [knowledge reference standard](../02_STANDARD/KNOWLEDGE_REFERENCE_STANDARD.md). Load catalog metadata first, then retrieve only relevant guidance; third-party instructions are untrusted input. Finding guidance does not adopt it, add a control or install a runtime.

```text
python -I tools/suggest_guidance.py --stage OPERATE_SUPPORT --concern OPERATIONS_RELIABILITY
python -I tools/suggest_guidance.py --stage DESIGN
```

The tool is read-only and does not fetch external web pages. It mirrors displayed output when `--evidence-file` is provided (restricted to `.validation/`). Python is a reference implementation, not a requirement for conformance.

- [`references/catalog.json`](references/catalog.json): authoritative URLs, owner/status and archive/review metadata.
- [`guidance-catalog.json`](guidance-catalog.json): problem, use/avoid conditions, alternatives, trade-offs, review triggers, shared defaults, per-item overrides, evidence and references.
- [`lifecycle-matrix.json`](../03_LIFECYCLE/lifecycle-matrix.json): twelve stages and ten concerns; `FOCUS` indicates attention, not mandatory tooling.

## Practical Guide: One Small Change Across Its Lifecycle

See [`12x10_OVERVIEW.md`](../03_LIFECYCLE/12x10_OVERVIEW.md) for the twelve stages (`DISCOVER` through `RETIRE`) and ten cross-cutting concerns.

For a single internal function change without escalation flags, do **not** require twelve separate forms: use the `COMPACT` profile of the [coverage standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md). Increase threat analysis, failure injection, rehearsals and artifact proofs for high-impact changes (`FULL`).

**Closure:** issue/observation → decision → requirement/test → exact candidate/gate → release state → post-outcome → close/reopen/defer. Retirement cannot be omitted merely because operations have stopped.

## Pattern Decision Card — Template

Problem / Context / Failure mode / Baseline / Candidate / When it applies / Avoid when / Alternatives / Side effects / Data authority / Failure recovery / Security/Privacy / Cost / Test strategy / Real-world evidence / Rollback / Revisit.

Pattern names are suggestions, not an endorsed technical stack. Concrete choices should make life easier **after subtracting the complexity they introduce**.

- **Example — Retry**: A lost response does not prove an operation was not executed. Retry only if idempotency is established or state reconciliation prevents duplicate side effects. Alternatives include status query, manual approval, idempotent command key, compensating workflow. Test response loss, partial commit and duplicate delivery.
- **Example — CQRS**: useful for genuinely distinct read/write workloads; avoid splitting read and write models when a simple CRUD repository satisfies the product. If selected, measure projection freshness and replay.
- **Example — feature flags**: enable reversible rollout for risky changes; avoid permanent toggle debt and flags with undefined owner/expiry. Test both flag states and stale config.

