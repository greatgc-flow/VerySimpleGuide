# Cross-domain Lessons Generalized

This historical audit records how lessons from different system categories were elevated to product-neutral semantics, without importing vendor-specific implementations.

## Durable collaboration systems
- Separate authoritative records from read projections.
- Commit immutable artifacts with digest verification before durable reference publication.
- Make diagnostics read-only and preserve observed uncertainty.
- Separate routing (selection) from orchestration (execution) and bound plans.
- Preserve external protocol identities separately from internal domain IDs.
- Treat capability declarations separately from measured outcomes.
- Treat public CLI cutover and rollback as an independently tested migration.

## Portable lifecycle systems
- Distinguish Core kernel, required Modules and Optional Extensions; built-in does not mean Core.
- Discover provider capabilities instead of hardcoding platform-specific branches.
- Test Core-only survival when extensions are missing or broken.
- Base backup, restore and reset behavior on state ownership and recovery classification.
- Gate the exact release candidate in real environments; build once and promote the same artifact.
- Distinguish delivery harnesses from end-user provider extensions.

**Conclusion:** the largest simplification came from separating **authority, boundary, evidence and lifecycle**, rather than growing feature catalogs. General standardizes shared meanings, not implementations.
