# Interoperability, Runtime Choice and Polyglot Contract

**The semantic contract is portable; a reference schema serialization or test harness is not a language or platform mandate.**

## Profiles
Products declare chosen capabilities in an `implementation-choice` record (language/runtime/OS/storage/transport/deployment/contract/evidence runner); entries are arrays with no fixed allowed-vendor list. Empty arrays are allowed for domain-irrelevant categories; missing vs empty must be deliberate. A chosen single-platform deployment can be perfectly conformant if it is a **local, justified constraint**.

## Contract design
- Separate behavior/semantics from transport encoding. JSON Schema is the shipped reference for **interchange/validation fixtures**, not an obligation to use JSON as an internal storage representation. YAML/TOML/CUE/Protobuf/Avro/IDL etc. MAY be used with lossless or explicitly documented mappings.
- Version public schemas, expose declared capability/version negotiation where relevant, and run consumer/provider contract tests. `--json` output restrictions apply only when the product declares a JSON CLI mode.
- Use external protocol adapters only when interoperating with external systems. In-process methods, embedded libraries, IPC and shared-memory implementations are not banned.
- Release/test artifacts can be multiple architectures/runtimes: define a frozen `artifact set` whose members each have exact digest/target/gate evidence.
- Unknown fields: strict validation of the **common namespace**; product-specific innovation in a namespaced `extensions` bag (see component registry and extension manifest). Register and version new common semantic values deliberately rather than silently accepting typos.
- Make protocol/routing/orchestration separation a design **default**. A tiny application MAY combine these behind one module as long as authority, policy, side-effect and evidence boundaries remain explicit and independently testable.

## Reference-only technology families
OpenAPI/AsyncAPI/Protobuf/gRPC; OpenTelemetry; OpenFeature; SLSA/in-toto; CycloneDX/SPDX; WebAssembly/WASI; policy engines; CUE/JSON Schema; containers/VMs/edge/serverless; agent-to-agent and tool-facing protocols are **candidate technologies** only. Product fit must be proven. Do not imply OpenTelemetry, OpenFeature, OpenAPI, Kubernetes, Python, GitHub or any vendor is required.
