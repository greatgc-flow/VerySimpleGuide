# Unified Package Standard 1.9.0

Applicable semantic responsibilities are binding; organizing them as fifteen controls is a default under [open technology principles](../01_METHOD/OPEN_TECHNOLOGY_PRINCIPLES.md). `primary_control` identifies the package semantic control domain; project `owner` identifies accountable decision authority. Artifact maintainership grants no acceptance authority. Discovery/funding mappings assign document/control responsibility, not business authority.

| ID | Control | Semantic ownership |
|---|---|---|
| UPS-CLI | CLI / Interface | Public behavioral contracts; CLI grammar/flags only for CLI surfaces |
| UPS-HELP | Help / Discovery | Read-only help, discovery and generated-view consistency |
| UPS-EXIT | Exit Semantics | Semantic exit classes; numeric codes may be product-specific |
| UPS-CONFIG | Configuration | Precedence, merge and null/empty/unknown behavior |
| UPS-LAYOUT | State / Filesystem | State kinds, ownership and recovery classes |
| UPS-SCHEMA | Schema / Version | Current data contract and version compatibility |
| UPS-COMP | Component Boundaries | Classes, required scopes and dependency ownership |
| UPS-EXT | External Boundary | Public adapter, provider and exporter ports |
| UPS-OBS | Observation / Diagnostics | Measured facts and non-mutating inspection |
| UPS-EVID | Evidence | Identity, provenance, freshness, traceability and retention |
| UPS-SEC | Security / Trust | Trust boundary, secrets and supply-chain containment |
| UPS-MIG | Migration / Compatibility | A→B transitions, cutover, rollback and retirement |
| UPS-TEST | Assurance | Risk-based testing, interaction matrices, fault/concurrency cases |
| UPS-REL | Release / Promotion | Build-once identity, fresh gates and artifact promotion |
| UPS-DOC | Documentation / SSOT | Machine-to-human views and drift controls |

Reuse an existing Control before adding a new one, but do not force an uncovered responsibility into an unsuitable Control. A demonstrated ownership gap may justify a versioned extension, split or merge using [`EVOLUTION_POLICY.md`](../06_GOVERNANCE/EVOLUTION_POLICY.md).

Human views must be generated from machine SSOT or covered by explicit drift checks before PASS. Contract/control/taxonomy evolution is permitted through an owned, versioned decision with an observed gap, alternatives, migration, conformance fixtures, evidence/security impact and revisit condition; preserve prior records. Invariant rule homes must be MANIFEST NORMATIVE_SOURCE or MACHINE_SSOT artifacts, never explanatory guides.
