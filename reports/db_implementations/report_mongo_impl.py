from db.mongo.mongodb_session import MongoDBSession
from reports.report_base_db import BaseReportDatabase

MONGO_REPORT_SCHEMA = {
    'type': 'object',
    'properties': {
        'time': {'type': 'number'},
        'source': {'type': 'string'},
        'id_in_source': {'type': 'string'},
        'user_id': {'type': 'string'},
        'detection': {'type': 'boolean'},
        'location': {
            'type': 'object',
            'properties': {
                'coordinates':
                    {
                        'type': 'object',
                        'properties': {
                         'lat': {'type': 'number'},
                         'lng': {'type': 'number'}
                        }
                    },
                'type': {'type': 'string'}
            },
            'required': ['lat', 'lng']
        }
    },
    'required': ['time', 'source', 'id_in_source', 'user_id', 'raw', 'location', 'detection']
}


class ReportMongoImpl(BaseReportDatabase):

    def __init__(self):
        self.db_session = MongoDBSession()

    def validate_report(self, converted_report):
        #TODO clarify more columns and constraints:
        # 1.important fields to validate if exist
        # 2.unique constraints for: system_id, uuid
        # 3.raw data model how dynamic is it?
        # validate(converted_report, MONGO_REPORT_SCHEMA)
        # throws ReportValidationException
        return True

    def convert_report(self, report):
        return report.to_dict()

    def create_db_report(self, converted_report):
        return self.db_session.save('reports', converted_report)
