# Deprecation and Retirement

Choose a legacy feature strategy from `legacy_feature_strategies` in [unified-package-standard.json](../06_GOVERNANCE/unified-package-standard.json): `RETAIN`, `ABSORB`, `SUPERSEDE`, `EXTRACT_EXTENSION`, `RETIRE`. This describes its architectural destination, independently of completion status or evidence result. EXTRACT_EXTENSION must satisfy [component boundaries](../02_STANDARD/COMPONENT_BOUNDARY.md).

Historical existence does not justify rebuilding a command or file. Keep useful lessons/tests while superseding implementations that violate authority or component contracts. Track deferred decisions and closure through [feedback](../01_METHOD/OPERATIONAL_FEEDBACK_LOOP.md), rather than adding PASS or DEFER to feature strategies.

Before retirement, assess user notice/migration, external dependencies, data retention/deletion, permissions, residual risk and remaining recovery obligations under the [coverage standard](../02_STANDARD/LIFECYCLE_COVERAGE_STANDARD.md).
