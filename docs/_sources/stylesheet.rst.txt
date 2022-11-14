.. _stylesheet:

***********************
Using a stylesheet file
***********************

As your project grows you may need to use multiple
style objects across multiple modules.

.. Put more information here.

.. tab:: stylesheet.py
   
   .. code-block:: python
      
      from adorable import color
      from adorable.stylesheet import export
      
      export(
          RED = color.from_name("red").fg,
          GREEN = color.from_name("green").fg,
          BLUE = color.from_name("blue").fg,
      )

.. tab:: main.py
   
   .. code-block:: python
      
      import adorable
      
      #adorable.printf("[Hello](RED), World!")
      adorable.markup_xml("<RED>Hello</RED>, World!")

Another method is to let adorable extract all
ansi objects from a module that it optionally
has to find. However using this method is not
recommended, because it "secretly" loads the
module and if no source is provided, access
the file and tries to find the stylesheet which
might fail.
