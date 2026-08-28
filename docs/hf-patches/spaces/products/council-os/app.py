"""Council OS — Hugging Face Space + MCP door.

Public product door is Council OS / Lobby on councilof.ai.
This Space MCP-connects that door to any N-site or agent client.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, _HERE.parent, _HERE.parent.parent / "play"):
    if (_candidate / "mcp_client.py").exists():
        sys.path.insert(0, str(_candidate))
        break
    if (_candidate / "door_kit.py").exists():
        sys.path.insert(0, str(_candidate))

import gradio as gr

from door_kit import THEME, footer, get_axis, list_fabric, living_totals
from mcp_client import SITES, fetch_board, pretty


def os_door() -> str:
    """Open the Council OS door: live board pointer + OS / lobby URLs.

    Returns:
        JSON door card. Council OS chrome lives on councilof.ai/os.
    """
    return pretty(
        {
            "kind": "council-os-door",
            "os": SITES["os"],
            "lobby": SITES["lobby"],
            "verify": SITES["verify"],
            "city": SITES["city"],
            "coliseum": SITES["coliseum"],
            "council_space": SITES["council_space"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": "One-door Council OS. This Space is not a second OS.",
        }
    )


with gr.Blocks(title="Council OS — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# Council OS
**Council of AI · CSOAI Ltd (UK 16939677)**

Live OS: [councilof.ai/os](https://councilof.ai/os) · Lobby: [/?lobby=home](https://councilof.ai/?lobby=home).

This Space is a door + MCP server. **Any site or agent can MCP here to reach Council OS.**
It does not host a second OS, board, or Elo league.

Living counts: `GET https://councilof.ai/api/gspc` · MCP: `https://councilof.ai/mcp`  
Measurement, not certification. Empty slots stay empty.
"""
    )
    with gr.Tab("OS door"):
        door_out = gr.Code(label="council-os", language="json")
        gr.Button("Open OS door").click(os_door, outputs=door_out)
        demo.load(os_door, outputs=door_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
        axis = gr.Textbox(label="Axis id", placeholder="governance")
        axis_out = gr.Code(label="get_axis", language="json")
        gr.Button("Get axis").click(get_axis, inputs=axis, outputs=axis_out)
    with gr.Tab("Fabric"):
        fabric_out = gr.Code(label="product Spaces", language="json")
        gr.Button("List product MCP doors").click(list_fabric, outputs=fabric_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
