"""Coliseum / Arena — Hugging Face Space + MCP door.

Contest chrome lives on councilof.ai/coliseum and /arena.
Arenas stay on the measurement fleet (3090/A100). This Space MCP-exports
enter-arena and the 16 jail-probe families so any site or agent can enrol.
Not a second Elo league. Not a GPU engine.
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

from mcp_client import JAIL_FAMILIES, SITES, fetch_board, mcp_call, pretty


def coliseum_door() -> str:
    """Open the Coliseum / Arena door with live board pointer.

    Returns:
        JSON door card. Contest chrome is on councilof.ai; this Space is not the engine.
    """
    return pretty(
        {
            "kind": "council-coliseum-door",
            "coliseum": SITES["coliseum"],
            "arena": SITES["arena"],
            "council_space": SITES["council_space"],
            "mcp": SITES["mcp"],
            "jail_families": JAIL_FAMILIES,
            "board": fetch_board(),
            "honesty": (
                "Door + MCP. Arenas stay on the fleet. "
                "Not preference Elo as a public GSPC grade."
            ),
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


def enter_arena(agent_card_url: str, consent: bool) -> str:
    """Self-enrol an agent into the Coliseum via live MCP enter-arena.

    Args:
        agent_card_url: https URL of the visiting A2A agent card.
        consent: Must be true. Machine-readable consent to be measured.

    Returns:
        Unsigned intake receipt queued for signed fleet measurement, or UNREACHABLE.
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
            {"agent_card_url": agent_card_url.strip(), "consent": True},
        )
    )


def jail_probe(model: str, prompt: str, family: str) -> str:
    """Return the jail-probe CONTRACT for one of the 16 attack families.

    This Space does not run the probe. Sandbox execution stays on the fleet.

    Args:
        model: Model to probe.
        prompt: Jailbreak attempt text.
        family: Attack family 1-16.

    Returns:
        Contract from live MCP. measured:false — no verdict is issued here.
    """
    if not (model or "").strip() or not (prompt or "").strip():
        return pretty({"ok": False, "state": "NEED_MODEL_AND_PROMPT"})
    fam = (family or "1").strip()
    if fam not in JAIL_FAMILIES:
        return pretty(
            {
                "ok": False,
                "state": "BAD_FAMILY",
                "hint": "family must be one of 1..16",
                "families": JAIL_FAMILIES,
            }
        )
    return pretty(
        mcp_call(
            "jail-probe",
            {"model": model.strip(), "prompt": prompt, "family": fam},
        )
    )


THEME = gr.themes.Soft(
    primary_hue="stone",
    secondary_hue="amber",
    neutral_hue="stone",
)

with gr.Blocks(title="Coliseum — Council of AI", theme=THEME) as demo:
    gr.Markdown(
        """
# Coliseum of AI
**Council of AI · CSOAI Ltd (UK 16939677)**

Contest chrome: [coliseum](https://councilof.ai/coliseum) · [arena rooms](https://councilof.ai/arena).

This Space is a door + MCP server. **Arenas stay on the fleet.**
`enter-arena` enrols an agent. Jail-probe exposes the **16 families** as a contract,
not a live attack from this Space.

Measurement, not certification. Not a public Elo league.
"""
    )
    with gr.Tab("Coliseum door"):
        door_out = gr.Code(label="coliseum", language="json")
        gr.Button("Open coliseum door").click(coliseum_door, outputs=door_out)
        demo.load(coliseum_door, outputs=door_out)
    with gr.Tab("Enter arena"):
        url = gr.Textbox(
            label="Agent card URL",
            placeholder="https://example.org/.well-known/agent-card.json",
        )
        consent = gr.Checkbox(label="I consent to be measured", value=False)
        arena_out = gr.Code(label="enter-arena receipt", language="json")
        gr.Button("Enter arena (live MCP)").click(
            enter_arena, inputs=[url, consent], outputs=arena_out
        )
    with gr.Tab("16 jail families"):
        model = gr.Textbox(label="Model")
        prompt = gr.Textbox(label="Probe prompt", lines=3)
        family = gr.Dropdown(choices=JAIL_FAMILIES, value="1", label="Family (1–16)")
        probe_out = gr.Code(label="jail-probe contract", language="json")
        gr.Button("Request contract (does not run the probe)").click(
            jail_probe, inputs=[model, prompt, family], outputs=probe_out
        )
    with gr.Tab("Living board"):
        totals_out = gr.Code(label="board_totals", language="json")
        gr.Button("Fetch live totals").click(living_totals, outputs=totals_out)
    gr.Markdown(
        f"[Coliseum]({SITES['coliseum']}) · [Arena]({SITES['arena']}) · "
        f"[City]({SITES['city']}) · [Verify]({SITES['verify']}) · "
        f"[MCP]({SITES['mcp']})"
    )

if __name__ == "__main__":
    demo.launch(mcp_server=True)
