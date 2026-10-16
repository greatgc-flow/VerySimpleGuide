# Public Cutover and Rollback Lifecycle

Track implementation maturity and **public-default cutover maturity** separately. A new engine may be `VERIFIED` while the public command still defaults to the legacy implementation.

Before changing the default, gate help/version parity, machine-output contracts, diagnostics and telemetry parity, safety/authorization behavior, existing scripts and automation, the entire public integration suite, and rollback-selector evidence.

Flip the default only after those requirements are met. The selector must not secretly migrate shared data back and forth or introduce uncontrolled side effects. After cutover, retain an explicit, tested recovery path for affected users.
