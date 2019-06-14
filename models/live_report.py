class ReportLocation(object):

    def __init__(self, lat, lng, street, city_origin):
        self.lat = lat
        self.lng = lng
        self.street = street
        self.city_origin = city_origin


class ReportText(object):

    def __init__(self, type, description, data_type, subtype):
        self.type = type
        self.description = description
        self.data_type = data_type
        self.subtype = subtype


class LiveReport(object):

    def __init__(self, sysid=None, creation_time=None, raw=None, city_origin=None):
        self.system_id = sysid
        self.uuid = raw['data']['uuid']

        self.creation_time = creation_time
        self.date_time = raw['date_time']

        self.reliability = raw['data']['reliability']
        self.pubMillis = raw['data']['pubMillis']
        self.confidence = raw['data']['confidence']

        self.report_text = ReportText(type=raw['type'],
                                      description=raw['data']['reportDescription'],
                                      data_type=raw['data']['type'],
                                      subtype=raw['data']['subtype'])

        self.location = ReportLocation(lat=raw['data']['location']['x'],
                                       lng=raw['data']['location']['y'],
                                       street=raw['data']['street'],
                                       city_origin=city_origin)

    @classmethod
    def load_live_report(cls, raw_report_dict):
        return cls(**raw_report_dict)

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
