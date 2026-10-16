# Twelve Lifecycle Stages × Ten Cross-Cutting Concerns

The objective is to expose missing value, owners, transitions and retirement obligations—not to inflate the number of process steps. The 120 cells in `lifecycle-matrix.json` are **reviewer prompts**, not implementation orders.

- **Vertical:** `DISCOVER`, `ASSESS`, `INITIATE`, `SPECIFY`, `DESIGN`, `IMPLEMENT`, `VERIFY`, `RELEASE`, `OPERATE_SUPPORT`, `IMPROVE`, `EVOLVE`, `RETIRE`.
- **Horizontal:** `OUTCOME_VALUE`, `USERS_ACCESSIBILITY`, `RISK_SECURITY`, `ARCHITECTURE_DEPENDENCIES`, `DATA_PRIVACY`, `QUALITY_ASSURANCE`, `RELEASE_SUPPLYCHAIN`, `OPERATIONS_RELIABILITY`, `ECONOMICS_SUSTAINABILITY`, `GOVERNANCE_EVIDENCE`.
- **Recursive scopes:** product, milestone, component, public interface, mutation, release and retirement; keep records proportionate.
- **Variants:** UI-only, embedded, library-only, research-only, automation and batch products can choose reasoned `N_A` or `OPTIONAL` entries.

For project use, record twelve stage decisions and ten concern decisions. Review interactions and create `cell_overrides` only where the default combined decision hides an important risk. If a PASS claim lacks evidence for the exact intersection, keep it `REQUIRED` or `DEFERRED`. The sample JSON is not production evidence.
