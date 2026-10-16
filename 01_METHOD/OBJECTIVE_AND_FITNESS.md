# Objective, Scope and Fitness

The standard is a tool for producing outcomes; document counts and test counts are not the goal. At initiation record:

1. **Problem and user outcome:** who is affected and what observable change is valuable.
2. **Scope and non-goals:** baseline, milestones and extensions; why each exclusion exists and when to revisit.
3. **Fitness signals:** user effect, safety, reliability, operational cost and maintainability where applicable; include definition, baseline, method, target and evidence source.
4. **Constraints and budgets:** compatibility, provider, runtime, regulations, trust boundaries, time, cost, token and resource ceilings.
5. **Acceptance authority:** who can ratify goals and trade-offs and who can change them.

Never invent an SLO or acceptance number. Mark unapproved values `UNRATIFIED`, and use `HOLD` when a required approval or measurement is missing.

**Very Simple fitness:** remove a feature, state or layer if its absence does not harm value or safety. Prefer evidence of repeated invariants before introducing custom generic abstractions, while allowing standards-based interoperability and small justified experiments. Optimize achieved outcomes, safety and lifetime cost rather than catalog size. Every new obligation must correspond to an outcome or demonstrated failure mode.

Design complete, implementation complete, verified, published, promoted and outcomes achieved are independent judgments. Limit any combined acceptance claim to its specific scope and candidate; record unverified dimensions as `UNKNOWN` or `HOLD`.
