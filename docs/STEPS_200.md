# Next 100 steps (121–220) — batch execute order

**Baseline:** 2026-08-23 after Block G deploy gate run. Truth rail: `https://councilof.ai/api/gspc` (14 board, 13 measured).

Status: ✅ done · 🔧 agent-ready · 👤 owner dashboard · ⏳ blocked on upstream

---

## Block H — Stabilize apex (121–135)

121. ⏳ DEPLOY-LOCK: disable Pages Git auto-deploy on `councilof-ai` (👤 Cloudflare)
122. 🔧 `scripts/batch-run-gates.mjs` — chain audit + e2e + ClaimGuard self-test
123. 🔧 E2E retry loop until deploy lands or 3 failures (clobber window)
124. ⏳ Assert homepage ≥20KB + CouncilLobby chunk post-deploy
125. ⏳ Assert `/gspc-scoreboard` ≥50KB post-deploy
126. ⏳ Assert `/models` 200 post-deploy
127. ⏳ Assert `/agui` 308→`/ag-ui` post-deploy
128. 🔧 Restore `mcp.json` → live `csoai-gspc-mcp` worker (was emptied 2026-08-19)
129. ⏳ Verify worker `tools/list` returns measure/verify/jail-probe/enter-arena
130. ⏳ `e2e-integration-stack.mjs` 14/14 green
131. ⏳ `run-frontend-audit.mjs` persona + route inventory green
132. 🔧 Document clobber signature in `DEPLOY-LOCK.md` cross-link
133. ⏳ Schedule drift-guard + assert-prerender on deploy success only
134. 👤 Set `AGUI_WIRE_URL` on Cloudflare Pages (RunPod :8785)
135. ⏳ AG-UI wire probe shows live on `/ag-ui` header

## Block I — ClaimGuard product lane (136–150)

136. ✅ ClaimGuard landed `products/claimguard/` + pytest
137. 🔧 `docs/CLAIMGUARD_MCP.md` — tool schema + wire path
138. 🔧 MCP tool descriptor `claimguard.check` in patch bundle
139. ⏳ councilof-ai `/api/chat` calls ClaimGuard on grade-claiming asks
140. ⏳ Fix chat "twelve axes" drift → canon 14 board / 13 measured
141. ⏳ `/api/chat` public_count matches `/api/gspc` totals
142. ⏳ Post-deploy CI: ClaimGuard `--live` against `/api/gspc`
143. ⏳ Integrity tile on Council Ledger links ClaimGuard
144. ⏳ MCP wire exposes `claimguard.check` alongside measure/verify
145. ⏳ E2E: overclaim ask → refused with signed finding
146. ⏳ Publish `CSOAI-ORG/claimguard` README sync from mirror
147. ⏳ Wire carder valve → ClaimGuard shared rules
148. ⏳ Nightly scheduled ClaimGuard on live board
149. ⏳ Document refusal strings in `CHAT_AGUI_OPENROUTER.md`
150. ⏳ ClaimGuard gate in `batch-run-gates.mjs`

## Block J — HF 100/100 batch (151–165)

151. 🔧 `scripts/upload-hf-patches.sh` — idempotent HF CLI upload
152. 👤 `HF_TOKEN` write scope for org `csoai`
153. 🔧 Patch `gspc-xr/README.md` (DET clone → XR axis)
154. 🔧 Patch `gspc-affect/README.md` (dedupe YAML + DOI)
155. 🔧 Patch `gspc-jail/README.md` (floor, UNTESTED separation)
156. 👤 Upload 3 dataset READMEs to HF
157. 👤 Create Space `csoai/gspc-affect` from `docs/hf-patches/spaces/gspc-affect/`
158. 👤 Create Space `csoai/gspc-jail` from `docs/hf-patches/spaces/gspc-jail/`
159. ⏳ Method DOI `10.5281/zenodo.21991104` on all 14 axis cards
160. ⏳ `task_categories` on all 14 axis cards
161. ⏳ Rebuild `gspc-normalized` (+care/affect/jail)
162. ⏳ Sync Kaggle XR after HF fix
163. ⏳ Carder valve pass all 14
164. ⏳ Public count string identical HF↔site↔API
165. ⏳ Declare HF 100/100 gate passed

## Block K — One-door Council OS + MCP wire (166–180)

166. ✅ One-door policy: `/ag-ui` `/agui` `/chat` `/sov-os` → `/?lobby=home` (PR revert #372 + `one-door-guard.yml`)
167. ✅ Static `csoai-site.pages.dev/ag-ui` postMessage bridge (dev/reference host only)
168. 🔧 E2E aligned to one-door (not iframe) — `e2e-integration-stack.mjs`
169. ⏳ Deploy `csoai-agui-wire` SSE on `/api/agui/*` inside Council OS lobby
170. 👤 `AGUI_WIRE_URL` env on Pages
171. ⏳ HITL consent before grade-claiming writes
172. ⏳ Session ledger hash-chain public
173. ⏳ Ask "governance leader?" → measure tool → board row
174. ⏳ Ask "verify this grade" → verify tool
175. ⏳ Ask "enter arena" → enter-arena tool
176. ⏳ Lobby deep-links share session grammar
177. ⏳ Benchmarkers lobby tab in `tabs.ts` → `/benchmarks`
178. ⏳ `/benchmark-index` third-party register linked from lobby
179. ⏳ E2E: ask→measure→verify smoke via lobby wire
180. ⏳ Document RAS = Receipts + Arena + Scorecard over Council OS

## Block L — Council OS surfaces (181–195)

181. ⏳ `/sov-os/` prerender stable (normPath fix landed)
182. ⏳ `/api/cards` honest UNPUBLISHED when `/signed/*` missing
183. ⏳ Merge functions-guard PR #324 if still open
184. ⏳ Playwright suite: Council OS routes (49 legacy failures)
185. ⏳ LivingBoard on home when apex fat
186. ⏳ Moody scorecard on `/scorecard` alias
187. ⏳ Honesty Elo disclosure on `/honesty`
188. ⏳ Live ledger route `/live-ledger`
189. ⏳ Arena UX law-graded (no public Elo on GSPC board)
190. ⏳ Wilson + McNemar on scorecard tiles only
191. ⏳ OpenRouter harness → board refresh (RunPod 3090 sim_burst)
192. ⏳ Signed arena Elo panel verify-this-leaderboard
193. ⏳ `/api/gspc` federation inbound from N-site results
194. ⏳ Benchmarkers tab + flywheel-nsite CI pattern doc
195. ⏳ Weekend demo: ask→board→verify→arena script

## Block M — N-site spray prep (196–220)

196. ⏳ Extract shared AEO/AGUI pack from openmoe/landlaw
197. ⏳ Parameterize brand + skills per site
198. ⏳ Prove pack on openmoe-site
199. ⏳ Prove pack on landlaw-site
200. ⏳ Prove pack on diyhelp-site
201. ⏳ Industry: fintech-industries-site
202. ⏳ healthtech → govtech → regtech → care fan-out
203. ⏳ Defer pokerhud/wowmcp/long-tail
204. ⏳ Stop MCP catalog sprawl as readiness metric
205. ⏳ Flywheel-nsite pattern per axis (unsigned → Mac sign)
206. ⏳ Receipt stack single import (`signed-receipts`)
207. ⏳ Finish a2a-signed-receipts README
208. ⏳ Brand badge pipeline from brand-assets
209. ⏳ Weekly drift-guard + ClaimGuard scheduled
210. ⏳ Jail McNemar when ready → update public_count
211. ⏳ Publish jail bank if gate passes
212. ⏳ Slot15 / human-vs-ai remain in-lane
213. ⏳ N-site outbound: AEO pack + GSPC instrument
214. ⏳ N-site inbound: signed results → HF benchmarks → `/api/gspc`
215. ⏳ Codabench README + seal before 2026-09-01
216. ⏳ Zenodo cite on papers + boards meta
217. ⏳ HF org profile links living board
218. ⏳ AEO: llms.txt / agent.json for HF
219. ⏳ Scale announcement only after gates 130+165 green
220. ⏳ Update `MASTER_PLAN.md` Phase completion stamps

---

## Batch runner

```bash
node scripts/batch-run-gates.mjs          # full gate chain
node scripts/batch-run-gates.mjs --retry 3  # retry e2e through deploy clobber
bash scripts/upload-hf-patches.sh           # needs HF_TOKEN
```

**Gate order:** deploy success → e2e 14/14 → frontend audit → ClaimGuard live → HF upload → N-site spray.
