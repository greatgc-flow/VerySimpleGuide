# External Protocol Adapter Standard

1. External task, artifact, message, session and context identities are **not** internal domain identities.
2. Persist external objects by `protocol + opaque remote identity + evidence references` rather than pretending they are locally owned.
3. Label a remote artifact `REFERENCE_ONLY` until verified ingestion yields an independently owned copy.
4. Label capabilities `DECLARED` or `MEASURED` per the [provider capability standard](PROVIDER_CAPABILITY_STANDARD.md).
5. Adapters use public domain/application ports instead of mutating storage privately.
6. Negotiate or configure versions/capabilities at the adapter boundary, not in Core-specific vendor branches.
7. Do not copy a remote service's complete lifecycle into the internal domain state machine.

## Stateless protocols and explicit handles
Protocols may be stateless or carry request-local metadata. Never equate transport-connection lifetime with durable work/session lifetime. Pass required internal and external handles explicitly through parameters or references; avoid hidden connection-scoped source-of-truth state.
