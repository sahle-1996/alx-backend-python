#!/usr/bin/env python3
"""function with annotated parameters and
return values with appropriate types."""

from typing import List, Tuple, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Takes a list of sequences and returns a list of tuples
    where each tuple contains a sequence from the list and its length.
    """

    return [(seq, len(seq)) for seq in lst]
