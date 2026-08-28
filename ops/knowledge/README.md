# Shared agent knowledge / outreach DB

**Path:** `ops/knowledge/outreach.sqlite`  
**Purpose:** single place for overnight (and daytime) agents to map outward surfaces, outreach, accounts, and per-axis publish state — avoid duplicate publishes and silent owner-gates.

## Tables

| Table | Role |
|-------|------|
| `surfaces` | Live URLs / status (HF, MCP, A2A, directories, Kaggle) |
| `outreach` | Outbound moves (email, PRs, listings) + `owner_gate` + `cost_usd` |
| `accounts` | Service accounts activated under `nicholas@csoai.org` / Nick |
| `axis_publish` | 14 GSPC board axes → HF dataset + Kaggle mirror status |
| `agent_moves` | Append-only agent bcId / move log |

## Canon lock

- Quotable board = **14** axes. Public ruling = live `totals.public_count` from https://councilof.ai/api/gspc  
- Do **not** invent “22 axes.”  
- Never remint HF DOIs (`10.57967/hf/10114`, `10.57967/hf/10116`).  
- ClaimGuard + banned-strings before public.

## Money confirm (do not spend without Nick)

Rows with `owner_gate=1` in `outreach`: HF Team/ZeroGPU Space runtime · RunPod overnight burn · G-Cloud Cyber Essentials fee · domains ~£30.

## Secrets

Never store passwords or API tokens in this DB or in git. Session secrets only under `/tmp/csoai-secrets/` (chmod 600).
