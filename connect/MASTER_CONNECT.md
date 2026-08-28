# CSOAI ESTATE — MASTER CONNECT

**Paste this whole file to any agent: DSH, Cursor, Grok Bot, Claude.**  
**Revision:** 2026-08-27 · Endpoints verified live at time of writing.  
RunPod SSH ports **MOVE** when a pod restarts — if a connect fails, re-resolve via the API (below); never assume the pod is dead.

---

## Part 1 — Fleet connection + working agreement

### The stack (one line each)

| Surface | Role |
|---------|------|
| **MacBook** | Control plane ONLY. Never build here. ~5GB free. |
| **RunPod** | Compute: builds, measurement, mining, GPU work. |
| **Oracle** | `oracle-micro-2` = always-on tiny box: RAG mirror, cron, keepalives. |
| **GitHub** | `CSOAI-ORG/councilof-ai` = single source of truth. **master only.** |
| **Cloudflare** | Pages project `councilof-ai` serves councilof.ai (production alias). |
| **Cursor** | Codebase indexes 187 repos, synced from GitHub. Read-only truth-hint. |

### RunPod pods (running now, ~$1.91/hr total)

| SSH | Pod | GPU | Role |
|-----|-----|-----|------|
| `ssh -p 12473 root@194.26.196.156` | sov-repull-20260808 | RTX3090 | **BUILD BOX** — repo at `/workspace/councilof-ai`, node22, deps installed. Site builds run here. |
| `ssh -p 13440 root@38.128.232.57` | sovos-light-master-mine | A100-class $1.39/hr | **MEASUREMENT ENGINE** — ollama fleet (14 models), `axis-engine.sh` + `arena-auto-loop.sh`. DO NOT STOP without checking `nvidia-smi` and `pgrep -af "axis\|arena\|ollama"` first — API shows gpu=0% **between batches**; it lies. |
| `ssh -p 39331 root@38.80.152.147` | oowm-agent-01-hub | cpu | OOWM hub |
| `ssh -p 53390 root@213.173.105.92` | oowm-agent-03-mine | cpu | OOWM miner |
| `ssh -p 33035 root@213.173.105.102` | oowm-agent-04-route | cpu | OOWM router |
| `ssh -p 41054 root@103.196.86.88` | oowm-agent-05-product | cpu | OOWM product |
| `ssh -p 55664 root@213.173.105.83` | sov-volume-sink-cpu | cpu | **Durability sink** — ONLY pod with network volume `sovos-merge-800` (800GB, EU-RO-1) |

**Re-resolve moved SSH ports** (key lives in `~/.runpod/config.toml` on the Mac):

```bash
K=$(grep -oE '[a-zA-Z0-9_-]{20,}' ~/.runpod/config.toml | head -1)
curl -s "https://api.runpod.io/graphql?api_key=$K" -H 'Content-Type: application/json' \
  -d '{"query":"query{myself{pods{name desiredStatus runtime{ports{ip isIpPublic privatePort publicPort}}}}}"}'
```

### Network volumes (survive pod stop; region-locked)

| Volume | Size | Region | Notes |
|--------|------|--------|-------|
| sovos-merge-800 | 800GB | EU-RO-1 | Attached to sov-volume-sink-cpu. **NEVER delete.** |
| k3-weights-2tb | 2000GB | EU-RO-1 | Model weights |
| sov-models | 300GB | CA-MTL-3 | Models |
| sov-artifacts | 200GB | CA-MTL-3 | Artifacts |
| sov-workspace | 200GB | CA-MTL-4 | Workspace |

**Rules:** a volume attaches only to pods in **its** datacenter. Pod-local `/workspace` disks survive STOP but die on TERMINATE — stop, never terminate, unless ruled. RunPod bills provisioned volume disk on stopped pods too (email 27 Aug) — stale stopped pods still cost money; flag them, don't silently delete.

### Oracle

```bash
ssh oracle-micro-2   # 141.147.73.85, ubuntu; in ~/.ssh/config; up 3+ weeks
```

956MB x86 free-tier box. RAG mirror at `/home/ubuntu/rag/`. Cron + keepalive only. It is **NOT** 24GB ARM — old docs claiming that are wrong. Nothing heavy runs here.

### Git: one tree, one truth

| | |
|---|---|
| **repo** | `git@github.com:CSOAI-ORG/councilof-ai.git` |
| **branch** | `master` is the ONLY integration branch. Rebase onto `origin/master` first. |
| **source** | `client/` — the root `src/` dir is **DEAD**, never edit it. |

- **DO NOT** create worktrees. Yesterday 25 worktrees each ran a dev server on its own port; every person saw a different site. Branch in the main checkout.
- **DO NOT** push in rapid bursts — Cursor's push treadmill starved the GitHub Actions queue (14 queued / 0 running). Batch pushes; one push per finished unit.
- Stage by name. Never `git add -A` in the main checkout.

### Owner rulings — decisions, not bugs. DO NOT "FIX".

1. `public/signed/card_index.json` = **EXACTLY 150 rows** (commits 7294a9a5, 6657a4da). 313 card files exist on disk. That mismatch is **INTENDED**. Do not reconcile.
2. `public/signed/chain.json` is deliberately **DELETED**. Do not restore.
3. `scripts/signed-json-guard.mjs` enforces both. If you think they're wrong, **SAY so to Nick** — do not change them. Reverted 4× yesterday. Never again.

### Build + gates (run on the 3090, not the Mac)

```bash
cd /workspace/councilof-ai && git fetch origin master && git reset --hard origin/master
npm install --no-audit --no-fund
npm run build:client
node scripts/prerender.mjs --dist dist/client --wait 900 --min 350
for g in check-prerender price-gate brand-gate signed-json-guard facts-gate pages-size-guard; do
  node scripts/$g.mjs dist/client || exit 1
done
```

**A GREEN BUILD IS NOT PROOF.** `check-prerender` PASSES pages that crash on hydration (React error boundary renders >350 chars — logged as **C-2026-0826-01**, bit us twice). After gates:

```bash
cd dist/client && python3 -m http.server 4321
```

Then **LOAD** `/`, `/os/`, `/products/`, `/compare/` in a real browser. No error boundary, real text, or it does not ship.

### Deploy (all three aliases or the apex stays stale)

```bash
npx wrangler pages deploy dist/client --project-name=councilof-ai --branch=production --commit-dirty=true
npx wrangler pages deploy dist/client --project-name=councilof-ai --branch=main --commit-dirty=true
npx wrangler pages deploy dist/client --project-name=councilof-ai --branch=master --commit-dirty=true
```

`councilof.ai` follows **PRODUCTION**. Verify on councilof.ai itself, never a preview URL. `csoai.org` 301s to councilof.ai (project `csoai-site` serves the redirect). Leave it.

### Content rules (gates enforce; violations block deploy)

- Never "certification" as a thing we issue. We **measure**. Never "we enforce".
- No public prices. No popularity claims. No internal codenames in public.
- **NEVER type a count.** Numbers derive from `GET /api/gspc` or `GET /api/state` (both carry `kind` + `as_of`). Board = **22 axes · 15 measured · 7 unmeasured** — read it, don't write it.
- `unmeasured` is a first-class published status. Never hide, shrink or grey it.
- New routes must be registered in `PRIMARY_PATHS` (`client/src/data/library-ia.ts`) or they ship flagged "archived".

### The defect we hunt (before claiming any fix works)

A checker that cannot observe its own failure; a name promising what code doesn't deliver. Real cases this week: prerender reading a never-written field (515 failures → "0 errored"); `"signed": true` with no signature bytes; a verifier passing a **FORGED** card; a TSA "ok" recorded from an RFC-3161 **REJECTION**; UNMEASURED reported for five measured axes. So: feed your fix the bad input it used to accept and **SHOW it failing**. A verify that cannot fail is not a verify.

### Verify cards (anyone, offline, no account)

```bash
curl -s https://councilof.ai/signed/verify-card.mjs -o v.mjs && node v.mjs card.json
```

Pins `did:web:csoai.org#card-attestation-1`. Three states, never two: **VALID** / **INVALID(reason)** / **UNCHECKABLE**. Could-not-check ≠ forged.

### Lane etiquette (all agents)

- Announce your lane in `councilof-ai/LANE_COORDINATION.md` before starting; check it first. *(Note: older paste said `council-os/LANES.md` — that path does not exist; use `LANE_COORDINATION.md`.)*
- One lane = one branch = one concern. Do not touch another lane's files.
- Kill every dev server you start. Check `lsof -iTCP -sTCP:LISTEN` before adding one.
- Report failures verbatim. Never summarize a red gate as "mostly passing".

---

## Part 2 — Durability, roadmap, identity

### Durability (live as of 2026-08-27)

The sink pod (`sov-volume-sink-cpu`, `ssh -p 55664 root@213.173.105.83`) runs `/workspace/durability-sync.sh` via cron at **:17 every 2 hours**. It PULLS `/workspace` from the 3090 build box and the A100 measurement engine onto the 800GB network volume `sovos-merge-800` (survives stop AND terminate).

| | |
|---|---|
| **log** | `/workspace/durability-sync.log` on the sink — entries say OK or FAIL with timestamp; FAIL after pod restart usually means source SSH port moved — update hardcoded ports (12473 and 13440 today) |
| **backups** | `/workspace/durability/3090-build/` and `/workspace/durability/a100-measure/` |
| **excluded** | `node_modules`, `dist`, `.ollama`, `*.gguf`, `*.safetensors` — models re-pull; WORK does not |

**Rule:** stop pods, never terminate — but if something is terminated anyway, the sink has everything up to the last :17 sync.

### S3 / keystones

RunPod network volumes expose an S3-compatible API (endpoint per datacenter, e.g. `s3api-eu-ro-1.runpod.io` for sovos-merge-800). Access keys are minted in RunPod console under Settings → S3 keys — an owner step; agents cannot create them. Once Nick mints a key pair, keystone artifacts (signed boards, card stores, chain snapshots) should be `aws s3 cp`'d there as the third copy: pod-local → network volume → S3 API reachable from anywhere. Until those keys exist, the sink volume is the durability floor.

### 90-day technical roadmap (decided — execute in order, do not relitigate)

1. **CANONICALIZATION (weeks 1–3):** adopt RFC 8785 (JCS) as v2 preimage rule. Add signed-in-body `canon` field: `"jcs-rfc8785"` for NEW cards; absent field = legacy CPython v1 rule. NEVER re-sign existing v1 cards — verifier dispatches on the field.
2. **OMISSION GAP (weeks 2–6):** linear hash chain CANNOT detect omission inside a withheld run — stop claiming otherwise. Target COSE Receipts (RFC 9942) + SCRAPI api shape; self-host Trillian-Tessera or anchor into Rekor.
3. **SIGNING (weeks 3–8):** "3-of-3 MPC" is three shares on ONE machine = single failure domain. Migrate to FROST-Ed25519 with shares in distinct trust domains. FROST emits standard Ed25519 sig — pinned DID key and verifiers stay unchanged.
4. **MEASUREMENT (weeks 4–10):** Inspect AI primary harness; lm-evaluation-harness for capability baselines; garak + PyRIT for adversarial axes. Sign each run as MEASUREMENT with config digest + instrument version in preimage.
5. **DISTRIBUTION (weeks 6–12):** ship `verify-card.mjs` under MIT with live browser demo (VALID / INVALID / UNCHECKABLE). HuggingFace Space running it. Council OS canvas: fork OpenCompany or Activepieces — build ONLY measure→sign→re-attest node.

**Do-not list:** ERC-3643/tokenization; Sigstore keyless/Fulcio; C2PA trust lists (vocabulary only); n8n for third-party hosting (use Activepieces).

### Business identity (use these, never invent)

| | |
|---|---|
| **Email** | nicholas@csoai.org (ALL business mail; privateemail.com) |
| **Company** | CSOAI LTD · Companies House 16939677 · 3rd Floor, 86-90 Paul Street, London EC2A 4NE |
| **GitHub** | org CSOAI-ORG (gh CLI authed on Mac; token has repo+workflow) |
| **HF** | user Nicholastempleman; org csoai — use `huggingface-cli` token; `HF_TOKEN` in `~/.env` is **DEAD** |
| **DID** | `did:web:csoai.org` — 4 published keys; cards pin `#card-attestation-1` |

### Sign-ups, auth, browser on pods (honest boundary)

The A100 has Chromium + Playwright installed. Agents **may:** drive an already-authenticated session (Nick logs in once, profile persists), fill research/prep, stage applications to submission point. Agents **must NOT:** create accounts, enter passwords, complete sign-ups, accept ToS, or send email on Nick's behalf without explicit go. Free-tier programmes worth staging (£0): NLnet NGI Zero (call opens 3 Sep, UK eligible), AIRR Rapid Access (20k GPU hours), NVIDIA Inception, HuggingFace org credits. Stage forms; hand Nick the submit button.

---

## Part 3 — Repo addendum (2026-08-27, from live probes + overnight lane)

*This section is what agents in `CSOAI-ORG/.github` and Cursor cloud runs need on top of Parts 1–2.*

### Multi-repo map (do not conflate)

| Repo | Branch | Owns |
|------|--------|------|
| `CSOAI-ORG/councilof-ai` | **master** | Site (`client/`), Pages deploy, `/api/*`, signed artifacts, gates |
| `CSOAI-ORG/.github` | **main** | Ops register, `connect/` outreach stubs, ClaimGuard export, overnight verify |
| `CSOAI-ORG/csoai-static-deploy2` | **main** | MCP Worker (`csoai-gspc-mcp`), `csoai.org` static chrome, honesty/arenas |

Cloud agents boot in `.github`. Site changes require `councilof-ai` on the 3090 build box.

### ADR-001 dual counts — read both layers, never conflate

Live `GET https://councilof.ai/api/gspc` (verified 2026-08-27):

```json
{
  "totals": {
    "public_count": "22 axes · 15 measured",
    "measured_axes": 15,
    "quotable_axes": 15,
    "by_family": {
      "gspc": { "axes": 14, "measured": 14 },
      "financial": { "axes": 8, "measured": 1 }
    }
  }
}
```

| Layer | Count | Use when |
|-------|-------|----------|
| **Board (site API)** | 22 · 15 measured · 7 unmeasured | Public copy, homepage grammar, `public_count` — **read from API, never type** |
| **GSPC family** | 14 measured of 14 | Behavioural measurement instrument, jail TIE, directory PRs citing GSPC |
| **Signed export** (`export/gspc-board/board.json`) | 14/14 | ClaimGuard, offline verify, HF dataset spine — unchanged until owner re-signs |

**Owner reconcile pending:** `ops/verify-overnight-pack.sh` with `STRICT=1` still expects `14 measured of 14` in `public_count` and will **FAIL** until verify script + badges + agent-card + AGENT-ONBOARDING are updated with owner ruling. ClaimGuard on export still **PASS**es 14/14. Do not "fix" the API or export from an outreach lane — escalate to Nick.

### Stale surfaces (may lag ADR-001)

Until owner reconcile + deploy, these may still cite **14/14** while live API says **22·15**:

- `public/AGENT-ONBOARDING.md` (CDN)
- `badge/axes.json`, `api/feed.xml`
- Directory PR bodies in `connect/directories/*`
- MCP registry description "14 of 14" (registry **1.0.3** is live; Worker runtime may still answer **1.0.0** until `CF_API_TOKEN` restored — see `ops/cf-api-token-restore.md`)

### `connect/` directory (this repo)

| Path | Purpose |
|------|---------|
| `connect/MASTER_CONNECT.md` | **This file** — fleet paste + addendum |
| `connect/agent-cards/` | A2A card generator + validator |
| `connect/mcp/gspc/server.json` | MCP registry manifest |
| `connect/a2a/directory-submissions.md` | A2A + aggregator status |
| `connect/directories/*.md` | Awesome-list PR drafts (7 submitted 2026-08-25) |

### Owner gates (cannot execute from agent lane)

See `ops/morning-sheet-owner-actions-2026-08-25.md`:

1. **Kaggle** — token → `/tmp/csoai-secrets/kaggle.json`
2. **Discussion #97** — personal GH session (2FA)
3. **CF_API_TOKEN + CF_ACCOUNT_ID** — MCP Worker 1.0.3 + `csoai.org` honesty/arenas deploy
4. **CONFIRM** HF Team / RunPod spend
5. **ADR-001 reconcile** — verify script canon vs live `public_count`

### Cross-repo write permissions

- `cursor[bot]` often gets **403** on `gh` push to forks — use **GitHub MCP** for cross-repo PRs.
- Never remint DOIs: `10.57967/hf/10114` (board), `10.57967/hf/10116` (bench). Methodology spine on live API: `10.5281/zenodo.21991104`.

### card_index war (structural, not cosmetic)

`LANE_COORDINATION.md` adjudicates: automation pushed **41-byte stub** (`__LOAD_FROM__/tmp/...`) claiming 75578B; honest restore = **150 rows** (owner ruling). `signed-json-guard.mjs` blocks stubs on deploy. Do not join the 335-card storm.

### Overnight verify (`.github` lane)

```bash
STRICT=1 bash ops/verify-overnight-pack.sh
bash ops/claimguard-publish-gate.sh export trust/evidence-pack
```

Register tip: `ops/overnight-register-2026-08-24.md`. Mining gaps: `ops/knowledge/outreach.sqlite`.

### Machine surfaces (quick ref)

| Surface | URL |
|---------|-----|
| Living board | https://councilof.ai/api/gspc |
| State | https://councilof.ai/api/state |
| Agent card | https://councilof.ai/.well-known/agent-card.json |
| Verify | https://councilof.ai/gspc-verify |
| MCP | https://councilof.ai/mcp (registry `io.github.CSOAI-ORG/gspc`) |
| DID | https://csoai.org/.well-known/did.json |
| Compliance Training World | https://councilof.ai/compliance-training-world/catalog.html *(ships on councilof-ai #863)* |
| Council OS | https://councilof.ai/os |

### Agent pivot — 2026-08-28 (read this first if you just joined)

| Do | Don't |
|----|-------|
| Align from **live master** + this file + JEEVES `docs/MASTER_RUNDOWN_NEXT100_2026-08-28.md` | Mine old overnight-register timer loops / post-FINAL SUPPRESSED logs |
| Ship free site + Council OS gaps (training world, product doors, count honesty) | Reopen closed #819 `cursor/council-os-harmony-ff6e` |
| Quote `totals.public_count` from `GET /api/gspc` (`22 axis · 15 measured` as of this note) | Invent / hardcode "22 measured" or remint DOIs |
| Prefer product PRs on `councilof-ai` (e.g. **#863** training + doors) | Keep appending identical overnight register reaffirms on `.github` #74 |
| **Owner:** disable Cursor automation `ralph-overnight-until-4am` | Wait for the timer to invent new work |

Live board probe at this note: `public_count=22 axis · 15 measured` · ClaimGuard export still `14/14` GSPC family.

---

*End MASTER CONNECT. When in doubt: probe live endpoints, read `LANE_COORDINATION.md`, append — never silently "fix" owner rulings.*
