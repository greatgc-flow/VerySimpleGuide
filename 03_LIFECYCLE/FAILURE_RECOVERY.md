# Mutation Failure and Recovery

Determine applicability before attaching a mutation contract. Consider idempotency, safe retries, crash boundaries, compensation, duplicate detection, concurrency fences and uncertain execution.

**Execution certainty:** `NOT_STARTED`, `MAY_HAVE_STARTED`, `STARTED`, `TERMINAL`. When the status is `MAY_HAVE_STARTED`, prohibit blind retry until reconciliation or external evidence resolves whether an irreversible effect occurred.

Recovery-journal rules live in the [data safety standard](../02_STANDARD/DATA_SAFETY_STANDARD.md).

Commit points and residual-resource ownership: see the [data safety standard](../02_STANDARD/DATA_SAFETY_STANDARD.md).
