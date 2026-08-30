# E2E action pack — 2026-08-30

External SCITT/GitHub mail + internal GSPC cards + outbound listing PRs.
Goal: improve what we already ship; help others with tests; do not thrash lists.

## A. Verdict map (what we learned)

### Architecture [#461](https://github.com/ietf-wg-scitt/draft-ietf-scitt-architecture/issues/461) vs our cards

| Layer | ActaSeal failure (#461) | Our card-v1 today |
|-------|-------------------------|-------------------|
| Bind claim / verdict fields | They signed status/claims/authorities | We sign full body (`accuracy`, axis, model, …) |
| Bind evidence bytes | Missing `content_hash` of evidence | **Also missing** — no `rows_digest` / `content_hash` in published body |
| Substitute evidence, keep score | Signature still verified (shipped bug) | **Same structural gap** for offline evidence |

**Safe:** stranger cannot change `accuracy` without breaking Ed25519 / id.
**Not safe:** stranger with our score string + different graded rows still verifies.
Arena harness already designs `rows_digest` into the preimage (`harness/arena/measurement_card.py`) — not what `/signed/cards/*` publishes (9 body fields only).

ActaSeal public kit worth copying for UX: [actaseal/actaseal-verify](https://github.com/actaseal/actaseal-verify) — offline verifier, tamper demo, conformance vectors with expected PASS/FAIL, CI Action, zero-network `verify.py`.

### CPB / AAC / related GitHubs (action-state-group)

- `scitt-payload-binding` — CPB draft home + `vectors/` + registry (Michael offering TS §§4.1/5/7.1 vs KATs)
- `agent-action-capsule` — AAC profile; PR #40 frozen composition vectors (Iman ask; Anton accepted)
- `scitt-cose` — COSE receipts substrate (not a TS)
- `capsule-anchor` — neutral TS (digest → RFC9162 receipt) — closest public TS we can aim at
- `capsule-emit` / `capsule-ledger` / `capsule-emit-mesh` — emit + ledger path

**Our honest gap:** no live `POST /entries` / transparency service; SCITT profile docs + `.well-known/scitt.json` only.

### Listing PR cluster (sort like #77)

| PR | State | Blocker |
|----|-------|---------|
| [agentrust #77](https://github.com/agentrust-io/awesome-ai-governance/pull/77) | open, Imran CHANGES_REQUESTED then we fixed copy | was **dirty** (CCS landed on main); content already matches his ask |
| AthenaCore #70, morganrcu #43, punkpeye #12480, a2a #158 | clean / waiting | no review |
| getprobo #56, docker #4733, xai #398, Eleuther #4018 | blocked (checks/review) | wait |
| a2a #157 (GSPC) + #158 (EUNOMIA) | both open | prefer one narrative; don't spam |

**Procedure for listing PRs:** quote living `GET /api/gspc` → `totals.public_count` + Zenodo methodology DOI `10.5281/zenodo.21991104` + McNemar caveat; never freeze “14 of 14”; rebase when upstream adds neighbors.

---

## B. Actionable steps (ordered)

### P0 — do now (unblocks others / fixes our own honesty)

1. **Finish PR #77 mergeability** — rebase onto main keeping CCS + our GSPC line; ping Imran (draft below).
2. **Ship evidence-substitution KAT** (public, in `packages/gspc-card-verifier` or `public/signed/kats/`):
   - Fixture A: card body includes `rows_digest` (next-format or harness shape); swap rows → must FAIL.
   - Fixture B: today’s card-v1 without digest → document that signature still VALID (honest gap demo for #461).
3. **Label `actions/verify-card` as non-canonical** in README + HOW-TO-VERIFY (different `content_id` recipe, no pin) so strangers don’t get a false VALID.
4. **RunPod** — top-up or snapshot/delete volume (mail 13:10 UTC) before data loss.
5. **Close or triage stale councilof-ai PRs** that fight the living 22·15 grammar (#432, #816, #898-era copy) — keep one source of truth: `/api/gspc`.

### P1 — help others (tests / drafts we can offer without asking first on Anton’s plate)

6. **Optional GitHub comment on #461** (draft below) — disclose our same gap + point at ActaSeal pattern + offer measurement-card KAT when published. Do **not** sell; do **not** claim we solved it.
7. **Offer Michael (SCITT list) a consumer note** only if we run his TS CPB KATs — otherwise stay quiet until we have results.
8. **CPB Artifact Type sketch** (internal doc first): register GSPC measurement card as a future CPB type with typed digest refs (`rows_digest`, bank digest). No unsolicited PR on `scitt-payload-binding`.
9. **Interop help for Tiago contestability** — if we implement anything, share reconstruction vectors for findings 1/2/5 he already accepted; skip 3/4 until he decides.

### P2 — E2E product improvements (internal)

10. **Card format bump path:** migrate issuance to include `rows_digest` (or attachment digests per DOCTRINE) without breaking old verifiers (profile version field).
11. **COSE wrap of existing card preimage** + optional register to `capsule-anchor` as an experiment (not production claim).
12. **Twin-recipe KAT:** card-v1 vs content_id vs Action verify-card — wrong recipe must not silently VALID.
13. **www.csoai.org SSL** / CF token — still broken for `csoai-site` deploy; separate from councilof.ai carry-on (already live).
14. **DIGITAL** — hold drafts until Emek’s TR Art 12(5)-(6) reply; then send map-only Joel/Tiago drafts if Nick says **send**.

### Do not

- Unsolicited reply on Iman→Steven/Anton CPB ask (Anton already accepted).
- Open PRs on action-state-group repos unless invited.
- Send DIGITAL / C2PA drafts without explicit **send**.

---

## C. Email / GitHub drafts (PrivateEmail — do not send until Nick says send)

### C1. PR comment — agentrust #77 (GitHub)

@imran-siddique — rebased onto main and kept the new CCS entry. Blurb still matches your review: Governance Frameworks; living `totals.public_count` (**22 axis · 15 measured**); methodology DOI [10.5281/zenodo.21991104](https://doi.org/10.5281/zenodo.21991104); McNemar caveat (4 separated / 10 ties) in the line. Ready for another look.

### C2. Optional — SCITT architecture #461 comment

Thanks for writing this up — we hit the same shape on an independent measurement board (signed claim body includes the score; underlying graded-row / bank bytes were not in the preimage). Claim tamper fails verification; evidence substitution with an unchanged score would not. We are adding a public negative KAT that demonstrates both sides, and treating “verdict without evidence digest” as a profile requirement rather than an issuer footgun. Happy to link the vectors here when they land. (Council of AI / GSPC; nothing to sell.)

### C3. Optional — short note to ActaSeal (if we want reciprocity)

To: via GitHub @actaseal / no cold email needed if we only comment on #461.

### C4. DIGITAL — hold

Drafts already in PrivateEmail Drafts (Joel map-only; Emre+Tiago measurement ask). **Do not send** until TR coordination answer lands or Nick says send.

### C5. RunPod — ops, not IETF

Subject: Network volume — top-up or export
Body: Confirm balance / export volume before deletion window; keep overnight register jobs from failing mid-run.

### C6. Listing-PR hygiene ping (only if a maintainer asked)

Template: counts from `GET https://councilof.ai/api/gspc` → `totals.public_count`; DOI `10.5281/zenodo.21991104`; measurement not certification.

---

## D. Tests to ship (concrete)

| ID | Test | Helps |
|----|------|-------|
| T1 | Evidence-substitution KAT (with/without `rows_digest`) | Us + #461 readers + ActaSeal comparison |
| T2 | Multi-runtime preimage KAT (JS/Python) for `0.0` floats | CPB-style byte agreement |
| T3 | Wrong-recipe verifier matrix | Strangers using `actions/verify-card` |
| T4 | Optional: run CPB known-answer vectors from `scitt-payload-binding/vectors` in CI as consumer | Michael / Steven / Anton |
| T5 | Live surface: `/api/gspc` totals grammar gate in CI (already partially present) | Listing PRs never lie |

---

## E. Internal GitHub procedure checklist

1. Living facts only from `/api/gspc` (and signed board attestation).
2. Brand-gate: no forbidden tokens in training HTML (fixed in #941).
3. Listing PRs: one blurb grammar everywhere; rebase promptly on conflict.
4. SCITT engagement: substrate first (AAC/CPB/cose); our Artifact Type later; no drive-by PRs.
5. Confirm-before-send on all PrivateEmail drafts.


## F. Status log (2026-08-30)

- DIGITAL Art 12 reply to Emek **sent** (PrivateEmail 14:57Z) — forward-wait; co-sign only if he asks.
- `.github` PR #83 — action pack doc (open).
- Evidence-bind KAT + verify-card non-canonical warning — branch `cursor/evidence-bind-kat-ff6e` on councilof-ai.
- agentrust #77 still dirty; clean replacement PR in flight (`add-csoai-gspc-rebased`).
- Outbound listing PRs waiting review (clean): AthenaCore #70, visenger #13, morganrcu #43, punkpeye #12480.
- RunPod low-balance mail — **ops needed by Nick** (no API token in this VM); top-up or export volume.
- Do not unsolicited-reply Iman/Anton CPB thread; Anton already accepted.

- councilof-ai **PR #946** (draft): evidence-bind KAT + HOW-TO-VERIFY #461 note + verify-card non-canonical — https://github.com/CSOAI-ORG/councilof-ai/pull/946
- agentrust clean listing **PR #86** (mergeable, needs Imran review) — close dirty #77/#83 — https://github.com/agentrust-io/awesome-ai-governance/pull/86
