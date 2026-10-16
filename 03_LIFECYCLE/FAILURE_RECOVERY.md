# Mutation Failure and Recovery

Determine applicability before attaching a mutation contract. Consider idempotency, safe retries, crash boundaries, compensation, duplicate detection, concurrency fences and uncertain execution.

**Execution certainty:** `NOT_STARTED`, `MAY_HAVE_STARTED`, `STARTED`, `TERMINAL`. When the status is `MAY_HAVE_STARTED`, prohibit blind retry until reconciliation or external evidence resolves whether an irreversible effect occurred.

Recovery journals verify plan identity and executed steps. Do not reconstruct a new plan that silently forgets recorded actions and then report success. Distinguish process cancellation, safe compensation and a truly verified terminal outcome.
