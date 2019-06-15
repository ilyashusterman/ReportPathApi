from db.mongo.mongodb_base import MongoDBBase
from reports.report_base_db import BaseReportDatabase


class ReportMongoImpl(BaseReportDatabase):

    def __init__(self):
        self.db = MongoDBBase()

    def validate_report(self, report):
        #TODO clarify more columns and constraints:
        # 1.important fields to validate if exist
        # 2.unique constraints for: system_id, uuid
        # 3.raw data model how dynamic is it?
        return True

    def get_converted_report(self, report):
        return report.to_dict()

    def create_report_to_db(self, converted_report):
        return self.db.save('reports', converted_report)
