# Pattern decision card — template

Problem / Context / Failure mode / Baseline / Candidate / When it applies / Avoid when / Alternatives / Side effects / Data authority / Failure recovery / Security/Privacy / Cost / Test strategy / Real-world evidence / Rollback / Revisit.

Pattern names are suggestions, not an endorsed technical stack. Concrete choices should make life easier **after subtracting the complexity they introduce**.

**Example — Retry**: A lost response does not prove an operation was not executed. Retry only if idempotency is established or state reconciliation prevents duplicate side effects. Alternatives include status query, manual approval, idempotent command key, compensating workflow. Test response loss, partial commit and duplicate delivery.

**Example — CQRS**: useful for genuinely distinct read/write workloads; avoid splitting read and write models when a simple CRUD repository satisfies the product. If selected, measure projection freshness and replay.

**Example — feature flags**: enable reversible rollout for risky changes; avoid permanent toggle debt and flags with undefined owner/expiry. Test both flag states and stale config.
