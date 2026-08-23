# ClaimGuard

**The receipt for your claims.** Verifies a signed GSPC board’s Ed25519
`site_attestation`, payload completeness, and whether natural-language claims
are supported by the board.

Measurement, not certification. CSOAI Ltd (UK 16939677).

## Why it exists

Session failure mode: mutate a signed result after signing, or claim
“16 measured axes” / “jail separation resolved” when the living board says
otherwise. ClaimGuard fails those deterministically — including when we make them.

## Install

```bash
pip install cryptography
# or: pip install -e .
```

## Usage

```bash
python claimguard.py --self-test
python claimguard.py check --live
python claimguard.py check --live --claim "16 measured axes"
python claimguard.py check --board board.json --claim "14 quotable axes" --json

# Article 50 (EU AI Act) provenance — verify a signed C2PA-style manifest and
# fail any "marked per Article 50 / C2PA verified" claim it does not support.
python claimguard.py check --board board.json \
  --claim "this image is marked per Article 50" --c2pa manifest.json

# Emit the verdict as a composable in-toto Statement (v0.3), optionally DSSE-signed.
python claimguard.py check --board board.json --claim "14 quotable axes" --intoto
python claimguard.py check --board board.json --intoto --sign-key ed25519.seed
```

Exit code `0` = PASS, `1` = FAIL.

## What it checks

1. **Attestation** — Ed25519 over RFC 8785 canonical JSON of payload minus `site_attestation` (same as `/api/gspc`).
2. **Payload** — `axes[]` non-empty, totals present, MEASURED rows not empty.
3. **Claims** — rejects 16/15-axis overclaims, public Elo league, jail-separation-resolved while `UNTESTED`, certification language.
4. **Article 50 / C2PA provenance** (`--c2pa`, v0.2) — verifies a signed manifest
   (Ed25519 over RFC 8785 canonical `claim`), checks the IPTC/schema.org
   `digitalSourceType` marking, and **fails** any "marked / watermarked / C2PA
   verified / Article 50 compliant" claim that has no verifiable AI-marked
   manifest behind it. Not a full c2pa-rs (JUMBF/COSE/X.509) implementation — it
   verifies the signed-metadata layer; finding codes (`c2pa.*`,
   `claim.article50_*`) stay stable if a fuller parser is added upstream.

EU AI Act Article 50(2) machine-readable marking is enforceable from 2026-08-02
(legacy backstop 2026-12-02); detector interoperability is due 2027-02-02.

Living board: https://councilof.ai/api/gspc  
Axis canon: https://github.com/CSOAI-ORG/.github/blob/main/docs/GSPC_AXIS_CANON.md

## Licence

MIT © CSOAI Ltd
