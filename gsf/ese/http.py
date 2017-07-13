

# Python 3
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import Request, urlopen, URLError, HTTPError

import json

from ..error import ServerNotFoundError


def get(url):
    """Performs an ESE Rest HTTP GET command."""

    try:
        resp = urlopen(url).read().decode('utf-8')
    except HTTPError:
        raise
    except URLError as err:
        raise ServerNotFoundError(err.reason)

    return json.loads(resp)


def post(url, data):
    """Performs an ESE Rest HTTP GET command."""
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
        }
    data = json.dumps(data).encode('utf-8')
    req = Request(url, data, headers)
    try:
        resp = urlopen(req).read().decode('utf-8')
    except HTTPError:
        raise
    except URLError as err:
        raise ServerNotFoundError(err.reason)

    return json.loads(resp)