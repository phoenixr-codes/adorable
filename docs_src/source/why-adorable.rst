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


===============
No dependencies
===============

The adorable library has not a single dependency!
This is not something that makes the library any
better - it's just a flex |:sunglasses:|.

.. note::
   
   This is likely going to be changed in the future. The
   markup language VMML will be used. While VMML
   is created exclusively for this library
   it may be useful for other projects and is therefore
   kept as a separate library.


===========================
When should I use adorable?
===========================

adorable is not recommended for quick debugging.
The above mentioned
`rich <https://github.com/Textualize/rich>`_
library provides syntax with less writing good
for debugging.

adorable is suitable for pretty much any other
use case.

