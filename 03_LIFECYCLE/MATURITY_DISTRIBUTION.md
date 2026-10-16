# Capability Maturity and Artifact Distribution

Capability maturity is `PLANNED → DESIGN_FROZEN → IMPLEMENTING → IMPLEMENTED → VERIFIED → DEPRECATED → RETIRED`. VERIFIED requires fresh passing gates for the exact candidate; later changes require renewed verification. Pending, stale, unavailable, cancelled or required-but-skipped gates cannot satisfy it.

Distribution is separate and applies to an exact artifact identity:

| From | To | Guard |
|---|---|---|
| NOT_PUBLISHED | CANDIDATE | Freeze candidate identity and intended scope. |
| CANDIDATE | PUBLISHED | Authorize distribution; identify remaining limitations. |
| PUBLISHED | PROMOTED | Exact artifact passes all required gates and stable designation is approved. |
| CANDIDATE, PUBLISHED, PROMOTED | WITHDRAWN | Record reason, notice and recovery obligations; candidates may be abandoned before promotion. |
| WITHDRAWN | CANDIDATE | Explicit reinstatement decision; repeat current gates before republication/promotion. |

Other transitions are invalid. Replacement bytes create a new artifact identity and distribution record, preserving the withdrawn history. Publication proves availability, not verification; [release rules](RELEASE_PROMOTION.md) govern promotion.
