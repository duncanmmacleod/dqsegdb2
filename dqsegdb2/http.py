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
import scitokens
from scitokens.utils.errors import InvalidTokenFormat, InvalidAudienceError
from urllib.request import urlopen
from urllib.parse import urlparse

def request(url, **urlopen_kw):
    """Request data from a URL
    If the URL uses HTTPS and the `context` keyword
    is not given, a SciToken will be looked for a serialized
    scitoken from the following places in the order:

    1. A token string in the environment variable `${SCITOKEN}`
    2. A token in the file set by the environment variable `${SCITOKENS_FILE}`
    3. A valid token in the `${_CONDOR_CREDS}` directory

    The token must be unexpired and the audience must match the hostname
    of the target server.

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
    req = Request(url)
    if urlparse(url).scheme == 'https' and 'context' not in urlopen_kw:
        from ssl import create_default_context
        urlopen_kw['context'] = context = create_default_context()
        aud = urlparse(url).hostname
        token_data = None
        tok = None

        # look for a condor-created scitoken for the target url
        if os.environ.get('_CONDOR_CREDS'):
            for f in os.listdir(os.environ['_CONDOR_CREDS']):
                if f.endswith(".use"):
                    try:
                        with open(os.path.join(
                                  os.environ['_CONDOR_CREDS'],f)) as t:
                            token_data = t.read().strip()
                            tok = scitokens.SciToken.deserialize(token_data,
                                                                 audience=aud)
                            break
                    except (InvalidTokenFormat, InvalidAudienceError):
                        # ignore files that do not contain tokens
                        # or that are for a different audience
                        pass

        # use the token in the specified file
        if os.environ.get('SCITOKENS_FILE'):
            with open(os.environ.get('SCITOKENS_FILE')) as t:
                token_data = t.read().strip()
                tok = scitokens.SciToken.deserialize(token_data,
                                                     audience=aud)

        # use a serialized token in an environment variable
        if os.environ.get('SCITOKEN'):
            token_data = os.environ['SCITOKEN'].strip()
            tok = scitokens.SciToken.deserialize(token_data,
                                                 audience=aud)

        # check that this token has dqsegdb read permissions
        if token_data:
            token_enforcer = scitokens.Enforcer(tok['iss'], audience=aud)
            if token_enforcer.test(token, "read", "/DQSegDB") is False:
                raise ValueError('SciToken does not have read:/DQSegDB scope')

        # if we have a token, use it, otherwise look for x590 cert
        if token_data:
            req.add_header("Authorization", "Bearer " + token_data)
        else:
            from gwdatafind.utils import find_credential
            context.load_cert_chain(*find_credential())

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
