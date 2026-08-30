# Where the work lives

This repository is **org profile + community-health defaults only**.
Do not dump the SPA, measurement packages, or GPU jobs here.

| Surface | Repo | Deploy |
|---|---|---|
| Public site, Council OS, DSH | [CSOAI-ORG/councilof-ai](https://github.com/CSOAI-ORG/councilof-ai) | Cloudflare Pages `councilof-ai` → [councilof.ai](https://councilof.ai) |
| DID / static keys | [CSOAI-ORG/csoai-static-deploy2](https://github.com/CSOAI-ORG/csoai-static-deploy2) | Pages `csoai-site` → [csoai.org](https://csoai.org) (`did:web:csoai.org`) |
| Signed packages + fleet | [CSOAI-ORG/councilof-ai-monorepo](https://github.com/CSOAI-ORG/councilof-ai-monorepo) | Not the public site. See `ops/ESTATE-MAP.md` there. |

AG UI **is** Council OS: [councilof.ai/os](https://councilof.ai/os) (operable product frame). `/?lobby=*` on `/` is a dead dump.
Verify (use the slash until aliases land): [councilof.ai/gspc-verify/](https://councilof.ai/gspc-verify/).
Living board: [GET /api/gspc](https://councilof.ai/api/gspc) — quote `totals.public_count`. Do not hardcode counts.
Cursor / Grok MCP: [councilof.ai/mcp](https://councilof.ai/mcp).

**Cloud agents and automations.** Start them against [CSOAI-ORG/councilof-ai](https://github.com/CSOAI-ORG/councilof-ai), not this profile repo. A multi-repo environment may include this repo for community-health files; the working tree for site and Council OS is `councilof-ai` on `master`. Official success is `.github/workflows/deploy.yml` **build-deploy**. Ignore Vercel reds. Card catalog counts live on the API — do not restore a frozen verify total.

**Do not** redeploy the SPA onto `csoai-site`. **Do not** enable Pages Git auto-deploy on `councilof-ai` (clobbers the gated prerender). There is no RunPod wiring in this estate; fleet packages live in the monorepo.
