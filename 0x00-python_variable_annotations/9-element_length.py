#!/usr/bin/env python3
"""Defines a function with type-annotated parameters
and return values for sequences.
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(collection: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Computes the length of each sequence in an iterable
    and returns a list of tuples containing the sequence
    and its corresponding length.
    """
    return [(item, len(item)) for item in collection]
