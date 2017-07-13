"""
Defines exceptions for the GSF package.

"""


class ServerNotFoundError(Exception):
    """Exception gets raised when the user has passed in an incorrect net location (host:port).

    :Example:

    >>> from gsf import Server
    >>> server = Server('doesnotexist','9191')
    >>> print(server.services())
    # traceback information
    gsf.error.ServerNotFoundError: [Errno 11004] getaddrinfo failed

    """
    pass


class ServiceNotFoundError(Exception):
    """Exception gets raised when the user has passed in an incorrect service name.

    :Example:

    >>> from gsf import Server
    >>> server = Server('localhost','9191')
    >>> service = server.service('doesnotexist')
    >>> print(service.name)
    # traceback information
    gsf.error.ServiceNotFoundError: HTTP code 400, Reason: Bad Request

    """
    pass


class TaskNotFoundError(Exception):
    """Exception gets raised when the user has passed in an incorrect task name.

    :Example:

    >>> from gsf import Server
    >>> server = Server('localhost','9191')
    >>> service = server.service('ENVI')
    >>> task = service.task('doesnotexist')
    >>> print(task.name)
    # traceback information
    gsf.error.TaskNotFoundError: HTTP code 404, Reason: Not Found

    """
    pass


class JobNotFoundError(Exception):
    """Exception gets raised when the user has passed in an incorrect job number.

    :Example:

    >>> from gsf import Server
    >>> server = Server('localhost','9191')
    >>> job = server.job(-1) # job_id must be integer greater than 0
    >>> print(job.status)
    # traceback information
    gsf.error.JobNotFoundError: HTTP code: 404, Reason: Not Found
    """
    pass

