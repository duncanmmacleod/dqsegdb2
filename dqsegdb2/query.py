# DQSEGDB2
# Copyright (C) 2018  Duncan Macleod
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Query methods for DQSEGDB2
"""

from __future__ import absolute_import

import os

from . import api
from .http import request_json

DEFAULT_SEGMENT_SERVER = os.environ.setdefault(
    'DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')


def query_names(ifo, host=DEFAULT_SEGMENT_SERVER, versioned=False):
    """Query for all defined flags for the given ``ifo``

    Parameters
    ----------
    ifo : `str`
        the interferometer prefix for which to query

    host : `str`, optional
        the URL of the database, defaults to `DEFAULT_SEGMENT_SERVER`

    Returns
    -------
    flags : `set`
        the set of all define flag names in the format ``{ifo}:{name}``

    Examples
    --------
    >>> from dqsegdb2.query import query_names
    >>> query_names('G1')
    """
    url = api.name_query_url(host, ifo)
    names = request_json(url)['results']
    return {'{0}:{1}'.format(ifo, name) for name in names}


def query_versions(flag, host=DEFAULT_SEGMENT_SERVER):
    """Query for defined versions for the given flag

    Parameters
    ----------
    flag : `str`
        the name for which to query

    host : `str`, optional
        the URL of the database, defaults to `DEFAULT_SEGMENT_SERVER`

    Returns
    -------
    versions : `list` of `int`
        the list of defined versions for the given flag

    Examples
    --------
    >>> from dqsegdb2.query import query_names
    >>> query_names('G1:GEO-SCIENCE')
    [1, 2, 3]
    """
    ifo, name = flag.split(':', 1)
    url = api.version_query_url(host, ifo, name)
    return sorted(request_json(url)['version'])


def query_segments(flag, start, end, host=DEFAULT_SEGMENT_SERVER):
    """Query for segments for the given flag in a ``[start, stop)`` interval

    Parameters
    ----------
    flag : `str`
        the name for which to query

    start : `int`
        the GPS start time

    end : `int`
        the GPS end time

    host : `str`, optional
        the URL of the database, defaults to `DEFAULT_SEGMENT_SERVER`

    Returns
    -------
    segmentdict : `dict`
        a `dict` of flag information with the following keys

        - ``'ifo'`` - the interferometer prefix
        - ``'name'`` - the flag name
        - ``'version'`` - the flag version
        - ``'known'`` - the list of known segments
        - ``'active'`` - the list of active segments
        - ``'metadata'`` - a `dict` of flag information

    Examples
    --------
    >>> from dqsegdb2.query import query_segments
    >>> query_segments('G1:GEO-SCIENCE:1', 1000000000, 1000001000)
    """
    ifo, name, version = flag.split(':', 2)
    url = api.segment_query_url(host, ifo, name, version, start=start, end=end)
    return request_json(url)
