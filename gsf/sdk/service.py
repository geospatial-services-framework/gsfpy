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
    def __init__(self, url, session=None):
        self._url = url
        self._connection = requests if session is None else session
        self._service_info = self._http_get()


    def task(self, task_name):
        """
        Returns a GSF task object. See GSF Task for example.

        :param: task_name: The name of the task to retrieve.
        :return: a GSF Task object
        """
        return Task('/'.join((self._url, 'tasks', task_name)), session=self._connection)

    def tasks(self):
        """
        Returns a list of task names available on this service
        :return: a list
        """
        return self._http_get('tasks')['tasks']

    @property
    def name(self):
        return str(self._service_info['name'])
    
    @property
    def description(self):
        # Service may have a description
        description = self._service_info['description'] if 'description' in  self._service_info else ''
        return description

    @lru_cache(maxsize=None)
    def _http_get(self, path=None):
        """
        :return:
        """
        url = self._url if not path else '/'.join((self._url, path))
        response = self._connection.get(url)
        if response.status_code >= 400:
            raise ServiceNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        return response.json()