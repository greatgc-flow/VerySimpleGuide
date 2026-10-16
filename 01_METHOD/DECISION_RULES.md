# Decision Rules

1. For uncertain behavior, prefer explicit options, policies and schemas over hardcoding.
2. Distinguish missing, `null`, empty string, empty array and `UNKNOWN`.
3. Introduce bespoke generic frameworks when repeated consumer evidence or a strong documented reason justifies them; the "rule of three" is a heuristic, not a ban on experimentation.
4. The existence of a legacy feature does not automatically justify rebuilding it.
5. Do not force legacy command syntax, numeric exit codes or physical layout symmetry when the compatibility cost exceeds the benefit.
6. Do not rename public interfaces solely for aesthetics.
7. Keep external-system identity and status distinct from internal source-of-truth state; use opaque handles and evidence mappings.
8. Do not turn missing observations into a fabricated zero, infinity or success.
9. AI- or heuristic-derived statements are hypotheses or derived assessments, never original evidence.
10. Fail safely and transparently; do not report success when the effect is uncertain.
11. Language, OS, runtime, database and CI selection belong to the project's scope. The reference validator is not the sole path to conformity.
12. Separate binding invariants from overridable defaults. Document exceptions and proof under [open technology principles](OPEN_TECHNOLOGY_PRINCIPLES.md).
13. Allow bounded spikes, benchmarks and rollback in [technology exploration](TECHNOLOGY_EXPLORATION_LOOP.md).

Durable cross-domain lessons are organized by [authority and projection](../02_STANDARD/AUTHORITY_PROJECTION_STANDARD.md), [component boundaries](../02_STANDARD/COMPONENT_BOUNDARY.md), [observation and evidence](../02_STANDARD/OBSERVABILITY_EVIDENCE_STANDARD.md), [external identities](../02_STANDARD/PROTOCOL_ADAPTER_STANDARD.md), [bounded orchestration](../05_ARCHITECTURE/BOUNDED_ORCHESTRATION.md), [state recovery](../02_STANDARD/DATA_SAFETY_STANDARD.md) and [release identity](../03_LIFECYCLE/RELEASE_PROMOTION.md). Reuse those contracts instead of preserving product-specific implementation histories.
