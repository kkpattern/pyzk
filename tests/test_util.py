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
