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
```

Exit code `0` = PASS, `1` = FAIL.

## What it checks

1. **Attestation** — Ed25519 over RFC 8785 canonical JSON of payload minus `site_attestation` (same as `/api/gspc`).
2. **Payload** — `axes[]` non-empty, totals present, MEASURED rows not empty.
3. **Claims** — rejects 16/15/12-axis overclaims, public Elo league, jail-separation-resolved while `UNTESTED`, certification language. Exact match to living `totals.public_count` **PASS**es (currently **14 measured of 14 quotable**). “All 14 MEASURED” only PASSes when `measured_axes >= 14`.

Living board: https://councilof.ai/api/gspc  
Axis canon: https://github.com/CSOAI-ORG/.github/blob/main/docs/GSPC_AXIS_CANON.md

## Licence

MIT © CSOAI Ltd
