# Patch — add the Article 50 `detect` skill to the agent-card

**Target:** `CSOAI-ORG/councilof-ai` → `public/.well-known/agent-card.json`
(static file). **Additive only** — matches the existing skill schema and the
"explicitly_not / measurement only" framing. Pairs with the `/api/detect` Function
in `../councilof-ai-article50-detect/`.

## Why
The agent-card advertises `gspc-board`, `measured-badge`, and
`benchmark-quality-register`, but not the free Article 50 **detection/verification**
surface. Agents (and the constituencies Article 50 privileges) should be able to
discover it.

## Apply
Insert this object into the existing `"skills"` array (same shape as the others):

```json
{
  "id": "article50-detect",
  "name": "Article 50 provenance detection (free)",
  "description": "Verify a C2PA-style signed manifest for AI-generated content (EU AI Act Article 50). Deterministically checks the Ed25519-signed metadata layer and the IPTC/schema.org digitalSourceType; returns AI_MARKED / NOT_AI_MARKED / UNVERIFIABLE with a signed verdict receipt. The imperceptible-watermark layer we cannot see is declared, never claimed. Free for all; unrestricted for authorities, media, fact-checkers, researchers and civil society. Not certification.",
  "endpoint": "https://councilof.ai/api/detect",
  "tags": ["article-50", "provenance", "detection", "verification", "c2pa"]
}
```

Optional follow-ups (only once the backing surfaces exist — keep the card honest):
- `claimguard-check` skill once `claimguard.check` is wired as an MCP tool
  (`/.well-known/mcp.json`); do not advertise it before it responds.
- A top-level `"signed_receipts": true` only after `/api/detect` emits the in-toto/
  DSSE receipt from `../councilof-ai-article50-detect/intoto.ts`.

## Notes
- Keep `explicitly_not` and the measurement-only framing unchanged.
- No hardcoded board counts — the `gspc-board` skill already points at the live API.
- Deploy discipline: gated only (DEPLOY-LOCK); static file ships with the SPA build.
