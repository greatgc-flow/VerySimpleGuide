# VerySimpleGuide — Start Here

Standardize only semantics that must agree. Begin with [objectives and fitness](01_METHOD/OBJECTIVE_AND_FITNESS.md), [unified responsibilities](02_STANDARD/UNIFIED_STANDARD.md) and an explicit [COMPACT/FULL profile](02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md). Apply one [lifecycle backbone](01_METHOD/LIFECYCLE_VALUE_STREAM.md), with feedback returning to the affected decision.

## Separate classification dimensions

1. Plane: PRODUCT_RUNTIME or DELIVERY.
2. Component class: CORE, MODULE, EXTENSION, GENERATED_VIEW, EXTERNAL.
3. Required scope: BASE, declared milestone/product scopes, or no required scope.
4. Boundary role: NONE, ADAPTER, PROVIDER, EXPORTER.
5. State kind: CONFIG, DOMAIN_DATA, EVIDENCE, LOG, CACHE, TEMP, BACKUP, SCHEMA, SECRET, EXTERNAL_REF.
6. Recovery class: AUTHORITATIVE, DURABLE_DERIVED, REBUILDABLE, EPHEMERAL, EXTERNAL.
7. Maturity: PLANNED, DESIGN_FROZEN, IMPLEMENTING, IMPLEMENTED, VERIFIED, DEPRECATED, RETIRED.
8. Distribution: NOT_PUBLISHED, CANDIDATE, PUBLISHED, PROMOTED, WITHDRAWN.

These dimensions have constraints: use [component rules](02_STANDARD/COMPONENT_BOUNDARY.md) for MODULE/EXTENSION, [data policy](02_STANDARD/DATA_SAFETY_STANDARD.md) for kind/recovery/sensitivity and [distribution transitions](02_STANDARD/RELEASE_PROMOTION_STANDARD.md) for publication. Project `owner` identifies accountable decision authority; maintainership grants no acceptance authority.

## Verify the claim you make

Use [feedback closure](01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md) for measured observation through decision, exact-candidate verification and observed outcome. A document, green CI or publication alone cannot prove acceptance. [Independent assurance claims](04_ASSURANCE/ASSURANCE_CASE_AND_NEGATIVE_TEST.md) state what was actually checked.

Run `python -m pip install -r tools/requirements-validation.txt`, then `python -B tools/validate_package.py --evidence-file .validation/validation_evidence.txt`. Python/PowerShell are reference tools; project runtimes remain local choices. Pull optional guidance through the [knowledge index](08_KNOWLEDGE/README.md).
