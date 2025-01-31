#!/usr/bin/env python3
""" Given the parameters and the return values,
    add type annotations to the function.
    Hint: look into TypeVar.
"""

from typing import Mapping, Any, Union, TypeVar

T = TypeVar("T")


def safely_get_value(
        dct: Mapping,
        key: Any,
        default: Union[T, None] = None
) -> Union[Any, T]:
    """ More involved type annotations. """
    return dct[key] if key in dct else default
