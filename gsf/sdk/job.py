"""
Implements the GSF job class for the ESE job endpoint.
"""
import time
import re
from string import Template
import requests
from urllib.parse import urlparse, urlunparse

from ..job import Job as BaseJob
from ..dict import Dict as gsfdict
from ..error import JobNotFoundError


class Job(BaseJob):
    """
    Creates a GSF job used for querying job information.
    """

    def __init__(self,  url, session=None):
        self._url = url
        self._status = None
        self._connection = requests if session is None else session

        # Retrieve server from URL
        from gsf import Server
        self._Server = Server(taskUrl=self._url,session=self._connection)
        self._status = self._http_get()

    def __str__(self):
        self._status = self._http_get()
        props = dict(job_id=self._status['jobId'],
                        status=self._status['status'],
                        progress=self._status['jobProgress'],
                        progress_message=str(self._status['jobProgressMessage']),
                        error_message=str(self._status['jobErrorMessage']),
                        results=self._build_result())
        return Template('''
job_id: ${job_id}
self._status: ${self._status}
progress: ${progress}
progress_message: ${progress_message}
error_message: ${error_message}
results: ${results}
''').substitute(props)

    @property
    def job_id(self):
        """
        :return: the jobId of the job
        """
        return self._status['jobId']

    @property
    def status(self):
        """
        :return: the job self._status of the job
        """
        self._status = self._http_get()
        return self._status['jobStatus']

    @property
    def progress(self):
        """
        :return: the jobProgress of the job
        """
        self._status = self._http_get()
        return self._status['jobProgress']

    @property
    def progress_message(self):
        """
        :return: the jobMessage of the job
        """
        self._status = self._http_get()
        return str(self._status['jobMessage']) if "jobMessage" in self._status else ""

    @property
    def error_message(self):
        """
        :return: the jobError message of the job
        """
        self._status = self._http_get()
        return str(self._status['jobError']) if "jobError" in self._status else ""

    @property
    def results(self):
        """
        :return: the results of the job
        """
        self._status = self._http_get()
        return self._build_result()
    
    @property
    def Server(self):
        """
        Returns the Server
        """
        return self._Server

    def wait_for_done(self, status_callback=None):
        """
         Wait until job completes
        :param: status_callback: The callback to call at each check of jobStatus.
        """

        while not re.match('(Failed|Succeeded)', self._status['jobStatus']):
            self._status = self._http_get()
            if status_callback is not None and self._status['jobStatus'] != 'Failed':
                status_callback(self._status)
            time.sleep(1)
            
        # One more time when finished to get the last message and progress
        if status_callback is not None and self._status['jobStatus'] != 'Failed':
                status_callback(self._status)
        

    def cancel(self):
        """
        cancel the job
        """
        self._Server.cancelJob(self.job_id())

    def _http_get(self):
        """
        :return: the get response of job url
        """       
        response = self._connection.get(self._url)
        if response.status_code >= 400:
            raise JobNotFoundError(
                f'HTTP code {response.self._status_code}, Reason: {response.text}')
        return response.json()

    def _build_result(self):
        """
        :return: the results from the self._status 
        """    
        out_result = gsfdict()
        for out_param, value in self._status['jobResults'].items():
            # remove all the 'best' nonsense
            if 'best' in value :
                out_result[out_param] = value['best']
            else :
                out_result[out_param] = value
        return out_result
