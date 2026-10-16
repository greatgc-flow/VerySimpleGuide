# Recursive MECE — Axes, Scope and Evidence

## Two vertical resolutions
The twelve canonical product-value stages (`DISCOVER` through `RETIRE`) live in `03_LIFECYCLE/lifecycle-matrix.json`. The eight technical operation categories—discover/bootstrap, configure, execute/mutate, observe, recover, migrate/upgrade, package/release and operate/learn/deprecate—are a lower-level diagnostic **view**, not a competing sequence or a strict one-to-one mapping.

## Two horizontal resolutions
Ten product/user concerns are canonical in the lifecycle matrix. Eight technical surfaces—interface, configuration, state/data, component/extension, security, observability/evidence, quality/testing and distribution/compatibility—are additional engineering review prompts, not new canonical concerns.

**Control (normative owner) × Stage (lifecycle) × Concern (subject)** are different coordinates. Each requirement or risk has one primary owner and may have multiple evidence and secondary-control links. Distinguish semantic separation from physically separate files or databases.

Every project evaluates twelve stage decisions and ten concern decisions, with explicit `cell_overrides` only for interactions that general inference misses. `FOCUS` and `CONSIDER` highlight reviewer attention; they do not mean 120 implementations or certificates. Mark nonapplicable activities `N_A` with rationale and revisit policy. `PASS` must be tied to the exact scope, candidate, time and evidence.

Inspect each selected level recursively—project, milestone, component, interface, mutation, artifact, distribution and retirement—using objectives, ownership, contracts, tests, failure cases, evidence, next/revisit conditions and deprecation. Do not infer complete domain coverage from a green static package validator.
