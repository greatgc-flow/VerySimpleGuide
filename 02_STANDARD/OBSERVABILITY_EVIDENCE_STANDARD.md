# Observation, Diagnostics and Evidence Standard

Measurements preserve absence and uncertainty. Recommended vocabulary: `MEASURED`, `ABSENT`, `UNAVAILABLE`, `ERROR`, `STALE`, `UNKNOWN`.

Unknown quota is not unlimited; unknown health is not healthy; and an unknown capability is not supported.

Prefer at least two defenses for read-only diagnostics: read-only/query-only storage mode, no mutating public API or explicit read-only authorizer, and a consistent snapshot per rendered view. Diagnostics do not automatically repair; repair is a separate authorized mutation capability.

Evidence should identify exact source/candidate, time/freshness, provenance, tool/gate, result and a digest when applicable. CLI tools should be able to persist exactly the lines shown to the operator in an evidence file without claiming stronger assurance than was actually executed.

MEASURED baselines require evidence. Canonical version authority is `unified-package-standard.json`; version pins in records are checked against it. Release identity, gate freshness and distribution transitions live in the [release and promotion standard](RELEASE_PROMOTION_STANDARD.md).

Feedback history is chronological and alternates CLOSE/REOPEN, preserving the prior closure evidence. CLOSED requires a trailing CLOSE, closure evidence and revisit condition; OPEN or IN_PROGRESS work requires next action. A later target miss for the closure candidate/metric requires reopening or a later CLOSE decision explicitly naming that observation and accepting the exception. A generic decision reference is insufficient. Withdrawal of the closure artifact also requires reopening or a later CLOSE whose decision_ref matches the withdrawal decision and explicitly addresses its effect on this feedback. `--prior-project-trace` compares history prefixes and retained observations, changes, releases and executed test/gate records (including evidence_refs); pending proof may complete, while corrections to executed evidence append new IDs. A single ledger cannot prove historical immutability.

Report executed, skipped and N_A filesystem fixtures separately. Skips never count as executed and prevent NEGATIVE_TESTED=PASS. CI uses `--require-fs-tests` to fail on skipped applicable defenses; local `--no-fs-tests` leaves them unassessed. A junction fixture is N_A off Windows; a Windows symlink privilege denial is N_A when the separate junction defense is applicable.
