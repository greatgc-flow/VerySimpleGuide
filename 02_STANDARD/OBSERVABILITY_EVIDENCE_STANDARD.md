# Observation, Diagnostics and Evidence Standard

Measurements preserve absence and uncertainty. Recommended vocabulary: `MEASURED`, `ABSENT`, `UNAVAILABLE`, `ERROR`, `STALE`, `UNKNOWN`.

Unknown quota is not unlimited; unknown health is not healthy; and an unknown capability is not supported.

Prefer at least two defenses for read-only diagnostics: read-only/query-only storage mode, no mutating public API or explicit read-only authorizer, and a consistent snapshot per rendered view. Diagnostics do not automatically repair; repair is a separate authorized mutation capability.

Evidence should identify exact source/candidate, time/freshness, provenance, tool/gate, result and a digest when applicable. CLI tools should be able to persist exactly the lines shown to the operator in an evidence file without claiming stronger assurance than was actually executed.

Release identity and assurance: maturity is independent of distribution. Build once and promote the same exact artifact (or frozen target-specific artifact set); required gates must PASS with fresh evidence for that candidate and digest. Pending, unavailable, stale, cancelled or required-but-skipped gates cannot satisfy verification or promotion. A changed candidate requires renewed proof. Tags and publication alone prove no gate result.

MEASURED baselines require evidence. VERIFIED component `verification` reuses the maturity contract and requires declared gate IDs with fresh PASS proof for the exact candidate/digest, observed no later than verification. Canonical version authority is `unified-package-standard.json`; version pins in records are checked against it.

Distribution applies to an exact candidate/artifact identity:

| From | To | Guard |
|---|---|---|
| NOT_PUBLISHED | CANDIDATE | Freeze candidate identity and intended scope. |
| CANDIDATE | PUBLISHED | Authorize distribution; identify remaining limitations. |
| PUBLISHED | PROMOTED | Exact artifact passes all required gates and stable designation is approved. |
| CANDIDATE, PUBLISHED, PROMOTED | WITHDRAWN | Record reason, notice and recovery obligations; candidates may be abandoned before promotion. |
| WITHDRAWN | CANDIDATE | Explicit reinstatement decision; repeat current gates before republication/promotion. |


Other transitions are invalid. The trace `releases` array preserves ordered transitions from NOT_PUBLISHED. Each has a frozen intended `scope`, owner, decision, evidence and time; publication links minimal `changes` (including artifact references) and a dated deployment for that identity. Promotion requires fresh PASS gates before deployment. Withdrawal requires reason, notice and recovery obligations; reinstatement requires renewed gates before republication. Replacement bytes require a new candidate/artifact record. Closing feedback resolves its release ID and binds executed tests, gates, change and deployment to that identity, ordered test → gate → deployment/release → measured outcome. This checks recorded evidence relationships, not the truth of an external run reference.

Feedback history is chronological and alternates CLOSE/REOPEN, preserving the prior closure evidence. CLOSED requires a trailing CLOSE, closure evidence and revisit condition; OPEN or IN_PROGRESS work requires next action. A later target miss for the closure candidate/metric requires reopening or a later CLOSE decision explicitly naming that observation and accepting the exception. A generic decision reference is insufficient. Withdrawal of the closure artifact also requires reopening or a later CLOSE whose decision_ref matches the withdrawal decision and explicitly addresses its effect on this feedback. `--prior-project-trace` compares history prefixes and retained observations, changes, releases and executed test/gate records (including evidence_refs); pending proof may complete, while corrections to executed evidence append new IDs. A single ledger cannot prove historical immutability.

Report executed, skipped and N_A filesystem fixtures separately. Skips never count as executed and prevent NEGATIVE_TESTED=PASS. CI uses `--require-fs-tests` to fail on skipped applicable defenses; local `--no-fs-tests` leaves them unassessed. A junction fixture is N_A off Windows; a Windows symlink privilege denial is N_A when the separate junction defense is applicable.
