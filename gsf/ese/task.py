"""
Implements the GSF task class for the ESE task endpoint.
"""

# Python 3
try:
    from urllib.parse import urlparse, urlunparse
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError
    from urlparse import urlparse, urlunparse

from ..task import Task as BaseTask
from ..error import TaskNotFoundError
from ..decorators import memoize
from . import http
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

    def submit(self, parameters):
        submit_job_url = '/'.join((self._uri, 'submitJob'))
        try:
            status = http.post(submit_job_url, parameters)
        except HTTPError as err:
            raise TaskNotFoundError('HTTP code {}, Reason: {}'.format(err.code, err.reason))

        parsed_url = urlparse(self._uri)
        split_path = parsed_url.path.split('/')
        job_url = urlunparse((parsed_url.scheme,
                              parsed_url.netloc,
                              '/'.join((split_path[1], 'jobs', str(status['jobId']))),
                              None, None, None))
        return Job(job_url)

    @memoize
    def _http_get(self):
        try:
            info = http.get(self._uri)
            parameters = info['parameters']
            for parameter in parameters:
                parameter['name'] = str(parameter['name'])
                parameter['description'] = str(parameter['description'])
                parameter['display_name'] = str(parameter.pop('displayName'))
                if parameter['dataType'].count('['):
                    parameter['dimensions'] = '[' + parameter['dataType'].split('[')[1]
                parameter['type'] = str(parameter.pop('dataType').split('[')[0])

                parameter['direction'] = parameter['direction'].lower()
                parameter['required'] = True if parameter['parameterType'] == 'required' else False
                parameter.pop('parameterType')

                if 'defaultValue' in parameter:
                    parameter['default_value'] = parameter.pop('defaultValue')

                if 'choiceList' in parameter:
                    parameter['choice_list'] = parameter.pop('choiceList')

            return info

        except HTTPError as err:
            raise TaskNotFoundError('HTTP code {}, Reason: {}'.format(err.code, err.reason))
