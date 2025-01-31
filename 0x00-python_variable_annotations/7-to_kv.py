#!/usr/bin/env python3
""" Script defining a type-annotated function
that accepts a string and a numeric value,
returning a tuple with the string and squared value.
"""

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Returns a tuple where:
    - The first element is the input string `k`.
    - The second element is the square of `v` as a float.
    """
    return (k, float(v) ** 2)
