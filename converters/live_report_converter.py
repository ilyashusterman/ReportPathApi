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


def convert_live_report(live_report, city_origin=DEFAULT_CITY_ORIGIN):
    """
    Convert:
    1. report dates_times
    2. report texts
    3. report locations
    :param live_report: LiveReport
    :param city_origin: str
    :return: LiveReport with converted and fixed attributes
    """
    live_report.creation_time = get_report_date_time(live_report.creation_time)
    live_report.date_time = get_report_date_time(live_report.date_time, REPORT_DATE_TIME_FORMAT)
    live_report.timestamp = live_report.date_time.second

    live_report.report_text = convert_report_text(live_report.report_text)

    live_report.location.city_origin = city_origin

    return live_report


def get_report_date_time(creation_time, report_date_format=CREATION_TIME_FORMAT):
    creation_datetime = datetime.strptime(creation_time, report_date_format)
    return creation_datetime


def convert_report_text(report_text):
    report_text.data_type = REPORT_TEXT_CONVERSION_MAP['type'][report_text.data_type] if report_text.data_type in REPORT_TEXT_CONVERSION_MAP['type'] else REPORT_TYPE_DEFAULT
    report_text.subtype = get_subtype(report_text)
    return report_text


def get_subtype(report_text):
    return REPORT_TEXT_CONVERSION_MAP['subtype'][report_text.subtype] if report_text.data_type == REPORT_TYPE_ACCIDENT_CRASH else DEFAULT_SUBTYPE
