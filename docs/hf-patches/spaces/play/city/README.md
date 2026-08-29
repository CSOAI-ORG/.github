---
title: Council City
emoji: 🏛
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: City door + MCP to councilof.ai/city. No second board.
tags:
  - mcp-server
  - measurement
  - council-of-ai
---

# Council City — MCP door

Live city: [councilof.ai/city](https://councilof.ai/city).
This Space MCP-connects City to N-sites and any agent client. It does not host a second city.

| Client | How to connect |
|---|---|
| Cursor / Grok | Add only [`https://councilof.ai/mcp`](https://councilof.ai/mcp) |
| MCP | `https://councilof.ai/mcp` |
| Live worker | `https://councilof.ai/mcp` — tools `board_totals`, `get_axis`, `measure` |

Living counts: [GET /api/gspc](https://councilof.ai/api/gspc). Measurement, not certification.
CSOAI Ltd (UK 16939677).
