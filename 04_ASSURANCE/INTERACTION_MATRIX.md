# Required Interaction Matrix

Individually passing features can fail when combined. Select these interactions by risk, record applicability separately from evidence result, and track postponement under the [coverage standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md):

- Authority × projection loss/rebuild; mutation × concurrency; mutation × crash/restart.
- Retry × uncertain `MAY_HAVE_STARTED`; extension × broken/disabled extension.
- Provider × unavailable capability; observation × `UNKNOWN`/`STALE`.
- Backup × active writer; restore × stale process or generation.
- Adapter × protocol-version mismatch; external artifact × unavailable/tampered source.
- Routing × unknown quota/health; orchestration × budget/deadline.
- Approval × changed effect digest or duplicate use; exporter × unavailable destination.
- Public cutover × legacy automation and integration contract.

Scale the matrix with applicability and risk; it is not an unconditional instruction to implement every possible pair.
