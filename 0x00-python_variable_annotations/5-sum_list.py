#!/usr/bin/env python3
"""
A script that defines a function 'sum_list', which takes a list of floats
and returns their total sum as a float.
"""

from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Takes a list of floats and returns the sum of all elements.

    Args:
        input_list (List[float]): A list containing float values.

    Returns:
        float: The sum of all the elements in the list.
    """
    total = 0.0
    for num in input_list:
        if isinstance(num, float):
            total += num
    return total
