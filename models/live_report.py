from models.parsers.live_report_parser import LiveReportParser


class LiveReport(object):

    def __init__(self, sysid=None, creation_time=None, raw=None, city_origin=None):
        #TODO clarify how dynamic LiveReport attributes could change:
        # 1.how many are minimal attributes? what should we expect
        # 2.more case scenarios of live_reports (need to make more json inputs)
        # if the class more dynamic then it should instance of Bunch or dynamic namedtuple for example
        # and other logic for Parse its attributes
        self.system_id = sysid
        self.raw = raw

        self.uuid = None

        self.creation_time = creation_time
        self.date_time = None
        self.timestamp = None

        self.reliability = None
        self.pubMillis = None
        self.confidence = None

        self.report_text = None  # :type : ReportText

        self.city_origin = city_origin
        self.location = None  # :type : ReportLocation

    @classmethod
    def load_live_report(cls, raw_report_dict):
        report_live = cls(**raw_report_dict)
        parsed_live_report = LiveReportParser.parse_live_report(report_live)
        return parsed_live_report

    def to_dict(self):
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
