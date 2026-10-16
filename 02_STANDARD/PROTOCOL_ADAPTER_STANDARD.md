# External Protocol Adapter Standard

1. External task, artifact, message, session and context identities are **not** internal domain identities.
2. Persist external objects by `protocol + opaque remote identity + evidence references` rather than pretending they are locally owned.
3. Label a remote artifact `REFERENCE_ONLY` until verified ingestion yields an independently owned copy.
4. Advertised capability is `DECLARED`; successful execution, observed quota, latency and reliability require separate `MEASURED` evidence.
5. Adapters use public domain/application ports instead of mutating storage privately.
6. Negotiate or configure versions/capabilities at the adapter boundary, not in Core-specific vendor branches.
7. Do not copy a remote service's complete lifecycle into the internal domain state machine.

## Stateless protocols and explicit handles
Protocols may be stateless or carry request-local metadata. Never equate transport-connection lifetime with durable work/session lifetime. Pass required internal and external handles explicitly through parameters or references; avoid hidden connection-scoped source-of-truth state.
