# Games · City · Coliseum as Hugging Face MCP Spaces

**Yes.** They should be Hugging Face Spaces, and those Spaces should speak MCP so N-sites and any agent client can call them. They must **not** become a second contest engine or a second board.

Truth rail: [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)  
Live worker: [`https://councilof.ai/mcp`](https://councilof.ai/mcp)  
Directory: [`connect/mcp/hf-play-spaces.json`](../connect/mcp/hf-play-spaces.json)  
**All products** (OS, ClaimGuard, Verify, RAS, FAQ, East-West, fabric, playground): [`HF_PRODUCT_MCP_FABRIC.md`](HF_PRODUCT_MCP_FABRIC.md) · [`connect/mcp/hf-product-spaces.json`](../connect/mcp/hf-product-spaces.json)

---

## What each Space is

| Surface | Live site | HF Space | MCP job |
|---|---|---|---|
| **Games** | [gspc-arena](https://councilof.ai/gspc-arena) (`/games` is 404 — games load into Council Space) | [`csoai/games-catalog`](https://huggingface.co/spaces/csoai/games-catalog) | Catalog + `enter-arena` + living totals |
| **City** | [city](https://councilof.ai/city) | [`csoai/council-city`](https://huggingface.co/spaces/csoai/council-city) | City door + `get_axis` / `measure` contract |
| **Coliseum / Arena** | [coliseum](https://councilof.ai/coliseum) · [arena](https://councilof.ai/arena) | [`csoai/council-coliseum`](https://huggingface.co/spaces/csoai/council-coliseum) | `enter-arena` + **16 jail families** (contract only) |

Patches: [`docs/hf-patches/spaces/play/`](hf-patches/spaces/play/).

The existing static printers on `games-catalog` and `council-space` stay as thin doors until the Gradio+MCP upload lands (overnight publish or `HF_TOKEN`).

---

## How MCP reaches “anywhere else”

```
N-site / Cursor / Claude / any MCP client
  → Hugging Face Space  (MCP badge / SSE)
      → https://councilof.ai/mcp   (measure · verify · jail-probe · enter-arena · board_totals · get_axis)
          → living board GET /api/gspc
          → fleet (3090/A100) for real runs
```

1. Add the Space at [huggingface.co/settings/mcp](https://huggingface.co/settings/mcp) (MCP badge).
2. Or point the client at the Space SSE URL in [`hf-play-spaces.json`](../connect/mcp/hf-play-spaces.json).
3. Or keep calling the worker directly — Spaces are a second door, not a second truth rail.

Gradio `demo.launch(mcp_server=True)` exposes each typed function as a tool. Functions proxy JSON-RPC; they do not grade.

---

## 16 jails

`jail-probe` on the live worker takes `family` **1–16**. The Coliseum Space lists those families and returns the **contract** (`measured:false`). Sandbox execution stays on the fleet. That is the 16-jail surface — not 16 board axes.

---

## What this is not

- Not 22/22 measured (living board is slots vs measurements — quote `totals.public_count`)
- Not a public Elo league
- Not certification
- Not a GPU contest hosted on the Space (no ZeroGPU required)

---

## Publish

```bash
export HF_TOKEN=hf_...   # write on org csoai
bash scripts/publish-play-spaces.sh
```

Overnight path: `scripts/overnight-hf-publish.sh` also copies the play Spaces when `HF_TOKEN` is set.
