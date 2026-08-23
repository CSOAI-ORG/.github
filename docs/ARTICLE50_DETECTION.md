# Move 1 — Free Article 50 detection endpoint (spec)

**Status:** design · **Depends on:** ClaimGuard v0.2 `c2pa.py` (landed) ·
**Regulatory clock:** Art. 50(2) enforceable 2026-08-02 · legacy backstop
2026-12-02 · detector interop 2027-02-02.

> Counts/leaders defer to [`/api/gspc`](https://councilof.ai/api/gspc). This spec
> defines a *verification* surface; it never issues a certification.

---

## Why this is the opening move

Article 50(2) obliges GenAI providers to (a) mark output machine-readably and
(b) make a **detection solution available free of charge**, with **guaranteed
free, unrestricted access to authorities, media, fact-checkers, independent
researchers, and civil society.** The Code of Practice names **C2PA Content
Credentials + a watermark** as the pre-cleared path, and sets **2027-02-02** for
**interoperability between detection mechanisms.**

CSOAI already runs a "verify free, forever" surface and two on-point axes
(provenance, detector-interop). The clever move is to become the **neutral,
free detection + provenance-verification endpoint** the law now privileges —
before the benchmark crowd notices this tier exists.

## Chess frame

- **Our move:** ship a free, neutral C2PA/provenance verifier the regulation's
  favoured constituencies can hit with no account.
- **Opponent replies:** (1) big labs point to their *own* detectors → we counter
  with **neutrality + interoperability** (we verify *anyone's* mark, they verify
  only theirs); (2) a startup ships a paid detector → we counter with **free +
  signed + open method**; (3) "you're just reading metadata" → we counter that we
  verify the *signed* metadata layer and publish exactly what we cannot see
  (watermark/pixels) — the honesty gate.
- **Tempo:** the 2027-02-02 interop deadline is a forcing move. First credible
  free interop verifier becomes the reference. Move now.

---

## Endpoint contract

### `POST /api/detect`
Verify a supplied provenance manifest (and, later, an asset) and return a signed,
deterministic verdict.

**Request**
```jsonc
{
  "manifest": { /* C2PA-style signed manifest (see ClaimGuard c2pa.py) */ },
  "asset_hash": "sha256:…",        // optional; if given, must match manifest.claim.asset.hash
  "claims": ["marked per Article 50"]  // optional NL claims to adjudicate
}
```

**Response**
```jsonc
{
  "ok": true,
  "verdict": "AI_MARKED | NOT_AI_MARKED | UNVERIFIABLE",
  "source_type": "trainedAlgorithmicMedia",
  "signer": "did:web:acme.example#c2pa-1",
  "findings": [ {"status":"PASS","code":"c2pa.signature_valid","message":"…"} ],
  "detected": { "metadata_layer": "verified", "watermark_layer": "not_checked" },
  "receipt": { "alg":"Ed25519", "sig":"…", "signer":"did:web:csoai.org#board-attestation-1" }
}
```

Rules:
- Reuse ClaimGuard `verify_c2pa_manifest` for the metadata layer verbatim (one
  code path, CLI + API + CI identical).
- **Never** assert the watermark layer we cannot see — return
  `watermark_layer: "not_checked"` and say so (honesty gate).
- Sign the response as a CSOAI receipt (see `RECEIPT_INTEROP.md`) so the verdict
  is itself verifiable and loggable.

### `GET /.well-known/ai-content-detection.json`
Machine-discoverable descriptor of the free detection service (what it verifies,
access policy, rate limits, contact) so agents and regulators can find it.

### `GET /api/detect/health`
Liveness + which layers are supported this build.

## Access policy (write it into the response + docs)
- No account, no fee for the public.
- **Unrestricted** for authorities, media, fact-checkers, researchers, civil
  society (the law's named set). Publish this as policy, not just behaviour.
- Reasonable-fee escape hatch only applies to providers with <1M MAU under the
  Code — we don't need it; state "free for all verification."

## Layers (be explicit about scope)
| Layer | Who owns | CSOAI detect v1 |
|---|---|---|
| Signed metadata (C2PA) | provider | **Verified** (deterministic) |
| Imperceptible watermark (SynthID etc.) | provider | **Not checked** — declared, roadmap via partner detectors |
| Hard binding to asset bytes | provider | Optional `asset_hash` match |

## Build steps (smallest → shippable)
1. Wrap `products/claimguard/c2pa.py` behind a Cloudflare Function `/api/detect`
   in `councilof-ai` (Python worker or port verify to TS mirroring `c2pa.py`).
2. Sign the verdict with the board key path (`RECEIPT_INTEROP.md`).
3. Publish `.well-known/ai-content-detection.json` + policy page.
4. Rebrand `/gspc-verify/` copy to include "Article 50 free detection."
5. Add `run-frontend-audit.mjs` route check for `/api/detect` + well-known.

## Done-when
`curl -X POST councilof.ai/api/detect` with a valid manifest returns
`verdict: AI_MARKED` and a verifiable CSOAI receipt; with a tampered manifest
returns `UNVERIFIABLE`; the well-known descriptor is 200; access policy is public.

## Non-goals
Not certification. Not watermark decoding (declared, not claimed). Not a takedown
or remediation service.
