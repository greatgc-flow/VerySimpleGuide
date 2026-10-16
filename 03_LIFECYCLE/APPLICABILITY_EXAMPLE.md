# The 12×10 Review Space and 12+10 Applicability Ledger

The design space contains twelve stages × ten concerns = 120 `FOCUS`/`CONSIDER` questions. It is a **static reviewer checklist**, not 120 individual approvals or test results.

In practice, complete twelve stage decisions and ten concern decisions in `07_CONTRACTS/examples/project-lifecycle.example.json` with owner and rationale. Add `cell_overrides` only where a particular intersection has a materially different status; document evidence and re-evaluation criteria for exceptions.

Example: `DESIGN × RISK_SECURITY = DEFERRED` means design risk evaluation awaits a named threat-model review. A broad design-stage PASS does not automatically certify the security intersection. Combining applicable states is not an automatic compliance certification algorithm; conflicts retain the more cautious proof obligation. `PASS` is valid only with scope, timestamp/candidate and actual evidence.
