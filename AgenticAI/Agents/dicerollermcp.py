# Dice Roller MCP
# This module implements a simple dice roller as an MCP (Modular Chat Plugin) using the FastMCP framework.
# Invoke using the command line: `python dicerollermcp.py` to start the MCP server on port 8000.

import random
import re
from fastmcp import FastMCP

mcp = FastMCP(name="Dice_Roller_MCP")


def _roll_dice(n_dice: int, sides: int = 6) -> list[int]:
    """Internal implementation: roll `n_dice` dice with `sides` sides.

    This helper is a normal Python function (callable) so other tools
    in this module can call it directly. Validation is performed here.
    """
    if not isinstance(n_dice, int):
        raise ValueError("Invalid dice count: `n_dice` must be an integer.")
    if n_dice < 1:
        raise ValueError("Invalid dice count: must roll at least one die (n_dice >= 1).")
    if not isinstance(sides, int):
        raise ValueError("Invalid sides: `sides` must be an integer.")
    if sides < 2:
        raise ValueError("Invalid sides: dice must have at least 2 sides (sides >= 2).")

    return [random.randint(1, sides) for _ in range(n_dice)]


@mcp.tool()
def roll_dice(n_dice: int, sides: int = 6) -> list[int]:
    """MCP-exposed tool wrapper for `_roll_dice`.

    Keeps the tool registration separate from the internal implementation
    so internal code can call `_roll_dice` directly (avoiding FunctionTool
    wrapper objects being non-callable).
    """
    return _roll_dice(n_dice, sides)


def _parse_dice_token(token: str) -> tuple[int, int]:
    """Parse a single dice token like '2d6' or 'd8'. Returns (count, sides).
    Raises ValueError with a descriptive message on invalid format.
    """
    token = token.strip()
    m = re.fullmatch(r"(\d*)[dD](\d+)", token)
    if not m:
        raise ValueError(f"Invalid dice token: '{token}'. Expected format like '2d6' or 'd8'.")
    count_str, sides_str = m.groups()
    count = int(count_str) if count_str else 1
    sides = int(sides_str)
    if count < 1:
        raise ValueError(f"Invalid dice count in token '{token}': must be >= 1.")
    if sides < 2:
        raise ValueError(f"Invalid sides in token '{token}': must be >= 2.")
    return count, sides


@mcp.tool()
def roll_multiple(specs: str) -> dict:
    """Roll multiple dice groups specified in dice notation.

    Accepts either:
    - a single string like '2d6 + 1d20' (plus signs and whitespace allowed), or
    - a list of strings like ['2d6', '1d20'].

    Returns a dictionary with detailed results:
    {
      'rolls': { '2d6': [3,4], '1d20': [17] },
      'sums': { '2d6': 7, '1d20': 17 },
      'total': 24
    }

    Raises ValueError with descriptive messages for invalid inputs.
    """
    tokens = []
    if isinstance(specs, str):
        # split on '+' signs
        parts = specs.split('+')
        tokens = [p.strip() for p in parts if p.strip()]
        if not tokens:
            raise ValueError("Empty dice specification string provided to roll_multiple.")
    elif isinstance(specs, (list, tuple)):
        if not specs:
            raise ValueError("Empty dice list provided to roll_multiple.")
        tokens = []
        for item in specs:
            if not isinstance(item, str):
                raise ValueError("Invalid item in dice list: each item must be a string like '2d6'.")
            if item.strip():
                tokens.append(item.strip())
    else:
        raise ValueError("Invalid specs type: must be a string like '2d6 + 1d20' or a list of such strings.")

    results = {"rolls": {}, "sums": {}, "total": 0}
    for token in tokens:
        count, sides = _parse_dice_token(token)
        rolls = _roll_dice(count, sides)
        results["rolls"][token] = rolls
        group_sum = sum(rolls)
        results["sums"][token] = group_sum
        results["total"] += group_sum

    return results


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8035)
