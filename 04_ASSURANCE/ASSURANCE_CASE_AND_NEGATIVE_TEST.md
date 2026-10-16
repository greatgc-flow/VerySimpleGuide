# Assurance Cases and Negative Verification

The evidence chain is **Claim → Scope/Candidate → Requirement/Obligation → Test/Gate → Fresh Evidence → Verdict**.

- `DOCUMENTED` is a design statement; `SCHEMA_CHECKED` demonstrates structural validity; `PRODUCT_VERIFIED` needs a product's real passing run.
- A document merely existing is not proof. Prove that the validator rejects representative malformed counterexamples.
- A gate described by a Markdown path without execution evidence is only a planned test.
- Scope `N_A`, `PASS` and `DEFERRED` need their recorded rationale, owner and revisit conditions where applicable.
- Never conflate Common Standard design validity with deployed product assurance.

## Representative negative cases
Reject changed, missing, extra or traversal-based manifest paths; invalid JSON schemas; evidence-free `VERIFIED`/`PROMOTED`; orphan requirements, tests, gates and feedback; closed feedback without measured post-outcomes; unowned deferral or rejection; and stale or mismatched candidate digests.

This package proves schema, sample and reference model properties, not live concurrency, provider, OS or security outcomes. Project execution may use `--project-trace`, `--project-registry` and `--project-lifecycle`, but real dependency topology and production tests require external gates.
