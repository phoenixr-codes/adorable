"""
Utilities for creating color objects.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from copy import copy
from enum import auto, IntEnum
import operator
from typing import Any, Union
import warnings

from . import _palette
from . import webcolors
from .ansi import Ansi, _get_ansi_string, paint
from .term import Terminal
from .utils import _copydoc, _get_closest_color,  RGB, HEX, T_RGB


_NOT_INITIALIZED: str = "color not initialized"
_ALREADY_INITIALIZED: str = "color already initialized"


class _GroundError(Exception):
    pass


class _Ground(IntEnum):
    NONE = auto()
    FORE = auto()
    BACK = auto()
    BOTH = auto()
    
    @staticmethod
    def check(
        *checks: tuple[
            Callable[..., bool],
            Union[Color, int],
            Union[Color, int],
            str
        ]
    ) -> None:
        """
        Parameters
        ----------
        checks
            Each entry contains four fields.
            
            # A callable (usually a function from the
              :pylib:`operator` library).
            # A :class:`_Ground` or :class:`Color` instance.
              (If latter is given, the ground is extracted
              from it.)
            # Another one for comparison.
            # A string to display when the comparison
              returns ``False``.
        
        Raises
        ------
        ``TypeError``
            Entry contains value with invalid type.
        
        ``_GroundError``
            The comparison returned ``False``.
        """
        msg = "invalid ground set"  # in case a string is missing
        for check in checks:
            args: list[int] = []
            for arg in check[1:]:
                if isinstance(arg, Color):
                    args.append(arg._ground)
                
                elif isinstance(arg, str):
                    msg = arg
                
                elif isinstance(arg, int):
                    args.append(arg)
                
                else:
                    raise TypeError(
                        "expected 'Color', 'int' or 'str', "
                        f"got {arg.__class__.__name__!r}"
                    )
            
            if not check[0](*args):
                raise _GroundError(msg)

class Color(Ansi, metaclass = ABCMeta):
    """
    Abstract Base Class for terminal dependent
    colors.
    """
    _termtype: Terminal
    
    def __init__(self, **data: Any):
        """
        .. attention::
           
           Directly initializing this class is
           prohibited. Use one of the available
           class methods such as
           :meth:`from_name`, :meth:`from_rgb` or
           :meth:`from_hex`.
        
        Parameters
        ----------
        data
            Various metadata set by subclasses
            for internal use.
        """
        self._ansi: list[Any] = []
        self._off = [0]
        self._data = data
        self._ground: _Ground = _Ground.NONE
    
    def __str__(self) -> str:
        if not self.is_initialized():
            warnings.warn(
                f"{self.__class__.__name__} instance at "
                f"{hex(id(self))} is not initialized. Use "
                "`.bg`, `.fg` or `.on()` to initialize it.",
                RuntimeWarning
            )
            return ""
        
        return self.enable_str()
    
    def __or__(self, other: Color) -> Color:
        """
        Returns the color that is supported. Returns
        the color with a larger color palette when
        both are supported. Returns the color with a
        smaller color palette when neither is supported.
        """
        if not isinstance(other, Color):
            return NotImplemented
        
        if other.is_supported() and self.is_supported():
            return max(self, other, key = lambda x: x._termtype)
        
        if other.is_supported():
            return other
        
        if self.is_supported():
            return self
        
        return min(self, other, key = lambda x: x._termtype)
    
    def __add__(self, other: Ansi) -> Ansi:
        if isinstance(other, Color):
            _Ground.check((
                operator.ne,
                other, _Ground.NONE,
                _NOT_INITIALIZED
            ), (
                operator.ne,
                other, self,
                "both colors are set to the same ground"
            ))
        
        elif not isinstance(other, Ansi):
            return NotImplemented
        
        obj = copy(self)
        return obj.extend(other)
    
    def __iadd__(self, other: Ansi) -> Ansi:
        if isinstance(other, Color):
            _Ground.check((
                operator.ne,
                other, _Ground.NONE,
                _NOT_INITIALIZED
            ), (
                operator.ne,
                other, self,
                "both colors are set to the same ground"
            ))
        
        elif not isinstance(other, Ansi):
            return NotImplemented
        
        return self.extend(other)
    
    def __call__(self, *args: Any, **kwargs: Any) -> str:
        _Ground.check((
            operator.ne,
            self, _Ground.NONE,
            _NOT_INITIALIZED
        ))
        
        return paint(*args, style = self, **kwargs)
    
    def enable_str(self) -> str:
        _Ground.check((
            operator.ne,
            self, _Ground.NONE,
            _NOT_INITIALIZED
        ))
        
        return super().enable_str()
    
    def disable_str(self) -> str:
        _Ground.check((
            operator.ne,
            self, _Ground.NONE,
            _NOT_INITIALIZED
        ))
        
        return super().disable_str()
    
    def is_initialized(self) -> bool:
        """
        .. versionadded:: 0.1.0
        
        Checks if the color is initialized or not.
        """
        return self._ground != _Ground.NONE
    
    def is_supported(self) -> bool:
        """
        .. versionadded:: 0.1.1
        
        Checks if the color system is supported
        or not.
        """
        return self._termtype.is_supported()
    
    def _get_ansi(self) -> str:
        return _get_ansi_string(self._ansi)
    
    @abstractmethod
    def _form(self, ground: _Ground) -> list[int]:
        """
        Forms the ansi sequence by returning a list
        of its attributes.
        """
        ...
    
    @property
    def fg(self) -> Color:
        """
        Sets the color to foreground mode.
        """
        _Ground.check((
            operator.eq,
            self, _Ground.NONE,
            _ALREADY_INITIALIZED
        ))
        
        self._ansi.extend(self._form(_Ground.FORE))
        self._ground = _Ground.FORE
        
        return self
    
    @property
    def bg(self) -> Color:
        """
        Sets the color to background mode.
        """
        _Ground.check((
            operator.eq,
            self, _Ground.NONE,
            _ALREADY_INITIALIZED
        ))
        
        self._ansi.extend(self._form(_Ground.BACK))
        self._ground = _Ground.BACK
        
        return self
    
    def on(self, other: Color) -> Color:
        """
        Sets the color to foreground mode and adds
        another color as background mode.
        
        Parameters
        ----------
        other
            Background color to set for this style.
            May already be initialized as background
            mode.
        """
        _Ground.check((
            lambda a, b, back, fore: a != back and b != fore,  # type: ignore
            self, other, _Ground.BACK, _Ground.FORE,
            "second color must not be set to background"
        ))
        
        self = self.fg
        self.extend(other.bg if other._ground != _Ground.BACK else other)
        
        self._ground = _Ground.BOTH
        
        return self
    
    @classmethod
    @abstractmethod
    def _from_rgb(cls, rgb: T_RGB) -> Color:
        ...
    
    @classmethod
    def from_rgb(cls, rgb: T_RGB | tuple[float, float, float]) -> Color:
        """
        Get color from RGB value.
        
        .. seealso::
           
           :doc:`Creating Colors <creating-color>`
        """
        values: list[int] = []
        for i in rgb:
            if isinstance(i, float):
                i = round(i * 255)
            values.append(i)
        
        return cls._from_rgb(values)  # type: ignore
    
    @classmethod
    def from_name(cls, name: str) -> Color:
        """
        Get color from Web Color name.
        
        .. seealso::
           
           :doc:`Creating Colors <creating-color>`
        """
        return cls.from_rgb(webcolors.COLORS[name.lower()])
    
    @classmethod
    def from_hex(cls, hex: HEX) -> Color:
        """
        Get color from HEX value.
        
        .. seealso::
           
           :doc:`Creating Colors <creating-color>`
        """
        if isinstance(hex, int):
            # convert to string
            hex = f"{hex:X}"
            
            # leading 0s will be removed so we need
            # to add them (e. g. 0x0AF -> AF -> 0AF)
            if len(hex) < 3:
                hex = hex.zfill(3)
            
            elif 3 < len(hex) < 6:
                hex = hex.zfill(6)
        
        if not isinstance(hex, str):
            raise TypeError("hex value must be int or str")
        
        hex = hex.removeprefix("#")
        
        if len(hex) == 3:
            # convert to a six chars long string
            hex = "".join(char * 2 for char in hex)
        
        elif len(hex) != 6:
            raise ValueError(
                "hex value should consist of 3 or 6 characters "
                "(e. g. `0xFFFFFF` or `0xFFF`)"
            )
        
        h = iter(hex)
        
        rgb = [int(char, 16) * 16 + int(next(h), 16) for char in h]
        return cls.from_rgb(rgb)  # type: ignore

class Color0bit(Color):
    _termtype: Terminal = Terminal.NOCOLOR
    
    def _form(self, ground: _Ground) -> list[int]:
        return []
    
    @classmethod
    def _from_rgb(cls, rgb: T_RGB) -> Color0bit:
        return cls()

class Color3bit(Color):
    _termtype: Terminal = Terminal.BIT3
    
    def _form(self, ground: _Ground) -> list[int]:
        value = self._data["ansi"]
        
        if ground in [_Ground.NONE, _Ground.BOTH]:
            raise ValueError()
        
        return [
            30 + value
        ]
    
    @classmethod
    def _from_rgb(cls, rgb: T_RGB) -> Color3bit:
        color: int = _get_closest_color(
            RGB(*rgb),
            enumerate(_palette.ANSI3BIT)
        )
        return cls(ansi = color, rgb = rgb)

class Color8bit(Color):
    _termtype: Terminal = Terminal.BIT8
    
    def _form(self, ground: _Ground) -> list[int]:
        value = self._data["ansi"]
        
        if ground in [_Ground.NONE, _Ground.BOTH]:
            raise ValueError()
        
        return [
            38 if ground == _Ground.FORE else 48,
            5,
            value
        ]
    
    @classmethod
    def _from_rgb(cls, rgb: T_RGB) -> Color8bit:
        color: int = _get_closest_color(
            RGB(*rgb),
            enumerate(_palette.ANSI8BIT)
        )
        return cls(ansi = color, rgb = rgb)

class Color24bit(Color):
    _termtype: Terminal = Terminal.BIT24
    
    def _form(self, ground: _Ground) -> list[int]:
        r, g, b = self._data["rgb"]
        
        if ground in [_Ground.NONE, _Ground.BOTH]:
            raise ValueError()
        
        return [
            38 if ground == _Ground.FORE else 48,
            2,
            r, g, b
        ]
    
    @classmethod
    def _from_rgb(cls, rgb: T_RGB) -> Color24bit:
        return cls(rgb = rgb)

def get_color() -> type[Color]:
    t = Terminal.get_term([])
    for colortype in [Color0bit, Color3bit, Color8bit, Color24bit]:
        if colortype._termtype == t:
            return colortype
    
    return Color0bit  # unreachable

@_copydoc(Color.from_hex)
def from_hex(*args: Any, **kwargs: Any) -> Color:
    col = get_color()
    return col.from_hex(*args, **kwargs)

@_copydoc(Color.from_rgb)
def from_rgb(*args: Any, **kwargs: Any) -> Color:
    col = get_color()
    return col.from_rgb(*args, **kwargs)

@_copydoc(Color.from_name)
def from_name(*args: Any, **kwargs: Any) -> Color:
    col = get_color()
    return col.from_name(*args, **kwargs)

def empty() -> Color0bit:
    """
    .. versionadded:: 0.1.0
    
    Returns a new instance of :class:`Color0bit`.
    """
    return Color0bit()

