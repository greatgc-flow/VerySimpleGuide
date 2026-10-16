# Observation, Diagnostics and Evidence Standard

Measurements preserve absence and uncertainty. Recommended vocabulary: `MEASURED`, `ABSENT`, `UNAVAILABLE`, `ERROR`, `STALE`, `UNKNOWN`.

Unknown quota is not unlimited; unknown health is not healthy; and an unknown capability is not supported.

Prefer at least two defenses for read-only diagnostics: read-only/query-only storage mode, no mutating public API or explicit read-only authorizer, and a consistent snapshot per rendered view. Diagnostics do not automatically repair; repair is a separate authorized mutation capability.

Evidence should identify exact source/candidate, time/freshness, provenance, tool/gate, result and a digest when applicable. CLI tools should be able to persist exactly the lines shown to the operator in an evidence file without claiming stronger assurance than was actually executed.
