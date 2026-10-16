# Data Safety Standard

## Backup policy by recovery class
- `AUTHORITATIVE`: protect by default.
- `DURABLE_DERIVED`: protect according to retention policy while preserving source provenance.
- `REBUILDABLE`: optionally back up or rebuild after restore.
- `EPHEMERAL`, cache and temp: exclude by default.
- `EXTERNAL`: record reference and verification metadata; never delete external source data implicitly.
- `SECRET`: exclude or encrypt and handle through a separate documented policy.

Creating a file alone is not a backup success. Require a complete manifest, verified authoritative hashes, reopening/read verification and declared exclusions.

**Restore:** verify manifest → restore authority → verify schema/hashes → establish new generation/fence → rebuild projections → reconcile external handles → invariant checks → activate.

**Reset:** produce a state-classification-based plan before applying effects; offer preview, preserve externally owned state by default and verify what was actually removed. Avoid reporting false success when deletion is uncertain.
