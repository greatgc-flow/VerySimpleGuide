# Operational Feedback and Closure

Observation enters the [lifecycle backbone](LIFECYCLE_VALUE_STREAM.md) at OPERATE_SUPPORT/IMPROVE and returns to the affected requirement or decision. Preserve observation time, source identity, provenance and evidence; distinguish measured facts from inference.

## Awareness

Keep open observations, decisions and next actions visible to the people who act on them, through a surface the product or team already uses. Review them on a declared cadence or trigger. Any product command that reports this state is read-only [discovery](../02_STANDARD/CLI_STANDARD.md). No specific tool, command grammar, configuration format or label scheme is required.

## Vocabulary

The canonical vocabularies are `feedback_dispositions`, `feedback_statuses` and `feedback_events` in [unified-package-standard.json](../06_GOVERNANCE/unified-package-standard.json):

- Disposition: `PENDING`, `ACCEPT`, `REJECT`, `DEFER`, `DUPLICATE` describes the decision. `PASS` and `N_A` are never dispositions; legacy feature strategy uses its own vocabulary (`RETAIN`, `ABSORB`, `SUPERSEDE`, `EXTRACT_EXTENSION`, `RETIRE`).
- Status: `OPEN`, `IN_PROGRESS`, `CLOSED` describes completion separately.
- Events: `CLOSE`, `REOPEN` preserve immutable history. `REOPEN` returns status to `OPEN` or `IN_PROGRESS`, requires `decision_ref` and `prior_closure_evidence_ref`, and requires `next_action` while the work is open.

## Records and closure

Feedback records link observation, accountable `owner`, priority, rationale and next action. Rejection and duplication need a decision reference; deferral needs a decision, owner and `revisit_trigger`. Review the backlog proportionately; absent telemetry supplies no evidence of zero problems.

Do not silently bury gaps or invent compliance. An exception records its ID, impacted scope, reason, owner, acceptance authority, residual risk, expiry or revisit trigger, alternative safeguard and evidence link where relevant.

Closing accepted work requires linked requirements, reproduced failure or approved exception, passing tests and fresh gates for the exact closure candidate (`closure_candidate_identity`), release evidence (`release_evidence_ref`) and an independently observed post-release outcome (`POST_RELEASE_OUTCOME`) meeting acceptance, or an explicit approved exception (`decision_ref`). Merge or publication alone does not close it. Rejected or duplicate feedback can close through a recorded decision; deferral preserves the revisit obligation. Contradictory outcome evidence reopens the record; observed incidents, vulnerabilities and legal duties may also reopen it.

Schemas and references validate the closure model; product acceptance authority evaluates actual outcomes. Artifact maintainership grants no such authority.
