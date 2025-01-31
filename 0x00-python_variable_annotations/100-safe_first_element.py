#!/usr/bin/env python3
"""Augment the code with the correct duck-typed annotations."""

from typing import List, Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return the first element of a sequence or None if it's empty."""

    return lst[0] if lst else None
