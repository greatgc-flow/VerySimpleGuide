# Compatibility and Migration Standard

UPS-SCHEMA owns the current valid shape; UPS-MIG owns the A→B transition. Public-default cutover is a scoped migration, separate from implementing the replacement:

1. Inventory public behavior, consumers, parity and intentional differences.
2. Prepare a side-effect-free candidate selector and tested rollback/recovery route.
3. Run the full public and legacy compatibility sweep against the exact proposed candidate, including help/version, machine output, diagnostics, authorization and automation where applicable.
4. Approve and flip the public default only after required checks pass.
5. Observe post-cutover outcomes and recover if acceptance fails.
6. Gate deprecation and [retirement](../03_LIFECYCLE/DEPRECATION_RETIREMENT.md) separately.

Candidate-selector tests precede the flip; post-cutover observation does not replace them. Selectors must not silently migrate shared data. See [cutover scope](../03_LIFECYCLE/CUTOVER_ROLLBACK.md) and [release identity](RELEASE_PROMOTION_STANDARD.md).
