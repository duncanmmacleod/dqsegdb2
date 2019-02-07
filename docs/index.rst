.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>

########
DQSEGDB2
########

.. image:: https://travis-ci.com/duncanmmacleod/dqsegdb2.svg?branch=master
   :target: https://travis-ci.com/duncanmmacleod/dqsegdb2
.. image:: https://coveralls.io/repos/github/duncanmmacleod/dqsegdb2/badge.svg
   :target: https://coveralls.io/github/duncanmmacleod/dqsegdb2
.. image:: https://img.shields.io/pypi/l/dqsegdb2.svg
   :target: https://choosealicense.com/licenses/gpl-3.0/
.. image:: https://zenodo.org/badge/136390328.svg
   :target: https://zenodo.org/badge/latestdoi/136390328

`dqsegdb2` is a simplified Python implementation of the DQSEGDB API as
defined in `LIGO-T1300625 <https://dcc.ligo.org/LIGO-T1300625/public>`__.

.. note::

    This package does not provide a complete implementation of the API
    as defined in LIGO-T1300625, and only supports ``GET`` requests for
    a subset of information available from a DQSEGDB server.
    Any users wishing to make ``POST`` requests should refer to the official
    DQSEGDB Python client available from https://pypi.org/project/dqsegdb/.

    However, `dqsegdb2` is light,  with minimal dependencies, so might be
    useful for people only interested in querying for segment information.

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
