#!/usr/bin/env python3
""" Given the parameters and the return values,
    add type annotations to the function.
    Hint: look into TypeVar.
"""

from typing import Mapping, Any, Union, TypeVar

U = TypeVar('U')


def safely_get_value(
        dct: Mapping[Any, U],
        key: Any,
        default: Union[U, None] = None
) -> Union[U, None]:
    """ Retrieves a value from a dictionary safely. """
    return dct.get(key, default)
