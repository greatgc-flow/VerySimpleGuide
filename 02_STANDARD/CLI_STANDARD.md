# CLI and Public Interface Standard

## Universal public-interface obligations
For each existing UI, API, library, event or CLI surface, declare inputs, outputs, errors, compatibility, side effects, actor authorization and observable completion. Version the contract where relevant; test promised behavior and expose limitations. Discovery/help must be read-only. A success report requires the contracted effect and postconditions; diagnostics preserve uncertainty. No CLI is required for a product without one.

## CLI profile: product-local grammar
A lifecycle utility may use `<product> backup` or `<product> repair`; a domain system may prefer `<product> <noun> <verb>`. A globally identical command tree is **not required**.

## Public flags (when applicable)
- `--help` / `-h`: read-only for the public command.
- `--version`: read-only for a versioned root CLI.
- `--json`: if offered, stdout is exclusively machine-readable output; diagnostics go to stderr.
- `--dry-run`: no mutation; show the proposed effects and limits.
- `--apply`: explicit authorization when preview is the default.
- `--yes` / `-y`: bypass ordinary confirmation only, never safety, fencing, security or prerequisite gates.

The product must decide and test how `--dry-run` and `--apply` interact. Safe precedence or a usage error are both possible documented policies.

## CLI profile: semantic exit classes
- `SUCCESS`: contracted effect and postconditions completed.
- `USAGE`: invalid grammar, argument or schema input.
- `DECLINED`: the user chose not to proceed.
- `PRECONDITION_FAILED`: a necessary pre-execution condition was absent.
- `BLOCKED`: security, policy, fencing or authority rejected the operation.
- `VERIFICATION_FAILED`: postcondition or evidence validation failed.
- `ROLLED_BACK`: a started mutation was compensated or returned to a declared safe state.
- `RUNTIME_FAILED`: an external runtime, provider, I/O or environment failed.
- `INTERNAL_ERROR`: an implementation defect not captured above.

Numeric exit values may differ for legacy compatibility; publish the semantic-to-number mapping for each product.
