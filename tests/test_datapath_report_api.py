import json
import os
from unittest import TestCase

from datapath_report_api import DataPathReportApi

TEST_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), ''))


def load_json_file(filename):
    with open(os.path.join(TEST_PATH, filename), '+r') as f:
        return json.loads(f.read())


def get_mock_report():
    return load_json_file('../input.json')


class TestDataPathReportApi(TestCase):

    def setUp(self):
        self.mock_live_report = get_mock_report()
        self.datapath_api_handler = DataPathReportApi()

    def test_create_live_report(self):
        create_response, did_created_successfully = self.datapath_api_handler.create_report(self.mock_live_report)
        self.assertTrue(did_created_successfully)
        self.datapath_api_handler.remove_report(self.mock_live_report)
