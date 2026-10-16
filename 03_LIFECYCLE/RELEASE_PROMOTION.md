# Release and Promotion Contract

**source candidate → identity freeze → BUILD ONCE → deterministic gates → reality/live gates → evidence index → PROMOTE THE SAME ARTIFACT**. [Distribution transitions](MATURITY_DISTRIBUTION.md) distinguish candidate publication, stable designation and withdrawal.

1. Verification and distribution refer to the same artifact identity. For multiple platforms, freeze an artifact set whose members each have an exact target, digest and gate result.
2. Never rebuild an unverified different artifact after passing release gates.
3. Creating a tag or release page is not a passing gate.
4. Do not promote to stable before all required real-environment gates finish successfully.
5. Timeout, stale evidence or cancelled runners produce `HOLD`, not implicit success.
6. Preserve source SHA, artifact digest(s), gate run IDs and timestamps in an evidence index.
