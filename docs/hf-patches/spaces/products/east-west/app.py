"""East-West — Hugging Face Space + MCP door.

100-move play / crosswalk lives on councilof.ai/east-west/.
This Space MCP-connects that door. It is not a second play engine.
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

from door_kit import THEME, footer, get_axis, living_totals
from mcp_client import SITES, fetch_board, pretty


def east_west_door() -> str:
    """Open the East-West 100-move play door.

    Returns:
        JSON door card. Play chrome is on councilof.ai/east-west/.
    """
    return pretty(
        {
            "kind": "east-west-door",
            "site": SITES["east_west"],
            "os": SITES["os"],
            "verify": SITES["verify"],
            "mcp": SITES["mcp"],
            "board": fetch_board(),
            "honesty": "Door only. East-West play stays on-site. Same living board.",
        }
    )


with gr.Blocks(title="East-West — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# East-West
**Council of AI · CSOAI Ltd (UK 16939677)**

Live play: [councilof.ai/east-west/](https://councilof.ai/east-west/).

This Space is a door + MCP server for N-sites. It does not host the 100-move engine.
Measurement, not certification.
"""
    )
    with gr.Tab("East-West door"):
        door_out = gr.Code(label="east-west", language="json")
        gr.Button("Open door").click(east_west_door, outputs=door_out)
        demo.load(east_west_door, outputs=door_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
        axis = gr.Textbox(label="Axis id", placeholder="governance")
        axis_out = gr.Code(label="get_axis", language="json")
        gr.Button("Get axis").click(get_axis, inputs=axis, outputs=axis_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
