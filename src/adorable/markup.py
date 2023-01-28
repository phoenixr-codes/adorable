"""
Markup utilities for adorable.

.. warning::
   
   Using XML for markup is likely going to be replaced in the
   future by a more friendly optimized markup language.

"""

from __future__ import annotations

__all__ = ["insert", "markup_xml"]

import html
import string
from typing import Any, Generator, Optional
import warnings
import xml.etree.ElementTree as ET

from .ansi import Ansi, AnsiNull
from .stylesheet import _globals


class XMLEscapeFormatter(string.Formatter):
    """
    If conversion specifier ``e`` (escape) is
    given or omitted, escape xml contents of
    the value. If ``r`` (raw) is given, insert
    without escaping.
    """
    
    @staticmethod
    def convert_field(value: str, conversion: Optional[str]) -> str:
        if conversion in ["e", None]:
            return html.escape(value)
        
        elif conversion == "r":
            return value
        
        raise ValueError(f"unknown conversion specifier {conversion}")

def get_ansi_from_tag(name: str, style: dict[str, Ansi] = {}) -> Ansi:
    """
    Returns the ansi object in the palette by the
    name. If the ansi object is not present, ``ValueError``
    is raised.
    
    Parameters
    ----------
    name
        The key of the ansi object.
    
    style
        The palette.
    
    Raises
    ------
    ValueError
        Key not present.
    
    Returns
    -------
    The matching ansi object.
    """
    if name in style:
        return style[name]
    
    raise ValueError(f"invalid tag {name!r}")

def style_element(
    element: ET.Element,
    style: dict[str, Ansi] = {},
    _previous_ansi: Ansi = AnsiNull(),
) -> Generator[str, None, None]:
    """
    Yields strings by styling them via their elemt names.
    
    Parameters
    ----------
    element
        The element to style.
    
    style
        The palette.
    
    Other Parameters
    ----------------
    _previous_ansi
        The ansi object used in the last iteration.
    
    Yields
    ------
    Text snippets styled.
    """
    for child in element:
        tag = child.tag
        ansi = get_ansi_from_tag(tag, style = style)
        
        yield ansi.enable_str() + (child.text or "")
        
        yield from style_element(
            child,
            style = style,
            _previous_ansi = ansi
        )
        
        yield (
            ansi.disable_str() +
            _previous_ansi.enable_str() +
            (child.tail or "")
        )

def insert(
    *args: Any,
    **kwargs: Any,
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """
    Returns ``args`` and ``kwargs`` as is.
    """
    return args, kwargs


def markup_xml(
    string: str,
    style: Optional[dict[str, Ansi]] = None,
    insert: Optional[tuple[tuple[Any, ...], dict[str, Any]]] = None
) -> str:
    """
    .. warning::
       
       Using XML for markup is likely going to be replaced in the
       future by a more friendly optimized markup language.
    
    Use XML to style a string. In order to
    format the string, provide the variables
    directly to this function. All variables
    will be escaped automatically unless ``!r``
    is added at the end. You can also use ``!e``
    to explicitly specify that the variable
    has to be escaped.
    
    Parameters
    ----------
    string
        The markup text.
    
    style
        Mapping of keys and the style to use.
        You may want to use
        :func:`adorable.filter_ansi`.
    
    insert
        Insert variables to string.
        
        .. seealso::
           :func:`insert`
    
    Returns
    -------
    Styled text.
    """
    warnings.warn(
        "XML markup is likely going to be replaced by "
        "another markup language in the future",
        PendingDeprecationWarning,
    )
    
    if style is None:
        style = {}
    
    if insert is None:
        insert = ((), {})
    
    style |= _globals
    text = XMLEscapeFormatter().format(string, *insert[0], **insert[1])
    
    root = ET.fromstring(f"<root>{text}</root>")
    text = root.text or ""
    text += "".join(style_element(root, style = style))
    
    return html.unescape(text)
