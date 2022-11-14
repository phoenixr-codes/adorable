*******************************
Caution When Using Ansi Strings
*******************************

.. important::
   
   The issues mentioned below are not exclusive
   to adorable. Other ansi related libraries will
   serve the same or similar results.

adorable will generate strings that are likely
to contain ansi sequences. The sequences are
invisible when printing. They contain information
about what style to use or reset etc. Because
these sequences are escaped characters, python
(and other languages as well) will interpret these
as characters.

.. repl::
   
   import adorable
   len(adorable.paint("Hello", style = adorable.BOLD))

Keep this in mind, when working with ansi strings.


==============================================
Using :pylib:`textwrap`  with ansi strings
==============================================

The textwrap library uses the built-in :pyfn:`len`
function among other things to return wrapped
text. So using it with strings that contains
ansi sequences will return not expected output.

The library :piplib:`ansiwrap` will only work
for very basic colors and is therefore discouraged.
However we might work on a project like  :pylib:`textwrap`
in the future that will work for all ansi sequences.


======================================
Getting the visible length of a string
======================================

As shown above, the built-in :pyfn:`len` function
will not take into account of invisible ansi
sequences.

The adorable library provides a general regex
pattern, that will match pretty much all ansi
sequences. With that, you can create your own
implementation of :pyfn:`len`:

.. repl::
    
   from typing import Any
   from adorable import ANSI_REGEX
   
   def visible_len(x: Any, /) -> int:
       if isinstance(x, str):
           x = ANSI_REGEX.sub("", x)
       return len(x)
   
   import adorable
   visible_len(adorable.paint("Hello", style = adorable.BOLD))


