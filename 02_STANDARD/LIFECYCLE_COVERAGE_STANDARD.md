# Proportionate Lifecycle Coverage

This is the normative home for profile selection and project assessment semantics. IDs, boolean flag fields and flag-to-entry mappings live only in [lifecycle-matrix.json](../03_LIFECYCLE/lifecycle-matrix.json); [project-lifecycle.schema.json](../07_CONTRACTS/schemas/project-lifecycle.schema.json) defines the interchange shape.

## Select a profile explicitly

`profile` is required: `COMPACT` or `FULL`, with no silent default. Record `escalation_flags`, `activity_flags` and `exposure_flags` as objects of booleans using the matrix's declared names. Any true escalation flag requires FULL. COMPACT is allowed only when `public_contract_change`, `authoritative_data`, `security_boundary` and `external_dependency` are all false.

COMPACT requires decisions for stages `SPECIFY`, `DESIGN`, `VERIFY` and concerns `OUTCOME_VALUE`, `RISK_SECURITY`, `QUALITY_ASSURANCE`, `GOVERNANCE_EVIDENCE`, plus entries derived from activity/exposure flags. FULL requires twelve stage and ten concern decisions, not 120 cell decisions. Omitted COMPACT entries are unassessed, never implicitly N_A or PASS. Both profiles use sparse `cell_overrides` for exceptional intersections; stage/concern results never imply a cell PASS.

## Keep scope, approach and result separate

A `disposition_record` uses `applicability` (`REQUIRED`, `OPTIONAL`, `N_A`), `approach` (`COMPLY`, `ADAPT`, `PRODUCT_SPECIFIC`) and `result` (`NOT_EVALUATED`, `PASS`, `FAIL`). Record accountable `owner` and `reason`. N_A needs rationale; ADAPT needs a documented equivalent contract. PASS needs `acceptance_criteria`, `candidate_identity` and `evidence_refs` for the exact assessed scope.

`deferred` records postponement with owner and `revisit_trigger`; it is not an applicability or result value and never satisfies REQUIRED. A PASS cannot conceal a conflicting N_A or deferred obligation. Retain unresolved obligations explicitly rather than fabricating success.

The validator derives required entries from profile/flags and rejects missing or unknown IDs and conflicting decisions. It validates schemas, references and encoded evidence conditions. The project's acceptance authority approves scoped conformance, adaptations and real outcomes; structural validation cannot certify operational conformity.

Keep traces proportionate: goal/scope, accountable owner, decision/acceptance, output/evidence and next/revisit route. External legal, safety or industry obligations may strengthen local coverage. Retirement includes applicable user migration, retention/deletion, access revocation and residual obligations.

Execution must have declared bounds (budget, deadline or stop condition). Uncertain execution requires reconciliation or blocked retry, never blind repetition. Each feedback observation requires an owned disposition and revisit or outcome; accepted closure requires requirement → executed proof → fresh exact-candidate gates → post-release outcome. Static package validation never implies product runtime verification. Suitable proof may be a regression, contract/property test, simulation or model proof; require RED evidence or an approved exception where defect reproduction is needed.
