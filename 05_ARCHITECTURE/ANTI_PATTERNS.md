# Anti-patterns to Detect (Not a Prescriptive Tech Stack)

- Core branches on optional providers by name or imports extension implementation privately.
- An extension edits Core-owned database tables without a public port.
- An external task/session identity is stored as an internal work identity.
- Missing or unknown data becomes zero, unlimited, healthy or supported.
- A query projection is treated as the authoritative source.
- A durable artifact reference is created before its blob is committed.
- A release is declared stable before its gates finish, or an artifact is rebuilt after validation.
- A public CLI default flips with only new-CLI unit tests and no legacy compatibility run.
- Process failure isolation is advertised as malicious-code security isolation.
- A plugin marketplace or generic runtime is built without proven shared needs.
- Old command names are resurrected only for symmetry.
- Human diagnostic text leaks into JSON-only stdout.

These are review prompts. Record context, alternatives and exceptions when a different trade-off is demonstrably appropriate.
