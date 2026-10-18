# Lifecycle Value Stream

Solve measurable user problems while reducing lifetime safety, support, transition and maintenance costs. Compare build, buy, reuse and no action before building; planned retirement can be a successful decision. Define outcomes and acceptance authority through [objectives and fitness](OBJECTIVE_AND_FITNESS.md).

The single backbone is [lifecycle-matrix.json](../03_LIFECYCLE/lifecycle-matrix.json): twelve logical stages, ten concerns, normal `next_stages` and uncertainty/failure `revisit_stages`. Stages may overlap and repeat; this is no sequential waterfall. For selected activities use **Outcome → Inputs → Decision/Owner → Outputs/Evidence → Acceptance → Next/Revisit**. Select coverage through the [profile standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md).

Development enters at requirements and design and follows requirement and acceptance → design decision → falsifiable check → minimal implementation → verification → [release](../02_STANDARD/RELEASE_PROMOTION_STANDARD.md) → observation; feedback reenters the affected stage rather than forming a second stage model. For code defects, reproduce the failure or record an approved exception; research, documentation and exploratory work may use a proportionate counterexample, proof, simulation or experiment. Keep changes small enough to review and verify independently.

[Technology exploration](TECHNOLOGY_EXPLORATION_LOOP.md) revisits assessment/design; [operational feedback](OPERATIONAL_FEEDBACK_LOOP.md) enters at observation/improvement and returns to the affected stage. Retirement learning may start new discovery while preserving the closed historical record.

Design coverage, structural checks, negative tests and operational verification are [independent claims](../04_ASSURANCE/ASSURANCE_CASE_AND_NEGATIVE_TEST.md). Lifecycle documentation alone establishes no product outcome. Scale evidence with impact and risk, rather than artifact counts.
