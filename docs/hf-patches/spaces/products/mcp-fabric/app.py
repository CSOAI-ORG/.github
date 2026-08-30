"""MCP fabric — directory of every product Space that MCP to Council OS.

This is the anywhere-index. Add one Space, or add them all.
Tools proxy the live worker. This Space is not a second MCP catalogue product.
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

from door_kit import THEME, footer, list_fabric, living_totals
from mcp_client import SITES, mcp_tools_list, pretty


def ping_worker() -> str:
    """Ping the live Council of AI MCP worker and list its tools.

    Returns:
        Live tools/list, or UNREACHABLE. Do not invent a catalogue.
    """
    return pretty(
        {
            "kind": "worker-ping",
            "mcp": SITES["mcp"],
            "os": SITES["os"],
            "tools": mcp_tools_list(),
        }
    )


with gr.Blocks(title="MCP fabric — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# MCP fabric
**Council of AI · CSOAI Ltd (UK 16939677)**

Every product is a Space. Every Space MCP-connects to [Council OS](https://councilof.ai/os)
and the live worker [`https://councilof.ai/mcp`](https://councilof.ai/mcp).

Add any Space (or this fabric) at [huggingface.co/settings/mcp](https://huggingface.co/settings/mcp).
N-sites do not host a second board.

Measurement, not certification.
"""
    )
    with gr.Tab("Fabric"):
        fabric_out = gr.Code(label="product Spaces", language="json")
        gr.Button("List fabric").click(list_fabric, outputs=fabric_out)
        demo.load(list_fabric, outputs=fabric_out)
    with gr.Tab("Ping worker"):
        ping_out = gr.Code(label="tools/list", language="json")
        gr.Button("Ping councilof.ai/mcp").click(ping_worker, outputs=ping_out)
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(footer())

if __name__ == "__main__":
    demo.launch(mcp_server=True)
