**********
Quickstart
**********

First, initialize a new color and then use it
along with text to print it.

.. code-block::
   
   import adorable
   from adorable import color
   
   RED = color.from_name("red").fg
   adorable.printc("Hello World", style = RED)

.. colored::
   
   [Hello World](red)

If this does not print text in color in the terminal,
feel free to
`open an issues on github <https://github.com/phoenixr-codes/adorable/issues/new?assignees=&labels=&template=missing-terminal-support.md&title=>`_
so it can be fixed. The reason for this might be that
your terminal is not supported.You can however
`force applying colors </color-system.html>`_.

.. code-block::
   
   import adorable
   from adorable import color
   
   BOLD = adorable.BOLD
   BLUE = color.from_name("blue").fg
   
   print(f"Hello {BOLD:wonderful} {BLUE:World}")

.. colored::
   
   Hello [wonderful](bold) [World](blue)
