# TODAY — top-down alignment (2026-08-24)

One page reconciling **online** (live on councilof.ai) vs **offline** (built in
`.github`, not yet deployed), then today's ordered actions. Grounded in what's
actually verifiable from this sandbox; owner-gated items are flagged, not faked.

> I cannot reach RunPod, the DSH/Hermes host, `nicholas@csoai.org`, or "last
> night's plans" from here (no creds in this sandbox). This aligns the plans that
> ARE in the repo + the live-site facts I can verify.

## Top-down
**Mission:** signed, stranger-verifiable AI measurement. **Two walls now open onto
us:** EU AI Act Article 50 (free, interoperable detection — live since 2026-08-02;
backstop 2026-12-02; interop 2027-02-02) and agent commerce (verify claims before
money moves). **The gap:** the engines that answer both are **built offline**; the
**online** site doesn't serve them yet.

## Online vs offline (reconcile the gap)
| Capability | Online (councilof.ai) | Offline (`.github`, ready) | Today |
|---|---|---|---|
| Signed GSPC board | ✅ `/api/gspc` live | mirrored fixture | — |
| Article 50 **issue** passport | ✅ `/api/article50` (HMAC, trusts boolean) | — | — |
| Article 50 **verify** (C2PA) | ❌ **missing** | ✅ `detect.ts` patch (validated) | 👤 apply + deploy |
| Standard in-toto/DSSE receipts | ❌ | ✅ `intoto.ts` + `receipts.py` (Node↔Py proven) | 👤 apply |
| Transparency log | ❌ | ✅ `tlog.py` | 🔧 port |
| Detector-interop suite | ❌ | ✅ `docs/detector-interop/` (2 cases, CI-tested) | 🔧 HF publish |
| Agent-card `detect` skill | ❌ | ✅ agent-card patch | 👤 apply |
| ClaimGuard | in CI elsewhere | ✅ v0.3 PyPI-ready + `--intoto` | 👤 PyPI publish |
| Apex aliases `/lobby /scorecard /honesty /verify` | ❌ REAL-404 | n/a | 👤 gated deploy (Block B/G) |
| CI batch gate | n/a | ✅ `harness-ci.yml` | ✅ done |

## Today — ordered actions
### A. Executed here (agent, done today)
1. ✅ P1 CI gate · P2 in-toto/DSSE util · P3 interop suite (+negative case) · P4 agent-card skill.
2. ✅ `/api/detect` verify Function (cross-language validated).
3. ✅ Batch 6/6 green every commit; PR #8 updated.

### B. Critical path — owner-gated (unblocks the most)
1. 👤 **Apply the 3 site patches** to `councilof-ai` (`functions/api/detect.ts` +
   `intoto.ts`, agent-card skill) **or grant me write/collaborator access** so I
   open the PR there directly. Token is read-only today.
2. 👤 **Gated deploy** (DEPLOY-LOCK): fix apex alias 404s + ship `/api/detect`.
3. 👤 **Confirm infra paid** — hosting/domains for councilof.ai + csoai.org
   (inbox flagged overdue/expiry). A dark surface during the Article 50 window is
   self-inflicted.
4. 👤 **Creds to unlock the rest:** PyPI token (publish ClaimGuard), a
   `security_events` token (verify the CodeQL claim + add CI to the 4 cold repos),
   IMAP secret (read `nicholas@csoai.org`).

### C. Next executable-here (say go)
- Wire `intoto.ts` into `detect.ts` so verdicts ship the standard receipt.
- More interop cases (watermark declarations); HF dataset scaffold for `csoai/detector-interop`.
- Draft the DRCF response doc (owner reviews before any send).

## The one decision that moves everything
**Grant write access to `councilof-ai`** (or apply the patches). Everything is
built, validated, and staged; only deploy/creds are missing.
