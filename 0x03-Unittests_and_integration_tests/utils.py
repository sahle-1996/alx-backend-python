#!/usr/bin/env python3
"""Utility functions for GitHub organization client.
"""
import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested: Mapping, keys: Sequence) -> Any:
    """Access a value in a nested mapping using a sequence of keys.
    Parameters
    ----------
    nested: Mapping
        The nested mapping from which to retrieve values
    keys: Sequence
        Sequence of keys defining the path to the value
    Example
    -------
    >>> nested = {"x": {"y": {"z": 42}}}
    >>> access_nested_map(nested, ["x", "y", "z"])
    42
    """
    for key in keys:
        if not isinstance(nested, Mapping):
            raise KeyError(key)
        nested = nested[key]
    return nested


def get_json(url: str) -> Dict:
    """Fetch JSON content from a URL.
    """
    res = requests.get(url)
    return res.json()


def memoize(func: Callable) -> Callable:
    """Decorator to cache method results.
    Example
    -------
    class Sample:
        @memoize
        def method(self):
            print("method executed")
            return 100
    >>> instance = Sample()
    >>> instance.method
    method executed
    100
    >>> instance.method
    100
    """
    cache_attr = "_{}".format(func.__name__)

    @wraps(func)
    def memoized(self):
        """Retrieve or set cached method result."""
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, func(self))
        return getattr(self, cache_attr)

    return property(memoized)
