# Data Safety Standard

Classify named state using [kind and recovery class](CONFIG_STATE_SCHEMA.md), plus the orthogonal `secret` sensitivity flag. Apply policy in this order: ownership/authority establishes who may act; recovery class determines preservation; kind selects handling; sensitivity adds confidentiality safeguards. A CACHE/TEMP label never downgrades authoritative data, and SECRET kind always requires secret handling even if its flag is absent or false.

| Recovery class | Preservation default |
|---|---|
| AUTHORITATIVE | Protect recoverable content by default. |
| DURABLE_DERIVED | Retain according to policy with source provenance. |
| REBUILDABLE | Rebuild or optionally back up; prove regeneration under declared equivalence. |
| EPHEMERAL | Exclude by default after confirming no authoritative content. |
| EXTERNAL | Preserve handles/verification metadata; no implicit source deletion. |

Secret handling overlays every class: encrypt protected copies and control access, or use a documented separate recovery policy. Exclusion must preserve the authoritative recovery obligation through an approved alternative; sensitivity alone never permits silent data loss.

Backup success requires a complete manifest, verified authoritative hashes, reopening/read checks and declared exclusions. Restore: verify manifest → restore authority → verify schema/hashes → establish generation/fence → rebuild projections → reconcile external handles → invariant checks → activate.

Reset uses a classification-based preview and authorized plan, preserves external ownership by default and verifies actual removals. Uncertain deletion cannot report success.

AUTHORITATIVE state excluded from backup requires `recovery_alternative`: an approval decision, approver, alternative mechanism and restore evidence. A reference alone cannot establish recoverability.
