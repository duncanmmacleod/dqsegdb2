[![Linux Build Status](https://img.shields.io/circleci/project/github/duncanmmacleod/dqsegdb2/master.svg)](https://circleci.com/gh/duncanmmacleod/dqsegdb2)
[![Documentation Status](https://readthedocs.org/projects/dqsegdb2/badge/?version=latest)](https://dqsegdb2.readthedocs.io/en/latest/?badge=latest)
[![Coverage status](https://codecov.io/gh/duncanmmacleod/dqsegdb2/branch/master/graph/badge.svg)](https://codecov.io/gh/duncanmmacleod/dqsegdb2)
[![License](https://img.shields.io/pypi/l/dqsegdb2.svg)](https://choosealicense.com/licenses/gpl-3.0/)
[![DOI](https://zenodo.org/badge/136390328.svg)](https://zenodo.org/badge/latestdoi/136390328)

DQSEGDB2 is a simplified Python implementation of the DQSEGDB API as defined in
LIGO-T1300625.

This package only provides a query interface for `GET` requests, any users
wishing to make `POST` requests should refer to the official `dqsegdb` Python
client available from https://github.com/ligovirgo/dqsegdb/.

# Basic Usage

```python
>>> from dqsegdb2.query import query_segments
>>> print(query_segments('G1:GEO-SCIENCE:1', 1000000000, 1000001000))
```
