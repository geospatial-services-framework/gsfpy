
from functools import lru_cache
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlunparse, urlparse

from ..error import ServerNotFoundError
from ..error import ServiceNotFoundError
from ..error import JobStatusNotFoundError
from ..error import JobNotFoundError
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
        """Returns the server host name"""
        return self._server

    @property
    def port(self):
        """Returns the server port"""
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
        """Returns a list of the requestHandlers types"""
        handlersList = []
        for handler in self._server_info['configuration']['requestHandlers']:
            handlersList.append(handler['type'])
        return handlersList
    
    @property
    def info(self):
        """ Returns server information full"""
        return self._server_info

    @property
    def url(self):
        """ Returns the server url """
        return self._url

    def services(self):
        """Returns a list of services"""
        services_info = self._http_get(self._services_path)
        self._services_list = []
        for service in services_info['services']:
            self._services_list.append(service['name'])
        return self._services_list

    def service(self, service_name):
        """
        Service takes in a service name then returns the properties and tasks of the service.

        :param service_name: The name of the service to return.
        :return: Returns the gsf.service object.
        """
        # Just in case the services property is not called before
        if len(self._services_list) == 0 :
            self.services()
        if not service_name in self._services_list:
            raise ServiceNotFoundError(f"Service {service_name} not found")
        return Service('/'.join((self._url, self._services_path, service_name)), session=self._connection)

    def job(self, job_id):
        """
        :param jobID:
        :return: a Job object
        """
        return Job('/'.join((self._url, 'jobs', str(job_id))))

    def getJobs(self, jobStatus=None, limit=None, offset=0, taskName=None):
        """
        :param jobStatus: Filter with jobStatus 
        :param limit: limit parameter of /jobs url or /searchJob post request
        :param offset: offset parameter of /jobs url or /searchJob post request
        :taskName: Filter on taskName
        :return: a job list
        """

        if jobStatus is not None:
            if jobStatus.lower() not in Job.JOB_STATUS_MAP:
                raise JobStatusNotFoundError(f"Status {jobStatus} not found")
        # GSF 2.X version using /jobs
        if self.version.startswith("2."):
            jobs = []
            url_path = 'jobs?offset='+str(offset)+('&limit='+str(limit) if limit is not None else '&limit=-1')
            rawjobs = self._http_get(
                path=url_path)
            if jobStatus is not None and taskName is not None:
                for job in rawjobs['jobs']:
                    if job['jobStatus'].casefold() == jobStatus.casefold() and job['taskName'].casefold() == taskName.casefold():
                        jobs.append(job)
            elif jobStatus is not None:
                for job in rawjobs['jobs']:
                    if job['jobStatus'].casefold() == jobStatus.casefold():
                        jobs.append(job)
            elif taskName is not None:
                for job in rawjobs['jobs']:
                    if job['taskName'].casefold() == taskName.casefold():
                        jobs.append(job)
            else:
                jobs = rawjobs['jobs']

        # GSF 3.X version using /searchJobs
        elif self.version.startswith("3."):
            jobsearch = {
                'offset': offset,
                'totals': 'all',
                'sort': [["jobSubmitted", -1]],
                'query': {}
            }
            if limit is not None :
                jobsearch['limit'] = str(limit)
            if jobStatus is not None:
                jobsearch['query']['jobStatus'] = {'$eq': jobStatus}
            if taskName is not None:
                jobsearch['query']['taskName'] = {"$eq": taskName}

            response = self._connection.post(
                '/'.join((self._url, "searchJobs")), json=jobsearch)
            rawjobs = response.json()
            jobs = rawjobs['jobs']

        return jobs

    @property
    def jobs(self):
        """
        :return: all jobs as a list
        """
        return self.getJobs()

    def cancelJob(self, jobId,raiseErrorIfNotRunning=True):
        """
        :param jobId: the job id to cancel
        :return: the HTTP response "message": "Cancel Sent"
        """

        job = self.job(jobId)
        jobStatus = job.status
        if jobStatus != 'Started':
            if raiseErrorIfNotRunning : 
                raise JobNotFoundError(
                    f'Job id {jobId} is not running, status is {jobStatus}')
            else:
                return {  "message": f'Job {jobId} status is {jobStatus}, Cancel Not Sent' }
        
        # if GSF 2.X send a delete request to http://server/job-console/jobId
        if self.version.startswith("2."):
            response = self._connection.delete("/".join((self.url,"job-console",str(jobId))))
        # if GSF 3.X send put request 
        elif self.version.startswith("3."):
            request_body = {
                "jobStatus": "CancelRequested"
            }
            response = self._connection.put('/'.join((self._url, "jobs", str(jobId))), json=request_body)
        if response.status_code >= 400:
            raise JobNotFoundError(
                f'HTTP code {response.status_code}, Reason: {response.text}')
        return response.json()

    @lru_cache(maxsize=None)
    def _http_get(self, path=None):
        """
        :return:
        """
        try:
            response = self._connection.get('/'.join((self._url, path)))
            if response.status_code >= 400:
                raise ServerNotFoundError(
                    f'HTTP code {response.status_code}, Reason: {response.text}')
        except ConnectionError as err:
            raise ServerNotFoundError(f'Reason: {err}') from err
        return response.json()
