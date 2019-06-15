import logging
import uuid
from datetime import datetime

from models.report_location import ReportLocation
from models.report_text import ReportText

from config.settings import REPORT_DATE_TIME_FORMAT
from config.settings import CREATION_TIME_FORMAT
from config.settings import DEFAULT_REPORT_RELIABILITY
from config.settings import DEFAULT_REPORT_CONFIDENCE
from config.settings import DEFAULT_REPORT_SYSTEM_ID
from config.settings import DEFAULT_REPORT_TYPE
from config.settings import DEFAULT_REPORT_DESCRIPTION
from config.settings import DEFAULT_REPORT_DATA_TYPE
from config.settings import DEFAULT_REPORT_SUB_TYPE
from config.settings import DEFAULT_REPORT_LOCATION_DICT
from config.settings import REPORT_DEFAULT_X
from config.settings import REPORT_DEFAULT_Y
from config.settings import REPORT_DEFAULT_STREET


class LiveReportParser(object):
    """
    LiveReportParser is responsible for giving default attributes if attributes
    was initialized with None from the raw input
    """
    @classmethod
    def parse_live_report(cls, live_report):
        default_report_date = cls.get_default_time()
        live_report = cls.set_none_to_defaults(live_report, default_report_date)
        if 'data' not in live_report.raw:
            live_report.raw['data'] = dict()
            logging.info('raw attribute does not contain "data" attribute for %s sysid' % live_report.system_id)

        live_report.uuid = live_report.raw['data'].get('uuid', uuid.uuid4().hex)
        live_report.date_time = live_report.raw.get('date_time', default_report_date.strftime(REPORT_DATE_TIME_FORMAT))
        live_report.pubMillis = live_report.raw['data'].get('pubMillis', default_report_date.timestamp())

        live_report.reliability = live_report.raw['data'].get('reliability', DEFAULT_REPORT_RELIABILITY)
        live_report.confidence = live_report.raw['data'].get('confidence', DEFAULT_REPORT_CONFIDENCE)

        live_report = cls.parse_report_text(live_report)
        live_report = cls.parse_locations(live_report)

        return live_report

    @classmethod
    def get_default_time(cls):
        return datetime.utcnow()

    @classmethod
    def set_none_to_defaults(cls, live_report, default_report_date=datetime.utcnow()):
        live_report.raw = dict() if live_report.raw is None else live_report.raw
        live_report.creation_time = live_report.creation_time if live_report.creation_time is not None else default_report_date.strftime(CREATION_TIME_FORMAT)
        live_report.system_id = live_report.system_id if live_report.system_id is not None else DEFAULT_REPORT_SYSTEM_ID
        return live_report

    @classmethod
    def parse_report_text(cls, live_report):
        live_report.report_text = ReportText(
            type=live_report.raw.get('type', DEFAULT_REPORT_TYPE),
            description=live_report.raw['data'].get('reportDescription', DEFAULT_REPORT_DESCRIPTION),
            data_type=live_report.raw['data'].get('type',  DEFAULT_REPORT_DATA_TYPE),
            subtype=live_report.raw['data'].get('subtype', DEFAULT_REPORT_SUB_TYPE)
        )
        return live_report

    @classmethod
    def parse_locations(cls, live_report):
        location_dict = live_report.raw['data'].get(
            'location', DEFAULT_REPORT_LOCATION_DICT
        )
        live_report.location = ReportLocation(
            lat=location_dict.get('x', REPORT_DEFAULT_X),
            lng=location_dict.get('y', REPORT_DEFAULT_Y),
            street=live_report.raw['data'].get('street', REPORT_DEFAULT_STREET),
            city_origin=live_report.city_origin
        )
        return live_report
