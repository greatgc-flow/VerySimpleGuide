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

PASS stage, concern and cell decisions require nonblank revisit conditions. A recorded FAIL or fired `trigger_observation_ids` requires `feedback_ids` resolving to owned OPEN/IN_PROGRESS actions in the same project trace; each trigger observation must be addressed by those actions.

Use scoped requirements for selected interactions: `control_ids` and optional stage/concern coordinates identify the selected risk, with the existing owner and acceptance. Declared `product_gate_obligations` resolve directly to trace test/gate IDs; selected `invariant_ids` resolve their catalog obligation names the same way. At PASS, promotion or accepted closure, each scoped requirement needs passing executed proof and all obligations for the same candidate; unfinished scope needs an explicit pending decision. No exhaustive pairing or new control taxonomy is implied.

Trace observations, tests and gates inherit the checked project objective owner; feedback and change/release records name their accountable decision owners.

PASS cell overrides resolve by stage/concern and candidate to a passing scoped requirement in the associated trace. Promotion includes every declared gate obligation for its frozen scope. A requirement's declared candidate limits its promotion assessments, so earlier and later candidates can coexist. Scoped executed proof matches the assessed artifact digest, with tests before required gates and proof before deployment/promotion or component verification. VERIFIED components resolve scoped PASS requirements and their obligations against the associated trace; local copies of gate evidence cannot override pending trace proof. ADOPT feedback requirements must resolve in that trace; explicitly pending implementation and outcome work is allowed.
