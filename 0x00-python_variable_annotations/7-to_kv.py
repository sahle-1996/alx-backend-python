#!/usr/bin/env python3
"""
This script defines a type-annotated function
that takes a string and a numeric value (int or float),
and returns a tuple.
"""

from typing import Union, Tuple

def pair_with_square(key: str, value: Union[int, float]) -> Tuple[str, float]:
    """Accepts a string and an int or float, and returns
    a tuple where the first element is the string and the second
    element is the square of the numeric value as a float."""
    
    return key, float(value ** 2)
