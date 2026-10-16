# A Small Applicability Record

Select a profile using the [coverage standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md); use [project-lifecycle.example.json](../07_CONTRACTS/examples/project-lifecycle.example.json) for the exact serialization. The matrix's 120 prompts are not 120 approvals or tests.

For example, a required design/security assessment awaiting a threat-model review has `applicability: REQUIRED`, `approach: COMPLY`, `result: NOT_EVALUATED`, `deferred: true`, a named `owner`, `reason` and `revisit_trigger`. It remains unsatisfied. If this intersection differs from its stage/concern records, use a sparse `cell_overrides` entry.

After actual assessment, a PASS needs acceptance criteria, candidate identity and evidence for that scope. Broad stage/concern success supplies no automatic cell result; sample evidence supplies no product verification.
