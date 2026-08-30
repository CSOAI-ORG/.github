---
title: Council MCP playground
emoji: 🛠
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: Live MCP tool rail. Not OpenAI chat, not ZeroGPU.
tags:
  - mcp-server
  - measurement
  - council-of-ai
---

# MCP playground — door

`tools/list` + `tools/call` against [`https://councilof.ai/mcp`](https://councilof.ai/mcp).
This is the architecture-doc API playground **without** hosting inference.

| Client | How to connect |
|---|---|
| Cursor / Grok | Add only [`https://councilof.ai/mcp`](https://councilof.ai/mcp) |
| MCP | `https://councilof.ai/mcp` |
| Live worker | `https://councilof.ai/mcp` |

Not an OpenAI-compatible router. Measurement, not certification.
CSOAI Ltd (UK 16939677).
