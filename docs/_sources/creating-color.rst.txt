***************
Creating Colors
***************

.. code-block::
   
   from adorable import color

.. admonition:: Preference
   :class: tip
   
   Using web color names for creating colors is
   preferred because you can directly see what color
   is used. Exceptions can be made for specific
   brand colors or a pixel color of an image for example.
   
   The reason for this is, that the color that will
   be printed will not exactly have the same color
   as the one provided.


===
RGB
===

.. code-block::
    
   color.from_rgb((50, 100, 200))
   color.from_rgb((.2, .4, .8))


===
HEX
===

.. code-block::
   
   color.from_hex(0xC0FFEE)
   color.from_hex("#C0FFEE")
   color.from_hex("c0ffEE")
   
   color.from_hex(0xFAE) # same as 0xFFAAEE
   color.from_hex("#faE")
   color.from_hex("FAE")


=========
Web Color
=========

.. code-block::
   
   color.from_name("red")
   color.from_name("grEeN")

.. seealso::
   
   For a list of available names, look at
   `this list <https://www.w3schools.com/colors/colors_names.asp>`_.


=====
Other
=====

If you are using other color coordinate systems
than those mentioned above, you may want to use
the built-in :pylib:`colorsys` library.

.. code-block::
   
   from colorsys import *
   
   color.from_rgb(yiq_to_rgb(0.2, 0.4, 0.8))
   color.from_rgb(hls_to_rgb(0.2, 0.4, 0.8))
   color.from_rgb(hsv_to_rgb(0.2, 0.4, 0.8))


