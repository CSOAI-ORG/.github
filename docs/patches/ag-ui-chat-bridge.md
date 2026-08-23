# Patch: ag-ui.html chat → POST /api/chat (via parent postMessage)

Apply to `csoai-static-deploy2/ag-ui.html` on branch `cursor/agui-chat-bridge-ff6e`.

When embedded in `councilof.ai/ag-ui`, the static AG-UI asks the parent `AgUiBridge` to proxy chat to `POST /api/chat` — same contract as Council Lobby (`grounded` / `live` / `refused`).

Falls back to local keyword answers when not embedded.

See `docs/CHAT_AGUI_OPENROUTER.md` for architecture.
