# Authority and Projection Standard

The default data flow is **immutable/ordered authority → declared reducer or projection → disposable query view**.

- An authoritative blob or event must exist and be verified before a durable reference to it becomes visible.
- A projection, cache or search index declared `REBUILDABLE` must be recreatable from the specified authoritative source and snapshot under declared equivalence criteria. Bit-for-bit determinism is required only when the product promises it.
- A projection database must not silently become the original source of truth.
- Separate a mutation request and its evidence from a successfully committed state transition. A reducer or transition validator may reject invalid input.

**Artifact sequence:** stage → digest → verify → durable blob commit → metadata commit → durable reference append. The reference cannot become durable before its blob.

**Durable-derived material:** accepted or user-approved derived knowledge can be `DURABLE_DERIVED`, but must retain source provenance and must not overwrite the original authoritative record.

**Freshness:** a rebuildable index, search projection or query view should state which authoritative point-in-time it includes. Recommended metadata includes `source_ref`, `source_type`, `projection_generation` or `index_generation`, `source_watermark`, `retrieval_method`, `score` and `score_semantics`. Never hide a stale index. A search relevance score is not truth confidence.
