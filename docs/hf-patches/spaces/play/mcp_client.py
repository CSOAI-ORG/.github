"""Live MCP bridge — Council of AI worker is the only tool rail.

Spaces are doors. They do not grade, do not host a second board, and do not
run the contest engine. Every tool call is JSON-RPC to councilof.ai/mcp
(fallback: the published worker). Counts always come from GET /api/gspc.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

MCP_PRIMARY = "https://councilof.ai/mcp"
MCP_FALLBACK = "https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp"
BOARD_URL = "https://councilof.ai/api/gspc"
UA = "CSOAI-HF-MCP-Space/1.1"
TIMEOUT = 25


def _rpc(method: str, params: dict[str, Any] | None = None, *, url: str) -> dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": UA,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def mcp_call(tool: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call one live MCP tool. Never invent a result on failure."""
    last_err = None
    for url in (MCP_PRIMARY, MCP_FALLBACK):
        try:
            body = _rpc("tools/call", {"name": tool, "arguments": arguments or {}}, url=url)
            if body.get("error"):
                return {
                    "ok": False,
                    "state": "MCP_ERROR",
                    "endpoint": url,
                    "tool": tool,
                    "error": body["error"],
                }
            return {
                "ok": True,
                "state": "LIVE",
                "endpoint": url,
                "tool": tool,
                "result": body.get("result"),
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = f"{type(exc).__name__}: {exc}"
    return {
        "ok": False,
        "state": "UNREACHABLE",
        "tool": tool,
        "error": last_err or "both MCP endpoints failed",
        "honesty": "No cached tool result is presented as live.",
    }


def fetch_board() -> dict[str, Any]:
    """Living board. UNREACHABLE is a first-class state — never a stale count."""
    req = urllib.request.Request(
        BOARD_URL, headers={"Accept": "application/json", "User-Agent": UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
        totals = data.get("totals") or {}
        return {
            "ok": True,
            "state": "LIVE",
            "source": BOARD_URL,
            "public_count": totals.get("public_count"),
            "axes": totals.get("axes"),
            "measured_axes": totals.get("measured_axes"),
            "unmeasured_axes": totals.get("unmeasured_axes"),
            "count_grammar": totals.get("count_grammar"),
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "state": "UNREACHABLE",
            "source": BOARD_URL,
            "error": f"{type(exc).__name__}: {exc}",
            "honesty": "No cached axis count is presented as live.",
        }


def pretty(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


# Surfaces each Space may deep-link. Spaces do not host these engines.
SITES = {
    "city": "https://councilof.ai/city",
    "coliseum": "https://councilof.ai/coliseum",
    "arena": "https://councilof.ai/arena",
    "council_space": "https://councilof.ai/gspc-arena",
    "os": "https://councilof.ai/os",
    "lobby": "https://councilof.ai/?lobby=home",
    "verify": "https://councilof.ai/gspc-verify/",
    "honesty": "https://councilof.ai/honesty/",
    "faq": "https://councilof.ai/faq/",
    "east_west": "https://councilof.ai/east-west/",
    "board": BOARD_URL,
    "mcp": MCP_PRIMARY,
    "mcp_hub": "https://huggingface.co/settings/mcp",
}

# 16 jail-probe families (attack families on the live jail-probe contract).
JAIL_FAMILIES = [str(i) for i in range(1, 17)]

# Live worker tools (MEASURED from tools/list). claimguard.check is not on the worker yet.
LIVE_TOOLS = (
    "measure",
    "verify",
    "jail-probe",
    "enter-arena",
    "board_totals",
    "get_axis",
    "verify_card",
    "list_cards",
)


def mcp_tools_list() -> dict[str, Any]:
    """List tools on the live worker. Never invent a catalogue on failure."""
    last_err = None
    for url in (MCP_PRIMARY, MCP_FALLBACK):
        try:
            body = _rpc("tools/list", {}, url=url)
            if body.get("error"):
                return {
                    "ok": False,
                    "state": "MCP_ERROR",
                    "endpoint": url,
                    "error": body["error"],
                }
            tools = (body.get("result") or {}).get("tools") or []
            return {
                "ok": True,
                "state": "LIVE",
                "endpoint": url,
                "names": [t.get("name") for t in tools if isinstance(t, dict)],
                "tools": tools,
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = f"{type(exc).__name__}: {exc}"
    return {
        "ok": False,
        "state": "UNREACHABLE",
        "error": last_err or "both MCP endpoints failed",
        "honesty": "No cached tool list is presented as live.",
    }


def check_claim(claim: str) -> dict[str, Any]:
    """Thin living-board claim check. Not the full ClaimGuard CLI.

    Uses GET /api/gspc. Rejects 22/22, '16 measured axes', Elo-as-grade,
    and certification language. Numeric 'N measured' must match live
    totals.measured_axes. Stale 14/13 copy is not applied.
    """
    text = (claim or "").strip()
    board = fetch_board()
    if not text:
        return {"ok": False, "state": "NEED_CLAIM", "board": board}
    if not board.get("ok"):
        return {
            "ok": False,
            "state": board.get("state") or "UNREACHABLE",
            "board": board,
            "honesty": "Cannot audit a claim without a live board.",
        }

    findings: list[dict[str, str]] = []
    measured = board.get("measured_axes")
    axes = board.get("axes")
    public = board.get("public_count")

    def fail(code: str, message: str) -> None:
        findings.append({"status": "FAIL", "code": code, "message": message})

    if re.search(r"22\s*/\s*22|all\s+22\s+(axes?\s+)?(are\s+)?measured", text, re.I):
        fail(
            "claim.twenty_two_of_twenty_two",
            "Slots and measurements are labelled separately. Quote totals.public_count.",
        )
    if re.search(r"\b16\s+measured\s+axes\b", text, re.I):
        fail(
            "claim.sixteen_measured",
            "16 jail-probe families are not 16 measured axes. Quote totals.public_count.",
        )
    if re.search(r"\b(elo|éelo)\s+league\b|\bpublic\s+elo\b|\belo\s+ranking\b", text, re.I):
        fail(
            "claim.elo_league",
            "GSPC public ranking is Wilson+McNemar, not Elo. Elo league is not on /api/gspc.",
        )
    if re.search(r"\bcertif(y|ied|ication)\b", text, re.I):
        fail(
            "claim.certification",
            "Measurement, not certification — certification language is unsupported.",
        )
    for m in re.finditer(r"\b(\d+)\s+measured(?:\s+axes?)?\b", text, re.I):
        n = int(m.group(1))
        if measured is not None and n != measured:
            fail(
                "claim.measured_mismatch",
                f"Claim says {n} measured; live totals.measured_axes is {measured}. "
                f"Quote {public!r}.",
            )
    for m in re.finditer(r"\b(\d+)\s+(?:board\s+)?(?:slots|axes)\b", text, re.I):
        n = int(m.group(1))
        if "measured" in text.lower():
            continue
        if axes is not None and n != axes:
            fail(
                "claim.slot_mismatch",
                f"Claim says {n} slots/axes; live totals.axes is {axes}. Quote {public!r}.",
            )

    return {
        "ok": not findings,
        "state": "LIVE",
        "kind": "living-board-claim-check",
        "claim": text,
        "public_count": public,
        "findings": findings,
        "honesty": (
            "Thin Space check against GET /api/gspc. "
            "Full CLI is products/claimguard. MCP claimguard.check is not on the worker yet."
        ),
        "site": SITES["honesty"],
        "verify": SITES["verify"],
    }


def load_fabric() -> dict[str, Any]:
    """Product + play MCP directory. Missing file is not a live count."""
    here = Path(__file__).resolve().parent
    candidates = [
        here / "catalog.json",
        here.parent / "products" / "catalog.json",
    ]
    for parent in here.parents:
        hit = parent / "connect" / "mcp" / "hf-product-spaces.json"
        if hit.exists():
            candidates.append(hit)
            break
    for path in candidates:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_loaded_from"] = str(path)
            return data
    return {
        "ok": False,
        "state": "NO_CATALOG",
        "honesty": "Fabric directory file was not copied next to this Space.",
        "live_worker": MCP_PRIMARY,
    }
