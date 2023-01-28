****************
Styling A String
****************

Styling strings is fundamental when using adorable
and there are multiple ways of doing so.

============================
``paint()`` and ``printc()``
============================

One method is using the ``paint`` function (and
the equivalent version ``printc`` in order to
directly print it).

.. code-block::
   
   import sys
   from adorable import color, paint, printc
   
   RED = color.from_name("red").fg
   YELLOW = color.from_name("yellow").bg

*The snippets below have the same result.*

.. autofunction:: adorable.ansi.paint
   :noindex:

.. code-block::
   
   print(paint("Hello, World!", style = RED + YELLOW), file = sys.stderr)

.. autofunction:: adorable.ansi.printc
   :noindex:

.. code-block::
   
   printc("Hello, World!", style = RED + YELLOW, file = sys.stderr)


=======================
Calling the ansi object
=======================

Another method is to call the ansi object like
it would be a function.

.. code-block::
   
   from adorable import color
   
   RED = color.from_name("red").fg
   print(RED("Hello, World!"))


.. _using-markup:

============
Using markup
============

It is often necessary to only style specific
parts of a string. Instead of concatenating these
parts, markup can be used.

.. code-block::
   
   from adorable import color, filter_ansi, markup_xml
   
   RED = color.from_name("red").fg
   
   print(markup_xml("Hello [colorful](RED) World", filter_ansi(locals())))

The above example uses the :func:`adorable.filter_ansi` method,
however a :ref:`stylesheet` should be used, especially
for large projects.
