*********
Changelog
*********

.. note::
   
   Only releases **after** 0.0.1b2 are recorded here.

========================
0.1.3.post1 (28-01-2023)
========================

-------
Changed
-------

* |:wastebasket:| Removed unused imports.
* |:sparkles:| Reformatted source code style.


==================
0.1.3 (21-01-2023)
==================

-------
Changed
-------

* |:hammer:| Increased quality of detection
  for color system.


==================
0.1.2 (21-01-2023)
==================

-----
Added
-----

* |:new:| Added function :func:`adorable.use`.


-------
Changed
-------

* |:hammer:| Fixed an issue where multiple 8bit
  colors could not be created.

* |:hammer:| Calling ``str()`` on a
  :class:`adorable.color.Color`` object will now
  actually throw a warning and return an empty
  string when the color is not initialized.

==================
0.1.1 (01-12-2022)
==================

-----
Added
-----

* |:new:| Added method
  :meth:`adorable.term.Terminal.is_supported`.

* |:new:| Added method
  :meth:`adorable.color.Color.is_supported`.

* |:new:| Added ``|`` operator for class
  :class:`adorable.color.Color`.


-------
Changed
-------

* |:new:| :meth:`adorable.term.Terminal.get_term`
  now caches the result.

* |:wastebasket:| :class:`adorable.color.Color` now
  has the default ``__repr__`` method.


-------
Removed
-------

* |:wastebasket:| Removed ``BIT4`` value of
  enum :class:`adorable.term.Terminal`.


==================
0.1.0 (29-10-2022)
==================

-----
Added
-----

* |:new:| Added stylesheet module
  (:ref:`stylesheet`, :mod:`adorable.stylesheet`).
* |:new:| Function :func:`adorable.markup.markup_xml`
  now takes styles configured via a stylesheet
  into account.
* |:new:| Added function
  :func:`adorable.color.empty`.
* |:new:| Added method
  :meth:`adorable.color.Color.is_initialized`.
* |:hammer:| Class :class:`adorable.ansi.Ansi` now supports
  ``+`` and ``+=`` operations too.


-----
Fixed
-----

* |:hammer:| Corrected error messages.
* |:hammer:| Calling
  :meth:`adorable.color.Color.enable_str` and
  :meth:`adorable.color.Color.disable_str` now
  raise Exceptions when color is not initialized.


-------
Changed
-------

* |:new:| :class:`adorable.color.Color` now has
  a more descriptive explanation on how to use
  the ``__init__`` method.


==================
0.0.1 (26-10-2022)
==================

-----
Added
-----

* |:tada:| First stable release.


-------
Changed
-------

* |:hammer:| :func:`adorable.markup.markup_xml` now
  raises ``PendingDeprecationWarning`` again like in
  version 0.0.1rc1 because there currently is no
  alternative markup syntax. **Keep in mind however**
  that this will be deprecated in a future release.


=====================
0.0.1rc2 (25-10-2022)
=====================

-----
Fixed
-----

* |:bug:| Fixed a bug where the short HEX notation
  would sometimes return an incorrect RGB value.


-------
Changed
-------

* |:hammer:| :func:`adorable.markup.markup_xml` now
  raises ``DeprecationWarning`` instead of
  ``PendingDeprecationWarning``.
* |:hammer:| Improved error message when an invalid
  HEX value is provided in
  :meth:`adorable.color.Color.from_hex`.


=====================
0.0.1rc1 (25-10-2022)
=====================

-----
Added
-----

* |:tada:| First release candidate.


.. note for future
   
   The structure should look like this:
   
   
   0.0.2 (2022-07-07)
   ==================
   * |:bug:| Fixed a bug where something bad happens
     (:issue:`174057`).
   * |:new:| Added an awesome feature.
   
   0.0.1 (2022-06-06)
   ==================
   
   * |:tada:| First release
   
