# Operational Closed-Loop Contract

Observation → Feedback → Disposition → Requirement/Decision → Counterexample or approved exception → Exact-candidate gate → Deployment → Post-outcome → CLOSE / REOPEN.

This complements the development loop with explicit operational entry and exit rules:

1. Every observation has an observation time, source identity, provenance and evidence reference. AI inference must be differentiated from measured fact.
2. Feedback carries the observation link, owner, impacted scope, priority, next action and review date. Use a deduplication key where recurring failures warrant it.
3. Record `ACCEPT`, `REJECT`, `DEFER` or `DUPLICATE`. Rejections require rationale and authority; deferrals require ownership and a revisit trigger. Do not silently delete findings.
4. Accepted findings link to requirement/decision IDs, a regression or failing counterexample and implementation/gate evidence. If this is impossible, record a scoped risk exception.
5. Merge and public release alone do not close the issue: require fresh gate evidence for the exact candidate and an observed result meeting the objective, or approved risk acceptance.
6. Contradicting post-outcome evidence produces a new `REOPEN` event; preserve the original immutable closure history.
7. No-deployment paths (e.g. `REJECT`, `DEFER`) can be valid dispositions when the decision, owner and revisit policy are recorded.
8. Review backlogs proportionately by impact and risk. Absence of telemetry means `NO_EVIDENCE`, not proof of zero problems.

**Design closure** is a verified model of states, evidence and transitions; **operational closure** requires real source observations through measurable post-release outcomes for a specific product. This package establishes the former, not the latter.
