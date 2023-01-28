"""
Various utilities used internally.
"""

from __future__ import annotations

from collections import namedtuple
from collections.abc import Callable, Iterable, Mapping
from math import sqrt
import re
from typing import Any, Optional, TypeVar, Union


RGB = namedtuple("RGB", "r g b")

T = TypeVar("T")

T_RGB = Union[tuple[int, int, int], RGB]
T_HLS = tuple[float, float, float]

HEX = Union[str, int]


def _copydoc(
    source: Any,
    replace: Optional[
        Mapping[
            re.Pattern[str],
            Union[
                str,
                Callable[[re.Match[str]], str]
            ]
        ]
    ] = None,
) -> Callable[[T], T]:
    """
    Copies docstring of another function.
    
    Parameters
    ----------
    source
        The object whose text should be copied.
    
    replace
        A mapping of regex patterns and either callables or
        string to replace the matches with.
    """
    def decorator(fn: T) -> T:
        doc = source.__doc__
        
        if replace is not None:
            for pattern, replace_with in replace.items():
                doc = pattern.sub(
                    replace_with,
                    doc
                )
        
        fn.__doc__ = doc
        return fn
    return decorator

def _get_closest_color(
    color: RGB,
    colors: Iterable[tuple[T, RGB]]
) -> T:
    """
    Returns first value of a tuple by finding
    the closest rgb color.
    
    Parameters
    ----------
    color
        The rgb color to find the closest possible
        rgb color from the ``colors`` parameter.
    
    colors
        Sequence of two-sized tuples. Second value is
        an rgb value that ``color`` could approach.
        The first value is any value that will be returned
        if the second value is the closest to ``color``.
    
    Returns
    -------
    Associated value of closest color.
    """
    diffs = {}
    for value, rgb in colors:
        if color == rgb:
            return value
        
        diff = sqrt(
            abs(color.r - rgb.r) ** 2 +
            abs(color.g - rgb.g) ** 2 +
            abs(color.b - rgb.b) ** 2
        )
        
        diffs[diff] = value
    
    return diffs[min(diffs.keys())]

