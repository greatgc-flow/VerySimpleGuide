# Search, Memory and Context

- A search index is a `REBUILDABLE` projection, not authoritative source content.
- Search scores represent relevance, not truth confidence.
- Accepted durable memories are `DURABLE_DERIVED` and must retain source references.
- Derived memory never overwrites original source evidence; supersede/revoke events preserve history.
- A context pack is a bounded `EPHEMERAL` projection for a particular work session.
- Procedures are Skill/Instruction assets; volatile observed facts belong to Observation.
- Knowledge graphs, ontologies and automatic memory rewriting are optional advanced extensions.

**Memory acceptance:** source → candidate → explicit policy or owner acceptance → durable derived memory. Keep statuses small, e.g. `CANDIDATE`, `ACCEPTED`, `SUPERSEDED`, `REJECTED`, `REVOKED`. Do not silently promote an AI summary or search snippet into permanent truth.
