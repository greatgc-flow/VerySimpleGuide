# Artifact authority and ownership (R12)

- Hash Manifest/Checksums track **bytes and package inventory**, not normative authority.
- `06_GOVERNANCE/artifact-ownership.json` tracks one primary Control and document role **for each packaged source artifact**; its own entry is included. This is an index, not a replacement for content-level SSOT.
- `MACHINE_SSOT` owns structured facts; `NORMATIVE_SOURCE` owns contract prose; `HUMAN_GUIDE` is explanatory, not a competing state ledger; `GENERATED_VIEW` must match its source generator; `EXAMPLE` demonstrates but never proves actual product behavior; `REFERENCE_CATALOG` is advisory; `ASSURANCE_EVIDENCE` is historic scoped proof; `VALIDATION_TOOL` is reference implementation.
- Related Controls may consume a document. A reference is **not** co-ownership. Artifacts may concern multiple lifecycle stages but always have one package owner; project-specific accountability is separate.
- Cached interpreter outputs (`__pycache__`, `.pyc`) and mutable `.validation` output are not canonical package artifacts; validators must remain deterministic on re-run.
- R12 packages include historic audit reports as `ASSURANCE_EVIDENCE`. Historic statuses do not supersede this version's live validation result.
