# Applicability Policy

Every scoped obligation separates three orthogonal dimensions defined in `06_GOVERNANCE/unified-package-standard.json`:
- **Applicability:** `REQUIRED`, `OPTIONAL`, `N_A`
- **Implementation approach:** `COMPLY`, `ADAPT`, `PRODUCT_SPECIFIC`
- **Assessment result:** `NOT_EVALUATED`, `PASS`, `FAIL`

Do not hide missing ownership behind "where applicable", "where practical" or "when feasible" without recording a decision.
- `N_A` requires an explicit `owner`, `reason`, and `revisit_trigger`, and its `result` must remain `NOT_EVALUATED`.
- `ADAPT` requires an explicit `reason` and equivalent contract (`acceptance_criteria`).
- `PASS` requires `acceptance_criteria`, `candidate_identity`, and non-empty `evidence_refs`.
- Deferral (`deferred: true`) requires `owner`, `reason`, and `revisit_trigger`; a deferred item never satisfies a `REQUIRED` obligation and cannot claim `PASS`.
