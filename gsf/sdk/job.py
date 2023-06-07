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

    def __init__(self,  url,inArcGIS=None):
        self._url = url
        self._status = None
        parsed_url = urlparse(self._url)
        server_url = parsed_url.netloc.split(":")[0]
        server_port = parsed_url.netloc.split(":")[1] if len(parsed_url.netloc.split(":")) == 2  else "80"

        self._inArcGIS  = True if inArcGIS is not None else False
        
        from .server import Server
        self._server = Server(server_url,server_port)

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
        if self._status is None :
            self._status = self._http_get()
        return self._status['jobId']

    @property
    def status(self):
        """
        :return: the jobself._status of the job
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

    def wait_for_done(self):
        """
        Wait until job completes
        """
        if not self._inArcGIS :
            while not re.match('(Failed|Succeeded)', self.status) :
                time.sleep(1)
        else :
            import arcpy
            while not re.match('(Failed|Succeeded)', self.status) and not arcpy.env.isCancelled :
                arcpy.SetProgressorLabel(str(self._status['jobMessage']) if "jobMessage" in self._status else "")
                arcpy.SetProgressorPosition(int(self._status['jobProgress']))
                time.sleep(1)
            if arcpy.env.isCancelled :
                self._server.cancelJob(self.job_id)
            arcpy.ResetProgressor()

    def _http_get(self):
        """
        :return: the get response of job url
        """       
        response = requests.get(self._url)
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
