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

"""API URL implementation for DQSEGDB
"""


def _query(**kwargs):
    """Return a URL query string based on some key, value pairs
    """
    return '&'.join('{0}={1}'.format(key, value) for
                    key, value in sorted(kwargs.items()))


def segment_query_url(host, ifo, name, version, start=None, end=None,
                      include='metadata,known,active'):
    """Returns the URL to use in querying for segments
    """
    return '{host}/dq/{ifo}/{name}/{version}?{query}'.format(
        host=host, ifo=ifo, name=name, version=version,
        query=_query(s=start, e=end, include=include))


def version_query_url(host, ifo, name):
    """Returns the URL to use in querying for flag versions
    """
    return '{host}/dq/{ifo}/{name}'.format(host=host, ifo=ifo, name=name)


def name_query_url(host, ifo):
    """Returns the URL to use in querying for flag names
    """
    return '{host}/dq/{ifo}'.format(host=host, ifo=ifo)
