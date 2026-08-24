# GSPC axis HF card index

Ready-to-upload dataset cards for the **14 quotable board axes**.
Canon: [`../GSPC_AXIS_CANON.md`](../GSPC_AXIS_CANON.md).

**Living numbers:** [https://councilof.ai/api/gspc](https://councilof.ai/api/gspc) — never freeze scores on cards.  
**Method DOI:** [https://doi.org/10.5281/zenodo.21991104](https://doi.org/10.5281/zenodo.21991104)  
**Public ruling:** 13 measured of 14 quotable; `jail` is floor with separation **UNTESTED**.

| # | Axis id | Bench | HF dataset | Patch README |
|---|---|---|---|---|
| 1 | `governance` | GovBench | [`csoai/gspc-gov`](https://huggingface.co/datasets/csoai/gspc-gov) | [`axes/gspc-gov/README.md`](axes/gspc-gov/README.md) |
| 2 | `safety` | DefBench | [`csoai/gspc-agi`](https://huggingface.co/datasets/csoai/gspc-agi) | [`axes/gspc-agi/README.md`](axes/gspc-agi/README.md) |
| 3 | `provenance` | ProvBench | [`csoai/gspc-prv`](https://huggingface.co/datasets/csoai/gspc-prv) | [`axes/gspc-prv/README.md`](axes/gspc-prv/README.md) |
| 4 | `continuity` | PQCBench | [`csoai/gspc-asi`](https://huggingface.co/datasets/csoai/gspc-asi) | [`axes/gspc-asi/README.md`](axes/gspc-asi/README.md) |
| 5 | `conformance` | MCPBench | [`csoai/gspc-mcp`](https://huggingface.co/datasets/csoai/gspc-mcp) | [`axes/gspc-mcp/README.md`](axes/gspc-mcp/README.md) |
| 6 | `openness` | OSSBench | [`csoai/gspc-oss`](https://huggingface.co/datasets/csoai/gspc-oss) | [`axes/gspc-oss/README.md`](axes/gspc-oss/README.md) |
| 7 | `machinery-conformity` | MachBench | [`csoai/gspc-mach`](https://huggingface.co/datasets/csoai/gspc-mach) | [`axes/gspc-mach/README.md`](axes/gspc-mach/README.md) |
| 8 | `care` | CareBench | [`csoai/gspc-care`](https://huggingface.co/datasets/csoai/gspc-care) | [`axes/gspc-care/README.md`](axes/gspc-care/README.md) |
| 9 | `cross-reality` | XRAIV | [`csoai/gspc-xr`](https://huggingface.co/datasets/csoai/gspc-xr) | [`axes/gspc-xr/README.md`](axes/gspc-xr/README.md) |
| 10 | `detector-interop` | DetBench | [`csoai/gspc-det`](https://huggingface.co/datasets/csoai/gspc-det) | [`axes/gspc-det/README.md`](axes/gspc-det/README.md) |
| 11 | `art5-safeguard` | Art5Bench | [`csoai/gspc-art5`](https://huggingface.co/datasets/csoai/gspc-art5) | [`axes/gspc-art5/README.md`](axes/gspc-art5/README.md) |
| 12 | `swarm` | SwarmBench v2b | [`csoai/gspc-swarm`](https://huggingface.co/datasets/csoai/gspc-swarm) | [`axes/gspc-swarm/README.md`](axes/gspc-swarm/README.md) |
| 13 | `affect` | AffectBench | [`csoai/gspc-affect`](https://huggingface.co/datasets/csoai/gspc-affect) | [`axes/gspc-affect/README.md`](axes/gspc-affect/README.md) |
| 14 | `jail` | GoldBank-Detector | [`csoai/gspc-jail`](https://huggingface.co/datasets/csoai/gspc-jail) | [`axes/gspc-jail/README.md`](axes/gspc-jail/README.md) |

## Spaces (affect + jail)

| Space | Patch | HF URL |
|---|---|---|
| `gspc-affect` | [`spaces/gspc-affect/`](spaces/gspc-affect/) | [https://huggingface.co/spaces/csoai/gspc-affect](https://huggingface.co/spaces/csoai/gspc-affect) |
| `gspc-jail` | [`spaces/gspc-jail/`](spaces/gspc-jail/) | [https://huggingface.co/spaces/csoai/gspc-jail](https://huggingface.co/spaces/csoai/gspc-jail) |

## Upload

```bash
export HF_TOKEN=hf_...
bash scripts/upload-hf-patches.sh
```

Footer on every card: CSOAI Ltd UK 16939677 · measurement, not certification.
