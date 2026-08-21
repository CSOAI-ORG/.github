# Security policy

CSOAI Ltd publishes signed measurements. A broken verifier, a leaked signing
key, or a forged receipt is a security issue. A low score is not.

## Report a vulnerability

Email [nicholas@csoai.org](mailto:nicholas@csoai.org) with:

- the repository or URL
- what is broken (key, signature, verifier, supply chain, or account)
- steps to reproduce
- impact if the receipt or grade can be forged or silently altered

Do not open a public issue for a signing-key or verifier failure.

We do not run a bug bounty. We will acknowledge a good-faith report and
say what we changed.

## Out of scope

- Model scores, ties, or unpublished banks
- Requests to remediate a measured system
- Social-engineering of ranked parties

## Public keys and verify

Verify grades at [councilof.ai/gspc-verify](https://councilof.ai/gspc-verify).
The living board is [councilof.ai/api/gspc](https://councilof.ai/api/gspc).
The trust root is `did:web:csoai.org`.
