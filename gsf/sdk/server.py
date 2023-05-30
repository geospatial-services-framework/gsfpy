
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

        self._info_path = 'reports/server-info'
        self._server_info = self._http_get(self._info_path)
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
    def requestHandlers(self) :
        """Returns a list of requestHandlers"""
        handlersList = []
        for handler in self._server_info['configuration']['requestHandlers']:
            handlersList.append(handler['type'])
        return handlersList

    @property
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

    def service(self, service_name):
        """
        Service takes in a service name then returns the properties and tasks of the service.

        :param service_name: The name of the service to return.
        :return: Returns the gsf.service object.
        """
        if not service_name in self._services_list : 
            return None
        return Service('/'.join((self._url, self._services_path, service_name)))

    def job(self, job_id):
        """
        :param jobID:
        :return: a Job object
        """
        return Job('/'.join((self._url, 'jobs', str(job_id))))
    
    def getJobs(self, jobStatus=None, limit=-1):
        """
        :param jobStatus: Filters output with jobStatus 
        :param limit: limit parameter of jobs url  
        :return: a job list
        """
        jobs = self._http_get('jobs?limit='+str(limit))
        jobs_list = []
        for job in jobs['jobs'] :
            if jobStatus is None or job['jobStatus'] == jobStatus :
                jobs_list.append(job)
        return jobs_list
    
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