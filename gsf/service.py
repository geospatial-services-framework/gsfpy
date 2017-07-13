"""
The GSF service object connects to a GSF Service and its tasks.
"""
from __future__ import absolute_import
from abc import abstractmethod, abstractproperty
from string import Template
from .gsfmeta import GSFMeta
from .utils import with_metaclass


class Service(with_metaclass(GSFMeta, object)):
    """
    The GSF Service connection class.

    :Example:
	
    Import the modules for the example.

    >>> from gsf import Server
    >>> from pprint import pprint
	
    Connect to the GSF server and the retrieve the ENVI service.
	
    >>> server = Server('localhost','9191')
    >>> service = server.service('ENVI')
    >>> print(type(service))
    <class 'gsf.ese.service.Service'>
	
    Investigate service information.
	
    >>> print(service.description, type(service.description))
    ('ENVI processing routines', <type 'str'>)
    >>> print(service.name, type(service.name))
    ('ENVI', <type 'str'>)
    >>> tasks = service.tasks()
    >>> pprint(tasks)
    ['AdditiveLeeAdaptiveFilter',
     'AdditiveMultiplicativeLeeAdaptiveFilter',
     'ApplyGainOffset',
	 ...
	
    """

    def __str__(self):
        props = dict(name=self.name,
                     description=self.description
                     )
        return Template('''
name: ${name}
description: ${description}
''').substitute(props)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    @abstractproperty
    def description(self):
        """
        Returns a description of the service

        :return: a string
        """
        pass

    @abstractproperty
    def name(self):
        """
        Returns the name of the service

        :return: a string
        """
        pass

    @abstractmethod
    def tasks(self):
        """
        Returns a list of task names available on this service

        :return: a list
        """
        pass

    @abstractmethod
    def task(self, task_name):
        """
        Returns a GSF task object. See GSF Task for example.

        :param: task_name: The name of the task to retrieve.
        :return: a GSF Task object
        """
        pass