"""
Implements the GSF Service class for the ESE services endpoint.
"""

# Python 3
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from ..error import ServiceNotFoundError

from ..service import Service as BaseService
from .task import Task
from ..decorators import memoize
from . import http


class Service(BaseService):
    """
    Creates a GSF Service object that can list tasks and create task objects.
    """
    def __init__(self, url):
        self._url = url

    def task(self, task_name):
        return Task('/'.join((self._url, task_name)))

    def tasks(self):
        service_info = self._http_get()
        return service_info['tasks']

    @property
    def name(self):
        service_info = self._http_get()
        return str(service_info['name'])

    @property
    def description(self):
        service_info = self._http_get()
        return str(service_info['description'])

    @memoize
    def _http_get(self):
        try:
            return  http.get(self._url)
        except HTTPError as err:
            raise ServiceNotFoundError('HTTP code {}, Reason: {}'.format(err.code, err.reason))

