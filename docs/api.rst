API documentation
=================

The following API documentation was automatically generated from the source
code of `swcheckin` |release|:

.. contents::
   :local:

A note about backwards compatibility
------------------------------------

The `swcheckin` package started out as a single :mod:`swcheckin.checkin`
module. Eventually this module grew to a size that necessitated splitting up
the code into multiple modules (see e.g. :mod:`~swcheckin.__main__`,
:mod:`~swcheckin.southwest`).

While moving functionality around like this my goal is to always preserve
backwards compatibility. For example if a function is moved to a submodule an
import of that function is added in the main module so that backwards
compatibility with previously written import statements is preserved.

If backwards compatibility of documented functionality has to be broken then
the major version number will be bumped. So if you're using the `swcheckin`
package in your project, make sure to at least pin the major version number in
order to avoid unexpected surprises.

:mod:`swcheckin.__main__`
-------------------------

.. automodule:: swcheckin.__main__
   :members:

:mod:`swcheckin.checkin`
-------------------------

.. automodule:: swcheckin.checkin
   :members:

:mod:`swcheckin.config`
----------------------------

.. automodule:: swcheckin.config
   :members:

:mod:`swcheckin.openflights`
----------------------------

.. automodule:: swcheckin.openflights
   :members:

:mod:`swcheckin.southwest`
--------------------------

.. automodule:: swcheckin.southwest
   :members:
