from typing import Tuple, Any, Union, Sequence, List


def zoom_array(lst: Sequence[int], factor: Union[int, float] = 2) -> Tuple[Union[int, float], ...]:
    """Expands each element in lst by a given factor and returns a tuple."""

    factor = int(factor) if isinstance(factor, float) else factor
    zoomed_in: List[Union[int, float]] = [
        num for num in lst
        for _ in range(factor)
    ]
    return tuple(zoomed_in)


array = [12, 72, 91]

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3.0)
