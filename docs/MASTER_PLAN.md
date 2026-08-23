# Master plan — living Moody’s × LM Arena × AG-UI (one system)

**Goal:** One surface where a human (or agent) asks, and the instrument **measures / verifies / ranks** — Moody’s-style living grades + LM-Arena-style live contest UX + AG-UI wire — without inventing counts or selling Elo as a public verdict.

**Truth rail (non-negotiable):** `https://councilof.ai/api/gspc`  
Axis names: [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md) · Estate map: [`ESTATE_INVENTORY.md`](ESTATE_INVENTORY.md)

---

## Product formula (what “one system” means)

| Layer | Role | Steal from | Never do |
|---|---|---|---|
| **Moody’s** | Living scorecard: axis grades, Wilson intervals, SEPARATED/TIE/UNTESTED, signed stamp | `scorecard.html` (“Moody’s of AI”), LivingBoard | Preferance Elo as the public grade |
| **LM Arena** | Live contest UX: enter a model, battle, watch rooms | `/arena`, Coliseum, MCP `enter-arena` | Replace law-graded / McNemar ranking with vote Elo |
| **AG-UI** | Ask → tool run → HITL consent → ledger | `csoai-agui-wire` + CouncilLobby | Let the UI author grades |

**Ask → does it** path:

```
User/agent ask
  → AG-UI session (L1 SSE: /session /run /consent /ledger)
    → MCP tools (L0): measure | verify | jail-probe | enter-arena | claimguard.check
      → Living board API + signed receipts (did:web:csoai.org)
        → Moody’s scorecard / LivingBoard render (predicates only)
```

“RAS AG UI” in this plan = **Receipts + Arena + Scorecard** over the **AG-UI** wire (no separate RAS product string found in the estate).

---

## Execution order (weekend scale gate)

### Phase 0 — Stop track-loss (this repo + claim landings)
1. Keep axis canon + this plan in git (done / updating).
2. Land **ClaimGuard** as real code (`CSOAI-ORG/claimguard` or under `carder`) — session demo is **not** in any org tree yet.
3. Wire ClaimGuard into CI + chat (`/api/chat` already drifts vs `totals.public_count`).

### Phase 1 — Apex = fat product (blocks everything else)
**Problem:** `councilof.ai` serves a thin ~7KB shell; lobby / scorecard / honesty / verify / ledger are **REAL 404**. Fat prerender lives on `csoai-site.pages.dev`.

**Do:** Restore fat `councilof-ai` + static-deploy allowlist to apex so `/lobby`, `/scorecard`, `/honesty`, `/verify`, `/live-ledger` are 200 on the brand domain.

**Done when:** `curl -sI https://councilof.ai/lobby` and `/scorecard` are 200, and LivingBoard mounts on home.

### Phase 2 — AG-UI live on same origin
1. Deploy `csoai-agui-wire` under `councilof.ai/agui` (or Worker), not orphan GH Pages.
2. Point `.well-known/mcp.json` + catalog at real MCP worker tools: `measure`, `verify`, `jail-probe`, `enter-arena`.
3. Lobby deep-links (`lobbyLink.ts`) open the same session grammar.
4. HITL before any write that claims a grade.

**Done when:** Ask “what’s the governance leader?” → tool call → board row, not hallucinated count.

### Phase 3 — HF / Kaggle / Codabench 100/100 (then scale N-sites)
1. **P0:** Rewrite `csoai/gspc-xr` card (currently DET clone).
2. Ship HF Spaces for `gspc-affect` + `gspc-jail`.
3. Axis-card parity: tags, `task_categories`, Zenodo method DOI `10.5281/zenodo.21991104`.
4. Rebuild `gspc-normalized` (care / affect / jail).
5. Codabench README + seal before practice phase 2026-09-01.
6. Diff HF ↔ Kaggle for XR contamination.

**Done when:** All 14 axis datasets pass carder valves; affect+jail Spaces live; method DOI on cards.

### Phase 4 — One N-site engine, then fan-out
1. Extract shared AEO/AGUI pack from richest shells (`openmoe-site`, `landlaw-site`) — not 27 divergent `index.html`s.
2. Prove once: openmoe → landlaw → diyhelp.
3. Industry pack fan-out (fintech → healthtech → govtech → regtech → care).
4. Defer long-tail recreational sites until pack is single-sourced.

**Do not** treat ~356 MCP repos as readiness — GSPC SoT + receipts + apex AG-UI is the gate.

---

## What is already real (use it)

| Asset | Where |
|---|---|
| Living board API | `councilof.ai/api/gspc` |
| MCP measure/verify/jail/arena | Worker via `councilof.ai/.well-known/mcp.json` |
| Arena contest UX | `councilof.ai/arena` (live) |
| Scoreboard / benches | `/gspc-scoreboard`, `/*bench` (live) |
| Moody’s scorecard HTML | `csoai-site.pages.dev/scorecard` (fat host) |
| AG-UI wire + catalog | `CSOAI-ORG/csoai-agui-wire` (code; not on apex) |
| Lobby / LivingBoard | `councilof-ai` client (code; apex thin) |
| N-site #3 pattern | `flywheel-nsite` (CI live) |
| 14 HF axis banks + Kaggle mirrors | org `csoai` / user `nicktempleman` |
| Receipt stack | `signed-receipts`, `inspect-receipts`, `carder`, draft `a2a-signed-receipts` |

## What is chat-only / dark (land or kill)

| Claim | Status |
|---|---|
| ClaimGuard product | Session only — **land in git** |
| Elo league as GSPC ranking | **Reject** for public board; optional internal Honesty ladder only |
| “16 measured axes” | **False** — 14 board + 2 in-lane honesty |
| Apex lobby / AG-UI / scorecard | Coded, **404 on brand domain** |
| Dashboard SaaS | Undeployed; spare UI only |

---

## Agent ownership (parallel lanes)

| Lane | Owns | Repo home |
|---|---|---|
| A — Apex + lobby | Fat deploy, LivingBoard on home | `councilof-ai`, `csoai-static-deploy2` |
| B — AG-UI wire | `/agui`, SSE, consent, ledger | `csoai-agui-wire` |
| C — ClaimGuard | Product + CI + MCP tool | new `claimguard` or `carder` |
| D — HF 100/100 | Cards, Spaces, DOI, normalized | HF `csoai` + `carder` |
| E — N-site pack | Shared AEO shell | extract from `*-site` |

This agent (`.github`) keeps **canon + plan + inventory** so every lane shares one count rule.

---

## Success criteria (one sentence each)

1. Ask on `councilof.ai` → AG-UI runs `measure`/`verify` → LivingBoard updates from signed API.
2. Public grade = Moody’s-style axis row (Wilson + separation), never vote Elo.
3. Arena feels like LM Arena; receipts stay law-graded / deterministic.
4. ClaimGuard fails any overclaim that would have failed this week’s session.
5. HF 14/14 cards + Spaces clean → then N-sites scale from one pack.
