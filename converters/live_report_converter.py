from config.settings import DEFAULT_CITY_ORIGIN
from config.settings import REPORT_TYPE_ACCIDENT_CRASH
from config.settings import REPORT_TYPE_DEFAULT
from config.settings import DEFAULT_SUBTYPE

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
    live_report.location.city_origin = city_origin
    live_report.report_text.data_type = REPORT_TEXT_CONVERSION_MAP['type'][live_report.report_text.data_type] if live_report.report_text.data_type in REPORT_TEXT_CONVERSION_MAP['type'] else REPORT_TYPE_DEFAULT
    live_report.report_text.subtype = get_subtype(live_report)
    return live_report


def get_subtype(live_report):
    return REPORT_TEXT_CONVERSION_MAP['subtype'][live_report.report_text.subtype] if live_report.report_text.data_type == REPORT_TYPE_ACCIDENT_CRASH else DEFAULT_SUBTYPE