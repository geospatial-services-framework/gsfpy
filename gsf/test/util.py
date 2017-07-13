
import time


def assert_time_lt(timeout):
    """
    decorator checks that method elapsed time is less than
    :param timeout:
    :return:
    """
    def test_timeout(func):

        def test_timeout_inner(self, *args, **kwargs):
            start_time = time.time()
            r = func(self, *args, **kwargs)
            elapsed_time = time.time() - start_time
            self.assertTrue(elapsed_time < timeout, 'Timeout exceeded')
            return r
        return test_timeout_inner
    return test_timeout
