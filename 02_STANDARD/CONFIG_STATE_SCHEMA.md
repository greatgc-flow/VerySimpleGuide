# Configuration, State and Schema Standard

## Default precedence
`explicit CLI > explicit environment > project/local > user/product > declarative defaults`. A product may adapt this order if it owns and documents exactly one deterministic resolution policy.

## Merge semantics
By default scalar, object and array values all use **REPLACE**. `MERGE`, `APPEND` or `SET_UNION` are permitted only when declared for the precise key/schema; never silently deep-merge nested objects.

## Value distinctions
`ABSENT` (no key), `NULL` (explicit null), `EMPTY_STRING` (`""`), `EMPTY_ARRAY` (`[]`) and `UNKNOWN` (unmeasured/unavailable fact) are independent states. Avoid implicit coercion.

## Independent state dimensions
**Kind:** `CONFIG`, `DOMAIN_DATA`, `EVIDENCE`, `LOG`, `CACHE`, `TEMP`, `BACKUP`, `SCHEMA`, `SECRET`, `EXTERNAL_REF`.

**Recovery class:** `AUTHORITATIVE`, `DURABLE_DERIVED`, `REBUILDABLE`, `EPHEMERAL`, `EXTERNAL`.

Examples: an immutable original record is `DOMAIN_DATA + AUTHORITATIVE`; accepted derived knowledge is `DOMAIN_DATA + DURABLE_DERIVED`; a work/search index is `DOMAIN_DATA + REBUILDABLE`; a context pack is `CACHE + EPHEMERAL`; a remote task handle is `EXTERNAL_REF + EXTERNAL`.
