
from functools import lru_cache
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlunparse

from ..error import ServerNotFoundError
from ..server import Server as BaseServer
from .service import Service
from .job import Job

class Server(BaseServer):
    """
    The Server connects to GSF using HTTP requests.
    """
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self._services_path = 'services'
        self._url = urlunparse(('http', ':'.join((self._server, self._port)),
                                '', None, None, None))
        self._services_info = dict()

    @property
    def name(self):
        return self._server

    @property
    def port(self):
        return self._port

    def services(self):
        """Returns a list of services"""
        info = self._http_get()
        service_list = []
        for service in info['services']:
            service_list.append(service['name'])
        return service_list

    def service(self, service_name):
        """
        Service takes in a service name then returns the properties and tasks of the service.

        :param service_name: The name of the service to return.
        :return: Returns the gsf.service object.
        """
        return Service('/'.join((self._url, self._services_path, service_name)))

    def job(self, job_id):
        """

        :param jobID:
        :return:
        """
        return Job('/'.join((self._url, 'jobs', str(job_id))))

    @lru_cache(maxsize=None)
    def _http_get(self):
        """
        :return:
        """
        try:
            response = requests.get('/'.join((self._url, self._services_path)))
            if response.status_code >= 400:
                raise ServerNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        except ConnectionError as err:
            raise ServerNotFoundError(f'Reason: {err}') from err
        return response.json()