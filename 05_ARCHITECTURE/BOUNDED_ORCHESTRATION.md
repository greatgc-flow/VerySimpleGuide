# Routing, Orchestration and Approval

**Routing selects; it does not execute.** Inputs include declared capabilities, measured observations, evaluation evidence and policy. Prefer reproducible deterministic filters, tie-breaks and admission rules initially; AI recommendation is an optional advisor whose claims require separate measurement.

**Orchestration executes accepted bounded plans**. Define `max_depth`, `max_steps`, `max_fanout`, `max_attempts`, `deadline` and applicable budgets such as time, calls, tokens, artifacts or concurrency. Do not automatically introduce a workflow language, BPMN or generic scheduler.

**Approval** should be tied to the exact prospective side-effect digest and consumed once by default. Quorum, voting and leader election are optional extensions justified by use cases and separate security analysis.
