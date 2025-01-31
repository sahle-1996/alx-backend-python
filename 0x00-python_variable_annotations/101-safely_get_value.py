#!/usr/bin/env python3
"""Enhancing the function with proper duck-typed annotations."""

from typing import Sequence, Any, Optional


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """Retrieve the first element of a sequence or return None if empty."""
    
    return None if not lst else lst[0]
