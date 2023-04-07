"""
Implements the GSF job class for the ESE job endpoint.
"""
import time
import re
from string import Template
import requests

from ..job import Job as BaseJob
from ..dict import Dict as gsfdict
from ..error import JobNotFoundError

class Job(BaseJob):
    """
    Creates a GSF job used for querying job information.
    """
    def __init__(self,  url):
        self._url = url

        def __str__(self):
            status = self._http_get()
            props = dict(job_id=status['jobId'],
                         status=_STATUS_MAP[status['jobStatus']],
                         progress=status['jobProgress'],
                         progress_message=str(status['jobProgressMessage']),
                         error_message=str(status['jobErrorMessage']),
                         results=self._build_result())
            return Template('''
job_id: ${job_id}
status: ${status}
progress: ${progress}
progress_message: ${progress_message}
error_message: ${error_message}
results: ${results}
''').substitute(props)

    @property
    def job_id(self):
        status = self._http_get()
        return status['jobId']

    @property
    def status(self):
        status = self._http_get()
        return status['jobStatus']

    @property
    def progress(self):
        status = self._http_get()
        return status['jobProgress']

    @property
    def progress_message(self):
        status = self._http_get()
        return str(status['jobMessage'])

    @property
    def error_message(self):
        status = self._http_get()
        return str(status['jobError'])

    @property
    def results(self):
        status = self._http_get()
        return self._build_result(status)

    def wait_for_done(self):
        while not re.match('(Failed|Succeeded)', self.status):
            time.sleep(1)

    def _http_get(self):
        response = requests.get(self._url)
        if response.status_code >= 400:
            raise JobNotFoundError(f'HTTP code {response.status_code}, Reason: {response.text}')
        return response.json()

    def _build_result(self, status):
        out_result = gsfdict()
        for out_param, value in status['jobResults'].items():
            # remove all the 'best' nonsense
            out_result[out_param] = value['best']
        return out_result