# Next-week growth + moat plan — 2026-08-23

**Author:** strategy pass (agent), grounded in this repo's canon + live external research.
**Truth rail (unchanged):** counts, slots, dates always defer to
[`https://councilof.ai/api/gspc`](https://councilof.ai/api/gspc). This doc never
hardcodes board numbers; it plans *moves*, not measurements.

> Companion docs: [`MASTER_PLAN.md`](MASTER_PLAN.md) · [`STEPS_100.md`](STEPS_100.md) ·
> [`ESTATE_INVENTORY.md`](ESTATE_INVENTORY.md) · [`GSPC_AXIS_CANON.md`](GSPC_AXIS_CANON.md)

---

## 0. Method + honest scope

- **Read:** all committed canon/plans in this repo, the ClaimGuard product + spec,
  the audit scripts, and the live route reality.
- **Researched (2026):** EU AI Act status post-Digital-Omnibus, Article 50
  content-marking enforcement, the independent-eval landscape (METR, Apollo,
  Epoch, Artificial Analysis, LMArena), and the signed-attestation stack
  (in-toto / SLSA / Sigstore / C2PA).
- **Could not see:** local `~/Downloads` (not in repo or any connected tool).
  Inbox scan (last ~3 weeks) showed **no inbound from labs, regulators, press, or
  investors** — pipeline is not yet running through email. That absence is a
  finding, not a neutral fact (see §8).

---

## 1. The single biggest tailwind nobody in our lane is chasing: **EU AI Act Article 50**

The high-risk regime got **deferred** (Digital Omnibus, Reg (EU) 2026/1744):
Annex III → **2 Dec 2027**, Annex I → **2 Aug 2028**. Everyone is relaxing about
high-risk. **But the transparency tier did *not* move**:

- **2 Aug 2026 — live now:** Article 50(2) requires providers of generative AI to
  mark synthetic audio/image/video/text in a **machine-readable** way, and to make
  a **detection solution available — free of charge** to the public, with
  **guaranteed free, unrestricted access to authorities, media, fact-checkers,
  independent researchers, and civil society.**
- **2 Dec 2026 — hard backstop:** content from systems already on the market must
  carry the marking.
- **2 Feb 2027 — the one that is ours:** deadline for an **interoperability
  solution between detection mechanisms.**
- The Commission's Code of Practice pre-clears a **dual layer**: **C2PA Content
  Credentials** (signed metadata, X.509/Ed25519) **+ a watermark** (e.g. SynthID).

**Why this is CSOAI's moment:** the law now *mandates* a free, neutral,
machine-readable **detection + provenance-verification** capability, and it
*privileges the exact constituencies we already serve for free* (researchers,
fact-checkers, media, authorities). We already have the two axes that map 1:1 to
this — **provenance (ProvBench)** and **detector-interop (DetBench)** — plus a
"verify free, forever" surface and signed receipts. Nobody in the benchmark crowd
(METR/Apollo/Epoch/Artificial Analysis) is chasing the **provenance + detection
interoperability** gap. We should plant the flag before 2 Feb 2027.

Sources: FPF EU AI Act timeline (Jul 2026); Orrick, *Article 50 transparency*
(Aug 2026); EU Commission Code of Practice on AI-generated content (adequacy
opinion 8 Jul 2026).

---

## 2. Landscape map — where we are differentiated vs exposed

| Player | What they do | Overlap with CSOAI | Read |
|---|---|---|---|
| **METR** (~$71M raised '26; EU AI Office TA; NIST consortium) | Autonomy / catastrophic-risk evals | Low — capability, not provenance | Partner/echo, not compete |
| **Apollo Research** (now PBC) | Deception / scheming, monitoring | Low | Partner/echo |
| **Epoch AI** (UK AISI grant; runs on **Inspect**) | Benchmark **aggregation**, reproducible | Medium — they aggregate, we sign | Interop target |
| **Artificial Analysis** | Commercial "Intelligence Index" | Medium — public leaderboard | Contrast: we're signed + free |
| **LMArena** | Crowd **Elo** | UX only | Steal UX, reject Elo-as-verdict (canon) |
| **C2PA / CAI** (Adobe, MS, Google, OpenAI; W3C) | Content provenance standard | **High + complementary** | **Adopt + verify against** |
| **in-toto / SLSA / Sigstore (Rekor)** | Supply-chain attestation | **High + complementary** | **Wrap our receipts into it** |
| **New: AIIR, LLM-Supply-Chain-Attestation** | Eval/commit receipts as in-toto Statements + Sigstore keyless + Rekor | **Direct on the receipt moat** | **Interop now or get standardised around** |

**Takeaway:** our differentiation (deterministic, law-graded, *signed*, "publishes
what it cannot measure", free verification) is real and *not* head-to-head with the
capability-eval labs. **The threat is narrower and sharper:** the signed-receipt
world is standardising on **in-toto + Sigstore + C2PA**, and new entrants are
building "eval attestations" natively in that stack. Our bespoke
Ed25519 / did:web / RFC 8785 receipts are excellent but risk becoming an **island**.

---

## 3. Gap analysis — what's missed / weak (repo + external)

**Product-truth gaps (from our own audit):**
1. **Apex is broken to a serious visitor.** `/lobby`, `/scorecard`, `/honesty`,
   `/verify`, `/api/chat` are REAL-404 on `councilof.ai` while the fat prerender
   lives on a `.pages.dev` host. Any journalist, regulator, or lab who checks sees
   a thin/oddly-404ing site. This is the #1 credibility leak (STEPS_100 Block B).
2. **Sitemap advertises hundreds of URLs that 404** — active trust debt.
3. **AG-UI is coded but not on the brand origin** (`/ag-ui` 308→lobby).
4. **HF estate not 100/100** — `gspc-xr` card is a DET clone; `affect`+`jail`
   Spaces missing; method DOI (`10.5281/zenodo.21991104`) missing on most cards.
5. **Chat count drift** vs `totals.public_count` (the exact failure ClaimGuard
   exists to catch — not yet wired into `/api/chat`).

**Moat / standards gaps (external):**
6. **Receipt interop:** no in-toto Statement wrapper, no transparency log, no C2PA
   compatibility → we can't be consumed by the SLSA/PEP-740/GitHub-attestation
   ecosystem, and can't yet be the neutral verifier the Code of Practice wants.
7. **Single-key fragility:** `did:web:csoai.org#board-attestation-1` is effectively
   one signing key with no published rotation or transparency log. For a body whose
   product *is* trust, key governance is underspecified.
8. **Distribution is human-only:** tools exist but aren't registered where agents
   discover them (A2A Registry — you *just joined* — and MCP directories).
9. **ClaimGuard is narrow:** it checks board-count/overclaim rules only. It does
   **not** yet verify C2PA manifests or Article-50 marking claims — the thing the
   market will actually pay attention to this quarter.

**Operational-hygiene risk (from inbox — brief, non-invasive):**
10. **Live surfaces at risk:** a hosting invoice (Krystal) is flagged overdue and
    at least two domains are near expiry. A CSOAI surface going dark *during* the
    Article-50 window would be self-inflicted reputational damage. Triage the
    infra that serves `councilof.ai` / `csoai.org` specifically.

---

## 4. Moat map — deepen what we already have

| Moat | Today | Deepen to |
|---|---|---|
| **Signed truth rail** | Ed25519 over RFC 8785, did:web | + in-toto Statement + transparency log + key rotation |
| **Honesty gate** ("we publish our own losses") | Live concept | Make it *the* citable norm; invite others to publish theirs |
| **Free verification** | `/gspc-verify/` | Reframe as the **Article 50 free detection endpoint** |
| **Two on-point axes** (provenance, detector-interop) | Measured | Publish the **detector-interop conformance suite** (the 2 Feb 2027 need) |
| **ClaimGuard** | Board-claim linter (landed) | Article-50 **claim + C2PA** linter; PyPI + MCP + GH Action |
| **Determinism / no-Elo discipline** | Canon-enforced | Keep as the trust contrast vs crowd-Elo boards |

---

## 5. Clever moves (prioritised by leverage × regulatory timing)

Each move: *what → why now → smallest first step (this repo where possible) → owner.*

### Move 1 — "Free detection endpoint" for Article 50 (**highest leverage**)
- **What:** publish `/api/detect` + a `/.well-known/` provenance verifier that
  reads a C2PA manifest and cross-checks signer/provenance against the signed board;
  brand `/gspc-verify/` as *the* free, no-account detection service the Code of
  Practice guarantees to researchers/media/fact-checkers.
- **Why now:** enforceable since 2 Aug 2026; free-access mandate is a distribution
  subsidy written into law.
- **First step (here):** spec `docs/ARTICLE50_DETECTION.md` (endpoint contract +
  C2PA fields: `DigitalSourceType=trainedAlgorithmicMedia`, manifest verify, PASS/FAIL).
- **Owner:** Lane A (apex) + Lane C (ClaimGuard).

### Move 2 — Interop the receipt moat into the standard stack (**deepest moat**)
- **What:** express each GSPC signed receipt as an **in-toto Statement v1** with a
  CSOAI predicate (`csoai.gspc/measurement/v1`), keep our Ed25519/did:web signature,
  and additionally log to a **transparency log** (Rekor or a CSOAI append-only log).
  Add C2PA/DSSE compatibility so PyPI (PEP 740), GitHub attestations, and auditors
  can consume us natively.
- **Why now:** AIIR + LLM-Supply-Chain-Attestation are standardising "eval
  attestations" in exactly this stack; interop now = we're the *measurement
  predicate*, not a silo.
- **First step (here):** `docs/RECEIPT_INTEROP.md` mapping our fields → in-toto
  subject/predicate + DSSE envelope; land converter in `signed-receipts`/`carder`.
- **Owner:** receipt-stack owner.

### Move 3 — ClaimGuard → Article-50 claim + provenance linter
- **What:** extend ClaimGuard rules to (a) verify C2PA manifests, (b) fail
  "content is marked/watermarked per Article 50" claims that don't verify, (c) keep
  board-count rules. Ship to **PyPI**, add **MCP `claimguard.check`**, add a
  **GitHub Action**.
- **Why now:** it's already landed + tested here; small delta, big surface.
- **First step (here):** add `claim.article50_*` rules + a `--c2pa <file>` path in
  `products/claimguard/`; PyPI packaging.
- **Owner:** Lane C.

### Move 4 — Agent-native distribution (A2A + MCP registries)
- **What:** finish `a2a-signed-receipts`, register the CSOAI measurement agent and
  `measure`/`verify`/`claimguard.check` on **A2A Registry** (you joined 22 Aug) and
  public **MCP directories**; expose an agent-card that points at the signed board.
- **Why now:** agents are becoming the buyers of verification; be discoverable
  before competitors' receipts are.
- **First step:** finish `a2a-signed-receipts` README + publish agent-card;
  submit registry listing.
- **Owner:** Lane B (AG-UI/wire).

### Move 5 — Detector-interoperability conformance suite (own the 2 Feb 2027 gap)
- **What:** publish DetBench as an **open, neutral interop test** for detection
  mechanisms (does detector X read mark Y?) — the thing the ecosystem must build by
  2 Feb 2027. Invite C2PA/CAI, Epoch, UK AISI (Inspect), and fact-checking networks
  to run against it.
- **Why now:** first mover on the interop test = de-facto convener.
- **First step (here):** `docs/DETECTOR_INTEROP_SUITE.md` scope + call for
  participants.
- **Owner:** Lane D (HF/benches).

### Move 6 — Credibility + key governance hardening
- **What:** (a) fix apex 404s + sitemap trust debt (Block B); (b) publish key
  rotation + transparency policy for `did:web:csoai.org`; (c) put method/evidence
  DOIs on all axis cards; (d) triage the infra hosting the live surfaces.
- **Why now:** we're about to invite scrutiny from exactly the people who check.
- **First step:** the owner actions already queued in STEPS_100 Block B + a
  `docs/KEY_GOVERNANCE.md` stub.
- **Owner:** owner + Lane A.

---

## 6. Next-week workstreams (leverage-ordered, gated — not calendar-padded)

> Ordered by leverage; each has a **done-when** gate, not an effort estimate.

- **W1 — Apex is real.** Owner actions from STEPS_100 Block B (disable Pages Git
  auto-deploy, gated deploy, alias pack). **Done when:** `/lobby`, `/scorecard`,
  `/verify`, `/honesty` are 200 on `councilof.ai` and `run-frontend-audit.mjs`
  persona gauntlet ≥ 7/8.
- **W2 — Article 50 detection spec + `/api/detect` stub.** **Done when:**
  `docs/ARTICLE50_DETECTION.md` merged and a stub endpoint verifies a sample C2PA
  manifest against the board.
- **W3 — Receipt interop spec + converter.** **Done when:** one live board receipt
  round-trips as an in-toto Statement + DSSE and re-verifies.
- **W4 — ClaimGuard v0.2 (Article 50 + C2PA) to PyPI + MCP.** **Done when:**
  `pip install claimguard` works and `claimguard.check` is callable as an MCP tool.
- **W5 — Agent distribution.** **Done when:** CSOAI agent-card + tools listed on
  A2A Registry and at least one MCP directory.
- **W6 — HF 100/100 + DOIs + detector-interop call.** **Done when:** XR card fixed,
  affect+jail Spaces live, method DOI on all cards, interop suite doc published.

Wire everything into CI: `claimguard --self-test`, `drift-guard`,
`run-frontend-audit.mjs` on schedule (STEPS_100 #95).

---

## 7. Connections to open this week (target · why · the ask)

| Target | Why them | The specific ask |
|---|---|---|
| **EU AI Office** (already takes METR TA) | They need free, neutral detection/interop for Article 50 | Offer DetBench as an open interop reference + free verify endpoint |
| **C2PA / Content Authenticity Initiative** | Our provenance axis verifies their manifests | Become a public **verifier** listed in their ecosystem |
| **Epoch AI** | They aggregate on Inspect; we sign | Contribute **signed** GSPC results to their board; cross-cite |
| **UK AISI (Inspect team)** | Inspect is the eval substrate | Publish GSPC axis tasks as Inspect evals → distribution |
| **EFCSN / fact-checking networks** | Law guarantees them free detection access | Onboard them to the free verify endpoint as design partners |
| **Hugging Face** | Our 14 axis banks live there | Get the org profile + Spaces to link the living board; co-post |
| **A2A Registry** (joined 22 Aug) | Agent-native distribution | List the measurement agent + signed-receipt tool |

Rule (Firewall Charter): every one of these is *measurement + free access*, never a
paid rank. Keep the ask clean.

---

## 8. IP to grow / protect this week

1. **Publish the interop specs as citable IP** (`ARTICLE50_DETECTION.md`,
   `RECEIPT_INTEROP.md`, `DETECTOR_INTEROP_SUITE.md`) with Zenodo DOIs — turns
   strategy into referenceable standards work.
2. **PyPI-publish ClaimGuard** — a named, versioned, installable instrument is
   defensible surface + adoption telemetry.
3. **DOI every axis card** (method `10.5281/zenodo.21991104`, evidence
   `10.5281/zenodo.21973002`) — provenance of the board itself.
4. **Key-governance + transparency-log policy** — makes the signature *institution-
   grade*, not a single-key hobby.
5. **Trademark / naming hygiene** — lock "GSPC", "Council of AI", ClaimGuard usage
   consistent with canon before broader outreach draws attention.
6. **No email pipeline yet = opportunity:** a single well-placed post (Article 50 +
   free detection) aimed at researchers/journalists is likely the cheapest inbound
   we can manufacture.

---

## 9. What the owner has to do (agents can't)

- Cloudflare: disable Pages Git auto-deploy on `councilof-ai`, run gated deploy
  (STEPS_100 Block B/G).
- Set `AGUI_WIRE_URL`; deploy `csoai-static-deploy2`.
- HF write token → apply `docs/hf-patches/**`; create affect+jail Spaces.
- **Infra triage:** confirm the hosting/domains serving `councilof.ai` + `csoai.org`
  are paid and not expiring (inbox flagged overdue/expiry items).
- Approve PyPI + registry publishing for ClaimGuard / agent-card.

---

## 10. One-line thesis

**The high-risk delay pulled everyone's attention away from the exact tier where we
already have the instrument — Article 50 provenance + free, interoperable detection.
Interop our signed receipts into the C2PA / in-toto / Sigstore stack, ship the free
detection endpoint the law now guarantees, and convene the 2 Feb 2027 detector-
interop test — while fixing the apex so the people the law sends us don't see a 404.**
