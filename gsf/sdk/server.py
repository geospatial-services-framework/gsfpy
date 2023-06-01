
from functools import lru_cache
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlunparse

from ..error import ServerNotFoundError
from ..error import ServiceNotFoundError
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

        self._info_path = 'reports/server-info'
        self._server_info = self._http_get(path=self._info_path)
        self._services_list = []

    @property
    def name(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def description(self):
        """Returns the description of the server"""
        return self._server_info['description']

    @property
    def version(self):
        """Returns the GSF version of the server"""
        return self._server_info['version']

    @property
    def requestHandlers(self):
        """Returns a list of requestHandlers"""
        handlersList = []
        for handler in self._server_info['configuration']['requestHandlers']:
            handlersList.append(handler['type'])
        return handlersList

    def services(self):
        """Returns a list of services"""
        services_info = self._http_get(self._services_path)
        self._services_list = []
        for service in services_info['services']:
            self._services_list.append(service['name'])
        return self._services_list

    @property
    def info(self):
        """ Returns server information full"""
        return self._server_info

    @property
    def url(self):
        """ Returns server information full"""
        return self._url

    def service(self, service_name):
        """
        Service takes in a service name then returns the properties and tasks of the service.

        :param service_name: The name of the service to return.
        :return: Returns the gsf.service object.
        """
        if not service_name in self._services_list:
            raise ServiceNotFoundError(f"Service {service_name} not found")
        return Service('/'.join((self._url, self._services_path, service_name)))

    def job(self, job_id):
        """
        :param jobID:
        :return: a Job object
        """
        return Job('/'.join((self._url, 'jobs', str(job_id))))

    def getJobs(self, jobStatus=None, limit=10000000, offset=0, taskName=None):
        """
        :param jobStatus: Filters with jobStatus 
        :param limit: limit parameter of jobs url  
        :param offset: offset parameter 
        :taskName: Filters on taskName
        :return: a job list
        """
        # GSF 2.X version using /jobs
        if self.version.startswith("2."):
            jobs = self._http_get(path='jobs?limit='+str(limit)+'&offset='+str(offset))

        # GSF 3.X version using /searchJobs
        elif self.version.startswith("3."):
            jobsearch = {
                'limit': limit,
                'offset' : offset,
                'totals': 'all',
                'sort' : [["jobSubmitted",-1]],
                'query' : {}
            }
            if jobStatus is not None:
                jobsearch['query']['jobStatus'] = {'$eq': jobStatus }
            if taskName is not None:
                    jobsearch['query']['taskName'] = {"$eq": taskName}

            response = requests.post(
                '/'.join((self._url, "searchJobs")), json=jobsearch)
            jobs = response.json()

        return jobs['jobs']

    @property
    def jobs(self):
        """
        :return: all jobs as a list
        """
        return self.getJobs()

    @lru_cache(maxsize=None)
    def _http_get(self, path=None):
        """
        :return:
        """
        try:
            response = requests.get('/'.join((self._url, path)))
            if response.status_code >= 400:
                raise ServerNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        except ConnectionError as err:
            raise ServerNotFoundError(f'Reason: {err}') from err
        return response.json()
