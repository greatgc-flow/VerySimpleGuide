# Operational Feedback and Closure

Observation enters the [lifecycle backbone](LIFECYCLE_VALUE_STREAM.md) at OPERATE_SUPPORT/IMPROVE and returns to the affected requirement or decision. Preserve observation time, source identity, provenance and evidence; distinguish measured facts from inference.

The canonical vocabularies are `feedback_dispositions`, `feedback_statuses` and `feedback_events` in [unified-package-standard.json](../06_GOVERNANCE/unified-package-standard.json):

- Disposition: `PENDING`, `ACCEPT`, `REJECT`, `DEFER`, `DUPLICATE` describes the decision.
- Status: `OPEN`, `IN_PROGRESS`, `CLOSED` describes completion separately.
- Events: `CLOSE`, `REOPEN` preserve immutable history. `REOPEN` returns status to `OPEN`, retains prior closure evidence and requires `next_action` plus `decision_ref`.

Feedback records link observation, accountable `owner`, priority, rationale and next action. Rejection and duplication need a decision reference; deferral needs a decision, owner and `revisit_trigger`. Review the backlog proportionately; absent telemetry supplies no evidence of zero problems.

Closing accepted work requires linked requirements, reproduced failure or approved exception, passing tests and fresh gates for the exact closure candidate, release evidence and an observed outcome meeting acceptance (or explicit approved risk acceptance). Merge or publication alone does not close it. Rejected or duplicate feedback can close through a recorded decision; deferral preserves the revisit obligation. Contradictory outcome evidence reopens the record.

Schemas and references validate the closure model; product acceptance authority evaluates actual outcomes. Artifact maintainership grants no such authority.
