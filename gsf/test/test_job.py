
import unittest

from gsf.test.util import assert_time_lt
from gsf import Server
from gsf.job import Job
from gsf.error import JobNotFoundError
from gsf.test import config


class TestJob(unittest.TestCase):
    """Tests the gsf job interface."""

    @classmethod
    def setUpClass(cls):
        cls.server = Server(config.GSF_SERVER['name'])
        cls.service = cls.server.service(config.GSF_SERVICE['name'])
        cls.task = cls.service.task(config.GSF_TASK['name'])
        cls.job = cls.task.submit(config.GSF_TASK['parameters'])
        cls.job.wait_for_done()

    @classmethod
    def tearDownClass(cls):
        pass

    @assert_time_lt(config.INIT_TIME)
    def test_init(self):
        """Verify the server returns a gsf job instance quickly."""
        job = self.server.job(self.job.job_id)
        self.assertIsInstance(job, Job)
        self.assertIsInstance(self.job, Job)

    def test_job_id(self):
        """Verify job id returns an int."""
        self.assertIsInstance(self.job.job_id, int)

    def test_status(self):
        """Verify status returns a string and success."""
        self.assertIsInstance(self.job.status, str)
        self.assertEqual(self.job.status, 'Succeeded')

    def test_progress(self):
        """Verify progress is an int between 0 and 100."""
        progress = self.job.progress
        self.assertIsInstance(progress, int)
        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 100)

    def test_progress_message(self):
        """Verify progress message is a string."""
        self.assertIsInstance(self.job.progress_message, str)

    def test_error_message(self):
        """Verify error message is a string."""
        self.assertIsInstance(self.job.error_message, str)

    def test_results(self):
        """Verify results returns a dictionary."""
        self.assertIsInstance(self.job.results, dict)

    def test_invalid_id(self):
        """Verify getting an invalid job id throws and exception."""
        job = self.server.job(-1)
        with self.assertRaises(JobNotFoundError):
            job.status
