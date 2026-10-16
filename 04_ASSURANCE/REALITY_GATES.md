# Reality Gates

Use representative real-environment gates wherever deterministic or unit CI cannot establish operational claims. Examples: actual external CLI/provider, clean OS or sandbox, file-locking/antivirus/share semantics, network/TLS/proxy behavior, stable-to-candidate upgrade, installation/uninstallation and package-manager integration.

Every reality gate needs exact candidate identity and fresh evidence. A pass on an older commit or another artifact is **not** a pass on the current candidate. Explicitly preserve unsupported, unavailable and skipped conditions rather than manufacturing green results.
