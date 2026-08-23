# Next 100 steps — execute order

Status legend: ✅ done this run · 🔧 ready (patch/PR) · 👤 owner dashboard · ⏳ next agent

## Block A — Canon & track-loss (1–15)
1. ✅ Confirm 14 board + 2 in-lane (not 16 quotable)
2. ✅ Lock axis names in `docs/GSPC_AXIS_CANON.md`
3. ✅ Mine estate → `docs/ESTATE_INVENTORY.md`
4. ✅ Master plan Moody’s×Arena×AG-UI → `docs/MASTER_PLAN.md`
5. ✅ Reject Elo-as-public-GSPC in canon
6. ✅ Flag ClaimGuard chat-only → now landed
7. ✅ Create `CSOAI-ORG/claimguard` repo
8. ✅ Land `claimguard.py` + RFC8785 `canonical.py`
9. ✅ Self-test + pytest (mutation fails)
10. ✅ Live audit rejects 16-axes + jail-separation-resolved
11. ✅ CI workflow on claimguard
12. ✅ Product spec dated 2026-08-22
13. 🔧 Mirror ClaimGuard under `.github/products/claimguard`
14. ⏳ MCP tool `claimguard.check`
15. ⏳ Wire ClaimGuard into `/api/chat` claim path

## Block B — Apex fat restore (16–35)
16. ✅ Diagnose thin apex (7016 B) vs fat host
17. ✅ Read DEPLOY-LOCK (Pages Git race)
18. ✅ Confirm canon.json min_homepage_bytes=20000
19. ✅ Confirm assert-prerender-live checks CouncilLobby
20. ✅ Branch `cursor/apex-clobber-runbook-ff6e` on councilof-ai (PR #312 closed)
21. ✅ Ops runbook: disable Pages Git auto-deploy
22. 👤 Cloudflare dashboard: disable automatic Git deployments on `councilof-ai`
23. 👤 Re-run GHA `Build + deploy site` (workflow_dispatch)
24. ✅ Assert apex ≥20KB + CouncilLobby chunk (213 KB, 2026-08-23 audit)
25. 🔧 Assert `/lobby` `/scorecard` `/honesty` `/gspc-verify/` 200 (aliases still 404)
26. ⏳ Assert `/` still fat ~2 min later (clobber window)
27. 🔧 Drift-guard green (2 drifts: /library, /honesty)
28. ⏳ Fix sitemap URLs that REAL-404
29. 🔧 Align `/api/chat` public_count with totals (/api/chat 404)
30. ⏳ LivingBoard on home
31. 🔧 Moody’s scorecard on apex `/scorecard` (404)
32. 🔧 Honesty Elo disclosure page (404)
33. ⏳ Live ledger route
34. 🔧 Verify free route (/verify 404; /gspc-verify/ works)
35. ⏳ Document production alias = gated GHA only

## Block C — AG-UI ask→does-it (36–55)
36. ✅ Confirm `csoai-agui-wire` code exists
37. ✅ Confirm MCP worker tools measure/verify/jail/enter-arena
38. ⏳ Deploy AG-UI under `councilof.ai/agui`
39. ⏳ Point catalog MCP URL at real worker
40. ⏳ Lobby deep-links → same session grammar
41. ⏳ HITL consent before grade-claiming writes
42. ⏳ Session ledger hash-chain public
43. ⏳ Ask “governance leader?” → tool → board row
44. ⏳ Ask “verify this grade” → verify tool
45. ⏳ Ask “enter arena” → enter-arena
46. ⏳ ClaimGuard.check as MCP tool in wire
47. ⏳ Integrity tile on Council Ledger
48. ⏳ Remove orphan GH Pages dependency
49. ⏳ E2E: ask→measure→verify smoke
50. ⏳ Persona gauntlet includes AG-UI path
51. ⏳ Document RAS = Receipts+Arena+Scorecard over AG-UI
52. ⏳ CopilotKit L2 optional later
53. ⏳ Do not dual-ship undeployed dashboard
54. ⏳ Arena UX stays law-graded (no public Elo)
55. ⏳ Scorecard tiles = Wilson + separation

## Block D — HF / Kaggle 100/100 (56–80)
56. ✅ Confirm XR card is DET clone
57. 🔧 Patch `docs/hf-patches/gspc-xr/README.md`
58. ✅ Confirm affect duplicate YAML
59. 🔧 Patch affect README (deduped + DOI)
60. 🔧 Patch jail README to axis template
61. 🔧 Space scaffolds for affect + jail
62. 👤 Upload XR README to HF (`huggingface-cli upload`)
63. 👤 Upload affect + jail README
64. 👤 Create Spaces `csoai/gspc-affect` + `csoai/gspc-jail`
65. ⏳ Add method DOI to all 14 axis cards
66. ⏳ Add `task_categories` to all 14
67. ⏳ Rebuild `gspc-normalized` (+care/affect/jail)
68. ⏳ Sync Kaggle XR after HF fix
69. ⏳ Carder valve pass on all 14
70. ⏳ Codabench README
71. ⏳ Confirm practice bank hash seal
72. ⏳ Zenodo cite on papers + boards meta
73. ⏳ Space index.html n/state from API (optional JS)
74. ⏳ Kill stale “12 benchmarks” eyebrow on Spaces
75. ⏳ Update superseded alias cards still pointing wrong
76. ⏳ HF org profile links living board
77. ⏳ AEO: llms.txt / agent.json for HF where applicable
78. ⏳ Screenshot / visual QA Spaces
79. ⏳ Public count string identical HF↔site↔API
80. ⏳ Declare HF 100/100 gate passed

## Block E — N-site scale (81–100)
81. ⏳ Extract shared AEO/AGUI pack from openmoe/landlaw
82. ⏳ Parameterize brand + skills
83. ⏳ Prove pack on openmoe-site
84. ⏳ Prove pack on landlaw-site
85. ⏳ Prove pack on diyhelp-site
86. ⏳ Industry: fintech-industries-site
87. ⏳ healthtech → govtech → regtech → care
88. ⏳ Defer pokerhud/wowmcp/long-tail
89. ⏳ Stop MCP catalog sprawl as readiness metric
90. ⏳ Flywheel-nsite pattern per axis (unsigned → Mac sign)
91. ⏳ Receipt stack single import (`signed-receipts`)
92. ⏳ Finish a2a-signed-receipts README
93. ⏳ Brand badge pipeline from brand-assets
94. ⏳ One Notion inventory DB (optional)
95. ⏳ Weekly drift-guard + ClaimGuard scheduled
96. ⏳ Jail McNemar when ready → update public_count
97. ⏳ Publish jail bank if still pending
98. ⏳ Slot15 / human-vs-ai remain in-lane until gate
99. ⏳ Weekend demo script: ask→board→verify→arena
100. ⏳ Scale announcement only after gates 24+80 green

## Block F — Full frontend audit (101–110) — 2026-08-23
101. ✅ Live persona gauntlet run (3/8 pass)
102. ✅ drift-guard + assert-prerender-live run
103. ✅ ClaimGuard pytest + self-test PASS
104. ✅ `docs/FRONTEND_AUDIT_CHECKLIST.md` written
105. ✅ `docs/MONOREPO_RUNPOD_OPS.md` written
106. ✅ `scripts/run-frontend-audit.mjs` one-command audit
107. 🔧 Review councilof-ai PR #324 (functions-guard + /api/cards) — recommend merge
108. ⏳ Playwright suite update for Council OS routes (49 legacy failures)
109. ⏳ Re-run audit after gated deploy lands aliases
110. ⏳ HF upload + AG-UI deploy gates

## Owner actions required now
- 👤 Cloudflare: disable Pages Git auto-deploy on `councilof-ai` (DEPLOY-LOCK)
- 👤 Re-run deploy workflow; confirm alias routes 200 (homepage already fat)
- 👤 Merge councilof-ai PR #324 (API functions guard)
- 👤 HF write token in agent env → apply `docs/hf-patches/**`
