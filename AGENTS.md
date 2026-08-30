# AGENTS.md

## Cursor Cloud specific instructions

This repository (`CSOAI-ORG/.github`) is primarily the GitHub org profile plus
community-health defaults and docs. It is **not** a package or deployable site
(see `ESTATE.md` — the SPA, DID keys, and measurement packages live in other
repos). Two things here are actually runnable:

### 1. ClaimGuard — Python CLI product (`products/claimguard/`)

This is the main testable/runnable application: a claim-vs-signed-artifact
integrity checker (Ed25519 over RFC 8785 canonical JSON).

- Runs on the system Python (`/usr/bin/python3`, 3.12). Dependencies
  (`cryptography>=42`, `pytest`) are installed into the user site
  (`pip install --user ...`) by the update script — no virtualenv is used.
- `pytest` is installed to `~/.local/bin`, which is **not on PATH**. Invoke it
  as `python3 -m pytest`, not bare `pytest`. Same for the `claimguard` console
  script — prefer `python3 claimguard.py ...`.
- The module imports are flat (`import claimguard`, `import canonical`), so run
  all commands **from inside `products/claimguard/`** (the tests insert the
  package dir onto `sys.path`, but the CLI relies on cwd):

  ```bash
  cd products/claimguard
  python3 claimguard.py --self-test      # signature-holds / mutation-fails demo
  python3 -m pytest -q
  python3 claimguard.py check --live     # fetches https://councilof.ai/api/gspc
  python3 claimguard.py check --live --claim "16 measured axes"   # must FAIL
  ```

- Quote `totals.public_count` from the living GET. Do not freeze 13/14 or 15/22
  in this file. Cursor / Grok MCP is `https://councilof.ai/mcp`.
- Exit code `0` = PASS, `1` = FAIL (by design — mutated boards / overclaims
  must fail). CI equivalent lives in `products/claimguard/.github/workflows/claimguard.yml`.

### 2. Live audit scripts (`scripts/*.mjs`)

- Pure Node (v22), no npm dependencies — they use built-in `fetch`. Nothing to
  install.
- `node scripts/run-frontend-audit.mjs` and `node scripts/e2e-integration-stack.mjs`
  are **read-only audits against the live production host** `https://councilof.ai`
  (override with `--host`). They exit `1` when the live site's current state
  drifts from the audit's expectations. A non-zero exit here reflects the live
  deployment, **not** a broken local environment — do not try to "fix" the site
  from this repo.

### Lint

There is no configured linter (no ESLint/ruff/flake8/pre-commit). The only
quality gates are the ClaimGuard self-test + `pytest`. For a quick syntax
sanity check use `python3 -m py_compile <file>` and `node --check <file>`.
