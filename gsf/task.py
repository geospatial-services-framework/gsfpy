"""
The GSF task object provides task information and can submit a job to the GSF server with input.
"""
from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from pprint import PrettyPrinter
from .gsfmeta import GSFMeta
from .utils import with_metaclass

class Task(with_metaclass(GSFMeta, object)):
    """
    The GSF Task object connects to a GSF Task and its parameters. 

    :Example:
	
    Import the modules for the example.

    >>> from gsf import Server
    >>> from pprint import pprint
	
    Connect to the GSF server, and then retrieve the SpectralIndex task.
	
    >>> server = Server('localhost','9191')
    >>> service = server.service('ENVI')
    >>> task = service.task('SpectralIndex')
    >>> print(type(task))
    <class 'gsf.ese.task.Task'>
	
    Investigate task information.
	
    >>> print(task.uri, type(task.uri))
    ('http://localhost:9191/ese/services/ENVI/SpectralIndex', <type 'str'>)
    >>> print(task.description, type(task.description))
    ('This task creates a spectral index raster from one pre-defined spectral
    index. Spectral indices are combinations of surface reflectance at two
    or more wavelengths that indicate relative abundance of features of
    interest.', <type 'str'>)
    >>> print(task.display_name, type(task.display_name))
    ('Spectral Index', <type 'str'>)
    >>> task_parameters = task.parameters
    >>> pprint(task_parameters)
	
    Submit a job to the GSF Server.  See GSF Job for details on waiting for job to complete.
	
    >>> input_raster = dict(url='http://localhost:9191/ese/data/qb_boulder_msi',
                            factory='URLRaster')
    >>> parameters = dict(INPUT_RASTER=input_raster,
                          INDEX='Normalized Difference Vegetation Index')
    >>> job = task.submit(parameters)
    >>> print(type(job))
    <class 'gsf.ese.job.Job'>


    """

    def __str__(self):
        pretty_print = PrettyPrinter(indent=2)
        props = dict(name=self.name,
                     uri=self.uri,
                     display_name=self.display_name,
                     description=self.description,
                     parameters=pretty_print.pformat(self.parameters))
        return Template('''
name: ${name}
uri: ${uri}
display_name: ${display_name}
description: ${description}
parameters: ${parameters}
''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    @abstractmethod
    def __init__(self, uri=None):
        """
        Returns a GSF Task object based on the uri.

        :param uri: A String representing the unique id of the task.
        :return: None
        """
        self._uri = uri

    @abstractproperty
    def uri(self):
        """
        The unique identifier of this task

        :return: a string
        """
        pass

    @abstractproperty
    def name(self):
        """
        The name of the task

        :return: a string
        """
        pass

    @abstractproperty
    def display_name(self):
        """
        The display name of the task

        :return: a string
        """
        pass

    @abstractproperty
    def description(self):
        """
        The task description

        :return: a string
        """
        pass

    @abstractproperty
    def parameters(self):
        """
        A list of the task parameter definitions. Each task parameter is a dictionary containing, but not
        limited to, the following keys:

        ================= ========== ================= ==========================================================
        Key               Data Type  Type              Description
        ================= ========== ================= ==========================================================
        name              string     Required          The name of the parameter
        display_name      string     Required          The display name of the parameter
        type              string     Required          The parameter data type
        direction         string     Required          Can be *input* or *output*
        description       string     Required          The parameter description
        required          bool       Required          Indicates if the parameter is required
                                                       on input when submitting a job
        dimensions        string     Optional          Indicates if the parameter is an array if set.  Dimesions
                                                       is of the format *[dim1,dim2,...]*
        choice_list       list       Optional          A list of available choices for the parameter input
        min               type       Optional          The minimum value allowed for the parameter
        max               type       Optional          The maximum value allowed for the parameter
        ================= ========== ================= ==========================================================

        :return: a list of parameter dictionaries
        """
        pass

    @abstractmethod
    def submit(self, parameters):
        """
        Submits a task to the server asynchronously

        :param parameters: A dictionary of key-value pairs of parameter names and values.  The dictionary serves as input to the job. 
        :return: GSF Job object
        """
        pass
