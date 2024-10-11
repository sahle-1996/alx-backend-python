#!/usr/bin/env python3
"""
A script defining a type-annotated function 'floor' that takes
a floating-point number and returns its floor value as an integer.
"""

import math


def floor(n: float) -> int:
    """
    Calculates the floor value of a float.

    Args:
        n (float): The floating-point number to floor.

    Returns:
        int: The largest integer less than or equal to n.
    """
    return math.floor(n)

