"""Council MCP playground — architecture-doc Space 5, mapped honestly.

Not an OpenAI-compatible inference playground. Not ZeroGPU.
A typed door over the live worker tools/list + tools/call.
"""
from __future__ import annotations

import json
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

from door_kit import THEME, footer, living_totals
from mcp_client import LIVE_TOOLS, SITES, mcp_call, mcp_tools_list, pretty


def list_live_tools() -> str:
    """List tools currently advertised by the live Council of AI MCP worker.

    Returns:
        Live tools/list. A cached four-tool catalogue is not presented as live.
    """
    return pretty(mcp_tools_list())


def call_live_tool(tool: str, arguments_json: str) -> str:
    """Call one live MCP tool. This Space does not grade or infer.

    Args:
        tool: Worker tool name (measure, verify, jail-probe, enter-arena, …).
        arguments_json: JSON object of tool arguments.

    Returns:
        Live tools/call result, or UNREACHABLE / parse error.
    """
    name = (tool or "").strip()
    if not name:
        return pretty({"ok": False, "state": "NEED_TOOL", "tools": list(LIVE_TOOLS)})
    raw = (arguments_json or "").strip() or "{}"
    try:
        args = json.loads(raw)
    except json.JSONDecodeError as exc:
        return pretty({"ok": False, "state": "BAD_JSON", "error": str(exc)})
    if not isinstance(args, dict):
        return pretty({"ok": False, "state": "NEED_OBJECT"})
    return pretty(mcp_call(name, args))


with gr.Blocks(title="MCP playground — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# MCP playground
**Council of AI · CSOAI Ltd (UK 16939677)**

Architecture-doc “API Playground”, mapped honestly:
**live MCP tools only.** Not OpenAI `/v1/chat/completions`. Not ZeroGPU.

Worker: [`https://councilof.ai/mcp`](https://councilof.ai/mcp) · OS: [councilof.ai/os](https://councilof.ai/os)
"""
    )
    with gr.Tab("Live tools"):
        list_out = gr.Code(label="tools/list", language="json")
        gr.Button("List live tools").click(list_live_tools, outputs=list_out)
        demo.load(list_live_tools, outputs=list_out)
    with gr.Tab("Call tool"):
        tool = gr.Dropdown(choices=list(LIVE_TOOLS), value="board_totals", label="Tool")
        args = gr.Textbox(label="Arguments JSON", value="{}", lines=6)
        call_out = gr.Code(label="tools/call", language="json")
        gr.Button("Call live worker").click(
            call_live_tool, inputs=[tool, args], outputs=call_out
        )
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(f"{footer()} · [Worker]({SITES['mcp']})")

if __name__ == "__main__":
    demo.launch(mcp_server=True)
