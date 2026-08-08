# Dice Roller Client
# This module implements a Streamlit-based client for the Dice Roller MCP.
# It allows users to input dice specifications and roll them using the MCP server.
# Invoke using the command line: `streamlit run diceroller_client.py` to start the web interface.

import http
import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import random

st.set_page_config(page_title="Dice Roller — Play", page_icon="🎲")

_DICE_EXAMPLES = ["2d6 + 1d20", "d20", "4d8", "3d6 + 2d4 + d10"]


def _parse_dice_token(token: str) -> tuple[int, int]:
    token = token.strip()
    m = re.fullmatch(r"(\d*)[dD](\d+)", token)
    if not m:
        raise ValueError(
            f"Invalid dice token: '{token}'. Expected format like '2d6' or 'd8'."
        )
    count_str, sides_str = m.groups()
    count = int(count_str) if count_str else 1
    sides = int(sides_str)
    if count < 1:
        raise ValueError(f"Invalid dice count in token '{token}': must be >= 1.")
    if sides < 2:
        raise ValueError(f"Invalid sides in token '{token}': must be >= 2.")
    return count, sides


def roll_dice(n_dice: int, sides: int = 6) -> list[int]:
    if not isinstance(n_dice, int) or n_dice < 1:
        raise ValueError("n_dice must be an integer >= 1")
    if not isinstance(sides, int) or sides < 2:
        raise ValueError("sides must be an integer >= 2")
    return [random.randint(1, sides) for _ in range(n_dice)]


def roll_multiple(specs) -> dict:
    tokens = []
    if isinstance(specs, str):
        parts = specs.split("+")
        tokens = [p.strip() for p in parts if p.strip()]
        if not tokens:
            raise ValueError("Empty dice specification string provided.")
    elif isinstance(specs, (list, tuple)):
        if not specs:
            raise ValueError("Empty dice list provided.")
        tokens = [str(item).strip() for item in specs if str(item).strip()]
    else:
        raise ValueError(
            "Invalid specs type: must be string like '2d6 + 1d20' or a list of such strings."
        )

    results = {"rolls": {}, "sums": {}, "total": 0}
    for token in tokens:
        count, sides = _parse_dice_token(token)
        rolls = roll_dice(count, sides)
        results["rolls"][token] = rolls
        results["sums"][token] = sum(rolls)
        results["total"] += sum(rolls)

    return results


def _render_play_hints():
    st.markdown("**Play Hints**")
    st.write(
        "- Use `NdS` notation: `2d6` means roll two six-sided dice.\n"
        "- Combine groups with `+`: `2d6 + 1d20`.\n"
        "- `d20` is shorthand for `1d20`.\n"
    )
    st.markdown("**Examples:**")
    st.code("  \n".join(_DICE_EXAMPLES))


def main():
    st.title("🎲 Dice Roller")
    st.markdown("Enter dice notation (e.g., `2d6 + 1d20`) and press Roll.")

    with st.sidebar:
        st.header("Quick Hints")
        _render_play_hints()

    spec = st.text_input("Dice spec", value=_DICE_EXAMPLES[0])
    repeats = st.number_input("Repeat rolls (for averages)", min_value=1, max_value=100, value=1)

    # Configure MCP/OpenAI client 
    load_dotenv()
    url = "https://rachell-semimagnetic-gaylene.ngrok-free.dev"
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("OPENAI_API_KEY not found in environment. Set it in .env or export it to call the MCP.")

    client = OpenAI(api_key=api_key) if api_key else None

    def call_mcp(prompt: str) -> str:
        if not client:
            raise RuntimeError("OpenAI client not configured (OPENAI_API_KEY missing).")
        resp = client.responses.create(
            model="gpt-4o",
            tools=[
                {
                    "type": "mcp",
                    "server_label": "Dice_Roller_MCP",
                    "server_url": f"{url}/mcp",
                    "require_approval": "never",
                },
            ],
            input=prompt,
        )
        return resp.output_text

    if st.button("Roll"):
        if not client:
            st.error("Cannot call MCP: OPENAI_API_KEY not configured.")
            return

        try:
            runs = []
            for _ in range(repeats):
                prompt = (
                    f"Use the MCP server tools to run `roll_multiple` with specs=\"{spec}\". "
                    "Return the tool output only (JSON preferred)."
                )
                out = call_mcp(prompt)
                parsed = None
                try:
                    parsed = json.loads(out)
                except Exception:
                    try:
                        import ast

                        parsed = ast.literal_eval(out)
                    except Exception:
                        parsed = None
                runs.append({"raw": out, "parsed": parsed})

            st.success("MCP call(s) completed")
            last = runs[-1]
            if last["parsed"] and isinstance(last["parsed"], dict):
                st.subheader("Last roll breakdown (from MCP)")
                for token, rolls in last["parsed"].get("rolls", {}).items():
                    st.write(f"**{token}**: {rolls} (sum: {last['parsed'].get('sums', {}).get(token)})")
                st.markdown(f"**Total:** {last['parsed'].get('total')}")
                if repeats > 1:
                    totals = [r["parsed"].get("total", 0) for r in runs if r["parsed"]]
                    if totals:
                        st.subheader("Summary")
                        st.write(f"Runs: {repeats}")
                        st.write(f"Average total: {sum(totals)/len(totals):.2f}")
            else:
                st.subheader("Raw MCP output")
                for i, r in enumerate(runs, start=1):
                    st.write(f"Run {i}:")
                    st.code(r["raw"])
        except Exception as e:
            st.error(f"Error during MCP call: {e}")


if __name__ == "__main__":
    main()