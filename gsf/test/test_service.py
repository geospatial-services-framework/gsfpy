
import unittest

from gsf.test.util import assert_time_lt
from gsf import Server
from gsf.service import Service
from gsf.test import config
from gsf.error import ServiceNotFoundError


class TestService(unittest.TestCase):
    """Tests the gsf service interface."""

    @classmethod
    def setUpClass(cls):
        cls.server = Server(config.GSF_SERVER['name'])
        cls.service = cls.server.service(config.GSF_SERVICE['name'])

    @classmethod
    def tearDownClass(cls):
        pass

    @assert_time_lt(config.INIT_TIME)
    def test_init(self):
        """Verify the service method returns a service instance quickly."""
        service = self.server.service(config.GSF_SERVICE['name'])
        self.assertIsInstance(service, Service, 'service object does not implement gsf.Service')

    def test_tasks(self):
        """Verify tasks returns a list."""
        task_list = self.service.tasks()
        self.assertIsInstance(task_list, list)

    def test_name(self):
        """Verify service name returns a string."""
        service_name = self.service.name
        self.assertIsInstance(service_name, str)

    def test_description(self):
        """Verify description returns a string."""
        self.assertIsInstance(self.service.description, str)

    def test_invalid_service(self):
        """Verify an invalid service throws an exception."""
        service = self.server.service('Rfaefhguh')
        with self.assertRaises(ServiceNotFoundError):
            service.tasks()
