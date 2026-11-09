# Design Decisions

## 1.9.4 Single-home and ledger diet

- Peer debate (cx, ag, cc; two rounds, unanimous on items 1, 2, 4; majority plus cx acceptance on 5).
- Rule homes: `ARTIFACT_AUTHORITY.md` states that each rule has exactly one home; standards own product and runtime contracts, and a method guide may be the single home of a process obligation that no standard states. Moved the remaining runtime rules (recovery journals, derived-truth promotion, prototype authority) into their standards; orchestration knobs are now advisory under the standard's declared-bounds rule.
- Ledger: merged `control-coverage.json` into `unified-package-standard.json`; each control now carries its standard references and verification obligation. Checks keep their strength.
- Validator: every relative Markdown link must resolve (caught a stale link to the merged ledger).
- CI: replaced the string-only workflow test; the validator prints `prior_project_trace=COMPARED`, and pull-request CI requires that line.
- README navigation is a folder table.
- Kept on purpose: a single validator file (no consumer needs a module boundary yet).

## 1.9.3 Cross-audit closure

- Recursive MECE audit (vertical: rule to evidence to reentry; horizontal: counts, routing, inventory, CI) by independent peers; 13 findings plus README reachability: all resolved; F8 is a recorded non-goal.
- Validator: accept FAIL reentry records (schema wrappers allowed feedback and trigger ids), bind PASS and closure proof to the candidate digest and chronology, require a designated primary control, compare project ids, reject blank accountable owners, reconcile invariant homes with control coverage, and report skipped filesystem checks as `NOT_EVALUATED` instead of PASS.
- CI compares the pull-request base trace (`--prior-project-trace`) so executed evidence cannot be rewritten silently.
- Reachability: every document is reachable from README or START_HERE by Markdown links; deleted the unused interaction-matrix CSV; moved the commit-point and upgrade-gate rules to their normative standards (guides link back); deduplicated the DECLARED/MEASURED rule.
- Non-goal (F8): invariants carry no stage/concern coordinates; placement is declared per scoped requirement (`stage_id`, `concern_id`).
- Resolved (F13): WITHDRAWN is terminal for a candidate identity; reinstatement is a new candidate identity (unchanged bytes allowed) starting from NOT_PUBLISHED. The validator no longer accepts WITHDRAWN to CANDIDATE. This supersedes the R14 known limitation on same-candidate reinstatement.
- Gate ordering: required gates must be observed at or before deployment.
- Guard: the validator fails when any Markdown document is unreachable from README or START_HERE.

## 1.9.2 Upgrade and safety clarifications

- Exercise upgrades through the installed entry point and existing materialized state, including user edits; include the declared minimum runtime (#7, merged #12/#17).
- Require isolated unit checks that can fail when claimed behavior breaks; distinguish conversion from source preservation (#8/#16).
- Include ancillary outbound transfers in side effects and test offline claims with network denied (#14).
- Reject source/destination overlap and filesystem aliases before backup/restore writes, including control/temp paths (#18).
- Name commit points, distinguish compensation from cleanup failure and retain residual-resource ownership for retries (#23/#24).
- Audit current content and retained history before widening repository/archive access (#29).
- Clarify existing contracts without new vocabulary, schemas, coverage mappings or validator rules; existing version pins upgrade to 1.9.2 without rewriting historical evidence.
- Add one sentence to Very Simple fitness: scale implementation and verification effort to impact, risk and reversibility without weakening required evidence (#47).

## 1.9.1 MECE consolidation

- Give each rule one home: merge restating guides into their normative or parent files, give UPS-REL its own standard, and align N_A, REOPEN and control names with the validator and machine SSOT. Control IDs, invariant IDs, schemas and contract semantics are unchanged.
- Add an awareness step to operational feedback (#4) and repository guardrails to CONTRIBUTING (#5) without new tools, grammar, configuration formats or labels. Only `main` triggers push validation.
- Correct invariant ownership mappings and fail without filesystem writes when the PowerShell wrapper cannot find Python.
- Path map (old → new home):
  - `01_METHOD/DEVELOPMENT_CLOSED_LOOP.md` → `01_METHOD/LIFECYCLE_VALUE_STREAM.md`
  - `01_METHOD/OPTIONAL_KNOWLEDGE_ROUTING.md` → `08_KNOWLEDGE/README.md`
  - `02_STANDARD/PROJECTION_FRESHNESS_STANDARD.md` → `02_STANDARD/AUTHORITY_PROJECTION_STANDARD.md`
  - `03_LIFECYCLE/RELEASE_PROMOTION.md`, `03_LIFECYCLE/MATURITY_DISTRIBUTION.md` and the release section of `02_STANDARD/OBSERVABILITY_EVIDENCE_STANDARD.md` → `02_STANDARD/RELEASE_PROMOTION_STANDARD.md`
  - `04_ASSURANCE/TDD_TRACEABILITY.md` → `02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md`
  - `04_ASSURANCE/DRIFT_CONTROL.md` → `02_STANDARD/UNIFIED_STANDARD.md`
  - `06_GOVERNANCE/APPLICABILITY_POLICY.md` → `02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md`
  - `06_GOVERNANCE/LIFECYCLE_GUIDANCE_POLICY.md` → `02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md` (profiles, retirement), `02_STANDARD/UNIFIED_STANDARD.md` (one primary Control per stage/concern), `01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md` (incident reopening)
  - `06_GOVERNANCE/CONTROL_BOUNDARY_OWNERSHIP.md` → `02_STANDARD/UNIFIED_STANDARD.md`
  - `06_GOVERNANCE/EXCEPTION_DISPOSITION.md` → `01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md`

## R14 MECE and loop closure

- Close the v1.9.0 package trace with CI, deployment, measured outcome and an owner-approved RED exception.
- Bind evidence to the candidate; retain all controls without merging them or adding a blanket rule-ID registry. Enforce B2 selected-interaction obligations and report test skips honestly.
- Known limitation (M): Same-candidate reinstatement with fresh gate IDs conflicts with historical promotion obligations; rebinding requirements invalidates earlier promotions. Until historical assessment binding is supported, preserve prior records and use a new candidate identity with fresh requirements, tests and gates, even for unchanged bytes. Never rewrite executed evidence.

## R14 schema simplification

- Share local nonblank/reference shapes in the trace schema and remove minLength where the same nonblank pattern already implies it. Reuse positive trace fixtures and a single registry seed; preserve all constraints, candidate bindings and rejection checks without a contract change.

## R14 review associations

- Isolate candidate obligations within a shared scope and bind executed proof to the assessed artifact and time. Resolve VERIFIED and ADOPT against the associated trace, retain executed evidence across ledgers, and address withdrawal before leaving feedback closed. Reopened work may progress; exception observations append rather than rewrite evidence. The LF example claims evidence integrity coverage only.

## R14 actual package self-review

- Validate the package-owned R13/R14 trace in CI through the same project contract. Record executed local proof and the minimal change; retain IN_PROGRESS while commit/PR, required CI, deployment and measured outcome are pending. Examples never substitute for this work record.

## R14 scoped coverage and honest execution

- Reuse scoped requirements for selected controls/interactions and resolve their declared proof obligations at acceptance. Keep all fifteen controls. Inherit registry authority only through a checked project trace association. Separate filesystem execution/skips/N_A and require applicable defenses in CI.

## R14 feedback and revisit history

- Check chronological closure/reopening, candidate/metric regressions and specific exception decisions. Compare prior ledgers for history/evidence retention; require revisit conditions and open feedback for recorded lifecycle failures or triggers.

## R14 candidate and distribution bindings

- Extend existing trace records with minimal changes and ordered releases/deployment evidence. Resolve accepted closure to the same candidate/digest through executed proof, gates, change and outcome; consume the guarded distribution transitions and preserve withdrawal history.

## R14 evidence conditions (contract 1.9)

- Extend existing maturity, state and adoption records with checked evidence and feedback links; require measured baseline proof. Reuse gate evidence, and test mutation/protocol rejection boundaries. The canonical standard version is the single version authority; record pins and schema IDs follow it.

## R14 authority consolidation

- Repoint all thirteen explanatory invariant homes into existing standards; guides link to them. Reject nonauthoritative invariant homes rather than making whole guides normative.

## R14 vocabulary and guidance

- Check duplicated schema vocabulary against canonical lists and guidance applicability against cited source stages. Keep projection reproduction rules only in the authority standard.

## R13 simplification

- Keep one lifecycle backbone and unique directory numbers; separate contracts from governance and optional knowledge. Human views link to a single normative home per rule.
- Use explicit COMPACT/FULL profiles and sparse interaction overrides. Keep applicability, implementation approach and assessment result separate.
- Treat assurance claims independently; package checks cannot establish real product outcomes. Decision authority belongs to project owners, not artifact maintainers.
- Distinguish required component capabilities, removable extensions, state recovery and sensitivity. Sweep compatibility before public cutover; preserve exact release identity and withdrawal history.
- Keep MANIFEST.json as the sole inventory, explicitly excluding itself. Hashes detect accidental changes; provenance needs independently trusted evidence.
- Retain durable lessons in the method and standards; remove iteration audits and frozen validator output. Obtain current evidence from each validation run.
