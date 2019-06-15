
from unittest import TestCase

from config.settings import DEFAULT_REPORT_SYSTEM_ID
from config.settings import DEFAULT_REPORT_DESCRIPTION
from config.settings import DEFAULT_REPORT_LOCATION_DICT
from config.settings import DEFAULT_REPORT_CONFIDENCE
from config.settings import DEFAULT_REPORT_DATA_TYPE
from config.settings import REPORT_DEFAULT_STREET
from config.settings import DEFAULT_REPORT_RELIABILITY
from config.settings import DEFAULT_REPORT_SUB_TYPE
from config.settings import DEFAULT_REPORT_TYPE
from config.settings import DEFAULT_REPORT_SYSTEM_ID
from models.live_report import LiveReport
from models.parsers.live_report_parser import LiveReportParser
from tests.test_datapath_report_api import get_mock_report


class TestLiveReportParser(TestCase):

    def setUp(self) -> None:
        report_dict_raw = get_mock_report()
        self.live_report = LiveReport.load_live_report(report_dict_raw)

    def test_report_input_mock(self):
        report_dict_check = {
            'sysid': 'e347a32c-e0d7-45cc-98c1-6580033063e3',
            'creation_time': '2017-10-08T21:18:59.313Z',
            'raw': {
                'date_time': '08_10_2017 21:18:42 UTC',
                'type': 'waze_traffic_alerts_lv',
                'data': {
                    'subtype': 'ACCIDENT_MINOR',
                    'reliability': 7,
                    'pubMillis': 1507496096059,
                    'street': 'S Rainbow Blvd',
                    'type': 'ACCIDENT',
                    'location': {
                        'y': -115.242945,
                        'x': 36.116153
                    },
                    'confidence': 1,
                    'uuid': 'e62fa15b-f714-3739-8b29-00244ca25d69',
                    'reportDescription': ''
                }
            }
        }
        self.assertEqual(report_dict_check, self.live_report.to_dict())

    def test_empty_live_report_to_defaults(self):
        live_report = LiveReport()

        live_report_parsed = LiveReportParser.parse_live_report(live_report)
        report_dict_check = {
          'sysid': DEFAULT_REPORT_SYSTEM_ID,
          'creation_time': '2019-06-15T17:21:58.166Z',
          'raw': {
            'date_time': '15_06_2019 17:21:58 ',
            'type': DEFAULT_REPORT_TYPE,
            'data': {
              'subtype': DEFAULT_REPORT_SUB_TYPE,
              'reliability': DEFAULT_REPORT_RELIABILITY,
              'pubMillis': '',
              'street': REPORT_DEFAULT_STREET,
              'type': DEFAULT_REPORT_DATA_TYPE,
              'location': DEFAULT_REPORT_LOCATION_DICT,
              'confidence': DEFAULT_REPORT_CONFIDENCE,
              'uuid': '',
              'reportDescription': DEFAULT_REPORT_DESCRIPTION
            }
          }
        }
        report_live_dict_parsed = live_report_parsed.to_dict()
        """delete defaults dates do to mili seconds difference"""
        del report_dict_check['creation_time']
        del report_live_dict_parsed['creation_time']

        del report_dict_check['raw']['date_time']
        del report_live_dict_parsed['raw']['date_time']

        del report_live_dict_parsed['raw']['data']['uuid']
        del report_dict_check['raw']['data']['uuid']

        del report_live_dict_parsed['raw']['data']['pubMillis']
        del report_dict_check['raw']['data']['pubMillis']

        self.assertEqual(report_dict_check, report_live_dict_parsed)
