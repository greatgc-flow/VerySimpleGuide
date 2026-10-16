# Technology and Creative Design Openness Audit — R10 / Standard 1.5.0

## Evidence boundary
Based on direct inspection of General R9 (1.4.0), its 15 controls, 26 invariants, documents, machine schemas, validator and negative tests. External standards are **candidate references** and not required dependencies. The review does not constitute real project platform/runtime qualification.

| Finding | R9 risk | R10 treatment | Residual |
|---|---|---|---|
| Language/OS neutrality implicit only | Python/PowerShell tooling could appear mandatory | normative vs reference separation and implementation-choice record | provider-specific reality tests remain |
| Control count fixed 15 | future new concerns excluded | versioned evolution policy, maintain baseline | process cost for new controls |
| Framework-First / rule-of-three phrased as absolute | adoption/innovation inhibited | distinguish custom framework from use of established standard or spike | experimental debt must be tracked |
| Universal RED requirement | non-code research blocked | falsifiable methods with TDD where suitable; approved evidence-based exception | closed-defect regression still mandatory where applicable |
| Deterministic replay | probabilistic/AI/external non-repeatable workflows confused | declared logical equivalence, snapshot/evidence, classification boundary | requires product-level replay proof |
| Assumed CLI and static phases | UI/embedded/event-based release excluded | conditional interface/wave applicability | stronger per-product ownership required |
| Opaque enum classes | new platforms need new semantic tags | explicit namespaced extension metadata and versioned common evolution | schema and governance remain deliberately strict |
| Artifact uniqueness | multi-target OS/arch releases confused | immutable artifact *set* with digest per target | gate coverage per target |

## Technology reference survey (as at 2026-10-16)
- OpenAPI 3.2.1: programming-language-agnostic HTTP contract; https://spec.openapis.org/oas/latest.html
- OpenTelemetry: vendor-neutral telemetry; CNCF graduated May 2026; https://www.cncf.io/announcements/2026/05/21/cloud-native-computing-foundation-announces-opentelemetrys-graduation-solidifying-status-as-the-de-facto-observability-standard/
- OpenFeature: provider-independent feature flags; https://openfeature.dev/docs/reference/intro/
- SLSA provenance / in-toto: verifiable production identity; https://slsa.dev/spec/
- OWASP CycloneDX: SBOM and ML-BOM options; https://cyclonedx.org/specification/overview/
- WASI Component Model: evolving cross-language component capabilities; https://github.com/WebAssembly/component-model
- CUE: configuration/schema tooling choice, not canonical mandate; https://cue.dev/docs/
- Dapr: optional polyglot sidecar building blocks where runtime decoupling is justified; https://docs.dapr.io/concepts/overview/

## Judgment
R9 was *not* explicitly single-language or single-platform, but some heuristics looked non-overridable. R10 makes technology neutrality and innovation admission explicit while retaining hard authority/safety/release invariants. The reference Python validator remains Python-based: an independently implemented conformance runner is now explicitly allowed, but a second runner is **not yet independently verified**. Distinguish specification portability from proven toolchain portability.

## Validator openness regression
R10 tests **simulated growth beyond 15 controls** with governed machine SSOT/coverage updates in memory. The validator still rejects missing, duplicate, orphan or unmapped controls; it no longer rejects growth solely because the count is no longer exactly 15. This is a contract test, not permission to mutate the current baseline without a versioned decision.

## Count terminology correction
`tools/test_validator.py` combines invalid-input rejection scenarios with positive acceptance scenarios. The validator now labels its total `contract_fixture_checks`, not `negative_tests`, so the evidence claim cannot inflate pure negative-test coverage.
