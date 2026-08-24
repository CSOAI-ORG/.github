# Next 100 steps (121–220) — batch execute order

**Baseline:** 2026-08-23 · **Cannon fire:** 2026-08-24 — see [`CANNON_FIRE_2026-08-24.md`](CANNON_FIRE_2026-08-24.md)  
**Truth rail:** `https://councilof.ai/api/gspc` (14 board, 13 measured)

Status: ✅ done · 🔧 agent-ready · 👤 owner dashboard · ⏳ blocked on upstream

---

## Block H — Stabilize apex (121–135)

121. 👤 DEPLOY-LOCK: disable Pages Git auto-deploy on `councilof-ai` (Cloudflare)
122. ✅ `scripts/batch-run-gates.mjs`
123. ✅ E2E retry loop
124. ✅ Homepage fat ~214KB (2026-08-24)
125. ✅ `/gspc-scoreboard` living
126. ✅ `/models` 200
127. ✅ `/agui` 308→`/?lobby=home` (one-door)
128. ✅ `mcp.json` live worker (PR #378)
129. ✅ Worker tools measure/verify/jail-probe/enter-arena
130. ✅ `e2e-integration-stack.mjs` **PASS** 15/15
131. 🔧 Frontend audit — 2 leftovers (`/scorecard`, honesty copy)
132. ✅ Cannon + one-door docs
133. ⏳ Drift-guard schedule on deploy success only
134. 👤 `AGUI_WIRE_URL` on Cloudflare Pages
135. ⏳ Wire probe live inside lobby

## Block I — ClaimGuard product lane (136–150)

136. ✅ ClaimGuard product + pytest
137. ✅ `docs/CLAIMGUARD_MCP.md`
138. ✅ Patch bundle claimguard-chat
139. ✅ `/api/chat` ClaimGuard refuses overclaims (PR #434)
140. ✅ Chat canon 14/13 (no twelve / no 14-are-MEASURED)
141. ✅ public_count matches `/api/gspc`
142. ✅ ClaimGuard `--live` PASS/FAIL as required
143. ⏳ Integrity tile on Council Ledger
144. ⏳ MCP `claimguard.check` on worker
145. ✅ Overclaim ask refused
146. ⏳ Sync claimguard README to product repo
147. ⏳ Carder valve shared rules
148. ⏳ Nightly ClaimGuard schedule
149. ✅ Refusal strings documented
150. ✅ ClaimGuard in `batch-run-gates.mjs`

## Block J — HF 100/100 batch (151–165)

151. ✅ `scripts/upload-hf-patches.sh` (14 axes + Spaces)
152. 👤 `HF_TOKEN` write scope
153. ✅ XR README (was DET clone)
154. ✅ Affect README
155. ✅ Jail README
156. 👤 Upload dataset READMEs
157. 👤 Create Space `csoai/gspc-affect`
158. 👤 Create Space `csoai/gspc-jail`
159. ✅ Method DOI on all 14 cards in `docs/hf-patches/axes/`
160. ✅ `task_categories` on all 14
161. ⏳ Rebuild `gspc-normalized`
162. ⏳ Sync Kaggle XR
163. ⏳ Carder valve all 14
164. ⏳ Public count HF↔site↔API
165. ⏳ Declare HF 100/100 (cards ready; upload blocked)

## Block K — One-door Council OS + MCP wire (166–180)

166. ✅ One-door policy live
167. ✅ Static reference ag-ui bridge
168. ✅ E2E one-door aligned
169. ⏳ `csoai-agui-wire` SSE on `/api/agui/*`
170. 👤 `AGUI_WIRE_URL`
171. ⏳ HITL consent
172. ⏳ Session ledger hash-chain
173. ⏳ Ask → measure tool
174. ⏳ Ask → verify tool
175. ⏳ Ask → enter-arena
176. ⏳ Lobby deep-link session grammar
177. ⏳ Benchmarkers lobby tab
178. ⏳ `/benchmark-index` from lobby
179. ✅ `weekend-demo-smoke.mjs` **SALES-DEMO PASS**
180. ✅ WEEKEND_DEMO · REVENUE_SURFACES · IP_PORTFOLIO · NSITE_AEO_PACK

## Block L — Council OS surfaces (181–195)

181. ✅ `/sov-os` → lobby (one-door)
182. ✅ `/api/cards` live
183. ⏳ functions-guard PR #324
184. ⏳ Playwright Council OS suite
185. ✅ Living board live
186. ⏳ `/scorecard` alias (404; fat on csoai-site)
187. ✅ `/honesty` 200
188. ✅ verify / lobby / pricing / start live
189. ✅ No public Elo on GSPC board
190. ✅ Wilson + McNemar canon
191. ⏳ OpenRouter harness schedule
192. ⏳ Signed arena Elo panel
193. ⏳ N-site federation inbound
194. ✅ N-site pack docs
195. ✅ Weekend demo script **PASS**

## Block M — N-site spray prep (196–220)

196. ✅ `NSITE_AEO_PACK.md` spec
197. ⏳ Parameterize brand + skills
198. ⏳ Prove openmoe-site
199. ⏳ Prove landlaw-site
200. ⏳ Prove diyhelp-site
201. ⏳ fintech-industries-site
202. ⏳ healthtech → govtech → regtech → care
203. ✅ Defer long-tail (documented)
204. ✅ Stop MCP sprawl as readiness metric
205. ⏳ Flywheel-nsite per axis
206. ⏳ Receipt stack single import
207. ⏳ a2a-signed-receipts README
208. ⏳ Brand badge pipeline
209. ⏳ Weekly drift-guard + ClaimGuard
210. ⏳ Jail McNemar gate
211. ⏳ Publish jail bank
212. ✅ Slot15 / human-vs-ai in-lane only
213. ✅ N-site outbound contract
214. ✅ N-site inbound contract
215. ⏳ Codabench seal before 2026-09-01
216. ✅ Zenodo DOI on all 14 cards
217. ⏳ HF org profile → living board
218. ⏳ HF llms.txt / agent.json
219. ⏳ Scale announcement after HF upload + DEPLOY-LOCK
220. ✅ Cannon stamp [`CANNON_FIRE_2026-08-24.md`](CANNON_FIRE_2026-08-24.md)

---

## Batch runner

```bash
node scripts/weekend-demo-smoke.mjs       # sales-demo readiness
node scripts/e2e-integration-stack.mjs    # full stack
node scripts/batch-run-gates.mjs          # ClaimGuard + e2e + audit
bash scripts/upload-hf-patches.sh         # needs HF_TOKEN
```

**Today's yield:** E2E PASS · SALES-DEMO PASS · board 14/13 restored · chat ClaimGuard live · 14 HF cards ready · revenue/IP docs shipped.
