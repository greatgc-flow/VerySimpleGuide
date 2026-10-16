# Projection and Retrieval Freshness Standard

A rebuildable index, search projection or query view should state **which authoritative point-in-time** it includes. Recommended metadata includes `source_ref`, `source_type`, `projection_generation` or `index_generation`, `source_watermark`, `retrieval_method`, `score` and `score_semantics`.

Never hide a stale index. A search relevance score is **not** truth confidence. Reproduction and determinism follow [Authority and Projection](AUTHORITY_PROJECTION_STANDARD.md).
