# Lifecycle and Optional-Reference Governance

General provides a knowledge router and lifecycle review map; the accountable project `owner` makes scope-local applicability decisions. `primary_control` in package matrices identifies the package semantic control domain; artifact maintainership grants no product acceptance authority.

Every stage and concern has one primary control domain; cross-references may be many (`stage.id` must be listed in `sources[reference_id].stages`). `N_A` and `deferred: true` require owner, rationale and revisit trigger. Reference metadata captures owner URL, source status, review date, stage applicability and reconsideration trigger. Sources were reviewed as a dated snapshot and must be rechecked as needed. Observed incidents, vulnerabilities and legal duties may reopen outcome assessments via an immutable `REOPEN` event. Operational retirement requires closing relevant data, permissions and residual obligations, not merely stopping a process.

Fifteen baseline Controls are not a hard cap; use versioned evolution if a real unowned concern is proven.

## Proportionate profiles (`COMPACT` vs `FULL`) and sparse `cell_overrides`
Projects must explicitly select `"profile": "COMPACT"` or `"profile": "FULL"` alongside boolean `escalation_flags`, `activity_flags`, and `exposure_flags`:
- `COMPACT` is permitted only when all four `escalation_flags` (`public_contract_change`, `authoritative_data`, `security_boundary`, `external_dependency`) are `false`. It requires the baseline mandatory stages (`SPECIFY`, `DESIGN`, `VERIFY`) and concerns (`OUTCOME_VALUE`, `RISK_SECURITY`, `QUALITY_ASSURANCE`, `GOVERNANCE_EVIDENCE`), plus any stage or concern activated by `activity_flags` or `exposure_flags` in `03_LIFECYCLE/lifecycle-matrix.json`. Omitted entries in `COMPACT` are unassessed (never `N_A` and never `PASS`).
- `FULL` (required whenever any escalation flag is `true`) requires explicit applicability decisions for all 12 stages and 10 concerns (22 items, not 120 cells), with intersection-specific exceptions recorded only in sparse `cell_overrides`. Neither stage `PASS` nor concern `PASS` automatically certifies a specific intersection.

See [artifact authority](ARTIFACT_AUTHORITY.md), [package manifest](../MANIFEST.json), and [applicability example](../03_LIFECYCLE/APPLICABILITY_EXAMPLE.md).
