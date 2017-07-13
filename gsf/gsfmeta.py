"""
GSF Metaclass for overriding string representations.
"""
from abc import ABCMeta


class GSFMeta(ABCMeta):
    """
    GSF Metaclass for overriding string representations.
    """
    def __repr__(self):
        return '{0}.{1}'.format(__package__, self.__name__)