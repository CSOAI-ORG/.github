# One-door policy — Council OS is the AG UI

**Effective:** 2026-08-23 (`councilof-ai` commit `b2a9e89`, `one-door-guard.yml`)

## Rule

There is **one public OS door**: `https://councilof.ai/?lobby=home` (Council Lobby / Council OS).

These paths must **not** open a second console (no iframe of `csoai-site.pages.dev/ag-ui`):

| Path | Must |
|------|------|
| `/ag-ui` | 308 → `/?lobby=home` |
| `/agui` | 308 → `/?lobby=home` |
| `/chat` | 308 → `/?lobby=home` |
| `/sov-os` | 308 → `/?lobby=home` |

`AgUiBridge.tsx` and `SovOS.tsx` must be `<Redirect to="/?lobby=home" />` — enforced by `scripts/one-door-guard.mjs` in CI.

## What this supersedes

- PR #365 / #372 iframe bridge to static `ag-ui.html` — **reverted**; patch bundle in `docs/patches/` is historical reference only.
- E2E gate `scripts/e2e-integration-stack.mjs` now expects lobby redirect, not iframe 200.

## Static host role

`csoai-site.pages.dev/ag-ui` remains the **reference** AG UI shell (postMessage bridge for dev). It is not embedded on the brand domain.

## Wire lane

RunPod `agui_wire.py` (:8785) and `/api/agui/*` SSE wire into **Council OS lobby**, not a separate `/ag-ui` page.

See: [`CHAT_AGUI_OPENROUTER.md`](CHAT_AGUI_OPENROUTER.md), [`STEPS_200.md`](STEPS_200.md) Block K.
