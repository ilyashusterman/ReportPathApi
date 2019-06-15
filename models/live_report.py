from models.report_location import ReportLocation
from models.report_text import ReportText


class LiveReport(object):

    def __init__(self, sysid=None, creation_time=None, raw=None, city_origin=None):
        self.system_id = sysid
        self.raw = dict() if raw is None else raw

        self.uuid = None

        self.creation_time = creation_time
        self.date_time = None

        self.reliability = None
        self.pubMillis = None
        self.confidence = None

        self.report_text = None

        self.raw['city_origin'] = city_origin
        self.location = None

    def parse_raw(self):
        self.uuid = self.raw['data']['uuid']
        self.date_time = self.raw['date_time']

        self.reliability = self.raw['data']['reliability']
        self.pubMillis = self.raw['data']['pubMillis']
        self.confidence = self.raw['data']['confidence']

        self.report_text = ReportText(type=self.raw['type'],
                                      description=self.raw['data']['reportDescription'],
                                      data_type=self.raw['data']['type'],
                                      subtype=self.raw['data']['subtype'])

        self.location = ReportLocation(lat=self.raw['data']['location']['x'],
                                       lng=self.raw['data']['location']['y'],
                                       street=self.raw['data']['street'],
                                       city_origin=self.raw['city_origin'])

    @classmethod
    def load_live_report(cls, raw_report_dict):
        report_live = cls(**raw_report_dict)
        report_live.parse_raw()
        return report_live

    def to_json_string(self):
        return {
            'sysid': self.system_id,
            'creation_time': self.creation_time,
            'raw': {
                'date_time': self.date_time,
                'type': self.report_text.type,
                'data': {
                    'subtype': self.report_text.subtype,
                    'reliability': self.reliability,
                    'pubMillis': self.pubMillis,
                    'street': self.location.street,
                    'type': self.report_text.data_type,
                    'location': {
                        'y': self.location.lat,
                        'x': self.location.lng
                    },
                    'confidence': self.confidence,
                    'uuid': self.uuid,
                    'reportDescription': self.report_text.description
                }
            }
        }
