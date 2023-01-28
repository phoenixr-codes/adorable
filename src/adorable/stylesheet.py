"""
.. versionadded:: 0.1.0

Load ansi objects from a stylesheet file in
your project.
"""

# TODO: What if another library imports a library
#       that has a stylesheet? Maybe add check for
#       a package or some kind of labeling.

from __future__ import annotations

from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Union

from .ansi import Ansi


_globals: dict[str, Ansi] = dict()
"""Loaded style objects."""

_loaded: set[ModuleType] = set()
"""Loaded stylesheet modules."""


def remove_style(name: str) -> None:
    """
    Removes a style.
    
    Parameters
    ----------
    name
        The name of the style object.
    """
    del _globals[name]

def remove_all() -> None:
    """
    Removes all styles.
    """
    _globals.clear()

def export(**styles: Ansi) -> None:
    """
    Loads all objects.
    
    This usually called from a stylesheet module
    in order to make the ansi objects globally
    available.
    
    .. admonition:: Preference
       :class: tip
       
       This method is preferred over :func:`load_stylesheet`.
    
    .. caution::
       
       This will not filter out ansi objects but
       rather raise a ``TypeError``.
    
    Parameters
    ----------
    styles
        Ansi objects and an associated name.
    """
    for name, ansi in styles.items():
        if not isinstance(ansi, Ansi):
            raise TypeError(
                f"{name!r} ({ansi!r}) is not an "
                f"instance of {Ansi!r}"
            )
        _globals[name] = ansi

@cache
def load_stylesheet(
    source: Union[Path, ModuleType, str, None] = None,
    force: bool = False
) -> None:
    """
    Loads a stylesheet.
    
    .. admonition:: Preference
       :class: tip
       
       :func:`export` is preferred over this method.
    
    
    .. tip::
       
       The safest method is to import the stylesheet
       module and use it as the ``source`` argument.
       
       Alternatively the :func:`export` function may
       be used which is also safe.
    
    Parameters
    ----------
    source
        When a ``Path`` or ``str`` is given, it
        will load all style objects from that file
        by importing it. If the path is a directory
        it will try to find a file named ``_stylesheet.py``
        or ``stylesheet.py`` (in that order) and use
        it as a stylesheet.
        
        This function will attempt to load all style
        objects mentioned in the ``__all__`` variable.
        If that variable is not defined, it will filter
        all style objects defined in the module.
        
        .. caution::
           
           This will include built-in style objects such
           as ones imported from :mod:`adorable.style`.
        
        When no source is provided (default) the function
        will attempt to search the stylesheet file by
        querying the module that called this function.
        Then it will use the directory
        where the caller's source file is as the path. After that
        the same process takes place as when defining source
        with a ``Path``.
    
    force
        This function caches already loaded stylesheets -
        no matter what value the ``source`` parameter
        previously had. Forcing a rerun may be done by
        setting this to ``True``.
    
    Raises
    ------
    ``RuntimeError``
        Could not find source file.
    """
    import importlib.util as imp
    import inspect
    import sys
    
    from . import filter_ansi
    
    if source is None:
        callers = inspect.stack()
        for caller in reversed(callers):
            filename = caller.filename
            
            if filename == "<string>":
                continue
            
            source = Path(filename)
            break
        
        else:
            raise RuntimeError("cannot find source file")
        
        parent = source.parent
        
        for match in ["_stylesheet.py", "stylesheet.py"]:
            source = parent / match
            if source.exists():
                break
        
        else:
            raise RuntimeError("cannot find stylesheet")
    
    if isinstance(source, str):
        source = Path(source)
    
    if isinstance(source, Path):
        spec = imp.spec_from_file_location("_stylesheet_", str(source))
        if spec is None:
            raise RuntimeError("cannot load stylesheet")
        
        source = imp.module_from_spec(spec)
        if spec.loader is None:
            raise RuntimeError("cannot load stylesheet")
        
        sys.modules[source.__name__] = source
        spec.loader.exec_module(source)
    
    try:
        all_ = source.__all__
    except AttributeError:
        objects = source.__dict__
    else:
        objects = dict()
        for name in all_:
            objects[name] = source.__dict__[name]
    
    export(**filter_ansi(objects))
    _loaded.add(source)

