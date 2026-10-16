# Optional Engineering Guidance, Patterns and References

**Goal:** find the smallest relevant guidance, explain its applicability, compare alternatives, test its trade-offs and keep the option to reject it.

```text
python -I tools/suggest_guidance.py --stage OPERATE_SUPPORT --concern OPERATIONS_RELIABILITY
python -I tools/suggest_guidance.py --stage DESIGN
```

The tool is read-only and does not fetch external web pages. It mirrors displayed output when `--evidence-file` is provided (restricted to `.validation/`). Python is a reference implementation, not a requirement for conformance.

- [`references/catalog.json`](references/catalog.json): authoritative URLs, owner/status and archive/review metadata.
- [`guidance-catalog.json`](guidance-catalog.json): problem, use/avoid conditions, shared defaults, per-item overrides, evidence and references.
- [`lifecycle-matrix.json`](../03_LIFECYCLE/lifecycle-matrix.json): twelve stages and ten concerns; `FOCUS` indicates attention, not mandatory tooling.

## Practical Guide: One Small Change Across Its Lifecycle

1. **DISCOVER:** observe the symptom and user/operator impact; seek counterexamples and label inference separately from fact.
2. **ASSESS:** compare retaining, buying, reusing or changing the current solution, including cost and safety.
3. **INITIATE:** define owner, scope, non-goals, constraints and approval authority.
4. **SPECIFY:** set measurable acceptance, failure, null/empty/unknown and observability boundaries.
5. **DESIGN:** prefer the simplest safe plan; document data authority, security, recovery and trade-offs.
6. **IMPLEMENT:** make a small independently testable change in an appropriate language/platform.
7. **VERIFY:** proportionate positive, negative, edge, fault, security, compatibility and reality tests.
8. **RELEASE:** freeze source/candidate/artifact digest, rollout/rollback and operator handover.
9. **OPERATE_SUPPORT:** distinguish user symptoms, logs, traces, support cases, SLOs, costs and risks.
10. **IMPROVE:** connect accepted findings to regression coverage and measured post-release outcomes.
11. **EVOLVE:** review versioning, data migration, dual run and cutover for deprecated dependencies.
12. **RETIRE:** close user notices, replacement paths, lawful retention/deletion, access and residual obligations.

For a single internal function change, do **not** require twelve separate forms. Use `profile: "COMPACT"` or one small change record with applicable stages and explicit `N_A` decisions. Increase threat analysis, failure injection, rehearsals and artifact proofs for high-impact changes.

**Closure:** issue/observation → decision → requirement/test → exact candidate/gate → release state → post-outcome → close/reopen/defer. Retirement cannot be omitted merely because operations have stopped.

## Pattern Decision Card — Template

Problem / Context / Failure mode / Baseline / Candidate / When it applies / Avoid when / Alternatives / Side effects / Data authority / Failure recovery / Security/Privacy / Cost / Test strategy / Real-world evidence / Rollback / Revisit.

Pattern names are suggestions, not an endorsed technical stack. Concrete choices should make life easier **after subtracting the complexity they introduce**.

- **Example — Retry**: A lost response does not prove an operation was not executed. Retry only if idempotency is established or state reconciliation prevents duplicate side effects. Alternatives include status query, manual approval, idempotent command key, compensating workflow. Test response loss, partial commit and duplicate delivery.
- **Example — CQRS**: useful for genuinely distinct read/write workloads; avoid splitting read and write models when a simple CRUD repository satisfies the product. If selected, measure projection freshness and replay.
- **Example — feature flags**: enable reversible rollout for risky changes; avoid permanent toggle debt and flags with undefined owner/expiry. Test both flag states and stale config.

