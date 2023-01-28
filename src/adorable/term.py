"""
Utilities for working with the terminal color
system.
"""

from __future__ import annotations

__all__ = ["Terminal"]

from enum import auto, IntEnum
import os
import sys
from typing import Iterable, Optional, TextIO


cache: Optional[Terminal] = None
"""
Cache for supported terminal color system.
"""

class Terminal(IntEnum):
    """
    .. versionchanged:: 0.1.1
        Removed ``BIT4`` value.
    
    Enumeration for specifying the color system
    to use.
    """
    NOCOLOR = auto()
    BIT3 = auto()
    BIT8 = auto()
    BIT24 = auto()
    
    @classmethod
    def get_term(
        cls,
        stream: Optional[Iterable[TextIO]] = None,
        remember: bool = True,
    ) -> Terminal:
        """
        Returns the color system that is supported
        by the end user's terminal.
        
        The color system is checked in the
        following order:
        
        #. Is ``stream`` a valid terminal?
        #. Environment variable ``ADORABLE_COLOR``
        #. Environment variable ``NO_COLOR``
        #. Environment variable ``COLORTERM``
        #. Environment variable ``TERM``
        #. Fallback: :attr:`NOCOLOR`
        
        .. caution::
            
            The result of this function will be saved in
            the ``cache`` variable. The next time this function
            is called, the result in the cache will be returned
            if it is not ``None``. You can clear the cache at any
            time by setting ``cache`` to ``None``::
                
                from adorable import term
                term.cache = None
            
            .. versionadded:: 0.1.1
        
        Parameters
        ----------
        stream
            The streams to query.
            
            If all of the streams provided are invalid
            terminal, ``RuntimeError`` is raised.
            Defaults to ``stdout`` and ``stderr``.
            
            If you want to skip checking for a
            valid terminal you may set this to an empty
            iterable such as ``[]``.
        
        remember
            .. versionadded:: 0.1.1
            
            Caches the result.
        
        Examples
        --------
        .. code-block::
           
           # check if either stdout or stderr is valid
           Terminal.get_term()
           
           # skip terminal check
           Terminal.get_term([])
           
           # only check stdout
           Terminal.get_term([sys.stdout])
        
        Raises
        ------
        ``RuntimeError``
            Standard output is not a valid terminal.
        """
        global cache
        
        if cache is not None:
            return cache
        
        if stream is None:
            stream = [sys.stdout, sys.stderr]
        
        if any(
            not (st and st.isatty())
            for st in stream
        ):
            raise RuntimeError("standard output is not a valid terminal")
        
        ac = os.getenv("ADORABLE_COLOR")
        if ac == "nocolor":
            res = cls.NOCOLOR
        
        elif ac == "3bit":
            res = cls.BIT3
        
        elif ac == "8bit":
            res = cls.BIT8
        
        elif ac == "24bit":
            res = cls.BIT24
        
        elif int(os.getenv("NO_COLOR", "0")):
            res = cls.NOCOLOR
        
        elif os.getenv("COLORTERM", "0") in ["truecolor", "24bit"]:
            res = cls.BIT24
        
        elif (
            os.getenv("TERM", "")
                .removeprefix("xterm-")
                .removesuffix("color")
        ) == "256":
            res = cls.BIT8
        
        else:
            res = cls.NOCOLOR
        
        if remember:
            cache = res
        return res
    
    def is_supported(self) -> bool:
        """
        .. versionadded:: 0.1.1
        
        Checks if the color system is supported
        by the terminal.
        """
        return self.__class__.get_term() >= self

