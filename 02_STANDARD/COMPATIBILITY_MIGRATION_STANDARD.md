# Compatibility and Migration Standard

`UPS-SCHEMA` owns the current valid shape; `UPS-MIG` owns the state transition from version A to version B.

A public default cutover is **not** synonymous with implementing a replacement. Treat it as its own lifecycle:
1. Inventory current public behavior and consumers.
2. Record parity and intentionally different behavior.
3. Add a side-effect-free selector or rollback route where practical.
4. Flip the default explicitly.
5. Run a full public and legacy integration sweep.
6. Prove rapid recovery or rollback.
7. Gate deprecation and retirement separately.

Changing the default selector can break many existing public CLI tests even if all new CLI unit tests pass. Always include a compatibility regression gate tied to the exact cutover candidate.
