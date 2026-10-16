# SSOT and Human-View Drift Control

Machine-readable SSOT is authoritative; README, help, diagrams and reference views must be generated from it or covered by explicit drift checks. Execute **all blocking semantic lint before** producing `PASS`, not afterward.

Check stale maturity/distribution statuses, obsolete standard versions, retired terminology and conflicting human descriptions. `COMPLY` in a mapping is not proof of implemented or verified behavior. MANIFEST.json alone records inventory and excludes itself. Matching bytes/hashes detect accidental change, not provenance or semantic correctness; separately test schema validity, crossreferences and negative controls.
