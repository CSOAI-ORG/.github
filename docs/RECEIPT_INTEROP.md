# Move 2 — Receipt interop: in-toto / DSSE / Sigstore / C2PA crosswalk

**Status:** design · **Owner:** receipt-stack (`signed-receipts`, `carder`) ·
**Threat driver:** new entrants (AIIR, LLM-Supply-Chain-Attestation) are building
"eval attestations" natively on in-toto + Sigstore + Rekor. Our bespoke
Ed25519 / did:web / RFC 8785 receipt is excellent but risks becoming an island.

> The board's *content* and signature stay exactly as they are on
> [`/api/gspc`](https://councilof.ai/api/gspc). This move adds **wrappers and a
> log**, changing nothing about how we measure.

---

## The moat problem, stated plainly

Our signed receipt proves *we* signed *this* payload. The ecosystem, however, is
converging on a shared envelope so that **PyPI (PEP 740), GitHub attestations,
GRC platforms, and auditors consume attestations without bespoke code.** If GSPC
receipts aren't expressible in that envelope, we're uncomposable — a strategic
dead-end for a *trust* business.

## Chess frame

- **Our move:** keep our signature; additionally express each receipt as an
  **in-toto Statement v1** with a CSOAI predicate, wrap in **DSSE**, and record it
  in a **transparency log**. Offer optional **Sigstore keyless** co-signing for
  identity binding.
- **Opponent replies:** (1) "just use Sigstore, drop your key" → we keep did:web
  (offline-verifiable, no OIDC dependency) *and* add Sigstore as an option — best
  of both; (2) a competitor standardises an "eval predicate" → we publish ours
  first as the **measurement** predicate and cross-map; (3) "your log is
  self-hosted" → we mirror to public Rekor for third-party timestamping.
- **Tempo:** predicate-type land-grab. First credible `…/measurement/v1` predicate
  with real signed data behind it wins the citation.

---

## Target shapes

### 1. in-toto Statement v1 (the envelope everyone reads)
```jsonc
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    { "name": "gspc-board", "digest": { "sha256": "<sha256 of canonical payload>" } }
  ],
  "predicateType": "https://councilof.ai/attestations/measurement/v1",
  "predicate": {
    "schema": "csoai.gspc-axes/0.5",
    "totals": { /* from /api/gspc, not hardcoded */ },
    "method_doi": "10.5281/zenodo.21991104",
    "grading": "deterministic+wilson+mcnemar",
    "site_attestation": { "alg": "Ed25519", "signer": "did:web:csoai.org#board-attestation-1", "sig": "…" }
  }
}
```
The `subject.digest.sha256` is the SHA-256 over the **RFC 8785** canonical bytes of
the payload-minus-`site_attestation` — the exact bytes we already sign. This makes
our existing signature and the in-toto subject the *same* object.

### 2. DSSE envelope (Dead Simple Signing Envelope)
Wrap the Statement, `payloadType = application/vnd.in-toto+json`, and carry the
Ed25519 signature (and optionally a Sigstore signature) in `signatures[]`.

### 3. Transparency log
- **Phase 1:** CSOAI append-only hash-chained log (we already do hash-chaining in
  the AG-UI ledger) exposed at `/api/attestations/log`.
- **Phase 2:** mirror DSSE entries to public **Rekor** for independent timestamping.

### 4. C2PA crosswalk (ties Move 1 + Move 3 together)
A CSOAI detection receipt (`/api/detect`) is emitted in the *same* in-toto/DSSE
shape, with `predicateType …/detection/v1`, so an Article 50 verdict is itself a
composable, logged attestation.

---

## Field crosswalk

| CSOAI receipt | in-toto | Sigstore | C2PA |
|---|---|---|---|
| RFC 8785 canonical payload | `subject.digest.sha256` | artifact digest | claim hash |
| `site_attestation.sig` (Ed25519) | DSSE `signatures[].sig` | (optional) Fulcio cert | manifest signature |
| `signer` (`did:web:csoai.org#…`) | DSSE `keyid` | OIDC identity | signer field |
| board `schema`/`totals` | `predicate` | — | assertions |
| method DOI | `predicate.method_doi` | — | — |
| ledger hash-chain | — | Rekor log index | — |

## Build steps
1. `signed-receipts`: add `to_intoto_statement(payload, sig)` +
   `to_dsse(statement)` helpers (pure, deterministic; reuse `canonical`).
2. Add `verify_dsse` + `verify_intoto` round-trip tests (mirror ClaimGuard style).
3. Expose `GET /api/attestations/<id>.intoto.json` from `councilof-ai`.
4. Publish the two predicate schemas under `councilof.ai/attestations/*` and
   Zenodo-DOI them.
5. Optional: `cosign`/Sigstore co-sign in CI; mirror to Rekor.

## Done-when
One live board receipt round-trips: `/api/gspc` payload → in-toto Statement →
DSSE → re-verified by both our Ed25519 verifier **and** a generic
`cosign verify-blob`/in-toto verifier, with a log entry retrievable by digest.

## Implemented in `harness/` (2026-08-23, e2e-proven)
- `receipts.py` — in-toto Statement v1 + DSSE + verify (round-trips).
- `verify_external.py` — **independent** DSSE verifier (no shared internals) that
  accepts a board receipt from the published envelope + public key alone — interop
  proof that a third party / `cosign`-style tool can verify us.
- `tlog.py` + `/api/attestations/log` — hash-chained transparency log; e2e proves
  the chain verifies and that tampering any entry breaks it.
- `schemas/measurement.v1.json`, `schemas/detection.v1.json` — published predicate
  schemas, served at `/schemas/*`.
Remaining: move helpers into `signed-receipts`, Rekor mirror, Zenodo DOIs, apex.

## Non-goals
Not dropping did:web. Not moving measurement into CI. Not signing anything the
board didn't actually measure.
