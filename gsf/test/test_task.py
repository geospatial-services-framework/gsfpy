"""
Tests the GSF Task interface
"""

import unittest


from gsf import Server
from gsf.task import Task
from gsf.job import Job
from gsf.error import TaskNotFoundError

from gsf.test import config
from gsf.test.util import assert_time_lt


class TestTask(unittest.TestCase):
    """
    Test the GSF Task interface
    """
    @classmethod
    def setUpClass(cls):
        cls.server = Server(config.GSF_SERVER['name'])
        cls.service = cls.server.service(config.GSF_SERVICE['name'])
        cls.task = cls.service.task(config.GSF_TASK['name'])

    @classmethod
    def tearDownClass(cls):
        pass

    @assert_time_lt(config.INIT_TIME)
    def test_init(self):
        """Verify the service method returns a GSF Task instance quickly."""
        task = self.service.task(config.GSF_TASK['name'])
        self.assertIsInstance(task, Task)

    def test_name(self):
        """Verify task.name returns a string."""
        self.assertIsInstance(self.task.name, str)

    def test_display_name(self):
        """Verify task display name returns a string."""
        self.assertIsInstance(self.task.display_name, str)

    def test_description(self):
        """Verify task description returns a string."""
        self.assertIsInstance(self.task.description, str)

    def test_parameters(self):
        """Verify task parameters returns a list with a parameter dictionary."""
        parameters = self.task.parameters
        self.assertIsInstance(parameters, list)
        for parameter in parameters:
            self.assertIsInstance(parameter['name'], str)
            self.assertIsInstance(parameter['display_name'], str)
            self.assertIsInstance(parameter['type'], str)
            self.assertRegexpMatches(parameter['direction'], '(input|output)')
            self.assertIsInstance(parameter['description'], str)
            self.assertIsInstance(parameter['required'], bool)

    def test_submit(self):
        """Verify a gsf task can be submitted, run, and succeeded."""
        job = self.task.submit(config.GSF_TASK['parameters'])
        self.assertIsInstance(job, Job)
        job.wait_for_done()
        self.assertEqual(job.status, 'Succeeded', 'Failed to submit Job')

    def test_invalid_task(self):
        """Verify an invalid task name throws an exception."""
        task = self.service.task('ehfaefehfeabr')
        with self.assertRaises(TaskNotFoundError):
            p = task.parameters
