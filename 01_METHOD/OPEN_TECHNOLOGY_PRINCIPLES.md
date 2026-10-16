# Open Technology and Creative Architecture — Normative vs Reference

## Purpose
The standard **MUST NOT globally mandate a programming language, operating system, hosting model, cloud, database, CI provider, package manager, runtime, or architecture style.** Project-specific runtime constraints may be mandatory only when documented as scope-local requirements with source, owner, compatibility rationale and revisit trigger.

A reference implementation (Python validator, JSON Schema, shell/PowerShell wrapper) is **a convenient implementation, not the sole route to conformance**. Equivalent validators written in Go, Rust, Java, C#, JavaScript, shell or future languages are legitimate when the same conformance fixtures, pass/fail semantics, evidence and supply-chain checks succeed.

## Three normative levels
1. **INVARIANT**: breach directly violates the agreed safety/authority/security contract for an applicable scope (e.g. no silent positive invention from UNKNOWN, no unverified stable-promotion claim). A project may challenge the top-level standard through versioned governance, not silently override it.
2. **DEFAULT / HEURISTIC**: recommended starting pattern, e.g. 15 controls, rule of 2–3 consumers, one build artifact, RED-first TDD, a suggested implementation wave, declarative configuration, immutable records, generic extension host postponement. An alternative **MAY** be chosen using a recorded decision and evidence. A deviation is not automatically a product failure.
3. **EXAMPLE / REFERENCE TOOL**: illustration, file format, folder, language, OS, protocol, test runner, CLI syntax. Do not upgrade an example to a requirement.

## Technology-neutrality gate
- `implementation_language`, `runtime`, `os_targets`, `hardware_arch`, `storage_engine`, `transport`, `packaging`, `test_framework`, and `CI_provider` must be recorded as **project choices**, never inferred from the tools shipped in General.
- A CLI is not mandatory for library-only, UI-first, embedded, mobile, event-driven or serverless products. UPS-CLI applies to **public interfaces that actually exist** (API, UI, events, CLI); unavailable surfaces are N_A with rationale.
- `Core → Extension implementation import = 0` remains a good decoupling invariant. Composition roots, ports, inversion of control, compile-time linking, multi-process sidecars, and statically linked variants remain legitimate implementation choices.
- Cross-language boundaries may use direct FFI, stable ABI, HTTP/OpenAPI, gRPC/Protobuf, message/event contracts or WebAssembly components: choose by workload and measured costs. No transport is required universally.
- `BUILD ONCE → GATE → PROMOTE SAME ARTIFACT` means **identity-preserving promotion for each release target**. It does not require one binary to run unchanged across incompatible operating systems/architectures; build per target and verify each frozen digest.
- For probabilistic, externally stateful or AI-produced results, exact byte-for-byte replay is not always meaningful. Evidence/snapshot/source version and *declared equivalence criteria* govern verification; `REBUILDABLE` classification is used only when regeneration with acceptable logical equivalence is demonstrable.

## Innovation rights and constraints
A justified alternative to a DEFAULT **MUST** have: testable hypothesis, baseline, alternative, expected benefit, known risks, proof/falsification plan, bounded budget/stop rule, acceptance criterion, and exit/rollback strategy. Experimental work must not silently bypass authorization/security/release gates.

A single use case can justify adoption of a well-maintained interoperable standard; the 2–3-consumer rule applies to **inventing a bespoke generic framework**, not integrating an existing reusable library or proving an experimental prototype.

When a concern is truly unowned by the 15 control baseline, add a **versioned proposal** with owner, evidence of non-fit, alternatives, impact on migration, test obligations and review. `15` is a baseline, **not an eternal numerical ceiling**.
