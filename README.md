# VerySimpleGuide

A platform-neutral engineering reference: standardize shared semantics, keep implementations small and tie claims to evidence. This is a guide and validation toolkit, not an application or mandatory framework.

Start with [START_HERE.md](START_HERE.md), [objectives and fitness](01_METHOD/OBJECTIVE_AND_FITNESS.md), then the [unified standard](02_STANDARD/UNIFIED_STANDARD.md). Select [COMPACT or FULL](02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md) explicitly. The [lifecycle backbone](03_LIFECYCLE/README.md) supports iteration and scoped feedback; optional [knowledge](08_KNOWLEDGE/README.md) is retrieved as needed.

## Validate

```bash
python -m pip install -r tools/requirements-validation.txt
python -B tools/validate_package.py --evidence-file .validation/validation_evidence.txt
```

PowerShell wrapper: `.\tools\validate_package.ps1 -Python python -EvidenceFile .validation\validation_evidence.txt`.

To include project models:

```bash
python -B tools/validate_package.py \
  --project-trace path/to/project-trace.json \
  --project-registry path/to/component-registry.json \
  --project-lifecycle path/to/project-lifecycle.json \
  --evidence-file .validation/project_validation.txt
```

Evidence output belongs under `.validation/`. JSON examples illustrate contracts; their IDs and PASS labels are not real product evidence. [Assurance claims](04_ASSURANCE/ASSURANCE_CASE_AND_NEGATIVE_TEST.md) distinguish design, structural checks, negative tests and actual product verification. Package success cannot establish field outcomes.

## Navigation

`01_METHOD`: objectives and reasoning ([decision rules](01_METHOD/DECISION_RULES.md), [recursive coverage](01_METHOD/RECURSIVE_MECE.md)); `02_STANDARD`: normative contracts (e.g. [security and trust](02_STANDARD/SECURITY_TRUST_STANDARD.md), [capability catalog](02_STANDARD/CAPABILITY_CATALOG_STANDARD.md), [extensions and providers](02_STANDARD/EXTENSION_PROVIDER_STANDARD.md)); `03_LIFECYCLE`: stages and transitions; `04_ASSURANCE`: evidence and verification ([interaction matrix](04_ASSURANCE/INTERACTION_MATRIX.md), [core-only survivability](04_ASSURANCE/CORE_ONLY_SURVIVABILITY.md)); `05_ARCHITECTURE`: design guidance ([anti-patterns](05_ARCHITECTURE/ANTI_PATTERNS.md), [waves](05_ARCHITECTURE/IMPLEMENTATION_WAVES.md), [layout](05_ARCHITECTURE/PROJECT_SKELETON.md), [search and memory](05_ARCHITECTURE/SEARCH_MEMORY_CONTEXT.md)); `06_GOVERNANCE`: authority and evolution ([control catalog](06_GOVERNANCE/CONTROL_CATALOG.md), [artifact authority](06_GOVERNANCE/ARTIFACT_AUTHORITY.md)); `07_CONTRACTS/{schemas,examples}`: machine contracts and samples; `08_KNOWLEDGE`: optional guidance; `tools`: reference validation. [CHANGELOG.md](CHANGELOG.md) retains durable design decisions.

Applicable safety and authority responsibilities remain binding; control organization, language, OS, cloud and tooling are project choices under [open technology principles](01_METHOD/OPEN_TECHNOLOGY_PRINCIPLES.md). MANIFEST.json is the sole file inventory and excludes itself; hashes detect accidental change, not provenance.

Contribute via [CONTRIBUTING.md](CONTRIBUTING.md); report vulnerabilities per [SECURITY.md](SECURITY.md).

Original content and tooling use [Apache License 2.0](LICENSE). External links retain their own terms.
