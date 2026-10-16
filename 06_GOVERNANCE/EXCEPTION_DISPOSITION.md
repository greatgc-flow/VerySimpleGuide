# Exception and Disposition

Do not silently bury gaps or invent compliance. Record exception ID, impacted scope, reason, owner, acceptance authority, residual risk, expiry or revisit trigger, alternative safeguard and evidence link where relevant.

Feedback and exception records separate **disposition** (`PENDING`, `ACCEPT`, `REJECT`, `DEFER`, `DUPLICATE`), **completion status** (`OPEN`, `IN_PROGRESS`, `CLOSED`), and **history events** (`CLOSE`, `REOPEN`):
- Closing an `ACCEPT` item requires the exact release (`closure_candidate_identity`, `release_evidence_ref`) and independently observed post-release outcome (`POST_RELEASE_OUTCOME`), or an explicit approved exception (`decision_ref`).
- `REOPEN` is an immutable history event that returns `status` to `OPEN`, preserves prior closure evidence (`prior_closure_evidence_ref`), and requires `next_action` and `decision_ref`.
- Legacy feature lifecycle strategy uses a separate vocabulary (`RETAIN`, `ABSORB`, `SUPERSEDE`, `EXTRACT_EXTENSION`, `RETIRE`); `PASS` and `N_A` are never valid dispositions.
