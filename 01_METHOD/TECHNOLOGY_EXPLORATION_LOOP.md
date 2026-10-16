# Technology Scouting and Evidence-Based Innovation Loop

## Loop
`Problem/Opportunity → Scout multiple candidate approaches → Hypothesis → Low-cost spike/simulation/prototype → Baseline comparison → Decision (ADOPT/EXPERIMENT/DEFER/REJECT) → Controlled rollout → Observe cost/quality/safety → Retain/Adapt/Rollback ↺`.

Innovative options must be allowed to enter the loop without an a priori ban on language, OS, database, agent framework, container runtime, deployment paradigm or architecture style.

## Compare *capabilities and trade-offs*, not popularity
Assess fitness, interoperability, latency, throughput, resource consumption, operability, portability, maintainability, security threat model, vendor lock-in, licenses, longevity, staff/skill/toolchain, upgrade path and reversibility where applicable. Excluded dimensions are N_A with evidence. No invented benchmark scores.

Support exploratory non-code experiments, design prototypes, proofs, formal verification, model checking, property/metamorphic tests, scenario simulations, contract tests, fuzzing, replay tests, usability experiments and red/green TDD **as applicable**. Requirement-level verification **MUST** be falsifiable; universal pre-implementation RED is not mandatory for non-code research or exploratory claims. Operational accepted-defect closure may still require documented reproduced failure or an approved exception.

## Decision gates
- ADOPT: exact selected candidate with evidence and rollback; record implementation scope and ownership.
- EXPERIMENT: bounded risk, scope, run budget, exit date/trigger. Never mislabel experiment as stable maturity.
- DEFER: owner and revisit trigger. Unmeasured does not mean rejected.
- REJECT: reproducible reason (security, missing capability, cost, complexity), not a personal language preference.
- RETIRE: measure compatibility and migration burden; do not freeze a legacy technology forever.

## Future-resilience
Periodic technology radar review is **optional and proportionate**, triggered by major release, deprecation, security incident, capability gap, cost spike or architecture review. An always-on monitoring daemon, marketplace, AI auto-upgrader or mandatory trend adoption is not required.
