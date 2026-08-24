# Weekend demo — 5-minute sales script

**Tone:** cream / ink. Calm. Measurement body, not a SaaS pitch deck.  
**Truth rail:** [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)  
**Canon:** [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md) · **Surfaces:** [`REVENUE_SURFACES.md`](REVENUE_SURFACES.md)

Smoke before the call: `node scripts/weekend-demo-smoke.mjs`

---

## Arc (ask → board → verify → arena)

| Minute | Move | Exact URL | What you open |
|---|---|---|---|
| 0:00–0:45 | **Ask** | [`https://councilof.ai/?lobby=home`](https://councilof.ai/?lobby=home) | Council Lobby (one public OS door) |
| 0:45–2:00 | **Board** | [`https://councilof.ai/gspc-scoreboard`](https://councilof.ai/gspc-scoreboard) | Living React board |
| 2:00–3:30 | **Verify** | [`https://councilof.ai/gspc-verify/`](https://councilof.ai/gspc-verify/) | Trailing slash required |
| 3:30–4:30 | **Arena** | [`https://councilof.ai/arena`](https://councilof.ai/arena) | Law-graded contest UX |
| 4:30–5:00 | **Close** | see below | Free verify · enterprise `/start` · MCP |

Optional API proof (keep in a second tab): [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)

---

## What to say

### Open (15s)

> We are an independent measurement body. We measure published model behaviour against frozen rules, sign the result, and publish empty cells. Measurement — not certification. No grade is sold.

### Ask (lobby)

Type (or speak) an **axis ask**, not a pricing ask:

> How many GSPC axes are on the public board?

Or:

> What does the governance axis show on the living board?

Point at the reply. If chat drifts from `totals.public_count` on `/api/gspc`, **stop and open the API** — the board wins, chat does not.

### Board

> Fourteen quotable slots. Public ruling: thirteen measured of fourteen. Jail is on the board; separation stays **UNTESTED** until the McNemar gate. Wilson intervals and SEPARATED / TIE / UNTESTED — not a popularity league.

Open `totals` on `/api/gspc` if they want receipts:

- `totals.axes` → 14  
- `totals.measured_axes` → 13  
- `totals.public_count` → live string (do not memorize)

### Verify

> Anyone recomputes a card in the browser. Ed25519 over canonical JSON. No account. No fee. If the hash or the signature fails, it is not ours.

Key identity (say once): `did:web:csoai.org` — keys on `csoai.org`, not a grade behind a login.

### Arena

> Contests are law-graded. Enter a model, watch the room. Ranking follows the instrument — not crowd Elo on this board.

### Close (30s)

1. **Free forever:** read `/api/gspc`, recompute at `/gspc-verify/`.  
2. **Enterprise path:** [`/start`](https://councilof.ai/start) when the alias is live (today: open lobby + say “we start with a signed assessment, not a seat licence”).  
3. **Agents:** [`/.well-known/mcp.json`](https://councilof.ai/.well-known/mcp.json) — tools `measure`, `verify`, `jail-probe`, `enter-arena`.

One line:

> Measurement and verification stay free. Where we sell, we sell a signed evidence artefact — never a ranking or a placement.

---

## What NOT to say

| Do not say | Say instead |
|---|---|
| “Elo rating” / “league table” as the public GSPC grade | Wilson + McNemar; SEPARATED / TIE / UNTESTED |
| “Sixteen axes” / “16 measured” | 14 board slots; +2 in-lane honesty only (`slot15`, `human-vs-ai`) — not quotable |
| “Fifteen axes” | Public ruling is **13 of 14** measured |
| “We certify” / “certified safe” | We **measure**; empty cells stay empty |
| “Jail separation is resolved” | Jail measured; separation **UNTESTED** until gated |
| Hardcoded leader names or scores | Open `/api/gspc` — live API wins |
| SaaS seats / per-seat pricing story | Free measure + verify; artefacts priced as artefacts |
| Fake ARR / pipeline / “customers paying X” | Point at live surfaces and signed receipts only |

---

## Demo hygiene

- Prefer **fat apex** (homepage ≥ ~20 KB). Thin shell → defer board demo; do not improvise.  
- `/gspc-verify` without slash often **404** — always use `/gspc-verify/`.  
- `/pricing`, `/start`, `/enterprise`, `/regulators` may **404** while apex aliases are thin — use lobby + verify + MCP, and name the intended path honestly.  
- Never demo Elo as if it lived on `/api/gspc`. It does not.

---

## After the call

| Next | Where |
|---|---|
| Prospect verifies alone | `/gspc-verify/` |
| Ask again in lobby | `/?lobby=home` |
| Agent integration | `/.well-known/mcp.json` |
| Claim discipline | `products/claimguard/` · [`CLAIMGUARD_MCP.md`](CLAIMGUARD_MCP.md) |
| Surface inventory | [`REVENUE_SURFACES.md`](REVENUE_SURFACES.md) |
