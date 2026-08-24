# CRITICAL patch — resolve committed merge conflict in `client/src/App.tsx`

**Target:** `CSOAI-ORG/councilof-ai` · **Severity:** high (breaks the client build)

## What's wrong on `master`
`client/src/App.tsx` has **committed `git stash` conflict markers** (`<<<<<<< Updated
upstream` / `=======` / `>>>>>>> Stashed changes`, lines ~672–926). This is not
just a type error — the literal markers are invalid TS/JSX, so **`npm run check`
(`tsc --noEmit`) and the Vite client build both fail** on master. Discovered while
validating [councilof-ai#424](https://github.com/CSOAI-ORG/councilof-ai/pull/424)
(my `/api/detect` change is clean; this is pre-existing and unrelated).

## The fix (this patch)
`appfix-App.tsx.patch` removes the three markers and keeps the **"Stashed changes"**
side (the newer, audited version — it carries the `audit §0.2` comments and security
hardening), re-indented to match the surrounding routes. Verified:
- `git apply --check` applies cleanly to a fresh `master`.
- `tsc --noEmit` then reports **zero** errors in `App.tsx` (0 conflict markers).

Apply:
```bash
git apply docs/patches/councilof-ai-appfix-conflict/appfix-App.tsx.patch   # from councilof-ai root
npm run check   # App.tsx now clean
```

## DECISIONS TO CONFIRM (why I kept "Stashed changes")
The two sides differ semantically — please confirm these are the intended behaviours
(the "Stashed" side, which I kept, is on the right):

| Route | "Updated upstream" | **"Stashed changes" (kept)** |
|---|---|---|
| `/workbench` | `Workbench` (open) | **`RequireAuth`-gated `Workbench`** (security) |
| `/sov3` | redirect → `/workbench` | **`Workbench` component** |
| `/sovereign` | redirect → `/me` | **`SovereignHub` component** |
| `/csoai-law` | present (alias of MeokLaw) | **absent** (dropped) |

If any of these should follow the "upstream" behaviour instead (esp. the
`/csoai-law` alias, easily re-added), say so and I'll adjust. The security-relevant
one is `/workbench` auth-gating — the kept side is stricter.

## NOT fixed here — deeper pre-existing breakage the client also has (owner-only)
Removing the markers exposes breakages that were hidden behind the invalid syntax.
These are **missing files not committed to the repo** — I will not fabricate core
app infrastructure by guessing:

1. **Missing `client/src/components/RequireAuth`** — `App.tsx` imports it on line 5
   and uses it **12×**, but the file is absent. This alone breaks the Vite client
   build (esbuild can't resolve the import), independent of the conflict.
2. **Missing `server/` backend / `server/routers`** — `client/src/lib/trpc.ts`
   imports `AppRouter` from `../../../server/routers`, but **no `server/` path is
   tracked in the repo** (it is not gitignored — simply absent). This dangling
   `AppRouter` type is the **root cause of the tRPC errors** in `Support.tsx`,
   `VerifyCertificate.tsx`, `WatchdogIncidentReport.tsx` (they resolve to the
   "property collides with a built-in method" guard type). It is **not** a
   router-key rename — the whole backend module is missing.
3. Pre-existing `Compare` lazy-component typing on `/vs*` routes (both conflict
   sides had it).

**Implication:** `master`'s client currently cannot build or typecheck. This patch
fixes only the committed merge-conflict markers (one clear defect). Restoring
`RequireAuth` and the `server/` backend (or correcting those imports) is an
owner action — likely those live in a separate package or were left uncommitted.
The **Functions** layer (`functions/api/*`, which actually serves the API incl.
`/api/detect`) is independent of this client breakage and builds fine.

## Why a patch, not a PR
`App.tsx` (~1200 lines) is too large to push reliably via the API path available to
this run (git push is denied to `cursor[bot]`; only the MCP file API works, which
needs full-file inline content). Apply the patch, or grant `cursor[bot]` git write
and I'll push it directly.
