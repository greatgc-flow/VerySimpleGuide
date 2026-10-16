# Deprecation and Retirement

Do not confuse feature disposition with implementation maturity. Document each legacy item using a deliberate disposition: `RETAIN`, `ABSORB`, `SUPERSEDE`, `EXTENSION`, `DEFER`, `PASS` or `RETIRE`.

The fact that a historical command or source file exists is not a reason to reimplement it. If it violates the new authority or component boundary, absorb useful lessons and tests while superseding the implementation. Retirement additionally requires documented effects on users, external dependencies, data, permissions, retention obligations and rollback support.
