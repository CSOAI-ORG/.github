"""Live MCP client checks — no invented 22/22."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp_client import JAIL_FAMILIES, SITES, fetch_board, mcp_call, pretty


def test_sixteen_jail_families():
    assert JAIL_FAMILIES == [str(i) for i in range(1, 17)]


def test_sites_point_at_apex():
    for key in ("city", "coliseum", "arena", "council_space", "mcp", "board"):
        assert SITES[key].startswith("https://councilof.ai")


def test_fetch_board_is_live_or_unreachable():
    board = fetch_board()
    assert board["state"] in {"LIVE", "UNREACHABLE"}
    if board["state"] == "LIVE":
        assert board["axes"] == 22
        assert board["measured_axes"] == 15
        assert board["unmeasured_axes"] == 7
        assert "22.22" not in pretty(board)


def test_board_totals_tool():
    result = mcp_call("board_totals")
    assert result["state"] in {"LIVE", "UNREACHABLE", "MCP_ERROR"}
    if result["state"] == "LIVE":
        text = pretty(result)
        assert "22" in text
        assert "15" in text
