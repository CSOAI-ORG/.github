---
title: GSPC Verify
emoji: ✅
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: verify_card MCP door to /gspc-verify/. Ed25519, not chain-toy.
tags:
  - mcp-server
  - measurement
  - council-of-ai
---

# GSPC Verify — MCP door

Live verify: [councilof.ai/gspc-verify/](https://councilof.ai/gspc-verify/).
MCP `verify_card` / `list_cards` for any site. Ed25519 over signed cards — not Ethereum cert theatre.

| Client | How to connect |
|---|---|
| Any MCP client | Add this Space at [huggingface.co/settings/mcp](https://huggingface.co/settings/mcp) |
| SSE | `https://csoai-gspc-verify.hf.space/gradio_api/mcp/sse` |
| Live worker | `https://councilof.ai/mcp` — `verify_card`, `list_cards` |

Measurement, not certification. CSOAI Ltd (UK 16939677).
