# VerySimpleGuide — Start Here (General R12, Standard 1.7.0)

## One-sentence principle
Standardize only semantics that must agree. Do not force different products to share CLI syntax, directories, databases, technology stacks or implementation details.

## Eight independent classification axes
1. **Plane:** `PRODUCT_RUNTIME` or `DELIVERY`.
2. **Component class:** `CORE`, `MODULE`, `EXTENSION`, `GENERATED_VIEW`, `EXTERNAL`.
3. **Required scope:** `BASE`, milestone/product scopes or an empty set for optional functionality.
4. **Boundary role:** `NONE`, `ADAPTER`, `PROVIDER`, `EXPORTER`.
5. **State kind:** `CONFIG`, `DOMAIN_DATA`, `EVIDENCE`, `LOG`, `CACHE`, `TEMP`, `BACKUP`, `SCHEMA`, `SECRET`, `EXTERNAL_REF`.
6. **Recovery class:** `AUTHORITATIVE`, `DURABLE_DERIVED`, `REBUILDABLE`, `EPHEMERAL`, `EXTERNAL`.
7. **Maturity:** `PLANNED`, `DESIGN_FROZEN`, `IMPLEMENTING`, `IMPLEMENTED`, `VERIFIED`, `DEPRECATED`, `RETIRED`.
8. **Distribution:** `NOT_PUBLISHED`, `CANDIDATE`, `PUBLISHED`, `PROMOTED`, `WITHDRAWN`.

Never confuse component ownership with provider roles; verified capability with publication; failure isolation with security isolation; an external task identity with internal work identity; advertised with measured capability; a relevance score with truth; `UNKNOWN` with healthy or unlimited; creating a backup with restoring it successfully; or publishing a release with verified promotion.

## Technology-neutral design
No programming language, operating system, cloud, database, CI system or vendor is mandatory. Python and PowerShell are **reference validators**, not project runtime requirements. Distinguish `INVARIANT`, `DEFAULT/HEURISTIC` and `EXAMPLE/REFERENCE`. Justified experiments may change defaults through a reversible decision.

Keep the Core minimal; optional extensions must be removable without breaking `BASE`. Rebuildable projections must specify what equivalence means, including limits for nondeterminism or external inputs. Evaluate mutations for retry, idempotency, crash and uncertain-execution semantics. Hide external providers behind documented ports rather than branching by vendor in Core.

## What counts as a closed feedback loop?
Link **objective and acceptance metric → measured observation → disposition → requirement/counterexample → exact-candidate verification → promotion → observed outcome → close or reopen**. A document, green CI, or public release alone does not prove field acceptance.

## Reading and verification
1. [Objectives and fitness](01_METHOD/OBJECTIVE_AND_FITNESS.md)
2. [Operational closed loop](01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md)
3. [Lifecycle value stream](01_METHOD/LIFECYCLE_VALUE_STREAM.md)
4. [Unified standard](02_STANDARD/UNIFIED_STANDARD.md)
5. [Knowledge routing](08_KNOWLEDGE/README.md)
6. [Final recursive audit](07_AUDIT/FINAL_RECURSIVE_MECE_R12.md)

Run `python -m pip install -r tools/requirements-validation.txt` and `python tools/validate_package.py --evidence-file .validation/validation_evidence.txt`.

The 12 stages × 10 concerns form an **applicability review space**, not 120 mandatory implementations. Projects normally record 12 stage decisions and 10 concern decisions plus specific cell overrides as necessary. Inspect [artifact ownership](06_GOVERNANCE/ARTIFACT_AUTHORITY.md) and [applicability guidance](03_LIFECYCLE/APPLICABILITY_EXAMPLE.md).
