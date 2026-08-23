# Patch bundle: OpenRouter + AG-UI E2E unification

**Target repos:** `CSOAI-ORG/councilof-ai` + `CSOAI-ORG/csoai-static-deploy2`  
**Branch names:** `cursor/openrouter-agui-e2e-ff6e` (councilof-ai), `cursor/agui-chat-bridge-ff6e` (static-deploy2)

## What this fixes

1. **Chat ≠ AG-UI clarified** — Council Lobby chat is the public surface; AG-UI is the 15-tab measurement front door; they now share `POST /api/chat`.
2. **`/ag-ui` no longer redirects to lobby** — `_redirects` + `place-end-user-aliases` treat AG-UI as its own prerendered route.
3. **`/agui` → `/ag-ui`** — common alias.
4. **Static `ag-ui.html` chat** — postMessage to parent `AgUiBridge` → grounded `/api/chat` (falls back to local keywords offline).
5. **OpenRouter stays in harness lane** — `openrouter_board.py` feeds `/api/gspc`; public chat uses SOV_GATE or grounded rules.

## Files changed (councilof-ai)

| File | Change |
|---|---|
| `client/src/pages/AgUiBridge.tsx` | Nav shell + postMessage `/api/chat` proxy |
| `functions/api/chat.ts` | CORS + OPTIONS for iframe |
| `public/_redirects` | `/agui` → `/ag-ui` |
| `scripts/generate-redirects.mjs` | Preserve agui rules |
| `scripts/place-end-user-aliases.mjs` | `ag-ui` / `agui` alias pages |
| `scripts/assert-prerender-live.mjs` | Check `/ag-ui`, `/models` |
| `scripts/e2e-integration-stack.mjs` | One-pass E2E smoke |

## Files changed (csoai-static-deploy2)

| File | Change |
|---|---|
| `ag-ui.html` | `council-chat-ask` postMessage → parent bridge |

## Apply

```bash
# councilof-ai — copy from docs/patches/councilof-ai-openrouter-agui/ or cherry-pick local commit 67bca94
# static-deploy2 — ag-ui.html postMessage block

# After gated deploy:
node scripts/e2e-integration-stack.mjs
```

## Owner: set `AGUI_WIRE_URL` on Cloudflare Pages for `/api/agui/*` (RunPod `agui_wire.py :8785`).

See [`CHAT_AGUI_OPENROUTER.md`](../CHAT_AGUI_OPENROUTER.md).
