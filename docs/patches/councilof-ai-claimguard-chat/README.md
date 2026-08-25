# Patch notes — ClaimGuard into `POST /api/chat`

**Target repo:** `CSOAI-ORG/councilof-ai`  
**Product:** [`products/claimguard/`](../../../products/claimguard/) (mirror of `CSOAI-ORG/claimguard`)  
**Related:** [`CLAIMGUARD_MCP.md`](../../CLAIMGUARD_MCP.md) · [`GSPC_AXIS_CANON.md`](../../GSPC_AXIS_CANON.md) · openrouter chat notes in [`../councilof-ai-openrouter-agui/`](../councilof-ai-openrouter-agui/)

**Status:** Spec for implementers — wire when grade / axis-count asks hit chat. Measurement, not certification.

---

## Problem (living board)

Axis ask:

> How many GSPC axes are on the public board?

`POST /api/chat` must cite live `GET /api/gspc` totals — never invent counts. As of 2026-08-25 the signed board publishes:

- `totals.axes` = **14**  
- `totals.measured_axes` = **14**  
- `totals.public_count` = `14 measured of 14 quotable`  

(Historical 2026-08-18 sitting was 13/14.) ClaimGuard refuses overclaims (12/15/16 axes, certification, Elo-as-grade) and allows claims that match living `public_count`.

---

## When to invoke ClaimGuard

Before composing / returning an answer, if the user ask **implies** any of:

| Trigger class | Examples |
|---|---|
| Axis **count** | “how many axes”, “14/15/16 axes”, “twelve axes”, “full suite” |
| **Grade / leader** claim | “who leads”, “is X SEPARATED”, “jail resolved” |
| **League / Elo** | “Elo”, “ranking league”, “arena Elo as GSPC grade” |
| **Certification** | “certified”, “approved”, “compliant seal” |

Then:

1. Load live board (`GET /api/gspc` or cached stamp for the request).  
2. Run ClaimGuard claim audit on the **intended answer text** (or on a normalized claim extracted from the ask).  
3. On any `FAIL` finding → **refuse overclaim**; answer with board-backed language only.  
4. On `PASS` → continue existing grounded path.

Reference CLI:

```bash
python3 products/claimguard/claimguard.py check --live --claim "16 measured axes"
# expect FAIL · claim.sixteen_axes

python3 products/claimguard/claimguard.py check --live --claim "14 quotable axes"
# expect PASS (when attestation holds)
```

---

## Refuse overclaims (chat behaviour)

| Finding code (ClaimGuard) | Chat must |
|---|---|
| `claim.sixteen_axes` / fifteen | Refuse; state **14 quotable**, cite live `public_count`, +2 in-lane not quotable |
| Elo / league as public GSPC | Refuse; Wilson + McNemar only; Elo is not on `/api/gspc` |
| `claim.certification` | Refuse; “measurement, not certification” |
| Jail separation claimed SEPARATED while board says TIE | Refuse; cite live jail.separation |
| Quotable count ≠ `totals.quotable_axes` | Refuse; cite live totals |

Refusal shape (cream/ink, no apology theatre):

```
I will not overclaim the signed board.

Live ruling from GET /api/gspc: {totals.public_count}
Quotable slots: {totals.axes}. In-lane honesty rows are not board-quotable.

Recompute any card at /gspc-verify/. Measurement, not certification.
```

Set `state` to a refused / grounded-refuse variant consistent with existing chat contract (`grounded` / `live` / `refused`).

---

## Map “twelve axes” → correct living language

Legacy and verbal slips still say “twelve axes” (older suite folklore). Chat must **not** echo twelve as current board truth. Always prefer quoting live `totals.public_count`.

| User says | Correct language |
|---|---|
| “twelve axes” / “12 axes” | The public board is **14** quotable slots; cite live `public_count` (currently **14 measured of 14**). Twelve is not the living count. |
| “sixteen axes” / “16 measured” | **Refuse.** 14 board + 2 in-lane honesty — never “16 measured.” |
| “fifteen axes” | **Refuse.** Not 15; cite live `public_count`. |
| “all axes measured” | Only if `measured_axes === axes`; otherwise quote `public_count`. |
| “what’s the Elo” (as GSPC grade) | **Refuse** as board grade; point to Wilson / McNemar fields. |

Normalization helper (suggested):

```ts
function normalizeAxisCountTalk(q: string): string | null {
  if (/\b(twelve|12)\s+axes?\b/i.test(q)) {
    return "User referred to twelve axes — correct to live totals.public_count (14 quotable).";
  }
  if (/\b(sixteen|16)\s+(measured\s+)?axes?\b/i.test(q)) {
    return "OVERCLAIM: 16 axes — ClaimGuard must FAIL.";
  }
  if (/\b(fifteen|15)\s+(measured\s+)?axes?\b/i.test(q)) {
    return "OVERCLAIM: 15 axes — ClaimGuard must FAIL.";
  }
  return null;
}
```

Prefer **quoting `totals.public_count`** over typing a fresh fraction in prose.

---

## Wire sketch (`functions` / chat handler)

```ts
import { spawnSync } from "node:child_process";
// Prefer an in-process port of claimguard audit; CLI shown for estate clarity.

function claimGuardCheck(claim: string, boardUrl = "https://councilof.ai/api/gspc") {
  const r = spawnSync(
    "python3",
    ["products/claimguard/claimguard.py", "check", "--board-url", boardUrl, "--claim", claim, "--json"],
    { encoding: "utf8" },
  );
  return JSON.parse(r.stdout || "{}");
}

// Inside POST /api/chat, after axis / grade intent detected:
const draft = composeGroundedAnswer(ask, board); // existing path
const report = claimGuardCheck(draft);
if (report.findings?.some((f) => f.status === "FAIL")) {
  return refuseOverclaim(board, report);
}
return grounded(draft);
```

If Python is unavailable in the Pages function runtime, **port the claim regex + attestation verify** from `products/claimguard/claimguard.py` into the worker — do not weaken rules.

---

## Product reference

| Path | Use |
|---|---|
| `products/claimguard/claimguard.py` | Attestation + claim rules source of truth |
| `products/claimguard/CLAIMGUARD_PRODUCT_SPEC_2026-08-22.md` | Product non-goals |
| `products/claimguard/README.md` | Operator usage |
| `docs/CLAIMGUARD_MCP.md` | MCP `claimguard.check` descriptor |

---

## Acceptance

1. Ask “16 measured axes?” → refused with 14-quotable language; no Elo; no certification.  
2. Ask “twelve axes?” → corrected to live `public_count` (14 quotable) — never affirms 12.  
3. Ask “How many GSPC axes are on the public board?” → answer consistent with `totals.public_count` (currently **14 measured of 14 quotable**).  
4. `node scripts/weekend-demo-smoke.mjs` → `api.chat.canon` **PASS**.  
5. ClaimGuard `--self-test` still green in `batch-run-gates.mjs`.

---

## Out of scope

- Selling grades  
- Changing McNemar / bank publication  
- Adding Elo to `/api/gspc`  
- Softening ClaimGuard to make thin-apex marketing copy pass  
