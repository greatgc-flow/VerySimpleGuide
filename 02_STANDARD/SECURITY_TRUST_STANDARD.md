# Security and Trust Standard

- Public mutations define authenticated/authorized actor identity and exact effect scope.
- Bind approvals to an exact effect digest; make authorization single-use by default.
- Redact secrets from machine output, logs and evidence by default.
- Declared side effects include outbound data transfer (enrichment, downloads, fallbacks); an offline claim needs a network-denied check.
- Before widening access to a repository or archive, audit current content and its full retained history for secrets and private data.
- Verify supply-chain artifacts against source identity, digest and an explicit redirect/trust policy.
- Never interpret provider declarations or failure isolation as guaranteed security isolation.
- Forbid writable host mounts, unrestricted remote command execution and implicit deletion of external data by default; scoped explicit exceptions require authorization and safeguards.
