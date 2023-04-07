"""
Created on Jan 6, 2016

"""
import time
import unittest


from gsf.test.util import assert_time_lt
from gsf import Server
from gsf.server import Server as BaseServer
from gsf.error import ServerNotFoundError
from gsf.test import config


class TestServer(unittest.TestCase):
    """Tests the gsf server interface.."""

    @classmethod
    def setUpClass(cls):
        cls.server = Server(config.GSF_SERVER['name'])

    @classmethod
    def tearDownClass(cls):
        pass

    @assert_time_lt(config.INIT_TIME)
    def test_init(self):
        """Verify a server instance can be created quickly."""
        start_time = time.time()
        server = Server(config.GSF_SERVER['name'])
        self.assertIsInstance(server, BaseServer, 'server object does not implement gsf.Server')

    def test_services(self):
        """Verify services returns a list."""
        self.assertIsInstance(self.server.services(), list)

    def test_invalid_server(self):
        """Verify invalid host name throws an exception."""
        server = Server('fefabef')
        with self.assertRaises(ServerNotFoundError):
            services = server.services()

