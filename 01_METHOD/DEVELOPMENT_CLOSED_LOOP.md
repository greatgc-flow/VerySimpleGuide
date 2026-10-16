# Development Closed Loop

Evidence → Requirement → Decision → Counterexample/RED or equivalent proof → Minimal Implementation → Hardening/Real Environment Proof → Release → Observation/Evaluation → Disposition.

| Stage | Proportionate evidence |
|---|---|
| Evidence | Source/candidate identity, provenance and freshness |
| Requirement | Observable contract, owner and acceptance criteria |
| Decision | Alternatives, trade-offs, applicable exceptions |
| Counterexample / test / proof | For code changes, a failing regression test or suitable counterexample; for research, docs and experiments, a proportionate alternative validation method |
| Implementation | Small independently testable change; no hidden coupling |
| Reality proof | Representative runtime, fault and security checks where relevant |
| Release | Exact candidate identity, gating and rollback |
| Observation | Timestamped measured facts, preserving `UNKNOWN`, `STALE` and `ERROR` |
| Feedback | A tracked disposition returning to requirements and regression coverage |

For omitted activities, record `N_A` or `DEFERRED` with rationale, owner and revisit trigger. A checked document box is not a substitute for actual evidence. See [operational feedback](OPERATIONAL_FEEDBACK_LOOP.md) and [fitness criteria](OBJECTIVE_AND_FITNESS.md).
