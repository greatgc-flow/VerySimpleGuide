# Core-only Survivability

The minimum release test for optional extensions is:
1. Disable/remove every optional extension.
2. Exercise baseline help, version, configuration, required read paths and lifecycle smoke tests.
3. Verify authoritative Core state invariants.
4. Confirm no extension import is required for baseline startup.
5. Inject a broken extension and prove unrelated Core/Module functions remain functional.

Failure isolation does not by itself provide security isolation. Adapt the smoke surface to the actual product scope.
