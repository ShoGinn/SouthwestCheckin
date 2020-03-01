|PyPI|

.. DO-NOT-REMOVE-docs-badges-END

|Build Status| |Test Coverage| |RTD|

SW Checkin
==========
.. DO-NOT-REMOVE-docs-intro-START

|SW Heart|

This python script checks your flight reservation with Southwest and
then checks you in at exactly 24 hours before your flight. Queue up the
script and it will ``sleep`` until the earliest possible check-in time.

Requirements
------------

This script can either be ran directly on your host or within Docker.

Host
~~~~

-  Python3 (2.0 has hit twilight)
-  `pip`_

Setup
-----

Install Hosts Base Package Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage
^^^^^

.. code:: bash

   pip install swcheckin
   swcheckin -c CONFIRMATION_NUMBER -f FIRST_NAME -l LAST_NAME

Docker Usage
^^^^^^^^^^^^

See the `swcheckin-docker`_ build for the docker instructions


.. _swcheckin-docker: https://github.com/ShoGinn/swcheckin-docker/
.. _pip: https://pypi.python.org/pypi/pip

.. |Build Status| image:: https://img.shields.io/travis/com/ShoGinn/SouthwestCheckin.svg?label=Linux%20builds&logo=travis&logoColor=white
   :target: https://travis-ci.com/ShoGinn/SouthwestCheckin
   :alt: Travis buildstatus
.. |Test Coverage| image:: https://coveralls.io/repos/github/ShoGinn/SouthwestCheckin/badge.svg?branch=master
   :target: https://coveralls.io/github/ShoGinn/SouthwestCheckin?branch=master
   :alt: Coveralls Test Coverage
.. |SW Heart| image:: https://github.com/ShoGinn/SouthwestCheckin/raw/master/img/heart_1.jpg
   :alt: Sw Heart Image
.. |PyPI| image:: https://img.shields.io/pypi/v/swcheckin.svg?logo=Python&logoColor=white
   :target: https://pypi.org/project/swcheckin
   :alt: swcheckin @ PyPI
.. |RTD| image:: https://img.shields.io/readthedocs/swcheckin/latest.svg?logo=Read%20The%20Docs&logoColor=white
   :target: https://swcheckin.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

