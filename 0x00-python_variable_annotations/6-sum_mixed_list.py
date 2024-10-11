#!/usr/bin/env python3
"""
Script that defines a type-annotated function
which takes a list containing integers and floats,
and returns the sum of the elements as a float.
"""

from typing import List, Union

def calculate_sum(mixed_list: List[Union[int, float]]) -> float:
    """Takes a list of integers and floats, and returns
    their sum as a float."""
    total: float = 0.0
    for element in mixed_list:
        if isinstance(element, (int, float)):
            total += element
    return total
