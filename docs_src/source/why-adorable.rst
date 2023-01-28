****************
Why Use adorable
****************

There are many popular libraries like
`rich <https://github.com/Textualize/rich>`_ and
`termcolor <https://github.com/hfeeki/termcolor>`_
which allow you to style strings with ansi sequences.
But there are a few differences between this library
and others.

===============================
What is special about adorable?
===============================

adorable is very object orientated. All ansi
styles are objects that provide methods to
manipulate the color and apply it in different
ways

You can therefore share that style object across
your entire project.

End users also have control on the picked color
system in case it was wrongly guessed by setting
an environment variable.


===========================
When should I use adorable?
===========================

adorable is not recommended for quick debugging.
The above mentioned
`rich <https://github.com/Textualize/rich>`_
library provides syntax with less writing is
generally good for debugging.

adorable is suitable for pretty much any other
use case.

