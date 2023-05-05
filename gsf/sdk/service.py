"""
Implements the GSF Service class for the ESE services endpoint.
"""

import requests
from functools import lru_cache

from ..error import ServiceNotFoundError

from ..service import Service as BaseService
from .task import Task


class Service(BaseService):
    """
    Creates a GSF Service object that can list tasks and create task objects.
    """
    def __init__(self, url):
        self._url = url

    def task(self, task_name):
        return Task('/'.join((self._url, 'tasks', task_name)))

    def tasks(self):
        return self._http_get('tasks')['tasks']

    @property
    def name(self):
        service_info = self._http_get()
        return str(service_info['name'])

    @property
    def description(self):
        service_info = self._http_get()
        return str(service_info['name'])

    @lru_cache(maxsize=None)
    def _http_get(self, path=None):
        """
        :return:
        """
        url = self._url if not path else '/'.join((self._url, path))
        response = requests.get(url)
        if response.status_code >= 400:
            raise ServiceNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        return response.json()