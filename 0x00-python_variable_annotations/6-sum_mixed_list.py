#!/usr/bin/env python3
"""
This script defines a type-annotated function
that accepts a list of integers and floats,
then returns their sum as a float.
"""

from typing import List, Union

def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Function that accepts a list of integers and floats,
    and returns the sum as a float."""
    return sum(mxd_lst)
