|PyPI| |LIC|

.. DO-NOT-REMOVE-docs-badges-END

|Build Status| |RTD|

|Test Coverage| |CCMG|

SWcheckin
==========
.. DO-NOT-REMOVE-docs-intro-START

SWcheckin is a python script that checks your flight reservation with
Southwest.

Then checks you in at exactly 24 hours before your flight.

Queue up the script and it will ``sleep`` until the earliest possible
check-in time.

Installation
------------
Use the package manager `pip`_ to install swcheckin.

.. code:: sh

  $ pip install swcheckin

Usage
-----

``$ swcheckin -h``

--version                       Show the version and exit.
-c, --conf-num TEXT             Your SouthWest Confirmation Number  [required]
-f, --first, --first-name TEXT  The First name of the traveller  [required]
-l, --last, --last-name TEXT    The Last name of the traveller  [required]
-v, --verbose                   Shows debugging information
-h, --halp, --help              Show this message and exit.

Docker Usage
------------

See the `swcheckin-docker`_ build for the docker instructions

.. _swcheckin-docker: https://github.com/ShoGinn/swcheckin-docker/
.. _pip: https://pypi.python.org/pypi/pip

.. |Build Status| image:: https://img.shields.io/travis/com/ShoGinn/SouthwestCheckin.svg?label=Linux%20builds&logo=travis&logoColor=white
   :target: https://travis-ci.com/ShoGinn/SouthwestCheckin
   :alt: Travis buildstatus
.. |Test Coverage| image:: https://coveralls.io/repos/github/ShoGinn/SouthwestCheckin/badge.svg?branch=master
   :target: https://coveralls.io/github/ShoGinn/SouthwestCheckin?branch=master
   :alt: Coveralls Test Coverage
.. |PyPI| image:: https://img.shields.io/pypi/v/swcheckin.svg?logo=Python&logoColor=white
   :target: https://pypi.org/project/swcheckin
   :alt: swcheckin @ PyPI
.. |RTD| image:: https://img.shields.io/readthedocs/swcheckin/latest.svg?logo=Read%20The%20Docs&logoColor=white
   :target: https://swcheckin.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |CCMG| image:: https://img.shields.io/codeclimate/maintainability/ShoGinn/SouthwestCheckin
   :target: https://codeclimate.com/github/ShoGinn/SouthwestCheckin
   :alt: Code Climate maintainability Grade
.. |LIC| image:: https://img.shields.io/github/license/ShoGinn/SouthwestCheckin?style=flat
   :target: https://choosealicense.com/licenses/gpl-3.0/
   :alt: GitHub
