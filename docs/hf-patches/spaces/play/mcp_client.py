"""Live MCP bridge — Council of AI worker is the only tool rail.

Spaces are doors. They do not grade, do not host a second board, and do not
run the contest engine. Every tool call is JSON-RPC to councilof.ai/mcp
(fallback: the published worker). Counts always come from GET /api/gspc.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

MCP_PRIMARY = "https://councilof.ai/mcp"
MCP_FALLBACK = "https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp"
BOARD_URL = "https://councilof.ai/api/gspc"
UA = "CSOAI-HF-Play-Space/1.0"
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


# Surfaces each play Space may deep-link. Spaces do not host these engines.
SITES = {
    "city": "https://councilof.ai/city",
    "coliseum": "https://councilof.ai/coliseum",
    "arena": "https://councilof.ai/arena",
    "council_space": "https://councilof.ai/gspc-arena",
    "os": "https://councilof.ai/os",
    "verify": "https://councilof.ai/gspc-verify/",
    "board": BOARD_URL,
    "mcp": MCP_PRIMARY,
}

# 16 jail-probe families (attack families on the live jail-probe contract).
JAIL_FAMILIES = [str(i) for i in range(1, 17)]
