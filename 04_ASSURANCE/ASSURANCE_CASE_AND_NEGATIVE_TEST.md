# Independent Assurance Claims

Use **Claim → Scope/Candidate → Obligation → Check/Gate → Fresh Evidence → Result**. Canonical `outcome_contract.claim_kinds` and `claim_results` live in [unified-package-standard.json](../06_GOVERNANCE/unified-package-standard.json):

| Claim kind | Evidence addressed |
|---|---|
| DESIGN_COVERED | Explicit design and obligation coverage. |
| SCHEMA_CHECKED | Executed schema and static checks. |
| NEGATIVE_TESTED | Executed rejection of representative malformed inputs. |
| PRODUCT_VERIFIED | Product-specific real execution and acceptance. |

Each claim independently receives NOT_EVALUATED, PASS or FAIL; these are not a maturity ladder. No check means NOT_EVALUATED. Per-claim output states what ran; aggregate PASS requires every package-scope claim to PASS and an empty error set. Product verification remains NOT_EVALUATED without real product evidence and cannot be implied by package success.

Representative negative cases include missing/extra/changed or noncanonical manifest paths, evidence-output aliases of inputs, invalid contracts, evidence-free VERIFIED/PROMOTED, orphan trace links, unowned deferral and stale/mismatched candidates. A Markdown test path is a plan, not execution evidence. [Assessment records](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md) and [feedback closure](../01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md) define their own evidence conditions.

The reference validator checks models and encoded conditions. Real provider/OS/security, recovery, concurrency and user outcomes need project gates; see [reality gates](REALITY_GATES.md).
