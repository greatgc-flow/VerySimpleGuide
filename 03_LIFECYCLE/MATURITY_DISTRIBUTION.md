# Capability Maturity vs Artifact Distribution

**Capability maturity:** `PLANNED → DESIGN_FROZEN → IMPLEMENTING → IMPLEMENTED → VERIFIED → DEPRECATED → RETIRED`.

`VERIFIED` requires fresh passing evidence for every required gate on the **exact candidate**. `QUEUED`, `RUNNING`, `PENDING`, `CANCELLED`, `STALE`, `UNAVAILABLE`, `UNKNOWN` and a required-but-`SKIPPED` gate are not passing blocking outcomes.

**Distribution status:** `NOT_PUBLISHED → CANDIDATE → PUBLISHED → PROMOTED → WITHDRAWN`.

`PUBLISHED` means distributed or publicly available. `PROMOTED` means the verified exact artifact passed required gates and was designated as a stable release. Publication does not prove promotion; do not merge maturity and distribution into one enum.
