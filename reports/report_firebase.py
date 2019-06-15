from jsonschema import validate, ValidationError

from reports.exceptions import ReportValidationException
from reports.report_base_db import BaseReportDatabase
from db.firebase.firebase_db import FireBaseDB

from config.settings import DEFAULT_FIREBASE_REPORT_WEATHER
from config.settings import DEFAULT_FIREBASE_REPORT_STATE

FIREBASE_REPORT_SCHEMA = {
    'type': 'object',
    'properties': {
        'color': {'type': 'string'},
        'state': {'type': 'string'},
        'title': {'type': 'string'},
        'subtitle': {'type': 'string'},
        'time': {'type': 'number'},
        'weather': {'type': 'string'},
        'location': {
            'type': 'object',
            'properties': {
                'lat': {'type': 'number'},
                'lng': {'type': 'number'}
            },
            'required': ['lat', 'lng']
        }
    },
    'required': ['color', 'state', 'title', 'subtitle', 'time', 'weather']
}


class ReportFireBaseImpl(BaseReportDatabase):

    def __init__(self):
        self.db = FireBaseDB()

    def validate_report(self, converted_report):
        self.validate_payload(converted_report)
        return True

    def validate_payload(self, payload):
        """
        Validating payload with json schema more information at
        https://json-schema.org/understanding-json-schema/
        raises ReportValidationException
        :param payload: dict
        :return: None
        """
        try:
            validate(instance=payload, schema=FIREBASE_REPORT_SCHEMA)
        except ValidationError as e:
            raise ReportValidationException(e)

    def get_converted_report(self, report):
        return {
            'color': 'red' if report.report_text.subtype == 'major' else 'orange',
            'title': '{} {}'.format(report.report_text.type.title(), report.report_text.subtype.title()),
            'subtitle': report.location.street,
            'time': report.creation_time.timestamp(),
            'weather': report.report_text.weather if hasattr(report.report_text, 'weather') else DEFAULT_FIREBASE_REPORT_WEATHER,
            'state': report.report_text.state if hasattr(report.report_text, 'state') else DEFAULT_FIREBASE_REPORT_STATE,
            'location': {
                'lat': report.location.lat,
                'lng': report.location.lng
            }
        }

    def create_report_to_db(self, converted_report):
        return self.db.save('reports', converted_report)
