"""Shared Gradio chrome for product MCP doors.

Each Space stays a door. Common tools proxy the live worker.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, _HERE.parent, _HERE.parent / "play"):
    if (_candidate / "mcp_client.py").exists():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

import gradio as gr

from mcp_client import SITES, fetch_board, load_fabric, mcp_call, pretty

THEME = gr.themes.Soft(
    primary_hue="stone",
    secondary_hue="amber",
    neutral_hue="stone",
)


def living_totals() -> str:
    """Return live GSPC board totals via MCP board_totals.

    Returns:
        Slot count and measured count as two labelled numbers. Never summed.
    """
    via_mcp = mcp_call("board_totals")
    if via_mcp.get("ok"):
        return pretty(via_mcp)
    return pretty(fetch_board())


def get_axis(axis: str) -> str:
    """Fetch one live axis row from the GSPC board.

    Args:
        axis: Axis id as published on GET /api/gspc (e.g. governance, jail).

    Returns:
        MEASURED row or UNMEASURED declared slot. An empty slot is not an error.
    """
    name = (axis or "").strip()
    if not name:
        return pretty({"ok": False, "state": "NEED_AXIS", "hint": "Pass an axis id from GET /api/gspc."})
    return pretty(mcp_call("get_axis", {"axis": name}))


def enter_arena(agent_card_url: str, consent: bool) -> str:
    """Self-enrol an agent via live MCP enter-arena.

    Args:
        agent_card_url: https URL of the visiting A2A agent card.
        consent: Must be true. Machine-readable consent to be measured.

    Returns:
        Unsigned intake receipt from the live worker, or UNREACHABLE.
    """
    if not consent:
        return pretty(
            {
                "ok": False,
                "state": "CONSENT_REQUIRED",
                "honesty": "enter-arena will not run without consent:true.",
            }
        )
    return pretty(
        mcp_call(
            "enter-arena",
            {"agent_card_url": (agent_card_url or "").strip(), "consent": True},
        )
    )


def verify_card(card: str) -> str:
    """Verify a signed measurement card via live MCP verify_card.

    Args:
        card: Card JSON, or a councilof.ai / csoai.org URL to one.

    Returns:
        Live verify result, or UNREACHABLE. This Space does not re-sign cards.
    """
    payload = (card or "").strip()
    if not payload:
        return pretty({"ok": False, "state": "NEED_CARD", "site": SITES["verify"]})
    return pretty(mcp_call("verify_card", {"card": payload}))


def list_cards(axis: str, limit: int) -> str:
    """List published measurement cards from the live worker.

    Args:
        axis: Optional axis filter (e.g. governance).
        limit: How many rows (newest first). Counts are always reported in full.

    Returns:
        Card listing from live MCP list_cards.
    """
    args: dict = {"limit": int(limit or 10)}
    name = (axis or "").strip()
    if name:
        args["axis"] = name
    return pretty(mcp_call("list_cards", args))


def list_fabric() -> str:
    """List every Council of AI product Space and its MCP SSE URL.

    Returns:
        Fabric directory. Each Space MCP-connects to Council OS / the live worker.
    """
    catalog = load_fabric()
    return pretty(
        {
            "kind": "council-os-mcp-fabric",
            "os": SITES["os"],
            "lobby": SITES["lobby"],
            "mcp": SITES["mcp"],
            "add_on_hub": SITES["mcp_hub"],
            "board": fetch_board(),
            "fabric": catalog,
            "honesty": "Doors only. Add any Space SSE — or the worker — from anywhere.",
        }
    )


def footer() -> str:
    return (
        f"[Council OS]({SITES['os']}) · [Lobby]({SITES['lobby']}) · "
        f"[Verify]({SITES['verify']}) · [City]({SITES['city']}) · "
        f"[Coliseum]({SITES['coliseum']}) · [MCP]({SITES['mcp']}) · "
        f"[Add on Hub]({SITES['mcp_hub']})"
    )
