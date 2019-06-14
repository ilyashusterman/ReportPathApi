# from firebase.firebase import FirebaseAuthentication
# from firebase.firebase import FirebaseApplication

from db.base_database import BaseDatabase
from models.live_report import ReportLocation

from config.settings import FIREBASE_URL
from config.settings import DEFAULT_FIREBASE_SECRET
from config.settings import DEFAULT_FIREBASE_EMAIL
from config.settings import DEFAULT_FIREBASE_REPORT_WEATHER
from config.settings import DEFAULT_FIREBASE_REPORT_STATE


class FireBaseDataBase(BaseDatabase):

    @classmethod
    def init_firebase_client(cls, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL,
                             debug=False, admin=True):
        """
        initiating firebase client with parameters
        :param secret:
        :param email:
        :param debug:
        :param admin:
        :return:
        """
        # authentication = FirebaseAuthentication(secret, email, debug, admin)
        # return FirebaseApplication(FIREBASE_URL, authentication)
        return dict()

    def __init__(self, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL, debug=False, admin=True):
        self.client = self.init_firebase_client(secret, email, debug, admin)

    def validate_report(self, report):
        pass

    def get_converted_report(self, report):
        return {
            'color': 'red' if report.report_text.subtype == 'major' else 'orange',
            'title': '{} {}'.format(report.report_text.type.title(), report.report_text.subtype.title()),
            'subtitle': report.location.street,
            'time': '{} {}'.format(report.report_text.type.title(), report.report_text.subtype.title()),
            'weather': report.report_text.weather if hasattr(report.report_text, 'weather') else DEFAULT_FIREBASE_REPORT_WEATHER,
            'state': report.report_text.state if hasattr(report.report_text, 'state') else DEFAULT_FIREBASE_REPORT_STATE,
            'location': report.location
        }

    def create_report_to_db(self, converted_report):
        self.push_firebase(**converted_report)

    def push_firebase(self, color: str, location: ReportLocation, state: str, title: str, subtitle: str, time: float, weather: str):
        payload = {
            'color': color,
            'location': {
                'lat': location.lat,
                'lng': location.lng
            },
            'state': state,
            'subtitle': subtitle,
            'time': time,
            'title': title,
            'weather': weather
        }
        """
        saving dict object to firebase with (path, payload)
        """
        self.client.push(path='/reports', data=payload)
