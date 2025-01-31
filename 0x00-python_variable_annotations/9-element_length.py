#!/usr/bin/env python3
"""Defines a function with annotated parameters
and return values using appropriate types.
"""

from typing import List, Tuple, Sequence, Iterable


def element_length(items: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples containing each sequence
    from the input and its corresponding length.
    """
    return [(item, len(item)) for item in items]
