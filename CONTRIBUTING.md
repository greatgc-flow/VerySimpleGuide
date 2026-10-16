# Contributing

This is a reference architecture guide, not a mandatory technology framework.
Contributions should preserve technology neutrality and the distinction between
normative invariants, defaults/heuristics, and examples/reference material.

1. Describe the user problem, applicable scope and smallest useful change.
2. Name the affected primary Control and update the machine-readable source of truth.
3. Update schema, example, generated views, trace and artifact ownership as needed.
4. Add positive and negative tests for changes to validation contracts.
5. Run `python -m pip install -r tools/requirements-validation.txt` followed by
   `python tools/validate_package.py --evidence-file .validation/local.txt`.
6. If normative behavior changes, document a versioned evolution decision and
   compatibility path; do not silently weaken an invariant.

Do not submit secrets, production data, provider tokens or copies of third-party
standards. Keep all contributed source and public documentation in English.
The validation evidence folder is intentionally ignored by Git.
