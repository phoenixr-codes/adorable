"""
Utilities for working with the terminal color
system.
"""

from __future__ import annotations

from enum import auto, IntEnum
import os
import sys
from typing import Iterable, Optional, TextIO, Union

class Terminal(IntEnum):
    """
    Enumeration for specifying the color system
    to use.
    """
    NOCOLOR = auto()
    BIT3 = auto()
    BIT4 = auto()
    BIT8 = auto()
    BIT24 = auto()
    
    @classmethod
    def get_term(cls, stream: Optional[Iterable[TextIO]] = None) -> Terminal:
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
        
        Parameters
        ----------
        stream
            The stream to query.
            
            If all of the streams provided are invalid
            terminal, ``RuntimeError`` is raised.
            Defaults to ``stdout`` and ``stderr``.
            
            If you want to skip checking for a
            valid terminal you may set this to an empty
            iterable such as ``[]``.
        
        Examples
        --------
        .. code-block::
           
           Terminal.get_term()             # check if either stdout or stderr is valid
           Terminal.get_term([])           # skip terminal check
           Terminal.get_term([sys.stdout]) # only check stdout
        
        Raises
        ------
        ``RuntimeError``
            Standard output is not a valid terminal.
        """
        if stream is None:
            stream = [sys.stdout, sys.stderr]
        
        if any(
            not (st and st.isatty())
            for st in stream
        ):
            raise RuntimeError("standard output is not a valid terminal")
        
        ac = os.getenv("ADORABLE_COLOR")
        if ac == "nocolor":
            return cls.NOCOLOR
        
        if ac == "3bit":
            return cls.BIT3
        
        if ac == "8bit":
            return cls.BIT8
        
        if ac == "24bit":
            return cls.BIT24
        
        if int(os.getenv("NO_COLOR", "0")):
            return cls.NOCOLOR
        
        if os.getenv("COLORTERM", "0") in ["truecolor", "24bit"]:
            return cls.BIT24
        
        t = os.getenv("TERM", "").removeprefix("xterm-")
        if t == "256":
            return cls.BIT8
        
        return cls.NOCOLOR