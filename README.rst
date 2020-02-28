SW Checkin
==========

|Build Status| |Test Coverage| |Docker Build Status|
|Docker Image Size|

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

Docker
~~~~~~

-  Docker (tested with 1.12.6)

Setup
-----

Install Hosts Base Package Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   pip install .

Usage
^^^^^

.. code:: bash

   swcheckin -c CONFIRMATION_NUMBER -f FIRST_NAME -l LAST_NAME

Docker Usage
^^^^^^^^^^^^

.. code:: bash

   sudo docker run -it pyro2927/southwestcheckin:latest -c CONFIRMATION_NUMBER -f FIRST_NAME -l LAST_NAME

.. _pip: https://pypi.python.org/pypi/pip

.. |Build Status| image:: https://travis-ci.com/ShoGinn/SouthwestCheckin.svg?branch=master
   :target: https://travis-ci.com/ShoGinn/SouthwestCheckin
.. |Test Coverage| image:: https://coveralls.io/repos/github/ShoGinn/SouthwestCheckin/badge.svg?branch=master
   :target: https://coveralls.io/github/ShoGinn/SouthwestCheckin?branch=master
.. |Docker Build Status| image:: https://img.shields.io/docker/automated/pyro2927/southwestcheckin.svg?style=flat
   :target: https://hub.docker.com/r/pyro2927/southwestcheckin
.. |Docker Image Size| image:: https://images.microbadger.com/badges/image/pyro2927/southwestcheckin.svg
   :target: https://microbadger.com/images/pyro2927/southwestcheckin
.. |SW Heart| image:: https://github.com/ShoGinn/SouthwestCheckin/raw/master/img/heart_1.jpg
