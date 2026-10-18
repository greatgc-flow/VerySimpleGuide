# Release and Promotion Standard

Follow source candidate → identity freeze → build → gates → evidence index → promotion. Maturity is independent of distribution: publication proves availability, while gates prove scoped verification.

Build once and promote the same exact artifact (or frozen target-specific artifact set); required gates must PASS with fresh evidence for that candidate and digest. Pending, unavailable, stale, cancelled or required-but-skipped gates cannot satisfy verification or promotion. A changed candidate requires renewed proof. Tags and publication alone prove no gate result.

VERIFIED component `verification` reuses the maturity contract and requires declared gate IDs with fresh PASS proof for the exact candidate/digest, observed no later than verification.

Distribution applies to an exact candidate/artifact identity:

| From | To | Guard |
|---|---|---|
| NOT_PUBLISHED | CANDIDATE | Freeze candidate identity and intended scope. |
| CANDIDATE | PUBLISHED | Authorize distribution; identify remaining limitations. |
| PUBLISHED | PROMOTED | Exact artifact passes all required gates and stable designation is approved. |
| CANDIDATE, PUBLISHED, PROMOTED | WITHDRAWN | Record reason, notice and recovery obligations; candidates may be abandoned before promotion. |
| WITHDRAWN | CANDIDATE | Explicit reinstatement decision; repeat current gates before republication/promotion. |

Other transitions are invalid. The trace `releases` array preserves ordered transitions from NOT_PUBLISHED. Each has a frozen intended `scope`, owner, decision, evidence and time; publication links minimal `changes` (including artifact references) and a dated deployment for that identity. Promotion requires fresh PASS gates before deployment. Withdrawal requires reason, notice and recovery obligations; reinstatement requires renewed gates before republication. Replacement bytes require a new candidate/artifact record that preserves its predecessor's history.

Closing feedback resolves its release ID and binds executed tests, gates, change and deployment to that identity, ordered test → gate → deployment/release → measured outcome. This checks recorded evidence relationships, not the truth of an external run reference. Feedback history and reopening follow [observation and evidence](OBSERVABILITY_EVIDENCE_STANDARD.md).
