from datetime import datetime

from config.settings import DEFAULT_CITY_ORIGIN
from config.settings import REPORT_TYPE_ACCIDENT_CRASH
from config.settings import REPORT_TYPE_DEFAULT
from config.settings import DEFAULT_SUBTYPE
from config.settings import CREATION_TIME_FORMAT
from config.settings import REPORT_DATE_TIME_FORMAT

REPORT_TEXT_CONVERSION_MAP = {
    'type': {
        'ACCIDENT': REPORT_TYPE_ACCIDENT_CRASH,
        'ALL_OTHER': REPORT_TYPE_DEFAULT
    },
    'subtype': {
        'ACCIDENT_MAJOR': 'major',
        'ACCIDENT_MINOR': DEFAULT_SUBTYPE
    }
}


class ReportCalculations(object):
    """
    Responsible for all report metrics calculations and determination
    for values
    """
    @classmethod
    def calculate_report_accuracy(cls, live_report):
        better_reliability = live_report.reliability > 6
        confidence_reliability_multiplied = (live_report.confidence * live_report.reliability) > 20
        live_report.accurate = better_reliability and confidence_reliability_multiplied
        return live_report


class ReportConverter(object):

    @classmethod
    def convert_live_report(cls, live_report, city_origin=DEFAULT_CITY_ORIGIN):
        """
        Convert:
        1. report dates_times
        2. report texts
        3. report locations
        3. report calculations
        :param live_report: LiveReport
        :param city_origin: str
        :return: LiveReport with converted and fixed attributes
        """
        live_report.creation_time = cls.get_report_date_time(live_report.creation_time)
        live_report.date_time = cls.get_report_date_time(live_report.date_time, REPORT_DATE_TIME_FORMAT)
        live_report.timestamp = live_report.date_time.second

        live_report.report_text = cls.convert_report_text(live_report.report_text)

        live_report.location.city_origin = city_origin

        live_report.accurate = ReportCalculations.calculate_report_accuracy(live_report)
        return live_report

    @classmethod
    def get_report_date_time(cls, creation_time, report_date_format=CREATION_TIME_FORMAT):
        creation_datetime = datetime.strptime(creation_time, report_date_format)
        return creation_datetime

    @classmethod
    def convert_report_text(cls, report_text):
        report_text.data_type = REPORT_TEXT_CONVERSION_MAP['type'][report_text.data_type] if report_text.data_type in REPORT_TEXT_CONVERSION_MAP['type'] else REPORT_TYPE_DEFAULT
        report_text.subtype = cls.get_subtype(report_text)
        return report_text

    @classmethod
    def get_subtype(cls, report_text):
        return REPORT_TEXT_CONVERSION_MAP['subtype'][report_text.subtype] if report_text.data_type == REPORT_TYPE_ACCIDENT_CRASH else DEFAULT_SUBTYPE
