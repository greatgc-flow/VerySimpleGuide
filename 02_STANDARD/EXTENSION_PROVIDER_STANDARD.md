# Extension, Provider, Adapter and Exporter Standard

Component class and boundary role are **orthogonal**:
- `NONE`: no external boundary role.
- `ADAPTER`: maps an external protocol or model to an internal contract.
- `PROVIDER`: supplies execution environment or capabilities.
- `EXPORTER`: emits telemetry, evidence or internal events to another format/system.

A minimal extension manifest declares `id`, `version`, `component_class`, `required_scopes`, `boundary_roles`, `capabilities`, optional `config_schema_ref`, and `state_ownership`. Add entry points, migrations and failure-isolation machinery only as a product needs them.

## Framework restraint
Do **not** default to a bespoke plugin marketplace, dependency resolver, hot reload or generic extension host. Multiple real consumers with shared invariants justify reevaluation; two or three examples are a heuristic, not a hard threshold. A mature interoperability standard or high-value bounded experiment may justify an earlier adoption.

**Failure isolation ≠ security sandbox:** catching an extension error does not isolate malicious code from host memory or filesystem.

Prefer a small optional lifecycle interface such as `describe`, `health`, `plan(action)`, `execute(action)`. Avoid proliferating unconditional `before_*`/`after_*` hooks. Built-in optional extensions may be enabled by declarative configuration without supporting third-party marketplace installation.
