from unittest import TestCase

from converters.live_report_converter import ReportConverter
from models.live_report import LiveReport
from tests.test_datapath_report_api import get_mock_report


class TestDatabaseTestCase(TestCase):

    def setUp(self):
        report_dict_raw = get_mock_report()
        live_report = LiveReport.load_live_report(report_dict_raw)
        self.converted_report = ReportConverter.convert_live_report(live_report)
