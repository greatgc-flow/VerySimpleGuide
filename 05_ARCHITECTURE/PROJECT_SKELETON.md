# Illustrative Project Layout

This is a **logical role map**, not an imposed folder standard:

```text
project/
  kernel/          # essential CORE
  modules/         # required scope modules
  extensions/      # optional or milestone capabilities
  adapters/        # external boundary roles, optionally under extensions
  schemas/
  config/
  data/
  generated/
  tests/
  delivery/
    build/
    gates/
    evidence/
```

For stable existing products, freeze a logical component registry and dependency tests first; migrate source paths incrementally with behavior-preserving proof instead of large eager file moves.
