************
Color System
************

=====================
Specific Color System
=====================

Terminals support different kinds of ansi effects.
adorable tries to select the one that fits the
currently used terminal. So when creating colors
without specifying a specific color system, text
may appears different on other terminals. To avoid
this you can specify a specific color system to use.

The best one is the one that is supported by most
terminals. However it does not provide a large range
of colors::
    
    from adorable import Color3bit
    
    RED = Color3bit.from_name("red")

Here we use ``Color3bit`` instead of ``color``.
Note that ``Color3bit`` is a class in the ``color``
module.

Alternatively we can use fallback values::
    
    from adorable import color
    
    term = color.get_color()
    if term == color.Color3bit:
        WARN = color.from_name("red").bg
    
    else:
        WARN = color.from_name("orange").bg

There are many ways of handling supported colors
due to the object orientated syntax!


====================================
Migrating to a specific color system
====================================

Because the ``color`` library provides the same
functions as its classes you can edit the import
if you have used the ``color`` library in your
module::
    
    # from
    from adorable import color
    
    # to
    from adorable.color import Color3bit as color
    
    
    color.from_hex(0xC0FFEE).fg # still works


=====================================
Manipulating Third-party Color System
=====================================

It is possible to manually globally set a
color system for your terminal by using an
environment variable:

.. tab:: POSIX
   
   .. code-block:: bash
      
      export ADORABLE_COLOR="xyz"

.. tab:: Windows
   
   .. code-block:: console
      
      set ADORABLE_COLOR="xyz"
      setx ADORABLE_COLOR="xyz"

where ``xyz`` is one of:

* ``nocolor``
* ``3bit``
* ``8bit``
* ``24bit``

Alternatively you may use the :func:`adorable.use`
function. It works similar to setting the environment
variable::
    
    import adorable
    adorable.use("BIT3") # or: "NOCOLOR", "BIT8", "BIT24"

