#!/usr/bin/env python3
"""
A script for a type-annotated function 'concat' that takes two strings
and returns their concatenation.
"""


def concat(str1: str, str2: str) -> str:
    """
    Concatenates two strings and returns the result.

    Args:
        str1 (str): The first string.
        str2 (str): The second string.

    Returns:
        str: The concatenated result of str1 and str2.
    """
    return str1 + str2
