# Crown-jewel verification — 2026-08-23 (read-only, grounded)

Verified live against the GitHub org `CSOAI-ORG` with a **read-only** token, to
separate confirmed facts from the DSH report's summary. Where the token can't see
something, it says so — the honesty gate applies to our own audit too.

> Counts/leaders defer to [`/api/gspc`](https://councilof.ai/api/gspc). This file
> records repo-infra facts, not board measurements.

## Org shape (verified)
- **500+ public repos** (list query capped at 500; org-metadata endpoint returned
  403/404 to this token, so exact total unconfirmed here).
- **352 repos with `mcp` in the name** — matches the canon's ~356 catalog-sprawl
  note. Per `GSPC_AXIS_CANON` / `MASTER_PLAN`, catalog count is **not** a
  readiness signal.
- **3 archived**, rest active.

## Crown jewels — existence + activity (verified)
All 16 named crown-jewel repos exist and are **actively pushed (0–5 days ago)** —
the estate is live, not abandoned:
`councilof-ai, csoai-static-deploy2, csoai-agui-wire, claimguard, flywheel-nsite,
signed-receipts, carder, inspect-receipts, a2a-signed-receipts, codabench-gspc,
brand-assets, csoai-dashboard, .github, gspc-axis-boards, gspc-packs-hub,
gspc-regional`.

## CI / security posture (verified via readable contents API)
| Repo | Workflows | Notes |
|---|---|---|
| `councilof-ai` | 14 | deploy, drift-guard, persona-gauntlet, claims-e2e, reg-watch, nightly_board, … — the CI spine |
| `csoai-static-deploy2` | 12 | incl. `security.yml`, canon-drift-guard, govbench-board, nightly-e2e |
| `csoai-dashboard` | 6 | ci, deploy, vercel-deploy, sync-mcp-registry |
| `claimguard` | 1 | `claimguard.yml` (self-test + pytest) |
| `flywheel-nsite` | 1 | flywheel-nsite.yml |
| `signed-receipts` | 1 | publish.yml |
| `inspect-receipts` | 1 | publish.yml |
| **`csoai-agui-wire`** | **0** | **no `.github/workflows` — no CI/tests** |
| **`carder`** | **0** | **no CI** (inventory calls it "Strong" — but untested in CI) |
| **`a2a-signed-receipts`** | **0** | no CI (DRAFT, matches inventory) |
| **`codabench-gspc`** | **0** | no CI (README missing, matches inventory) |

**Bigger risk than CodeQL:** four IP repos (`csoai-agui-wire`, `carder`,
`a2a-signed-receipts`, `codabench-gspc`) have **no CI at all** — no tests, no
security scan, no gates. `carder` (fact-cards/valves) and `a2a-signed-receipts`
are moat pieces; shipping them CI-less is the real exposure.

## CodeQL "5 flagged repos" claim — **UNVERIFIABLE from here**
The code-scanning API returns **403 "Resource not accessible by integration"** for
this read-only token. I **cannot** confirm or deny which repos had CodeQL
auto-disabled. Verifying it needs a token with `security_events` scope (owner
action). Recorded as UNVERIFIED rather than asserted.

## Safe moves — prepared, not fired
1. **Re-enable CodeQL (prepared):** drop this reusable workflow into each flagged
   repo's `.github/workflows/codeql.yml` (owner applies; I won't write to other
   repos from here):
   ```yaml
   name: CodeQL
   on:
     push: { branches: [main, master] }
     pull_request: { branches: [main, master] }
     schedule: [{ cron: "0 3 * * 1" }]   # weekly — also resets the inactivity clock
   jobs:
     analyze:
       runs-on: ubuntu-latest
       permissions: { security-events: write, contents: read, actions: read }
       steps:
         - uses: actions/checkout@v4
         - uses: github/codeql-action/init@v3
           with: { languages: "javascript-typescript,python" }
         - uses: github/codeql-action/analyze@v3
   ```
   The weekly `schedule` is what stops GitHub's "disabled due to inactivity" warning.
2. **CI-cold repos first:** prioritise adding *any* CI (test + CodeQL) to
   `carder`, `a2a-signed-receipts`, `csoai-agui-wire`, `codabench-gspc` — higher
   value than re-enabling CodeQL on already-gated repos.
3. **BSI / ORCID / Codabench activation:** external account actions — owner-only;
   this sandbox has no credentials for them.

## What I could not reach (owner-gated / not in sandbox)
- Code-scanning state (403), private-repo/org metadata, the `nicholas@csoai.org`
  mailbox, the SOVOS `NEXT-WEEK-REVENUE-IP-PLAN` doc, and any DSH/k3/RunPod host.
