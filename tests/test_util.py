import unittest
import pyzk.util

class TestProgress(unittest.TestCase):
    def test_default_value(self):
        progress = pyzk.util.Progress()
        assert progress.current_value == 0
        assert progress.max_value == 100

    def test_change_value(self):
        progress = pyzk.util.Progress(current_value=0, max_value=100)
        progress += 3
        assert progress.current_value == 3
        progress -= 1
        assert progress.current_value == 2
        progress += (progress.max_value+1)
        assert progress.current_value == progress.max_value
        progress -= (progress.current_value+1)
        assert progress.current_value == 0

    def test_show(self):
        progress = pyzk.util.Progress(current_value=1.1, max_value=100)
        assert float(progress)*100 == 1.1
        assert str(progress) == r"1.1%"

class MockExceptionHandler(object):
    def __init__(self):
        self.call_count = 0
    def __call__(self, a, b):
        self.call_count += 1

def mock_target():
    raise IOError("Mock IOError")

class TestRetry(unittest.TestCase):
    def test_basic(self):
        MAX_RETRY = 6
        mock_exception_handler = MockExceptionHandler()
        target_with_retry = pyzk.util.Retry(
            mock_target,
            MAX_RETRY,
            mock_exception_handler)
        try:
            target_with_retry()
        except IOError:
            pass
        assert mock_exception_handler.call_count == MAX_RETRY-1
