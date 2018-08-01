.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>

########
DQSEGDB2
########

.. image:: https://travis-ci.com/duncanmmacleod/dqsegdb2.svg?branch=master
   :target: https://travis-ci.com/duncanmmacleod/dqsegdb2
.. image:: https://coveralls.io/repos/github/duncanmmacleod/dqsegdb2/badge.svg
   :target: https://coveralls.io/github/duncanmmacleod/dqsegdb2

`dqsegdb2` is a simplified Python implementation of the DQSEGDB API as
defined in `LIGO-T1300625 <https://dcc.ligo.org/LIGO-T1300625/public>`__.

This package only provides a query interface for GET requests,
any users wishing to make POST requests should refer to the official
dqsegdb Python client available from https://pypi.org/project/dqsegdb/.

============
Installation
============

.. code-block:: bash

   $ python -m pip install dqsegdb2

=====================
Package documentation
=====================

.. toctree::

   api
   http
   query

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
