# Every product is a Space that MCP to Council OS — anywhere

**Yes.** ClaimGuard, RAS, FAQ, East-West, Verify, Council Space, Council OS, the fabric index, Games, City, Coliseum, and the MCP playground are Hugging Face Spaces. Each Space speaks MCP so an N-site, Cursor, Claude, or any agent can reach **Council OS** without hosting a second engine.

Truth rail: [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)  
Live worker: [`https://councilof.ai/mcp`](https://councilof.ai/mcp)  
OS: [`https://councilof.ai/os`](https://councilof.ai/os)  
Directory: [`connect/mcp/hf-product-spaces.json`](../connect/mcp/hf-product-spaces.json)

Play subset (Games / City / Coliseum): [`HF_PLAY_MCP_SPACES.md`](HF_PLAY_MCP_SPACES.md)

---

## What we took from the architecture audit

The uploaded Council OS TODO (`CSOAI_Council_OS_Full_TODO_and_Architecture.md`) is right that **Hugging Face Spaces are the client layer** (audit §6.1) and that **Tiny Agents / MCP clients are a while-loop on this rail** (audit §1.3 D). Phase 1.2’s five demo Spaces map like this — we keep the form, not the invented engines:

| Audit Space | What we ship | Why |
|---|---|---|
| Council-AI-Demo + ZeroGPU | **Council OS door** (`csoai/council-os`) | Inference stays on Council OS / the fleet. Spaces do not load models. |
| Council-OS-Leaderboard + Elo | **Living board** on every door (`board_totals`) | No public Elo league. Quote `totals.public_count`. |
| Blockchain-Verifier | **GSPC Verify** (`csoai/gspc-verify`) | Ed25519 `verify_card` at `/gspc-verify/`. Not Ethereum theatre. |
| PDCA-Cycle-Visualizer | *not a product* | No PDCA surface on the living estate. Do not invent one. |
| Council-AI-API-Playground | **MCP playground** (`csoai/council-mcp-playground`) | `tools/list` + `tools/call` on the live worker. Not OpenAI `/v1/chat`. |

Docker, Kubernetes, CRM, and an OpenRouter-shaped router stay out of these Spaces.

---

## How MCP reaches Council OS from anywhere

```
N-site / Cursor / Claude / Hugging Face MCP / any agent
  → Product Space  (MCP badge / SSE)
      → https://councilof.ai/mcp
          → Council OS / city / coliseum / verify / lobby
          → living board GET /api/gspc
          → fleet (3090/A100) for real runs
```

1. **Cursor / Grok:** add only `https://councilof.ai/mcp` ([`connect/mcp/cursor-grok.json`](../connect/mcp/cursor-grok.json)).
2. Hub product Spaces are live **static doors** (`*.static.hf.space`). They do not speak Gradio MCP while org CPU quota is 0.
3. Do not add `*.hf.space/gradio_api/mcp/sse` — those hosts 404 / pause.

---

## Product map

| Product | Live site | HF Space | MCP job |
|---|---|---|---|
| **Council OS** | [os](https://councilof.ai/os) · [lobby](https://councilof.ai/?lobby=home) | `csoai/council-os` | OS door + fabric list + living totals |
| **Council Space** | [gspc-arena](https://councilof.ai/gspc-arena) | `csoai/council-space` | Space door + `enter-arena` |
| **Games** | [gspc-arena](https://councilof.ai/gspc-arena) | `csoai/games-catalog` | Catalog + `enter-arena` |
| **City** | [city](https://councilof.ai/city) | `csoai/council-city` | City door + `get_axis` / `measure` |
| **Coliseum / Arena** | [coliseum](https://councilof.ai/coliseum) | `csoai/council-coliseum` | `enter-arena` + 16 jail families |
| **ClaimGuard** | [honesty](https://councilof.ai/honesty/) | `csoai/claimguard` | Living-board claim check + `verify_card` |
| **Verify** | [gspc-verify](https://councilof.ai/gspc-verify/) | `csoai/gspc-verify` | `verify_card` + `list_cards` |
| **RAS** | [lobby](https://councilof.ai/?lobby=home) | `csoai/ras-assess` | Receipts + Arena + Scorecard door |
| **FAQ** | [faq](https://councilof.ai/faq/) | `csoai/faq` | Living FAQ (counts not frozen) |
| **East-West** | [east-west](https://councilof.ai/east-west/) | `csoai/east-west` | 100-move door |
| **Fabric** | [mcp](https://councilof.ai/mcp) | `csoai/mcp-fabric` | Directory of every door |
| **Playground** | [mcp](https://councilof.ai/mcp) | `csoai/council-mcp-playground` | Live `tools/list` + `tools/call` |

RAS means **Receipts + Arena + Scorecard** over AG-UI — not a separate product brand.

---

## What this is not

- Not 22/22 measured (quote `totals.public_count`)
- Not a public Elo league
- Not certification
- Not ZeroGPU / on-Space inference
- Not a Docker/K8s control plane (that stays estate-side)

---

## Publish

```bash
export HF_TOKEN=hf_...   # write on org csoai
bash scripts/publish-product-spaces.sh
bash scripts/publish-play-spaces.sh
```

Until `HF_TOKEN` is in the environment, existing Hub printers stay **static**.

**Org runtime (2026-08-29):** `csoai` cpu-basic quota is **0**. New Gradio Spaces return 402; converted Gradio Spaces pause and cannot restart. All 12 product doors are therefore published as **live static Spaces** (RUNNING) that fetch `GET /api/gspc` in-page. MCP from anywhere is the worker [`https://councilof.ai/mcp`](https://councilof.ai/mcp). Gradio+MCP SSE on the org needs a Team/Enterprise CPU quota.

```bash
export HF_TOKEN=hf_...   # write on org csoai
bash scripts/publish-static-product-doors.sh   # live static doors (works today)
# bash scripts/publish-product-spaces.sh       # Gradio — only after org CPU quota > 0
```

Overnight path: `scripts/overnight-hf-publish.sh` copies product Spaces when `HF_TOKEN` is set.
