.. _gsf:

******
GSF Py
******

GSF Py provides a client Python package, named gsf, to run IDL and ENVI analytics provided by the Geospatial Services Framework.
The Python package provides the ability to query for available tasks, retrieve task information, and submit jobs to the GSF server.

There is an additional client Python package available, named gsfarc, to provide the ability to run GSF analytics through ArcMap,
ArcGIS Pro, and ArcGIS Server.  

See http://www.harrisgeospatial.com/ for more details on product offerings.


Usage
=====

Demonstration of connecting to GSF Server and submitting a job.

Note: If not executing the Python client code on same system as the server, replace `localhost` with the server name.

To connect to GSF and list the available services, create a new instance of the GSF Server class with the URL to the server from the Python command line::

    >>> from gsf import Server
    >>> server = Server('localhost','9191')
    >>> server.services()

To get a dictionary of service information including a list of tasks, use the :code:`service()` method on the Server object::

    >>> envi_service = server.service('ENVI')
    >>> envi_service.tasks()

To get a GSF task object, use the :code:`task()` method on the Service object::

    >>> task = envi_service.task('SpectralIndex')
	
To get a list of task parameter information, use the :code:`parameters` property on the Task object::
	
    >>> task.parameters

To run a task asynchronously, use the :code:`submit()` method on the Task object.  A GSF Job object is returned
after the job has been submitted.

Debug Tip: To see if GSF server received the job and check job status, go to http://localhost:9191/job-console/

    >>> input_raster = dict(url='http://localhost:9191/ese/data/qb_boulder_msi',
                            factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
    >>> job = task.submit(parameters)
    >>> job.wait_for_done()


API Documentation
=================

.. toctree::
   :maxdepth: 2

   gsf_api




