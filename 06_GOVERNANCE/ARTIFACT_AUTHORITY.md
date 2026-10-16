# Artifact Authority and Ownership

- `MANIFEST.json` is the sole package file inventory and authority ledger (`path`, `sha256`, `size_bytes`, `role`, `primary_control`, `related_controls`); `MANIFEST.json` is explicitly self-excluded from its own `files` list.
- `sha256` and `size_bytes` in `MANIFEST.json` provide **accidental-change detection** (package integrity), **not** cryptographic provenance or authenticity. Provenance requires an independently trusted external digest or signature.
- `MACHINE_SSOT` owns structured facts; `NORMATIVE_SOURCE` owns contract prose and legal notices; `HUMAN_GUIDE` is explanatory, not a competing state ledger; `GENERATED_VIEW` must match its source generator; `EXAMPLE` demonstrates but never proves actual product behavior; `REFERENCE_CATALOG` is advisory; `ASSURANCE_EVIDENCE` is historic scoped proof; `VALIDATION_TOOL` is reference implementation and workspace tooling.
- `primary_control` identifies the package semantic control domain; related Controls may consume a document without co-ownership. Project `owner` in project records identifies accountable decision authority; artifact maintainership grants no acceptance authority.
- Cached interpreter outputs (`__pycache__`, `.pyc`) and mutable `.validation` output are not canonical package artifacts; validators must remain deterministic on re-run.
