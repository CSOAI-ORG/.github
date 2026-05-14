# MEOK AI Labs

**38 Model Context Protocol servers for AI governance + signed compliance attestations. EU-ready. Auditor-defensible. One install command.**

> 🛡️ The only MCP suite that ships verbatim EU regulation text (410 articles from EUR-Lex, daily-synced) with cryptographically signed compliance certificates your auditor verifies independently.

[![PyPI](https://img.shields.io/badge/PyPI-MEOK_AI_Labs-blue)](https://pypi.org/user/MEOK_AI_Labs/) [![npm](https://img.shields.io/npm/v/meok-setup)](https://www.npmjs.com/package/meok-setup) [![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/CSOAI-ORG)

## ⚡ One-shot install

```bash
npx meok-setup --pack governance       # 10 governance MCPs in one go
npx meok-setup --pack a2a              # 7 agent-to-agent governance MCPs
npx meok-setup --pack trade            # 7 UK trade vertical MCPs
npx meok-setup --pack industry         # 8 industry MCPs (medtech, fintech, crypto…)
npx meok-setup --pack cybersec         # 6 cybersecurity governance MCPs
npx meok-setup --pack all              # All 38 MCPs
```

Auto-writes Claude Desktop / Cursor / Windsurf configs. No API key required for free tier (10 calls/day per MCP).

## 🚨 The urgent cliff: Article 50

The **7 May 2026 EU Omnibus deal COMPRESSED** the Article 50 transparency deadline to **2 December 2026** (was Feb 2027). If you ship AI-generated content into the EU, **173 days from today** is the hard deadline.

→ `pip install watermarking-authenticity-mcp` (v1.2.0 ships C2PA 2.1 + Sigstore + the new deadline)

## 🛡️ Flagship governance MCPs

| Regulation | MCP | Enforcement | Penalty ceiling |
|---|---|---|---|
| **EU AI Act** | [`eu-ai-act-compliance-mcp`](https://pypi.org/project/eu-ai-act-compliance-mcp/) v1.4.0 — **410 articles in FTS5** | Art 50: 2 Dec 2026 · Annex III: 2 Dec 2027 | €35M or 7% turnover |
| **DORA** | [`dora-compliance-mcp`](https://pypi.org/project/dora-compliance-mcp/) | Live since 17 Jan 2025 | 1% daily turnover (CTPPs) |
| **NIS2** | [`nis2-compliance-mcp`](https://pypi.org/project/nis2-compliance-mcp/) | Live · 19 EU MS still transposing | €10M or 2% turnover |
| **CRA** | [`cra-compliance-mcp`](https://pypi.org/project/cra-compliance-mcp/) | Type A: 30 Aug 2026 | €15M or 2.5% turnover |
| **CSRD** | [`csrd-compliance-mcp`](https://pypi.org/project/csrd-compliance-mcp/) | FY 2024-2028 phased | up to €3.75M per breach |
| **GDPR** | [`gdpr-compliance-ai-mcp`](https://pypi.org/project/gdpr-compliance-ai-mcp/) | Live | 4% turnover |
| **UK AI Bill** | [`uk-ai-bill-compliance-mcp`](https://pypi.org/project/uk-ai-bill-compliance-mcp/) | Bill in progress | TBD |
| **MiCA** | [`mica-crypto-mcp`](https://pypi.org/project/mica-crypto-mcp/) | CASP transitional ends 1 Jul 2026 | up to €5M |
| **AI BOM** | [`ai-bom-mcp`](https://pypi.org/project/ai-bom-mcp/) | EU AI Act Art 11 + CycloneDX | — |
| **AI Bias** | [`bias-detection-mcp`](https://pypi.org/project/bias-detection-mcp/) | EU AI Act Art 10 + NYC LL 144 | — |

## 🤝 Agent-to-Agent governance (A2A pack)

When agents talk to other agents at scale, you need IAM, audit, and runtime policy. MEOK ships them as MCPs.

| MCP | Use |
|---|---|
| [`agent-policy-enforcement-mcp`](https://pypi.org/project/agent-policy-enforcement-mcp/) | IAM-for-agents — per-pair source→target policies with constraints |
| [`agent-audit-logger-mcp`](https://pypi.org/project/agent-audit-logger-mcp/) | Immutable signed A2A audit trail (DORA Art 17, NIS2 Art 21, EU AI Act Art 12) |
| [`agent-rate-limiter-mcp`](https://pypi.org/project/agent-rate-limiter-mcp/) | Fleet-wide rate limit across all MCPs |
| [`agent-handoff-certified-mcp`](https://pypi.org/project/agent-handoff-certified-mcp/) | Signed delegation certs when agent A → agent B |
| [`agent-prompt-injection-firewall-mcp`](https://pypi.org/project/agent-prompt-injection-firewall-mcp/) | Runtime guard against OWASP LLM Top-10 #1 |
| [`agent-data-residency-mcp`](https://pypi.org/project/agent-data-residency-mcp/) | GDPR Chapter V runtime guard for cross-region transfers |
| [`agent-identity-trust-mcp`](https://pypi.org/project/agent-identity-trust-mcp/) | DIDs, verifiable credentials, agent passports |

## 🏗️ UK trade verticals

Built by Nick Templeman (UK optical-practice operator) for UK trade buyers who feel left behind by horizontal AI compliance tooling:

| MCP | Domain |
|---|---|
| [`haulage-uk-compliance-mcp`](https://pypi.org/project/haulage-uk-compliance-mcp/) | UK Operator Licence, tachograph, drivers' hours, DVSA |
| [`skip-hire-ai-mcp`](https://pypi.org/project/skip-hire-ai-mcp/) | EA waste carrier registration, EWC codes |
| [`construction-iso-19650-mcp`](https://pypi.org/project/construction-iso-19650-mcp/) | UK BIM Level 2 (EIR/BEP/CDE) |
| [`nrswa-ai-mcp`](https://pypi.org/project/nrswa-ai-mcp/) | Section 50/58/74 street works |
| [`chas-elite-prep-mcp`](https://pypi.org/project/chas-elite-prep-mcp/) | CHAS / SafeContractor / Constructionline pre-qual |
| [`crane-hire-cpcs-mcp`](https://pypi.org/project/crane-hire-cpcs-mcp/) | CPCS / CISRS / NPORS + BS 7121 lift plans |
| [`concrete-pump-cpa-mcp`](https://pypi.org/project/concrete-pump-cpa-mcp/) | CPA Concrete Pumping standards |

## 🔒 Cybersecurity governance pack

| MCP | Coverage |
|---|---|
| [`cisa-kev-mcp`](https://pypi.org/project/cisa-kev-mcp/) | Known Exploited Vulnerabilities + BOD 22-01 |
| [`sbom-cyclonedx-mcp`](https://pypi.org/project/sbom-cyclonedx-mcp/) | SBOM CycloneDX + SPDX (EO 14028, NIS2, CRA) |
| [`mitre-attack-mcp`](https://pypi.org/project/mitre-attack-mcp/) | ATT&CK tactics + techniques mapper |
| [`mitre-atlas-mcp`](https://pypi.org/project/mitre-atlas-mcp/) | Adversarial AI threat landscape |
| [`slsa-supply-chain-mcp`](https://pypi.org/project/slsa-supply-chain-mcp/) | SLSA v1.0 levels |
| [`sigstore-cosign-mcp`](https://pypi.org/project/sigstore-cosign-mcp/) | Sigstore cosign + Rekor verification |
| [`owasp-agentic-mcp`](https://pypi.org/project/owasp-agentic-mcp/) | OWASP LLM Top-10 + agentic threats |

## 🩺 Industry verticals

| MCP | Buyer |
|---|---|
| [`mdr-medical-device-mcp`](https://pypi.org/project/mdr-medical-device-mcp/) | EU MDR/IVDR + AI/ML SaMD classification |
| [`fda-samd-mcp`](https://pypi.org/project/fda-samd-mcp/) | US FDA AI/ML SaMD + PCCP + GMLP |
| [`basel-ai-overlay-mcp`](https://pypi.org/project/basel-ai-overlay-mcp/) | Basel III + SR 11-7 model risk for banks |
| [`mifid-ii-ai-mcp`](https://pypi.org/project/mifid-ii-ai-mcp/) | MiFID II Article 17 algorithmic trading |
| [`aml-ai-mcp`](https://pypi.org/project/aml-ai-mcp/) | 6AMLD + UK MLR 2017 |
| [`coppa-ferpa-mcp`](https://pypi.org/project/coppa-ferpa-mcp/) | Children's privacy (COPPA, FERPA, UK AADC) |
| [`fsa-food-safety-mcp`](https://pypi.org/project/fsa-food-safety-mcp/) | UK FSA + EU Reg 178/2002 + HACCP |
| [`cobol-bridge-mcp`](https://pypi.org/project/cobol-bridge-mcp/) | COBOL → modern stack migration planner |

## 🔐 How MEOK attestations work

1. You subscribe to **Pro tier £79/mo** at [Stripe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
2. You run any audit from a MEOK MCP (via Claude Desktop, Cursor, Cline, VS Code MCP, Windsurf — any MCP client)
3. The MCP emits a signed certificate: HMAC-SHA256 payload + public `verify_url`
4. Your auditor pastes the cert at [`meok-attestation-api.vercel.app/verify`](https://meok-attestation-api.vercel.app/verify) — or runs `pip install meok-attestation-verify && meok-verify cert.json`
5. The signature validates without contacting MEOK. Trust through math, not "trust us."

365-day validity. Renews automatically on next audit.

## 💼 Pricing

| Tier | Price | What you get |
|---|---|---|
| **Free** | £0 | 10 calls/day per MCP. No API key. |
| **Pro** | £79/mo | Unlimited calls + cryptographically signed attestations + email support → [subscribe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836) |
| **Enterprise** | £1,499/mo | White-label + on-premise + SLA + dedicated Slack → hello@meok.ai |
| **48h Gap Analysis** | £4,999 | One-time expert review with signed report → [order](https://buy.stripe.com/4gM7sN2G0bIKeQJfL28k833) |
| **Notified Body partner** | Custom | Multi-assessment licence for TÜV, BSI, DNV, etc. → hello@meok.ai |

## 🌐 Live infrastructure

- **Catalogue:** [meok-attestation-api.vercel.app/catalogue](https://meok-attestation-api.vercel.app/catalogue)
- **Storefront:** [councilof.ai](https://councilof.ai) — every framework, every pack, one platform
- **PyPI:** [pypi.org/user/MEOK_AI_Labs](https://pypi.org/user/MEOK_AI_Labs/) (38+ packages, ~7,500 monthly downloads)
- **npm:** [npmjs.com/package/meok-setup](https://www.npmjs.com/package/meok-setup) (one-shot installer)
- **MCP Registry:** auto-published, daily ingested by PulseMCP + mcp.so

## 🎯 What's coming

- **Cloudflare Worker hosted MCP** at `mcp.councilof.ai` — no pip install needed
- **Managed Agent customer sessions** — embed a per-customer compliance advisor on your site
- **Slack ChatOps** — `@meok run audit` in your support channel
- **White-label Trust Centers** — host your own signed-attestation feed on your domain
- **Notified Body partnership program** — 5 conversations active

## 📬 Contact

- **Email:** hello@meok.ai
- **Founder:** Nicholas Templeman (UK)
- **Catalogue:** [councilof.ai](https://councilof.ai)
- **Verify any MEOK cert:** [meok-attestation-api.vercel.app/verify](https://meok-attestation-api.vercel.app/verify)

> MIT licensed. Built in London. Hating compliance dashboards since 2026.
