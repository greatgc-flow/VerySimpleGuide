# Lifecycle 12×10 overview (GENERATED FROM MACHINE SSOT)

FOCUS = a review priority in this stage; CONSIDER = assess applicability for the product. Neither requires installing a technology or producing an artifact.

| Stage | Objective | Output | Exit decision | Primary control | Next / Revisit | OUTCOME_VALUE | USERS_ACCESSIBILITY | RISK_SECURITY | ARCHITECTURE_DEPENDENCIES | DATA_PRIVACY | QUALITY_ASSURANCE | RELEASE_SUPPLYCHAIN | OPERATIONS_RELIABILITY | ECONOMICS_SUSTAINABILITY | GOVERNANCE_EVIDENCE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DISCOVER | Determine whether a problem is worth solving and describe measurable user outcomes. | Problem brief + baseline hypothesis | continue / stop / research further | UPS-DOC | ASSESS / DISCOVER | **F** | **F** | · | · | · | · | · | · | **F** | · |
| ASSESS | Compare build, buy, reuse and no-action options, including operating costs. | Options and feasibility decision | build / buy / reuse / no-go | UPS-COMP | INITIATE / DISCOVER | **F** | · | **F** | **F** | · | · | · | · | **F** | · |
| INITIATE | Define outcome owners, scope, risk and acceptance authority. | Charter + scope + owners + acceptance | fund / defer / stop | UPS-DOC | SPECIFY / DISCOVER, ASSESS | **F** | · | **F** | · | · | · | · | · | · | **F** |
| SPECIFY | Describe user, quality, data and security requirements in verifiable form. | Requirements + acceptance + non-goals | approve / revise | UPS-TEST | DESIGN / INITIATE | **F** | **F** | **F** | · | **F** | **F** | · | · | · | · |
| DESIGN | Explore boundaries, alternatives, failure modes, recovery and trade-offs. | Architecture decision + threat/data model | freeze for increment / experiment | UPS-COMP | IMPLEMENT / SPECIFY, ASSESS | · | · | **F** | **F** | **F** | · | · | **F** | · | · |
| IMPLEMENT | Create minimum maintainable changes with reproducible inputs and reviewable tests. | Change set + reproducible build input | ready for independent verification / redo | UPS-TEST | VERIFY / DESIGN | · | · | · | **F** | · | **F** | **F** | · | · | · |
| VERIFY | Test the exact candidate under representative negative, edge, fault, security and compatibility cases. | Evidence + acceptance decision + known risks | promote candidate / hold / rework | UPS-TEST | RELEASE / IMPLEMENT, DESIGN | · | **F** | **F** | · | · | **F** | · | · | · | **F** |
| RELEASE | Deliver the verified candidate with rollback and operator handover. | Artifact digest + release evidence + runbook | release / rollback / hold | UPS-REL | OPERATE_SUPPORT / VERIFY | · | · | · | · | · | · | **F** | **F** | · | **F** |
| OPERATE_SUPPORT | Observe user impact, reliability, incidents, cost, support and risk. | Observations + incidents + support + cost | continue / mitigate / improve / sunset | UPS-OBS | IMPROVE, EVOLVE, RETIRE / RELEASE | · | **F** | **F** | · | **F** | · | · | **F** | **F** | · |
| IMPROVE | Convert production feedback into regression coverage and measured post-release outcomes. | Disposition + changed requirement + post-outcome | adopt / defer / reject / reopen | UPS-EVID | SPECIFY, DESIGN, IMPLEMENT, OPERATE_SUPPORT, EVOLVE / OPERATE_SUPPORT | **F** | · | · | · | · | **F** | · | **F** | · | **F** |
| EVOLVE | Control compatibility, data migration, replacement and end-of-support changes. | Migration/cutover plan + rollback + compatibility evidence | transition / maintain / retire | UPS-MIG | DESIGN, VERIFY, RELEASE, RETIRE / ASSESS, OPERATE_SUPPORT | · | · | · | **F** | **F** | · | **F** | **F** | · | · |
| RETIRE | Close user notices, migration, retention, access revocation and remaining obligations. | Retirement evidence + access revocation + data disposition | close with evidence / reopen obligation | UPS-MIG | DISCOVER / OPERATE_SUPPORT, EVOLVE | · | **F** | **F** | · | **F** | · | · | · | **F** | **F** |

For owner/ref details use `lifecycle-matrix.json` (not this generated view).
