"""
Implements the GSF task class for the ESE task endpoint.
"""
from functools import lru_cache
import requests
from urllib.parse import urlparse, urlunparse

from ..task import Task as BaseTask
from ..error import TaskNotFoundError
from .job import Job


class Task(BaseTask):
    """
    Creates a GSF task that can submit jobs and list task parameters.
    """
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    @property
    def uri(self):
        return self._uri

    @property
    def name(self):
        info = self._http_get()
        return str(info['name'])

    @property
    def service_name(self):
        info = self._http_get()
        return str(info['serviceName'])

    @property
    def display_name(self):
        info = self._http_get()
        return str(info['displayName'])

    @property
    def description(self):
        info = self._http_get()
        return str(info['description'])

    @property
    def parameters(self):
        info = self._http_get()
        return info['parameters']

    def _jobs_url(self):
        """Returns the jobs url"""
        # this could be done better with some IOC
        parsed_url = urlparse(self.uri)
        return urlunparse((parsed_url.scheme,
                          parsed_url.netloc,
                          'jobs',
                          None, None, None))


    def submit(self, parameters):
        """
        """
        jobOptions = {
            "serviceName": self.service_name,
            "taskName": self.name,
            "jobOptions": {
                "route": "default",
                "jobResultsFile": "job_results.json"
            },
            "inputParameters": parameters
        }
        # Trace back the url to get the service name
        jobs_url = self._jobs_url()
        response = requests.post(jobs_url, json=jobOptions)
        if response.status_code >= 400:
            raise TaskNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        status = response.json()
        return Job('/'.join((jobs_url, status['jobId'])))

    def _reformat_info(self, parameters, direction):
        for parameter in parameters:
            parameter['name'] = str(parameter['name'])
            parameter['description'] = str(parameter['description'])
            parameter['display_name'] = str(parameter.pop('displayName'))
            if parameter['type'].count('['):
                parameter['dimensions'] = '[' + parameter['type'].split('[')[1]
            parameter['type'] = str(parameter.pop('type').split('[')[0])

            parameter['direction'] = direction

            if 'default' in parameter:
                parameter['default_value'] = parameter.pop('default')

            if 'choiceList' in parameter:
                parameter['choice_list'] = parameter.pop('choiceList')        
        return parameters

    @lru_cache(maxsize=None)
    def _http_get(self):
        response = requests.get(self._uri)
        if response.status_code >= 400:
            raise TaskNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        info = response.json()
        info['name'] = info.pop('taskName')
        info['parameters'] = []
        info['parameters'].extend(self._reformat_info(info['inputParameters'], 'input'))
        info['parameters'].extend(self._reformat_info(info['outputParameters'], 'output'))             
        info.pop('inputParameters')
        info.pop('outputParameters')
        return info
