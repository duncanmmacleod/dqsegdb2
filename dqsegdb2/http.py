# -*- coding: utf-8 -*-
# DQSEGDB2
# Copyright (C) 2018,2020  Duncan Macleod
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

"""HTTP interactions with DQSEGDB
"""

import os
import json
from urllib.request import urlopen
from urllib.parse import urlparse

def request(url, **urlopen_kw):
    """Request data from a URL
    If the URL uses HTTPS and the `context` keyword
    is not given, a SciToken will be looked for in the
    following search order:

    1. A file `${_CONDOR_CREDS}/scitokens.use`
    2. A file set by environment variable `${SCITOKENS_FILE}`
    3. The contents of the environment variable `${SCITOKENS}`

    If not SciToken can be found, an X509 credentials will be automatically
    loaded using :func:`gwdatafind.utils.find_credential`.

    Parameters
    ----------
    url : `str`
        the remote URL to request (HTTP or HTTPS)

    **urlopen_kw
        other keywords are passed to :func:`urllib.request.urlopen`

    Returns
    -------
    reponse : `http.client.HTTPResponse`
        the reponse from the URL
    """
    if urlparse(url).scheme == 'https' and 'context' not in urlopen_kw:
        from ssl import create_default_context
        urlopen_kw['context'] = context = create_default_context()
        req = Request(url)

        if os.environ.get('_CONDOR_CREDS'):
          scitokens_path = os.path.join(os.environ['_CONDOR_CREDS'],'scitokens.use')
        elif os.environ.get('SCITOKENS_FILE'):
          scitokens_path = 'scitokens.use'
        else:
          scitokens_path = ''

        if os.path.isfile(scitokens_path):
          with open(scitokens_path) as f: token_data = f.read()
        elif os.environ.get('SCITOKEN'):
          token_data = os.environ['SCITOKEN']
        else:
          token_data = None
          from gwdatafind.utils import find_credential
          context.load_cert_chain(*find_credential())

        if token_data:
          req.add_header("Authorization", "Bearer " + token_data.rstrip())
    else:
        req = Request(url)

    return urlopen(req, **urlopen_kw)


def request_json(url, **kwargs):
    """Request data from a URL and return a parsed JSON packet

    Parameters
    ----------
    url : `str`
        the remote URL to request (HTTP or HTTPS)

    Returns
    -------
    data : `object`
        the URL reponse parsed with :func:`json.loads`

    See also
    --------
    dqsegdb2.http.request
        for information on how the request is performed
    """
    out = request(url, **kwargs).read()
    if isinstance(out, bytes):
        out = out.decode('utf8')
    return json.loads(out)
