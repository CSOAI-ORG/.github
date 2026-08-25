# Activation pack — owner fire-book (corrected)

You open sessions / confirm spend. Agents prepare + verify + update the living registry.

## £0 first (do these; no money)

| # | Action | Pre-check | You do | Agent verifies |
|---|--------|-----------|--------|----------------|
| 0a | MCP registry already **1.0.3** (14 of 14 desc) | Registry isLatest | Optional: restore ``CF_API_TOKEN` (+ `CF_ACCOUNT_ID`)` on deploy2 to redeploy worker 1.0.3 | Worker `initialize` reports 1.0.3 |
| 0 | **DO NOT mint HF DOIs** | Registry shows DOIs LIVE | — | Already `10.57967/hf/10114` + `10116` |
| 1 | Kaggle mirror of GSPC board | `export/kaggle-gspc-board/` exists; no LIVE kaggle row | Paste API token to `/tmp/csoai-secrets/kaggle.json` | Dataset page 200 · registry → LIVE |
| 2 | Discussion #97 one-liner | status GATED | Post with your GH session (2FA) | Comment URL · registry → LIVE |
| 3 | Insurance drafts send | drafts NOT_SENT | Decide send/hold per broker | Update outreach rows |
| 4 | Merge/nudge awesome-a2a #157 | SUBMITTED | Optional maintainer nudge | PR state |

## Costs money — CONFIRM before spend

| # | Action | Why | Confirm phrase |
|---|--------|-----|----------------|
| A | **RunPod / A100 (or 3090) restart** | Measurement volume for any UNMEASURED / scale work | `CONFIRM RunPod` |
| B | **HF Team / Space CPU** | Only way Gradio Space actually RUNS (limit=0) | `CONFIRM HF Team` |
| C | G-Cloud Cyber Essentials fee | Marketplace gate | `CONFIRM G-Cloud` |
| D | Domains ~£30 | cibola | `CONFIRM domains` |

## Recommended next

1. **Not DOIs** — already live.  
2. **Highest £0 leverage now:** Kaggle token (or Discussion #97 if you’re at the keyboard with GH).  
3. **Highest paid leverage:** `CONFIRM RunPod` / A100 if you want measurement volume overnight.  
4. **Only if Space must run (not just exist):** `CONFIRM HF Team`.

## After every step

1. Agent re-reads registry + sqlite  
2. HTTP / listing / DOI tag check  
3. Updates `registry/outreach-registry.json` + `ops/knowledge/outreach.sqlite`  
4. Appends `ops/overnight-register-2026-08-24.md`
