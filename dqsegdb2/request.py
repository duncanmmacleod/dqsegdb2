# -*- coding: utf-8 -*-
# DQSEGDB2
# Copyright (C) 2022 Cardiff University
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

"""Request interface for dqsegdb2.
"""

from functools import wraps

from igwn_auth_utils import get as _get

DEFAULT_TOKEN_SCOPE = "dqsegdb.read"


@wraps(_get)
def get(url, *args, **kwargs):
    if url.startswith("http://") and requests.__version__ < "2.15.0":
        # workaround https://github.com/psf/requests/issues/4025
        kwargs.setdefault("cert", False)
    kwargs.setdefault("token_scope", DEFAULT_TOKEN_SCOPE)
    return _get(url, *args, **kwargs)


def get_json(*args, **kwargs):
    """Perform a GET request and return JSON.

    Parameters
    ----------
    *args, **kwargs
        all keyword arguments are passed directly to
        :meth:`igwn_auth_utils.requests.get`

    Returns
    -------
    data : `object`
        the URL reponse parsed with :func:`json.loads`

    See also
    --------
    igwn_auth_utils.requests.get
        for information on how the request is performed
    """
    response = get(*args, **kwargs)
    response.raise_for_status()
    return response.json()
