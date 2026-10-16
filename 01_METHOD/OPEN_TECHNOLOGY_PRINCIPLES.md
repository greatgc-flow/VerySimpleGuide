# Open Technology: Invariants, Defaults and Examples

No language, OS, hosting model, database, runtime, CI provider or architecture style is globally mandatory. A project may impose a local constraint with source, owner, reason and revisit trigger. The shipped Python, PowerShell and JSON Schema tools are reference implementations; equivalent runners must preserve the same contract, fixtures and evidence semantics.

1. **INVARIANT:** an applicable safety, authority or security obligation is binding. Changing it requires versioned governance, not a silent exception.
2. **DEFAULT / HEURISTIC:** a recommended implementation or organization. Record a short reason and proportionate evidence for an alternative; routine choices need no experiment dossier.
3. **EXAMPLE / REFERENCE:** an illustration, serialization, folder or tool. Its presence creates no project obligation.

The applicable semantic responsibilities in the [unified standard](../02_STANDARD/UNIFIED_STANDARD.md) remain binding; organizing a project into exactly fifteen controls is a default. Map alternative organization to those responsibilities. Propose a versioned change for a real semantic gap through [evolution policy](../06_GOVERNANCE/EVOLUTION_POLICY.md).

Scale proof to uncertainty and impact. Materially uncertain or risky alternatives need a hypothesis, baseline, bounded budget/stop rule, falsifiable acceptance and exit/rollback plan; see [technology exploration](TECHNOLOGY_EXPLORATION_LOOP.md). A mature standard or one valuable experiment can justify adoption; repeated consumers are a heuristic for inventing bespoke generic frameworks.

Apply the [interface contract](../02_STANDARD/CLI_STANDARD.md) only to surfaces that exist. A CLI is optional. Core dependency rules belong to [component boundaries](../02_STANDARD/COMPONENT_BOUNDARY.md); cross-language transport and linking remain local choices. Identity-preserving promotion is per release target or artifact set, not one binary for incompatible platforms. [Rebuildability](../02_STANDARD/AUTHORITY_PROJECTION_STANDARD.md) uses declared equivalence, including nondeterministic and external inputs.
