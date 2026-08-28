"""Council City — Hugging Face Space + MCP door.

City is the governed multi-agent surface on councilof.ai/city.
This Space MCP-connects that door to any N-site or agent client.
It does not host a second city or a second board.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, _HERE.parent):
    if (_candidate / "mcp_client.py").exists():
        sys.path.insert(0, str(_candidate))
        break

import gradio as gr

from mcp_client import SITES, fetch_board, mcp_call, pretty


def city_door() -> str:
    """Open the Council City door: live board pointer + site URLs.

    Returns:
        JSON door card. City chrome lives on councilof.ai/city.
    """
    return pretty(
        {
            "kind": "council-city-door",
            "site": SITES["city"],
            "os": SITES["os"],
            "council_space": SITES["council_space"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": "Door only. No second city, no second scoreboard.",
        }
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


def measure_contract(model: str) -> str:
    """Return the GSPC measurement CONTRACT for a subject (does not run a grade).

    Args:
        model: Subject name or model id.

    Returns:
        Contract from live MCP measure. measured:false — the worker does not grade here.
    """
    subject = (model or "").strip()
    if not subject:
        return pretty({"ok": False, "state": "NEED_SUBJECT"})
    return pretty(mcp_call("measure", {"model": subject}))


THEME = gr.themes.Soft(
    primary_hue="stone",
    secondary_hue="amber",
    neutral_hue="stone",
)

with gr.Blocks(title="Council City — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# Council City
**Council of AI · CSOAI Ltd (UK 16939677)**

Governed multi-agent city. Live surface: [councilof.ai/city](https://councilof.ai/city).

This Space is a door + MCP server for N-sites and any MCP client.
It does **not** host City. Living counts come from `GET /api/gspc`.
Measurement, not certification.
"""
    )
    with gr.Tab("City door"):
        door_out = gr.Code(label="city", language="json")
        gr.Button("Open city door").click(city_door, outputs=door_out)
        demo.load(city_door, outputs=door_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
        axis = gr.Textbox(label="Axis id", placeholder="governance")
        axis_out = gr.Code(label="get_axis", language="json")
        gr.Button("Get axis").click(get_axis, inputs=axis, outputs=axis_out)
    with gr.Tab("Measure contract"):
        model = gr.Textbox(label="Subject / model")
        measure_out = gr.Code(label="measure", language="json")
        gr.Button("Request contract (live MCP)").click(
            measure_contract, inputs=model, outputs=measure_out
        )
    gr.Markdown(
        f"[City]({SITES['city']}) · [Coliseum]({SITES['coliseum']}) · "
        f"[Games Space](https://huggingface.co/spaces/csoai/games-catalog) · "
        f"[Verify]({SITES['verify']}) · [MCP]({SITES['mcp']})"
    )

if __name__ == "__main__":
    demo.launch(mcp_server=True)
