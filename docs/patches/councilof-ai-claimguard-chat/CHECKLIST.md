# ClaimGuard × chat — implementer checklist

Copy into the `councilof-ai` PR that wires `POST /api/chat`.

- [ ] Detect axis-count / grade / Elo / certification intents on ask
- [ ] Load live `/api/gspc` (or request-scoped stamp)
- [ ] Run ClaimGuard on draft answer (or extracted claim)
- [ ] FAIL → refuse overclaim; cite `totals.public_count`
- [ ] Map “twelve / 12 axes” → 14 quotable / 13 measured language
- [ ] Never affirm 15, 16 measured, or Elo as GSPC public grade
- [ ] Never use certification language
- [ ] Keep cream/ink tone; measurement not certification
- [ ] Green: `python3 products/claimguard/claimguard.py --self-test`
- [ ] Green: `node scripts/weekend-demo-smoke.mjs` (`api.chat.canon`)

Full notes: [`README.md`](./README.md)
