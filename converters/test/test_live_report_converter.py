import os
import json
from unittest import TestCase


from models.live_report import LiveReport
from converters.live_report_converter import convert_live_report

TEST_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), ''))


def load_json_file(filename):
    with open(os.path.join(TEST_PATH, filename), '+r') as f:
        return json.loads(f.read())


class TestLiveReportConverter(TestCase):

    def setUp(self):
        self.live_report = LiveReport.load_live_report(load_json_file('input_mock.json'))

    def test_convert_live_report_data_type_accident(self):
        self.live_report.report_text.data_type = 'ACCIDENT'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.data_type, 'crash')

    def test_convert_live_report_data_type_all_other(self):
        self.live_report.report_text.data_type = 'ALL_OTHER'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.data_type, 'incident')

    def test_convert_live_report_data_type_undefined(self):
        self.live_report.report_text.data_type = 'NOT_DEFINED_TEST'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.data_type, 'incident')

    def test_convert_live_report_subtype_crash_major(self):
        self.live_report.report_text.data_type = 'ACCIDENT'
        self.live_report.report_text.subtype = 'ACCIDENT_MAJOR'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.subtype, 'major')

    def test_convert_live_report_subtype_crash_minor(self):
        self.live_report.report_text.data_type = 'ACCIDENT'
        self.live_report.report_text.subtype = 'ACCIDENT_MINOR'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.subtype, 'minor')

    def test_convert_live_report_subtype_not_defined(self):
        self.live_report.report_text.data_type = 'NOT_DEFINED_TEST'
        converter_report = convert_live_report(self.live_report)
        self.assertEqual(converter_report.report_text.subtype, 'minor')
