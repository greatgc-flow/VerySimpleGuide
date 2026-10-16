# Provider Capability Standard

Core and modules query capability descriptors rather than branching on provider names. Illustrative fields:

- `output_capture`: `DIRECT`, `EVIDENCE_FILE`, `NONE`.
- `network_control`: `BOOLEAN`, `PROFILE_ONLY`, `NONE`.
- `read_only_mount`: `SUPPORTED`, `UNSUPPORTED`, `UNKNOWN`.
- `max_parallel_instances`: integer or `UNKNOWN`.
- `isolation_level`: declared label with evidence reference.
- `supports_cancel`: true, false or `UNKNOWN`.

A provider's declaration is `DECLARED` capability; reality gates or measured observations establish what actually works. Keep the port intentionally small: `detect_capability()`, `describe_capabilities()`, `create(spec)`, `execute(instance, command_spec)`, `collect(instance, evidence_spec)`, `destroy(instance)`. Mark unnecessary operations `N_A` for the target capability.
