"""
Implements the GSF Server class for the ESE root endpoint.

"""

# Python 3
try:
    from urllib.parse import urlunparse
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError
    from urlparse import urlunparse


from ..server import Server as BaseServer
from .service import Service
from .job import Job
from ..decorators import memoize
from ..error import ServerNotFoundError
from . import http


class Server(BaseServer):
    """
    The Server connects to GSF using HTTP requests.
    """
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self._root_path = 'ese'
        self._services_path = 'services'
        self._url = urlunparse(('http', ':'.join((self._server, self._port)),
                                self._root_path, None, None, None))
        self._services_info = dict()

    @property
    def name(self):
        return self._server

    @property
    def port(self):
        return self._port

    def services(self):
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

    @memoize
    def _http_get(self):
        """

        :return:
        """
        try:
            return http.get('/'.join((self._url, self._services_path)))
        except HTTPError as err:
            raise ServerNotFoundError('HTTP code {}, Reason: {}'.format(err.code, err.reason))
