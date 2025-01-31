#!/usr/bin/env python3
"""Defines a type-annotated function that
returns a function to multiply a float by a given multiplier.
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Returns a function that multiplies its input by `multiplier`. """
    def multiply_by(value: float) -> float:
        return value * multiplier
    return multiply_by
