# Move 6 — Key governance + credibility hardening

**Status:** design · **Owner:** owner + Lane A · **Why now:** Moves 1–5 invite
scrutiny from exactly the people who check signatures, keys, and uptime.

> The board key signs [`/api/gspc`](https://councilof.ai/api/gspc). This move
> hardens the *institution* around that key; it changes no measurement.

---

## The exposure

For a body whose product **is** trust, three things are currently underspecified:

1. **Single-key fragility.** `did:web:csoai.org#board-attestation-1` is effectively
   one signing key with no published rotation, revocation, or transparency policy.
   One compromise or lost key = the whole board's provenance is in question.
2. **Apex credibility leak.** `/lobby`, `/scorecard`, `/honesty`, `/verify`,
   `/api/chat` are REAL-404 on the brand domain while the fat build lives on a
   `.pages.dev` host (ESTATE_INVENTORY audit). A regulator/journalist the law
   sends us sees a broken site.
3. **Live-surface hygiene.** Inbox flagged an overdue hosting invoice and near-
   expiry domains. A CSOAI surface going dark *during* the Article-50 window is
   self-inflicted damage.

## Chess frame

- **Our move:** publish a key-governance + transparency policy, fix the apex
  404s, and de-risk the infra that serves the brand domains — *before* outreach.
- **Opponent replies:** (1) "your signature is one key" → we point at published
  rotation + transparency log (Move 2); (2) "your site 404s" → already fixed;
  (3) "who watches the watcher?" → the honesty gate + reproducible method DOIs.
- **Tempo:** credibility is a prerequisite move — do it *before* §7 connections,
  or the first thing a partner does is find the 404.

---

## Deliverables

### 1. Key-governance policy (`did:web:csoai.org`)
| Property | Policy |
|---|---|
| Keys | Board-attestation key(s) enumerated in `did.json`; label each (`#board-attestation-N`) |
| Rotation | Scheduled + on-suspicion; overlap window; old key marked `revoked` not deleted |
| Revocation | Published revocation list; receipts carry `signer` keyid so old receipts stay verifiable against the key valid at signing time |
| Transparency | Every signing event appears in the append-only log (Move 2) |
| Offline verify | did:web stays resolvable + mirrored (no single point of failure) |
| Custody | Signing on the Mac estate-chain lane (MONOREPO_RUNPOD_OPS); document who holds it |

### 2. Apex credibility fix (executes STEPS_100 Block B/G)
- Owner: disable Pages Git auto-deploy on `councilof-ai`; run gated deploy so
  `place-end-user-aliases.mjs` lands `/lobby /scorecard /honesty /verify` as 200.
- Fix sitemap URLs that REAL-404 (trust debt).
- Gate: `run-frontend-audit.mjs` persona gauntlet ≥ 7/8.

### 3. Live-surface triage (from inbox signals)
- Confirm the hosting + domains serving `councilof.ai` and `csoai.org` are paid
  and not near expiry; move brand-critical DNS/hosting off any overdue account.
- Add an uptime + cert-expiry check to the weekly `run-frontend-audit.mjs`.

### 4. Reproducibility provenance
- Put method DOI `10.5281/zenodo.21991104` + evidence `10.5281/zenodo.21973002`
  on all axis cards (STEPS_100 #65/#72) so the board's own provenance is citable.

## Build steps
1. This doc → policy stub; expand `did.json` key labelling.
2. Owner: Cloudflare deploy actions (Block B/G).
3. Add cert/expiry + uptime checks to the audit runner.
4. DOI sweep on HF cards.

## Done-when
`did.json` enumerates + labels keys with a written rotation/revocation policy;
apex alias routes are 200; the audit runner checks cert expiry; brand infra is
confirmed paid; method DOI is on every axis card.

## Non-goals
Not re-keying in a way that breaks historical receipt verification. Not moving off
did:web. Not treating uptime as measurement.
