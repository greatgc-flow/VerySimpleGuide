# Historical R9 Audit — Objective, Closure and Recursive MECE

The independent subject was R8 / Standard 1.3.0 documents, schemas, samples and actual validator behavior. Written claims were not promoted to tested behavior.

| Dimension | R8 finding | R9 correction | Proof level |
|---|---|---|---|
| User outcome | Goals, costs and measurable acceptance were weakly connected | Objective/fitness ownership and success signals | Design/sample |
| Feedback loop | Mostly a Feedback → Requirement arrow | Observation → Disposition → Requirement/Test/Gate → Post-outcome links | Referential checks and negative tests |
| Recursive MECE | Cross-document links not machine-checked | Unique owner and obligation map across baseline Controls | Design coverage |
| Maturity | Conditional VERIFIED schema allowed empty evidence | Candidate, timestamp and proof required | Negative schema tests |
| Gate | PASS could lack digest or real evidence | Fresh PASS and candidate digest required | Contract and crossref |
| Validator | Focused on inventory, not JSON schemas | Draft 2020-12 schema, integrity, crossrefs and negative tests | Static artifact assurance |
| Evidence | Current run logs confused with frozen release evidence | Separate immutable baseline proof and current evidence output | Reproducible tooling |
| Minimality | Fifteen baseline Controls were sufficient | Retained Controls; resisted speculative frameworks | Design consistency |

**Vertical closure:** objective/measure → observation/feedback → requirement/decision → counterexample or RED → implementation → gate → release → measured post-outcome → closure/reopen. The validator demonstrates the sample's internal relationships; it does not validate real field telemetry or provider execution.

**Horizontal closure:** retain the eight orthogonal classification axes. Objective, evidence and feedback form a separate assurance relationship rather than additional component classes.

**Deliberately outside scope:** real provider/OS evidence; actual whole-project requirement/test/code/deployment graphs; human risk acceptance; concurrency, antivirus/locked-file and production crash reproduction.

**Conclusion:** R9 establishes a consistent general design, schemas and validation example. It cannot claim all products are operationally verified. Reducing missing links, false success and orphaned feedback is more valuable than expanding framework size. A subsequent audit mapped baseline Invariants to exactly one primary owner, a standard and a scoped verification obligation.
