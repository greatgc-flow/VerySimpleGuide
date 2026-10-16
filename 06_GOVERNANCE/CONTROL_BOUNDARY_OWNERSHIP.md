# Control Boundaries and Primary Ownership

The 15 shared Controls are a practical baseline, not a permanent maximum. Evidence of an unowned concern may justify a versioned addition, split or merge through governance. For a new requirement, first identify its appropriate existing owner's scope and verification obligation.

- `UPS-COMP`: component class, required scope and dependency direction.
- `UPS-EXT`: extension, adapter, provider and exporter public-port contract.
- `UPS-LAYOUT`: authority, recovery class and data-safety policy.
- `UPS-SCHEMA`: current version/shape; `UPS-MIG`: A→B transition, rollback and cutover.
- `UPS-OBS`: measured fact and diagnostic/repair separation; `UPS-EVID`: evidence identity, provenance and format.
- `UPS-TEST`: requirements, negative cases and reality-gate verification method.
- `UPS-REL`: exact-candidate gates and promotion of identical artifacts.
- `UPS-DOC`: canonical SSOT and generated/human view consistency.

A shared concern has **exactly one primary owner** and may list related Controls. Multiple references do not create multiple authoritative sources. `control-coverage.json` checks mappings and obligations. `invariant-coverage.json` maps baseline invariants to one primary Control and an explicit product-level verification obligation. `DESIGN_COVERED` does not mean an actual product passed its gates.
