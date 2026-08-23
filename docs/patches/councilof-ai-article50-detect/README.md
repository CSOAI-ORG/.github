# Patch — `functions/api/detect.ts` for `councilof-ai` (Article 50 verification)

**Target repo:** `CSOAI-ORG/councilof-ai` (the live SPA — I have read-only access,
so this is a ready-to-apply handoff, same as `councilof-ai-openrouter-agui/`).

## Why (gap this closes)
`functions/api/article50.ts` **issues** an HMAC passport but trusts a `watermarked`
boolean on input — it never cryptographically verifies a C2PA mark.
`functions/api/detect.ts` (this patch) **verifies** a supplied C2PA-style signed
manifest: it recomputes the canonical JSON of `manifest.claim` (recursively sorted
keys, no whitespace — the same rule `cross.ts` / `assess/key.ts` use), checks the
Ed25519 signature via WebCrypto, and reads the IPTC/schema.org `digitalSourceType`.
So the passport's `watermarked` / `source_type` become **proven, not claimed** —
and it stands up the free detection endpoint the Article 50 Code of Practice
guarantees to the public, media, fact-checkers, researchers, and authorities.

Verifies only the signed-**metadata** layer; the watermark layer is **declared**
(`watermark_layer: "not_checked"`), never claimed. Matches the file's
"honesty over appearance" discipline: the verdict receipt is Ed25519-signed **iff**
a board key is bound, else returned **unsigned** with an honest note (never faked).

## Apply
1. Copy `detect.ts` → `councilof-ai/functions/api/detect.ts` (Pages Functions are
   file-routed, so `POST/GET /api/detect` register automatically — no wiring).
2. (Optional, non-breaking) In `article50.ts`, when a caller supplies a `manifest`,
   call the same verify logic and set `watermarked` from the **verified** result
   instead of the input boolean; keep the boolean path for back-compat.
3. Add `/api/detect` to `scripts/run-frontend-audit.mjs` route checks.
4. UI (optional): add a "verify" affordance to the existing Article 50 page in
   `client/src` using the **real** design system — do NOT hand-roll a new page.
5. Optional env `BOARD_ATTESTATION_KEY_PKCS8_B64` (or reuse
   `ASSESS_SIGNING_KEY_PKCS8_B64`) to Ed25519-sign verdict receipts; absent = honest
   unsigned verdict.

## Deploy discipline
Gated deploy only. Respect `DEPLOY-LOCK.md` — never enable Cloudflare Pages Git
auto-deploy on `councilof-ai`. Run `npm run check` + `npm run test:pre-deploy`
before promoting.

## Correctness (validated cross-language)
The pure verify logic in `detect.ts` was validated against a manifest signed by the
`.github` reference engines (Python, RFC 8785): Node running `detect.ts`'s exact
`canon()` + WebCrypto `Ed25519` returns **true** for a valid manifest and **false**
after tampering. Canonical JSON (sorted keys, no whitespace) is byte-identical to
RFC 8785 for the ASCII/number payloads used across the estate (see
`.github/products/claimguard/canonical.py`), so CLI (ClaimGuard `--c2pa`), the
reference harness, and this Function all agree. Finding codes (`c2pa.*`,
`detect.*`) are stable across all three.

## `intoto.ts` (optional, recommended)
`intoto.ts` (in this bundle) ports the in-toto Statement v1 + DSSE wrapper to TS
(WebCrypto). Use it so `/api/detect` emits its verdict as the **standard** DSSE
envelope auditors read, instead of a bespoke receipt. Validated: a DSSE built by
`intoto.ts`'s exact logic (Node) verifies with the `.github` **independent** Python
verifier (`harness/verify_external.py`) — `signature_ok: true`. Same canonical rule,
PAE, and `payloadType` as `harness/receipts.py`.

## Provenance of this patch
Ported from the `.github` reference kit: `harness/detect.py`, `products/claimguard/c2pa.py`.
Specs: `docs/ARTICLE50_DETECTION.md`, `docs/RECEIPT_INTEROP.md`.
