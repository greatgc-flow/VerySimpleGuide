# Unified Package Standard 1.9.1

Applicable semantic responsibilities are binding; organizing them as fifteen controls is a default under [open technology principles](../01_METHOD/OPEN_TECHNOLOGY_PRINCIPLES.md). `primary_control` identifies the package semantic control domain; project `owner` identifies accountable decision authority. Artifact maintainership grants no acceptance authority. Discovery/funding mappings assign document/control responsibility, not business authority.

| ID | Control | Semantic ownership |
|---|---|---|
| UPS-CLI | CLI / Interface | Public behavioral contracts; CLI grammar/flags only for CLI surfaces |
| UPS-HELP | Help / Discoverability | Read-only help, discovery and generated-view consistency |
| UPS-EXIT | Exit Semantics | Semantic exit classes; numeric codes may be product-specific |
| UPS-CONFIG | Configuration | Precedence, merge and null/empty/unknown behavior |
| UPS-LAYOUT | State / Filesystem | State kinds, authority, recovery classes and data-safety policy |
| UPS-SCHEMA | Schema / Version | Current data contract and version compatibility |
| UPS-COMP | Component Boundary | Classes, required scopes and dependency ownership |
| UPS-EXT | Extension / Boundary | Public adapter, provider and exporter ports |
| UPS-OBS | Observation / Diagnostics | Measured facts and non-mutating inspection, separate from repair |
| UPS-EVID | Evidence | Identity, provenance, format, freshness, traceability and retention |
| UPS-SEC | Security / Trust | Trust boundary, secrets and supply-chain containment |
| UPS-MIG | Migration / Compatibility | A→B transitions, cutover, rollback and retirement |
| UPS-TEST | Assurance | Risk-based testing, negative and fault/concurrency cases, interaction matrices, reality gates |
| UPS-REL | Release / Promotion | Build-once identity, fresh gates and artifact promotion |
| UPS-DOC | Documentation / SSOT | Machine-to-human views and drift controls |

A shared concern, lifecycle stage or lifecycle concern has exactly one primary Control and may list related Controls; multiple references do not create multiple authoritative sources. [control-coverage.json](../06_GOVERNANCE/control-coverage.json) maps each standard to its Controls and verification obligation; [invariant-coverage.json](../06_GOVERNANCE/invariant-coverage.json) maps each baseline invariant to one primary Control and a product-level gate obligation. `DESIGN_COVERED` does not mean an actual product passed its gates.

For a new requirement, first identify the existing owner's scope and verification obligation. Reuse an existing Control before adding a new one, but do not force an uncovered responsibility into an unsuitable Control. A demonstrated ownership gap may justify a versioned extension, split or merge using [`EVOLUTION_POLICY.md`](../06_GOVERNANCE/EVOLUTION_POLICY.md).

Human views must be generated from machine SSOT or covered by explicit drift checks before PASS; review stale statuses, obsolete versions and conflicting descriptions. MANIFEST integrity alone establishes neither semantic correctness nor provenance. Contract/control/taxonomy evolution is permitted through an owned, versioned decision with an observed gap, alternatives, migration, conformance fixtures, evidence/security impact and revisit condition; preserve prior records. Invariant rule homes must be MANIFEST NORMATIVE_SOURCE or MACHINE_SSOT artifacts, never explanatory guides.
