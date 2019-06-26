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

"""Tests for :mod:`dqsegdb.api`
"""

import json

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from .. import query

KNOWN = [(0, 10)]
ACTIVE = [(1, 3), (3, 4), (6, 10)]
QUERY_SEGMENT = (2, 8)
KNOWN_COALESCED = [(2, 8)]
ACTIVE_COALESCED = [(2, 4), (6, 8)]


@mock.patch('dqsegdb2.query.request_json')
def test_query_names(request_json):
    names = ['name1', 'name2', 'name2']
    request_json.return_value = {'results': names}
    assert query.query_names('X1') == set(map('X1:{0}'.format, names))


@mock.patch('dqsegdb2.query.request_json')
def test_query_versions(request_json):
    versions = [1, 2, 3, 4]
    request_json.return_value = {'version': versions}
    assert query.query_versions('X1:test') == sorted(versions)


@pytest.mark.parametrize('flag, coalesce, known, active', [
    ("X1:TEST:1", False, KNOWN, ACTIVE),
    ("X1:TEST:1", True, KNOWN_COALESCED, ACTIVE_COALESCED),
    ("X1:TEST:*", False, KNOWN + KNOWN, ACTIVE + ACTIVE),
    ("X1:TEST:*", True, KNOWN_COALESCED, ACTIVE_COALESCED),
])
@mock.patch('dqsegdb2.query.query_versions', return_value=(1, 2))
@mock.patch('dqsegdb2.http.request', return_value=mock.MagicMock())
def test_query_segments(request, versions, flag, coalesce, known, active):
    result = {
        'ifo': 'X1',
        'name': 'TEST',
        'version': 1,
        'known': KNOWN,
        'active': ACTIVE
    }
    # this mock is a bit more complicated because query_segments() pops
    # keys out of the dict, and we want to call request_json multiple
    # times, so we need to mock further upstream
    request.return_value.read.return_value = json.dumps(result)

    out = query.query_segments(flag, 2, 8, coalesce=coalesce)
    assert out.pop('version') is (None if flag.endswith('*') else 1)
    assert out.pop('known') == known
    assert out.pop('active') == active
    for key in set(result) & set(out):
        assert out[key] == result[key]
