---
title: Games catalog
emoji: 🎮
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: Games door + MCP to Council Space. Not the engine.
tags:
  - mcp-server
  - measurement
  - council-of-ai
---

# Games catalog — MCP door

Games load into [Council Space](https://councilof.ai/gspc-arena) on councilof.ai.
This Space is a **door + MCP server**, not a contest engine.

| Client | How to connect |
|---|---|
| Any MCP client | Add this Space (MCP badge) at [huggingface.co/settings/mcp](https://huggingface.co/settings/mcp) |
| SSE | `https://csoai-games-catalog.hf.space/gradio_api/mcp/sse` |
| Live worker | `https://councilof.ai/mcp` — tools `enter-arena`, `board_totals` |

Living counts: [GET /api/gspc](https://councilof.ai/api/gspc) — quote `totals.public_count`. Do not freeze a table here.

Measurement, not certification. CSOAI Ltd (UK 16939677).
