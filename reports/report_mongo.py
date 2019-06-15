from db.mongo.mongodb_base import MongoDBBase
from reports.report_base_db import BaseReportDatabase


class ReportMongoImpl(BaseReportDatabase):

    def __init__(self):
        self.db = MongoDBBase()

    def validate_report(self, report):
        return True

    def get_converted_report(self, report):
        return report.to_dict()

    def create_report_to_db(self, converted_report):
        return self.db.save('reports', converted_report)
