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


ANSI_REGEX = re.compile("\x1b\\[.*?[ABCDEFGHJKfnsumlh]")
"""Regex pattern that matches most ansi escape sequences."""


def filter_ansi(style: Mapping[str, Any]) -> dict[str, Ansi]:
    """
    Filters all ansi objects inside a mapping. Useful when
    ansi objects are defined in a module so that ``locals()``
    or ``module.__dict__`` can be used.
    """
    return {k: v for k, v in style.items() if isinstance(v, Ansi)}

