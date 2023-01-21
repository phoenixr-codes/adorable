from collections.abc import Mapping
from typing import Any

from .color import (
    Color3bit,
    Color8bit,
    Color24bit,
)

from .style import (
    BOLD,
    DIM,
    ITALIC,
    UNDERLINE,
    BLINK,
    INVERSE,
    INVISIBLE,
    STRIKETHROUGH
)

from .ansi import *
from .markup import *
from .stylesheet import *
from .stylesheet import _globals
from . import term


ANSI_REGEX = re.compile("\x1b\\[.*?[ABCDEFGHJKfnsumlh]")
"""Regex pattern that matches most ansi escape sequences."""

def use(terminal: str) -> None:
    """
    .. versionadded:: 0.2.0b1
    
    A quick way of overriding the current color
    system manually.
    
    Parameters
    ----------
    terminal
        The color system as a string. This might
        be ``"NOCOLOR"``, ``"BIT3"``, ``"BIT8``
        or ``"BIT24"``.
    """
    term.cache = term.Terminal[terminal]

def filter_ansi(style: Mapping[str, Any]) -> dict[str, Ansi]:
    """
    Filters all ansi objects inside a mapping. Useful when
    ansi objects are defined in a module so that ``locals()``
    or ``module.__dict__`` can be used.
    """
    return {k: v for k, v in style.items() if isinstance(v, Ansi)}

