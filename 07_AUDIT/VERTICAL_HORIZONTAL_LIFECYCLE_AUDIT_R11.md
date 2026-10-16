# Historical R11 Recursive Lifecycle Audit (12 Stages × 10 Concerns)

## Gaps found in R10
- **Before development:** discovery, build/buy/reuse options, user experience, economics and sustainability.
- **Development and release:** real handover, acceptance, operational readiness and nonfunctional/security concerns throughout the lifecycle.
- **Operations and retirement:** support, incidents, SLOs and costs, supply chain, retention/deletion and access revocation.
- **Reference provenance:** URLs alone did not explain avoid-when cases, archival status or recheck triggers.
- **Normative drift:** some text could be read as a permanent 15-Control cap, absolute ban on custom frameworks or byte-deterministic projection requirement.

## Corrections
- A machine-readable 12×10 matrix captures owner, exit condition and normal/revisit transitions. Validator detects missing stages/concerns and orphan reference IDs.
- Optional guidance entries capture use, avoid, alternatives, evidence, source status and review triggers.
- Product applicability requires candidate-specific PASS evidence or explicit N_A/DEFERRED reasons and revisit.
- Six lifecycle Invariants were assigned to existing Controls, without new mandatory tooling or runtime.

## What the evidence does *not* prove
Passing sample schema tests do not certify real user outcomes, SLOs, compliance, incident readiness, lawful retention/deletion or live production behavior. Catalog sources are relevant candidates, not endorsements; archived materials must be labeled as such. A small low-risk change may use one short record rather than twelve forms.

## Next field validation examples
1. Evaluate one small project and trace DISCOVER → RELEASE → OBSERVE feedback.
2. For a stateful product, rehearse backup/restore, access revocation and retirement.
3. For CLI/API migration, verify parity, rollback and end-user support against the exact candidate.
4. Reconsider decisions when source guidance or real constraints change.
