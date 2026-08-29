---
title: ClaimGuard
emoji: 🛡
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: Claim check + verify_card MCP door. Not certification.
tags:
  - mcp-server
  - measurement
  - council-of-ai
---

# ClaimGuard — MCP door

Honesty: [councilof.ai/honesty/](https://councilof.ai/honesty/).
Thin living-board claim check + live `verify_card`. Full CLI is `products/claimguard`.

| Client | How to connect |
|---|---|
| Cursor / Grok | Add only [`https://councilof.ai/mcp`](https://councilof.ai/mcp) |
| MCP | `https://councilof.ai/mcp` |
| Live worker | `https://councilof.ai/mcp` — `verify_card`, `board_totals` |

Rejects a full-board-measured overclaim, “16 measured axes”, Elo-as-grade, certification language.
Quote [GET /api/gspc](https://councilof.ai/api/gspc) `totals.public_count`.
CSOAI Ltd (UK 16939677).
