# Practical Guide: One Small Change Across Its Lifecycle

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

For a single internal function change, do **not** require twelve separate forms. One small change record with applicable stages and explicit `N_A` decisions is sufficient. Increase threat analysis, failure injection, rehearsals and artifact proofs for high-impact changes.

**Closure:** issue/observation → decision → requirement/test → exact candidate/gate → release state → post-outcome → close/reopen/defer. Retirement cannot be omitted merely because operations have stopped.
