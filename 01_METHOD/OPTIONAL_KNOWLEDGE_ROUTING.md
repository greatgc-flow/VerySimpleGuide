# Optional Knowledge Routing

External style guides, design patterns, technology radars and industry standards are **reference candidates**. Their organizations' policies must not silently become mandatory General rules.

- **Pull, not preload:** load only metadata and index entries by default. Do not fill AI context or build inputs with entire external manuals.
- For each entry, record applicability, when to avoid it, alternatives, trade-offs, measurement and a recheck trigger.
- `ACTIVE` means the source is available, not that it is endorsed as the newest or best policy. `ARCHIVED` allows historical reference but not a claim of current authority.
- To adopt external guidance as `REQUIRED`, a project must explicitly record owner, scope, revision, verification and exit criteria.
- Named languages, clouds, database systems, CI products and AI agents remain examples and local choices.
- Adding guidance never implies adding a baseline Control or installing the referenced runtime in Core.
- Prefer existing standards/patterns before inventing a new one; document **Problem → Applicability → Avoid When → Alternatives → Trade-offs → Evidence → Retirement**.

Source-verification status is a dated snapshot; recheck when sources, risks or product context change. Data: `08_KNOWLEDGE/guidance-catalog.json` and `08_KNOWLEDGE/references/catalog.json`. The Python suggestion tool is a **read-only non-normative implementation**.
