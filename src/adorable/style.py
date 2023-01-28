"""
Common ansi styles.
"""

from __future__ import annotations
from typing import Any
from .ansi import Ansi

class Style(Ansi):
    def __init__(self, enable: Any, disable: Any):
        self._ansi = [enable]
        self._off = [disable]


BOLD = Style(1, 22)           # b
"""Bold style"""

DIM = Style(2, 22)            # d
"""Dim style"""

ITALIC = Style(3, 23)         # i
"""Italic style"""

UNDERLINE = Style(4, 24)      # u
"""Underline style"""

BLINK = Style(5, 25)          # f (flash)
"""Blink style"""

INVERSE = Style(7, 27)        # r (reverse)
"""Inverse style"""

INVISIBLE = Style(8, 28)      # h (hidden)
"""Invisible style"""

STRIKETHROUGH = Style(9, 29)  # s
"""Strike through style"""
