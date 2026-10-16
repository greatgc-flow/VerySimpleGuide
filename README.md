# VerySimpleGuide

**A platform-neutral, evidence-driven, lifecycle-wide architecture and engineering guide.**

This repository generalizes proven design, testing, delivery and operating lessons without copying any particular product's implementation. It is a **reference standard and validation toolkit**, not an application, code generator or mandatory framework.

## Principles
- **Very Simple:** standardize only required semantics; remove incidental complexity.
- **Recursive MECE:** inspect vertical ownership and horizontal concern coverage repeatedly at every relevant scope.
- **One Source, Multiple Uses:** derive human views and tests from canonical machine-readable contracts.
- **Evidence First:** attach assertions to exact candidates, observed facts and fresh gates.
- **Declarative by Default:** prefer schemas, config and policy over vendor-specific hardcoding.
- **Closed-Loop Improvement:** observation → decision → test/proof → minimal change → verification → deployment → measured outcome → revisit.
- **Technology Openness:** treat languages, tools, patterns and industry guidance as scoped choices, not global obligations.

## What the guide covers
The eight orthogonal classification axes, 15 baseline controls, component and state ownership, authority versus projections, optional extensions and provider contracts, defensive mutations, public-interface compatibility, bounded orchestration, release identity, evidence, field reality gates and retirement. The lifecycle guide spans 12 logical stages and 10 independent cross-cutting concerns. Optional engineering guidance and authoritative references are pulled on demand rather than loaded wholesale.

## Quick start
Read [START_HERE.md](START_HERE.md), [Unified Standard](02_STANDARD/UNIFIED_STANDARD.md), [Lifecycle Value Stream](01_METHOD/LIFECYCLE_VALUE_STREAM.md) and the [Optional Knowledge Catalog](08_KNOWLEDGE/README.md). Example JSON payloads in `07_CONTRACTS/examples` are illustrative: do not treat their invented IDs or sample PASS labels as real evidence.

### Validate this repository
```bash
python -m pip install -r tools/requirements-validation.txt
python tools/validate_package.py --evidence-file .validation/validation_evidence.txt
```

The validator mirrors the displayed output to the evidence file. The shipped PowerShell wrapper is syntax-compatible with Windows PowerShell 2.x/5.x where the required Python is available:
```powershell
.\tools\validate_package.ps1 -Python python -EvidenceFile .validation\validation_evidence.txt
```

### Validate a project's scoped models
```bash
python tools/validate_package.py \
  --project-trace path/to/project-trace.json \
  --project-registry path/to/component-registry.json \
  --project-lifecycle path/to/project-lifecycle.json \
  --evidence-file .validation/project_validation.txt
```

**Important:** a passing structural/semantic validation is not proof that external CI runs, operating conditions, security controls, data recovery or user outcomes were independently validated. Projects must supply their own real evidence and blocking gates.

## Repository navigation
`01_METHOD` contains objectives and loops; `02_STANDARD` defines contracts; `03_LIFECYCLE` defines transitions, release, and the 12×10 review space; `04_ASSURANCE` defines evidence and negative verification; `05_ARCHITECTURE` contains decisions; `06_GOVERNANCE` contains single ownership and evolution; `07_AUDIT` contains dated design audits; `07_CONTRACTS` defines JSON schemas (`07_CONTRACTS/schemas`) and examples (`07_CONTRACTS/examples`); `08_KNOWLEDGE` holds optional guidance and source links; `tools` holds the reference validator.

## Licensing and external materials
Original content and reference tooling in this repository are distributed under [Apache License 2.0](LICENSE). Linked external guides retain their own terms and are *not* relicensed or reproduced here. The guide does not prescribe a programming language, cloud, toolchain or development methodology.
