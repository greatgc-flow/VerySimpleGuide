# Lifecycle and Optional-Reference Governance

General provides a knowledge router and lifecycle review map; the product owner makes scope-local `REQUIRED` decisions.

Every stage and concern has one primary owner; crossreferences may be many. `N_A`/`DEFERRED` require scope, rationale and revisit. Reference metadata captures owner URL, source status, review date, applicability and reconsideration trigger. Sources were reviewed as a dated snapshot and must be rechecked as needed. Observed incidents, vulnerabilities and legal duties may reopen outcome assessments. Operational retirement requires closing relevant data, permissions and residual obligations, not merely stopping a process.

Fifteen baseline Controls are not a hard cap; use versioned evolution if a real unowned concern is proven.

## Lightweight 120-cell review
Decide applicability once for twelve stages and ten concerns (22 items). Combine them only as prompts, then specify exceptions in `cell_overrides` with owner, reason, evidence and revisit. If intersection `PASS` cannot be justified precisely, retain `REQUIRED` or `DEFERRED`. Neither stage PASS nor concern PASS automatically certifies a specific intersection.

See [artifact authority](ARTIFACT_AUTHORITY.md), [package manifest](../MANIFEST.json), and [applicability example](../03_LIFECYCLE/APPLICABILITY_EXAMPLE.md).
