# MEOK AI Labs

**Compliance MCP servers + signed attestations. EU-ready AI governance, automated.**

We ship Model Context Protocol servers that audit AI systems against real regulations — EU AI Act, DORA, NIS2, CRA, CSRD, GDPR, UK AI Bill — then emit cryptographically signed attestations auditors accept.

## ⚡ What's new

- **Signed attestation API live** — sign + verify HMAC-SHA256 certificates at <https://meok-attestation-api.vercel.app/>
- **Pro tier £199/mo** — unlimited compliance audits + signed attestations with public verify URLs — [subscribe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
- **Verify any MEOK cert** — `pip install meok-attestation-verify`

## 🛡️ Flagship compliance MCPs

| Regulation | MCP | Enforcement |
|---|---|---|
| EU AI Act | [`eu-ai-act-compliance-mcp`](https://pypi.org/project/eu-ai-act-compliance-mcp/) | 2 Aug 2026 — €35M or 7% turnover |
| DORA | [`dora-compliance-mcp`](https://pypi.org/project/dora-compliance-mcp/) | 17 Jan 2025 (live) — 1% daily turnover (CTPPs) |
| NIS2 | [`nis2-compliance-mcp`](https://pypi.org/project/nis2-compliance-mcp/) | 17 Oct 2024 (transposition) — €10M or 2% turnover |
| CRA | [`cra-compliance-mcp`](https://pypi.org/project/cra-compliance-mcp/) | 11 Dec 2027 — €15M or 2.5% turnover |
| CSRD | [`csrd-compliance-mcp`](https://pypi.org/project/csrd-compliance-mcp/) | FY 2024-2028 phased — up to €3.75M per breach |
| GDPR | [`gdpr-compliance-mcp`](https://pypi.org/project/gdpr-compliance-mcp/) | Live — 4% turnover |
| HIPAA | [`hipaa-compliance-mcp`](https://pypi.org/project/hipaa-compliance-mcp/) | Live |
| SOC 2 | [`soc2-compliance-mcp`](https://pypi.org/project/soc2-compliance-mcp/) | Evergreen |
| ISO 42001 | [`iso-42001-compliance-mcp`](https://pypi.org/project/iso-42001-compliance-mcp/) | Voluntary AIMS |
| NIST AI RMF | [`nist-rmf-ai-mcp`](https://pypi.org/project/nist-rmf-ai-mcp/) | US federal |
| UK AI Regulation | [`uk-ai-bill-compliance-mcp`](https://pypi.org/project/uk-ai-bill-compliance-mcp/) | Bill in 2026-2027 |
| AI-BOM | [`ai-bom-mcp`](https://pypi.org/project/ai-bom-mcp/) | EU AI Act Annex IV + NIST + CycloneDX ML-BOM |

## 🧩 Specialty MCPs

| MCP | What it does |
|---|---|
| [`dora-nis2-crosswalk-mcp`](https://pypi.org/project/dora-nis2-crosswalk-mcp/) | Dual compliance for EU banks |
| [`ai-incident-reporting-mcp`](https://pypi.org/project/ai-incident-reporting-mcp/) | One incident, all 6 regulatory clocks |
| [`gods-eye-geospatial-mcp`](https://pypi.org/project/gods-eye-geospatial-mcp/) | Civilian open-source geospatial with ethics gate |
| [`care-membrane-mcp`](https://pypi.org/project/care-membrane-mcp/) | Pre-inference ethics gate |
| [`proofof-ai-mcp`](https://pypi.org/project/proofof-ai-mcp/) | AI output verification |
| [`meok-attestation-verify`](https://pypi.org/project/meok-attestation-verify/) | Zero-dep cert verifier |

## 🏗️ How MEOK attestations work

1. You buy Pro — £199/mo at [Stripe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
2. You run an audit from any MEOK MCP (via Claude Desktop, Cursor, Cline, VS Code MCP, etc.)
3. Tool returns a signed cert: HMAC-SHA256 payload + public `verify_url`
4. Your auditor hits the verify URL or runs `meok-attestation-verify cert.json`
5. Signature validates without touching MEOK's backend
6. 365-day validity. Renew automatically on next audit.

## 💼 Pricing

- **Free** — 10 calls/day per MCP
- **Pro** — £199/mo — unlimited + signed attestations + priority support
- **Enterprise** — £1,499/mo — multi-tenant + co-branded PDFs + Trust Center webhooks — [subscribe](https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837)
- **£5,000 assessment** — 48h bespoke audit + signed deliverable — [book](https://buy.stripe.com/4gM7sN2G0bIKeQJfL28k833)

## 🤝 Partnership

Looking for 3 GRC consultancies to pilot a partnership — white-label these tools at your own pricing. Revenue share on every Pro subscription your clients keep. Contact **nicholas@csoai.org**.

## 🔗 Links

- Website: [meok.ai](https://meok.ai)
- PyPI org: [pypi.org/user/MEOK_AI_Labs](https://pypi.org/user/MEOK_AI_Labs/)
- Attestation API: [meok-attestation-api.vercel.app](https://meok-attestation-api.vercel.app/)
- Email: nicholas@csoai.org

---

© 2026 MEOK AI Labs · MIT licensed unless noted otherwise.
