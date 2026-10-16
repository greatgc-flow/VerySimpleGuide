# Capability, Skill, Catalog and Policy Standard

Keep these semantic owners distinct:

1. **Procedure source:** authoritative source of steps, skill or agent procedure; it may be a local artifact or external reference.
2. **Generated index:** `REBUILDABLE` view used to discover procedure sources.
3. **Declared capability catalog:** curated or declarative statement of advertised capabilities.
4. **Selection and activation policy:** the rules for choosing or enabling a capability and provider.
5. **Measured observation:** volatile runtime facts such as quota, version, current availability, latency and health.

Therefore procedure source ≠ index, declared ≠ measured, catalog ≠ routing policy, and volatile observations must not be written into static capability truths. A generated index should be rebuildable after deletion. If a procedure is a multi-file package, the package digest should cover normalized relative paths, file bytes and stable ordering.
