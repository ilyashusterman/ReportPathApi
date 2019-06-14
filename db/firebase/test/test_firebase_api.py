from unittest import TestCase

from converters.live_report_converter import convert_live_report
from db.firebase.firebase_api import FireBaseDataBase
from models.live_report import LiveReport
from tests.test_datapath_report_api import get_mock_report


class TestFireBaseDataBase(TestCase):

    def setUp(self):
        self.firebase_db = FireBaseDataBase()

    def test_get_converted_report(self):
        report_dict_raw = get_mock_report()
        live_report = LiveReport.load_live_report(report_dict_raw)
        converted_report = convert_live_report(live_report)
        converted_report_firebase = self.firebase_db.get_converted_report(converted_report)
        self.assertIn('color', converted_report_firebase)
        self.assertIn('title', converted_report_firebase)
        self.assertIn('subtitle', converted_report_firebase)
        self.assertIn('time', converted_report_firebase)
        self.assertIsInstance(converted_report_firebase['time'], float)


