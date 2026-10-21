"""Basic arithmetic without evaluating arbitrary code."""

import logging
from typing import Literal


def calculate(a: float, b: float, operation: Literal["add", "subtract", "multiply", "divide"]) -> str:
    """Perform one arithmetic operation on two numbers."""
    logging.info("TOOL | calculate | %s %s %s", a, operation, b)
    if operation == "add":
        return str(a + b)
    if operation == "subtract":
        return str(a - b)
    if operation == "multiply":
        return str(a * b)
    if operation == "divide":
        return "Cannot divide by zero." if b == 0 else str(a / b)
    return "Unknown operation."
