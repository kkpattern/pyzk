import logging
import unittest

import pyzk.loggingx

class MockRecord(object):
    def __init__(self, levelno):
        self.levelno = levelno

class TestSingleLevelFilter(unittest.TestCase):
    def test_basic(self):
        info_record = MockRecord(logging.INFO)
        debug_record = MockRecord(logging.DEBUG)
        warning_record = MockRecord(logging.WARNING)
        error_record = MockRecord(logging.ERROR)
        critical_record = MockRecord(logging.CRITICAL)

        only_warning_filter = pyzk.loggingx.SingleLevelFilter(
            logging.WARNING, True)
        assert only_warning_filter.filter(info_record) == False
        assert only_warning_filter.filter(debug_record) == False
        assert only_warning_filter.filter(warning_record) == True
        assert only_warning_filter.filter(error_record) == False
        assert only_warning_filter.filter(critical_record) == False

        no_warning_filter = pyzk.loggingx.SingleLevelFilter(
            logging.WARNING, False)
        assert no_warning_filter.filter(info_record) == True
        assert no_warning_filter.filter(debug_record) == True
        assert no_warning_filter.filter(warning_record) == False
        assert no_warning_filter.filter(error_record) == True
        assert no_warning_filter.filter(critical_record) == True
