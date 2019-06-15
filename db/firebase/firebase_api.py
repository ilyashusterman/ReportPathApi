# from firebase.firebase import FirebaseAuthentication
# from firebase.firebase import FirebaseApplication

from db.base_database import BaseDatabase
from db.exceptions import DatabaseException
from jsonschema import validate

# from config.settings import FIREBASE_URL
from config.settings import DEFAULT_FIREBASE_SECRET
from config.settings import DEFAULT_FIREBASE_EMAIL
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


class FireBaseDataBase(BaseDatabase):

    @classmethod
    def init_firebase_client(cls, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL,
                             debug=False, admin=True):
        """
        initiating firebase client with parameters
        :param secret: str
        :param email: str
        :param debug: bool
        :param admin: bool
        :return:
        """
        # TODO finish implementing firebase with remote testing
        # authentication = FirebaseAuthentication(secret, email, debug, admin)
        # return FirebaseApplication(FIREBASE_URL, authentication)
        return dict()

    def __init__(self, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL, debug=False, admin=True):
        self.client = self.init_firebase_client(secret, email, debug, admin)

    def validate_report(self, report):
        #TODO
        #  no input validation needed for now
        return True

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
        self.validate_payload(converted_report)
        return self.save(converted_report)

    def validate_payload(self, payload):
        validate(instance=payload, schema=FIREBASE_REPORT_SCHEMA)

    def save(self, payload: dict):
        try:
            #TODO should check update/insert - merge command for mongo
            # if exist for unique keys then should modify/update else should insert
            return self.client.push(path='/reports', data=payload)
        except Exception as e:
            raise DatabaseException(e, database_name=self.name)
