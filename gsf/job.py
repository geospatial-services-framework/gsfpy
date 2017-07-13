"""
A GSF job object is returned from the GSF Task submit method and is used to query job status and retrieve job results.
"""
from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from .gsfmeta import GSFMeta
from .utils import with_metaclass

class Job(with_metaclass(GSFMeta, object)):
    """
    A GSF Job object connects to a GSF Job and its status.

    :Example:
	
    Import the modules for the example.

    >>> from gsf import Server
    >>> from pprint import pprint
	
    Connect to the GSF server, retrieve the SpectralIndex task, and submit a job.
	
    >>> server = Server('localhost','9191')
    >>> service = server.service('ENVI')
    >>> task = service.task('SpectralIndex')
    >>> input_raster = dict(url='http://localhost:9191/ese/data/qb_boulder_msi',
                            factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
    >>> job = task.submit(parameters)
	
    Wait for job to be done.
	
    >>> job.wait_for_done()
	
    Investigate job information and results.
	
    >>> print(job.job_id, type(job.job_id))
    (42, <type 'int'>)
    >>> print(job.status, type(job.status))
    ('Succeeded', <class 'str'>)
    >>> print(job.results,type(job.results))
    ({ 'OUTPUT_RASTER': { 'auxiliary_url': [ 'http://localhost:9191/ese/jobs/42/envitempfileFriJul151817462016242_1.hdr'],
                     'factory': 'URLRaster',
                     'url': 'http://localhost:9191/ese/jobs/42/envitempfileFriJul151817462016242_1.dat'}}, <class 'gsf.dict.Dict'>)

    Submit a job that will fail.
	
    >>> input_raster = dict(url='http://localhost:9191/ese/data/doesnotexist',
                            factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
    >>> job = task.submit(parameters)

    Wait for job to be done.

    >>> job.wait_for_done()
	
    Investigate job information and results.
	
    >>> print(job.job_id)
    43 
    >>> print(job.status)
    Failed 
    >>> print(job.results)
    {}
    >>> print(job.error_message)
    'Invalid value for parameter: INPUT_RASTER. Error: File: ...

    """

    def __str__(self):
        props = dict(job_id=self.job_id,
                     status=self.status,
                     progress=self.progress,
                     progress_message=self.progress_message,
                     error_message=self.error_message,
                     results=self.results)
        return Template('''
job_id: ${job_id}
status: ${status}
progress: ${progress}
progress_message: ${progress_message}
error_message: ${error_message}
results: ${results}
''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    @abstractproperty
    def job_id(self):
        """
        Returns the job_id

        :return: an integer greater than 0
        """
        pass

    @abstractproperty
    def status(self):
        """
        Returns the current job status. Status can be "Succeeded | Failed | Accepted | Started"

        :return: a string
        """
        pass

    @abstractproperty
    def progress(self):
        """
        Returns a percentage of job completion

        :return: an integer between 0 and 100
        """
        pass

    @abstractproperty
    def progress_message(self):
        """
        Returns the job progress message

        :return: a string
        """
        pass

    @abstractproperty
    def error_message(self):
        """
        Returns the job error message

        :return: a string
        """
        pass

    @abstractproperty
    def results(self):
        """
        Returns the output parameter results as a dictionary where each key is the output parameter name. The value depends on the parameter type.

        :return: a dictionary
        """
        pass

    @abstractmethod
    def wait_for_done(self):
        """
        Blocks execution until the job status message is either Succeeded or Failed. 

        :return: None
        """
        pass
