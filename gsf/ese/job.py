"""
Implements the GSF job class for the ESE job endpoint.
"""
import time
import re
from string import Template

# Python 3
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from ..job import Job as BaseJob
from ..dict import Dict as gsfdict
from ..error import JobNotFoundError
from . import http

_STATUS_MAP = dict(esriJobSucceeded='Succeeded',
                   esriJobFailed='Failed',
                   esriJobSubmitted='Accepted',
                   esriJobExecuting='Started')


class Job(BaseJob):
    """
    Creates a GSF job used for querying job information.
    """
    def __init__(self,  url):
        self._url = '/'.join((url, 'status'))

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
        return _STATUS_MAP[status['jobStatus']]

    @property
    def progress(self):
        status = self._http_get()
        return status['jobProgress']

    @property
    def progress_message(self):
        status = self._http_get()
        return str(status['jobProgressMessage'])

    @property
    def error_message(self):
        status = self._http_get()
        return str(status['jobErrorMessage'])

    @property
    def results(self):
        status = self._http_get()
        return self._build_result(status)

    def wait_for_done(self):
        while not re.match('(Failed|Succeeded)', self.status):
            time.sleep(1)

    def _http_get(self):
        try:
            return http.get(self._url)
        except HTTPError as err:
            raise JobNotFoundError('HTTP code: {}, Reason: {}'.format(err.code, err.reason))

    def _build_result(self, status):
        kv_result = gsfdict()
        for result in status['results']:
            kv_result[result['name']] = result['value']
        return kv_result

