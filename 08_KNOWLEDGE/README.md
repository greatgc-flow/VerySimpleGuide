# Optional Engineering Guidance, Patterns and References

**Goal:** find the smallest relevant guidance, explain its applicability, compare alternatives, test its trade-offs and keep the option to reject it.

```text
python tools/suggest_guidance.py --stage OPERATE_SUPPORT --concern OPERATIONS_RELIABILITY
python tools/suggest_guidance.py --stage DESIGN
```

The tool is read-only and does not fetch external web pages. It mirrors displayed output when `--evidence-file` is provided. Python is a reference implementation, not a requirement for conformance.

- [`references/catalog.json`](references/catalog.json): authoritative URLs, owner/status and archive/review metadata.
- [`guidance-catalog.json`](guidance-catalog.json): problem, use/avoid conditions, alternatives, evidence and references.
- [`lifecycle-matrix.json`](../03_LIFECYCLE/lifecycle-matrix.json): twelve stages and ten concerns; `FOCUS` indicates attention, not mandatory tooling.
