# Move 4 — Agent-native distribution (A2A Registry + MCP + agent-card)

**Status:** design · **Owner:** Lane B (AG-UI/wire) · **Signal:** owner joined
**A2A Registry** 2026-08-22 — the distribution rail is already half-open.

> Tools point at the signed board [`/api/gspc`](https://councilof.ai/api/gspc);
> nothing here hardcodes counts.

---

## Thesis

The next buyers of verification are **agents**, not humans. When an agent needs to
check "is this model's governance grade real?" or "is this content Article-50
marked?", it should discover a CSOAI tool and get a **signed** answer. We already
have the tools (`measure`, `verify`, `jail-probe`, `enter-arena`, and now
`claimguard.check`); they just aren't listed where agents look.

## Chess frame

- **Our move:** publish an **A2A agent-card** + register the measurement agent and
  MCP tools on **A2A Registry** and public **MCP directories**, each returning a
  **signed receipt** (Move 2 shape).
- **Opponent replies:** (1) a lab exposes its own "eval" tool → ours is
  cross-lab + signed + free-to-verify; (2) a registry floods with unsigned
  "rating" tools → we're the one whose output *verifies*; (3) MCP catalog sprawl
  (our own ~356 repos) dilutes us → we list **one** canonical measurement agent,
  not 356 (canon rule: catalog count is not readiness).
- **Tempo:** registries reward early canonical entries with ranking + citations.

---

## Deliverables

### 1. Agent-card (`/.well-known/agent-card.json` — already 200 on apex)
Extend it to advertise the tool surface + signed-receipt capability:
```jsonc
{
  "name": "Council of AI — measurement agent",
  "provider": { "organization": "CSOAI Ltd", "url": "https://councilof.ai" },
  "did": "did:web:csoai.org",
  "doi": "10.5281/zenodo.21991104",
  "capabilities": { "signed_receipts": true, "streaming": true },
  "skills": [
    { "id": "measure",  "description": "Deterministic GSPC axis grade (signed)" },
    { "id": "verify",   "description": "Verify a signed board/receipt" },
    { "id": "detect",   "description": "Article 50 / C2PA provenance verify (free)" },
    { "id": "claimguard.check", "description": "Fail overclaims + unbacked Article 50 marking" }
  ],
  "endpoints": { "mcp": "https://councilof.ai/.well-known/mcp.json",
                 "a2a": "https://councilof.ai/api/agui" }
}
```

### 2. `a2a-signed-receipts` — finish it
Currently DRAFT SPEC only (per estate inventory). Ship: README + reference
verifier + one worked example where an A2A response carries a DSSE/in-toto receipt
(Move 2). This is the *novel* wedge: **agent-to-agent verifiable measurement**.

### 3. Registry listings
| Registry | Listing | Note |
|---|---|---|
| **A2A Registry** (joined 22 Aug) | measurement agent + agent-card | primary |
| **MCP directories** (public) | one canonical GSPC MCP server | not 356 repos |
| **HF** org profile / Space | link board + agent-card | co-distribution |

### 4. `claimguard.check` as an MCP tool
Wrap ClaimGuard v0.2 (`audit()` + `--c2pa`) as MCP `claimguard.check` on the GSPC
worker so agents can lint their own claims before publishing.

## Build steps
1. Extend `/.well-known/agent-card.json` (councilof-ai) with skills + `signed_receipts`.
2. Finish `a2a-signed-receipts` README + reference verifier + example.
3. Add `claimguard.check` to `.well-known/mcp.json` worker tools.
4. Submit A2A Registry + one MCP directory listing (owner action — auth).
5. `e2e-integration-stack.mjs`: assert agent-card advertises the new skills.

## Done-when
An external agent can (a) discover the CSOAI measurement agent via A2A Registry,
(b) call `verify`/`detect`/`claimguard.check`, and (c) get a receipt that
re-verifies offline. `mcp.json` lists `claimguard.check`.

## Non-goals
Not listing 356 MCP repos as "readiness." Not a paid API. Not agent actions that
write a grade without HITL consent (MASTER_PLAN Phase 2).
