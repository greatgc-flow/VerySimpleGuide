# Lifecycle Coverage Without Stage-Gate Bureaucracy

1. For each applicable scope, record `REQUIRED`, `OPTIONAL`, `N_A`, `DEFERRED` or `PASS` for logical lifecycle stages (or an equally clear proportionate model).
2. **Reviewed ≠ implemented.** Baseline `FOCUS`/`CONSIDER` cells are prompts, not required technology, documents or implementations.
3. A stage `PASS` needs acceptance criteria and evidence for its scope. `N_A` and `DEFERRED` require reasons, an owner and revisit policy.
4. Minimum trace: goal/scope, primary owner, decision/acceptance, output, normal transition and defect/uncertainty reentry. Secondary cross-Control relationships are allowed without duplicate primary ownership.
5. Legal, regulatory, safety, accessibility, licensing, privacy and industry requirements can strengthen a product's own scoped controls; do not impose the same heavy burden on every project without justification.
6. Retirement checks external dependencies, user migration and notice, backup retention, lawful deletion, access revocation, decommissioning, residual risks and lessons—according to applicability.
7. Maintain `next_stages` and `revisit_stages` and never silently turn a failure into success or assert VERIFIED/PROMOTED without candidate-specific evidence.

The 12 stages × 10 concerns form 120 **review questions**, not 120 required test cases. Their SSOT is [`lifecycle-matrix.json`](../03_LIFECYCLE/lifecycle-matrix.json). The validator can prove coverage references and structure; field outcomes require the project's real evidence.
