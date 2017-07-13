"""
Defines a Dict class that subclasses from the builtin dict so it can print the contents of
a dictionary in a human readable format.
"""

from pprint import PrettyPrinter


class Dict(dict):
    """Inherits the built-in dict object so it can pretty print."""

    pretty_print = PrettyPrinter(indent=2)

    def __str__(self):
        return self.pretty_print.pformat(dict(self))

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()
