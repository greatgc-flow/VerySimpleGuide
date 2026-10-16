# Development Within the Lifecycle

Use the [lifecycle backbone](LIFECYCLE_VALUE_STREAM.md): requirement and acceptance → design decision → falsifiable check → minimal implementation → verification → release → observation. Feedback reenters the affected stage; this is not a second stage model.

For code defects, reproduce the failure or record an approved exception. Research, documentation and exploratory work may use a proportionate counterexample, proof, simulation or experiment; see [traceability](../04_ASSURANCE/TDD_TRACEABILITY.md). Keep changes small enough to review and verify independently.

Record applicability, approach and result separately under the [coverage standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md). Release gates belong to [release and promotion](../03_LIFECYCLE/RELEASE_PROMOTION.md); closure and reopening belong to [operational feedback](OPERATIONAL_FEEDBACK_LOOP.md).
