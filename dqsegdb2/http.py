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

"""HTTP interactions with DQSEGDB
"""

import calendar
import json
import os
import time

from six.moves.http_client import HTTPSConnection
from six.moves.urllib import request as urllib_request
from six.moves.urllib.parse import urlparse

from OpenSSL import crypto


class HTTPSAuthConnection(HTTPSConnection):
    def __init__(self, host, key_file=None, cert_file=None, **kwargs):
        if cert_file is None or key_file is None:
            cert, key = find_x509_credential()
            cert_file = cert_file or cert
            key_file = key_file or key
        HTTPSConnection.__init__(
            self, host, key_file=key_file, cert_file=cert_file, **kwargs)


class HTTPSAuthHandler(urllib_request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSAuthConnection, req)


def find_x509_credential():
    """Locate an X509 credential in the current environment
    """
    try:  # use X509_USER_PROXY from environment if set
        path = os.environ['X509_USER_PROXY']
    except KeyError:
        pass
    else:
        validate_x509_proxy(path)
        return path, path

    try:  # use X509_USER_CERT and X509_USER_KEY if set
        return os.environ['X509_USER_CERT'], os.environ['X509_USER_KEY']
    except KeyError:
        pass

    # search for proxy file on disk
    uid = os.getuid()
    path = "/tmp/x509up_u%d" % uid
    if os.access(path, os.R_OK):
        validate_x509_proxy(path)
        return path, path

    raise RuntimeError("Could not find a valid proxy credential")


def validate_x509_proxy(path):
    """Validate a proxy certificate as RFC3820 and not expired

    Parameters
    ----------
    path : `str`
        the path of the proxy certificate file

    Returns
    -------
    True
        if the proxy is validated

    Raises
    ------
    IOError
        if the proxy certificate file cannot be read
    RuntimeError
        if the proxy is found to be a legacy globus cert, or has expired
    """
    # load the proxy from path
    try:
        with open(path, 'rt') as f:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    except IOError as e:
        e.args = ('Failed to load proxy certificate: %s' % str(e),)
        raise

    # try and read proxyCertInfo
    rfc3820 = False
    for i in range(cert.get_extension_count()):
        if cert.get_extension(i).get_short_name() == 'proxyCertInfo':
            rfc3820 = True
            break

    # otherwise test common name
    if not rfc3820:
        subject = cert.get_subject()
        if subject.CN.startswith('proxy'):
            raise RuntimeError('Could not find a valid proxy credential')

    # check time remaining
    expiry = cert.get_notAfter()
    if isinstance(expiry, bytes):
        expiry = expiry.decode('utf-8')
    expiryu = calendar.timegm(time.strptime(expiry, "%Y%m%d%H%M%SZ"))
    if expiryu < time.time():
        raise RuntimeError('Required proxy credential has expired')


def request(url):
    """Request data from a URL
    """
    purl = urlparse(url)
    if purl.scheme == 'https':
        opener = urllib_request.build_opener(HTTPSAuthHandler)
        req = urllib_request.Request(url)
        response = opener.open(req)
    else:
        response = urllib_request.urlopen(url)
    out = response.read()
    if isinstance(out, bytes):
        return out.decode('utf8')
    return out


def request_json(url):
    return json.loads(request(url))
