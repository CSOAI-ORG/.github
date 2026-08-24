# Revenue surfaces — live sales inventory

**Host:** [`https://councilof.ai`](https://councilof.ai)  
**Audited:** 2026-08-24 (this file) · prior matrix [`FRONTEND_AUDIT_CHECKLIST.md`](FRONTEND_AUDIT_CHECKLIST.md)  
**Posture:** Measurement and verification are free. No fabricated ARR. Status below is HTTP reality on apex — not a wish list.

---

## Named sales surfaces

| Route | Role | Apex status (2026-08-24) | Notes |
|---|---|---|---|
| [`/pricing`](https://councilof.ai/pricing) | Buyer posture — free measure/verify, artefacts not seats | **404** when apex thin | Coded in stranger dirs; gated deploy / alias gap |
| [`/start`](https://councilof.ai/start) | Enterprise intake | **404** when apex thin | Use lobby ask until alias lands |
| [`/enterprise`](https://councilof.ai/enterprise) | Enterprise landing | **404** when apex thin | Same alias family |
| [`/government`](https://councilof.ai/government) | Public-sector landing | **404** when apex thin | Adjacent live: `/for/regulator` **200** |
| [`/regulators`](https://councilof.ai/regulators) | Regulator persona | **404** when apex thin | Prefer `/for/regulator` until fixed |
| [`/insurers`](https://councilof.ai/insurers) | Insurer reliance path | **404** when apex thin | Do not invent coverage language |
| [`/api-docs`](https://councilof.ai/api-docs) | Human API docs hub | **404** when apex thin | Agents use `/api/gspc` + MCP today |
| [`/gspc-verify`](https://councilof.ai/gspc-verify) | Verify (no slash) | **404** | Pretty URL missing |
| [`/gspc-verify/`](https://councilof.ai/gspc-verify/) | Verify (slash) | **Live 200** | **Always demo this form** |

### Supporting surfaces that close the demo

| Route | Status | Role in conversion |
|---|---|---|
| [`/`](https://councilof.ai/) · [`/?lobby=home`](https://councilof.ai/?lobby=home) | **Live** | Stranger → lobby ask (one OS door) |
| [`/gspc-scoreboard`](https://councilof.ai/gspc-scoreboard) | **Live** | Living board / “Moody’s” scorecard UX |
| [`/api/gspc`](https://councilof.ai/api/gspc) | **Live** | Truth rail JSON (14 / 13) |
| [`/arena`](https://councilof.ai/arena) | **Live** | Law-graded contests |
| [`/.well-known/mcp.json`](https://councilof.ai/.well-known/mcp.json) | **Live** | `measure` · `verify` · `jail-probe` · `enter-arena` |
| [`/os/`](https://councilof.ai/os/) | **Live** | Council OS shell |
| [`/assess`](https://councilof.ai/assess) · `/assess/` | **Live** | Signed assessment entry |
| `POST /api/chat` | **Live** (grounded asks) | Lobby ask path — ClaimGuard wire still open ([patch](patches/councilof-ai-claimguard-chat/)) |

---

## Apex thin vs fat

| Condition | Symptom | Sales implication |
|---|---|---|
| **Fat apex** | Homepage ≳ 20 KB, CouncilLobby chunk present | Full ask → board → verify → arena demo |
| **Thin apex** | ~7 KB shell; stranger routes 404 | Demo only `/api/gspc`, `/gspc-verify/`, MCP, arena if still 200 — **name the gap**, do not promise `/pricing` |

Root cause pattern: Pages Git auto-deploy clobbers gated prerender / missing `place-end-user-aliases`. See `councilof-ai` `DEPLOY-LOCK.md`.

When thin: treat `/pricing`, `/start`, `/enterprise`, `/government`, `/regulators`, `/insurers`, `/api-docs` as **coded, not sold**.

---

## Conversion path (honest)

```
stranger
  → verify free          https://councilof.ai/gspc-verify/
  → lobby ask            https://councilof.ai/?lobby=home
  → scoreboard           https://councilof.ai/gspc-scoreboard
  → enterprise           https://councilof.ai/start   (or lobby “start” ask while 404)
```

| Stage | Proof you show | Do not sell |
|---|---|---|
| Stranger | Brand home, “we measure” | Certification, Elo league |
| Verify free | Browser recompute + `did:web:csoai.org` | Account wall, fee for grade |
| Lobby ask | Axis question → grounded reply aligned to `/api/gspc` | Invented axis counts (“16”, “12”) |
| Scoreboard | 14 slots, 13 measured ruling | Preference Elo as public grade |
| Enterprise | Intake `/start` + signed assessment | Per-seat SaaS tiers |

**Money language (allowed):** signed evidence artefacts, assessment runs, enterprise onboarding — priced as artefacts / work, never as ranking placement.  
**Money language (forbidden here):** invented MRR, fake win rates, “X paying customers.”

---

## Persona → surface map

| Persona | Intended URL | Live fallback today |
|---|---|---|
| Buyer | `/pricing` | Lobby pricing ask + `/gspc-verify/` |
| Enterprise | `/start`, `/enterprise` | `/?lobby=home` + `/assess/` |
| Government | `/government` | `/for/regulator` |
| Regulator | `/regulators` | `/for/regulator` |
| Insurer | `/insurers` | Verify + board; no reliance warranty |
| API / agent | `/api-docs` | `/api/gspc` + `/.well-known/mcp.json` |
| Auditor | `/gspc-verify/` | Same (live) |

---

## Readiness gate

```bash
node scripts/weekend-demo-smoke.mjs
```

Sales-demo **PASS** requires living board API, verify slash route, MCP catalogue, and chat axis-ask grounded without overclaim drift. Stranger marketing routes may still FAIL independently — track them here, do not hide them.
