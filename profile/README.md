# Council of AI (CSOAI Ltd)

**An independent AI-measurement body.** We measure AI systems against the rules that govern them, sign the result (Ed25519), and publish what we cannot yet measure. Measurement, not certification. We do not remediate.

## The living board

**GET [`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc)** — axis counts, scores, and dates are live in the API.

Snapshot 31 Aug 2026 from that API (if this disagrees with the API, the API wins):

| | Live |
|---|---|
| Slots · measured · empty | **22 · 22 · 0** (`totals.public_count`) |
| Split | **14 model-comparison + 8 fact cards** (`by_family`) |
| Behavioural GSPC | **14 / 14 measured** (13 canonical + jail) |
| Signed cards | **335** (`n_cards == n_cells` on [`/signed/card_index.json`](https://councilof.ai/signed/card_index.json)) |
| Living stamp | **SIGNED** · `did:web:csoai.org#board-attestation-1` |
| Schema | `csoai.gspc-axes/0.5` |

UNMEASURED is first-class. A published empty slot is a visible gap, not a fail.

## Verify free, forever

[**councilof.ai/gspc-verify**](https://councilof.ai/gspc-verify/) — no account, no fee. A grade is never sold.

## Hosting

Live is **Cloudflare Pages + Wrangler** (`councilof-ai` → councilof.ai, `csoai-site` → csoai.org). Not Vercel.

## The honesty gate

We publish our own models losing our own arena — [councilof.ai/honesty](https://councilof.ai/honesty/).

## Surfaces

| Surface | URL |
|---|---|
| Council | [councilof.ai](https://councilof.ai) |
| Public site / DID | [csoai.org](https://csoai.org) |
| MEOK OS | [meok.ai](https://meok.ai) |
| RSS | [councilof.ai/api/feed.xml](https://councilof.ai/api/feed.xml) |
| Firewall Charter | [councilof.ai/firewall-charter](https://councilof.ai/firewall-charter/) |

**Open tooling:** [carder](https://github.com/CSOAI-ORG/carder) · [inspect-receipts](https://github.com/CSOAI-ORG/inspect-receipts) · [a2a-signed-receipts](https://github.com/CSOAI-ORG/a2a-signed-receipts) · [codabench-gspc](https://github.com/CSOAI-ORG/codabench-gspc)

## Sponsorship

Sponsorship funds the instrument — compute, item banks, and re-measurement. It never buys a result, a rank, or a faster verdict. The Firewall Charter binds that in public.

---

CSOAI Ltd · UK Companies House 16939677 · nicholas@csoai.org
