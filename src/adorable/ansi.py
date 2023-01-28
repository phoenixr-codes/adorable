from __future__ import annotations

from abc import ABC
from copy import copy
import re
from sys import stdout
from typing import Any, Optional, TextIO

from .utils import _copydoc


def paint(*args: Any, style: Optional[Ansi] = None, sep: str = " ") -> str:
    """
    Styles a string.
    
    Parameters
    ----------
    args
        Objects to style. The ``str()`` function will
        be called on each object.
    
    style
        Ansi object that styles the string.
    
    sep
        String that separates ``args``.
    
    Returns
    -------
    The styled string.
    """
    content = sep.join(map(str, args))
    
    if style is None:
        return content
    
    elif not isinstance(style, Ansi):
        raise TypeError(
            "expected `None` or `Ansi` for argument `style`, "
            f"got {style.__class__.__name__}"
        )
    
    return f"{style}{content}{style.disable_str()}"

formatc = paint  # noqa: E305
"""Alias of :func:`paint`."""

def printc(*args: Any, **kwargs: Any) -> None:
    """
    Prints a styled string.
    
    This function takes the same arguments as the
    built-in print function. It also provides
    an extra parameter.
    
    Parameters
    ----------
    args
        Positional arguments passed to :pyfn:`print`
    
    kwargs
        Keyword arguments passed to :pyfn:`print`
    
    style
        Ansi objects that styles the string.
    """
    paint_kwargs = {}
    
    for key in ["style", "sep"]:
        if key in kwargs:
            paint_kwargs[key] = kwargs.pop(key)
    
    print(paint(*args, **paint_kwargs), **kwargs)


class Ansi(ABC):
    _ansi: list[Any]
    _off: list[Any]
    
    def __str__(self) -> str:
        return self.enable_str()
    
    @_copydoc(paint, replace = {
        re.compile("style.+?the string.", re.DOTALL): ""
    })
    def __call__(self, *args: Any, **kwargs: Any) -> str:
        return paint(*args, style = self, **kwargs)
    
    def __add__(self, other: Ansi) -> Ansi:
        """
        Combines two styles.
        """
        obj = copy(self)
        obj.extend(other)
        
        return obj
    
    def __iadd__(self, other: Ansi) -> Ansi:
        """
        Combines this and another style.
        """
        return self.extend(other)
    
    def extend(self, *others: Ansi) -> Ansi:
        """
        Adds other ansi styles to this style.
        """
        for other in others:
            self._ansi.extend(other._ansi)
            self._off.extend(other._off)
        return self
    
    def enable_str(self) -> str:
        """
        Returns escape sequence to enable the ansi style.
        """
        return _get_ansi_string(*self._ansi)
    
    def enable(self, file: Optional[TextIO] = None) -> None:
        """
        Enables the ansi style.
        
        Parameters
        ----------
        file
            File to write to. Defaults to standard output.
        """
        file = file or stdout
        file.write(self.enable_str())
    
    def disable_str(self) -> str:
        """
        Returns escape sequence to disable the ansi style.
        """
        return _get_ansi_string(*self._off)
    
    def disable(self, file: Optional[TextIO] = None) -> None:
        """
        Disables the ansi style.
        
        Parameters
        ----------
        file
            File to write to. Defaults to standard output.
        """
        file = file or stdout
        file.write(self.disable_str())

class AnsiNull(Ansi):
    """
    An implementation of an ansi object that contains
    no data.
    
    Examples
    --------
    A simplified example could look like this::
        
        from typing import Optional
        from adorable.ansi import Ansi, AnsiNull
        
        def apply_ansi(text: str, ansi: Optional[Ansi] = None) -> str:
            if ansi is None:
                ansi = AnsiNull()
            
            return ansi(text)
    
    """
    def __init__(self) -> None:
        self._ansi = []
        self._off = []

def _get_ansi_string(*args: Any) -> str:
    """
    Creates an ansi escape sequence by seperating each
    argument with a semicolon (``;``). Every provided
    argument will be turned into a string.
    
    Examples
    --------
    .. repl::
       
       from adorable.ansi import _get_ansi_string
       _get_ansi_string(38, 5, "20")
    """
    return f"\x1b[{';'.join(map(str, args))}m"

