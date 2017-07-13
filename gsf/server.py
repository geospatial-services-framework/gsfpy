"""
The GSF server object is used to connect to the server and retrieve information about available services and jobs.

"""
from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from .gsfmeta import GSFMeta
from .utils import with_metaclass

class Server(with_metaclass(GSFMeta, object)):
    """
    The GSF server connection class.

     :Example:

     Import the modules for the example.
	 
     >>> from gsf import Server
	 
     Connect to the GSF server and print information.
	 
     >>> server = Server('localhost','9191')
     >>> print(type(server))
     <class 'gsf.ese.server.Server'>
     >>> print(server.name, type(server.name))
     ('localhost', <type 'str'>)
     >>> print(server.port, type(server.port))
     ('9191', <type 'str'>)
	 
     Investigate available services.
	 
     >>> services = server.services()
     >>> print(services, type(services))
     ([u'IDL', u'ENVI'], <type 'list'>)
	 
	 Investigate jobs on the GSF server.
	 
	 >>> job = server.job(1)
	 >>> print(job.results)


    """

    def __str__(self):
        props = dict(name=self.name,
                     port=self.port)
        return Template('''
name: ${name}
port: ${port}
''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __init__(self, server=None, port='9191'):
        """
        Returns the GSF Server object based on server and port.

        :param server: The server name as a string.
        :param port: The port number as a string.
        :return: GSF Server object
        """
        self._server = server
        self._port = port

    @abstractproperty
    def name(self):
        """
        Returns the server hostname.

        :return: a string
        """
        pass

    @abstractproperty
    def port(self):
        """
        Returns the server port number.

        :return: a string
        """

    @abstractmethod
    def services(self):
        """
        Returns a list of available services.

        :return: a list
        """
        pass

    @abstractmethod
    def service(self, service_name):
        """
        Returns the GSF Service object based on the service_name. See GSF Service for example.

        :param service_name: The service to connect to.
        :return: GSF Service object 
        """
        pass

    @abstractmethod
    def job(self, job_id):
        """
        Returns the GSF Job object based on the job_id. See GSF Job for more information.

        :param job_id: The job_id for which to retrieve job information.
        :return: GSF Job object
        """
        pass
