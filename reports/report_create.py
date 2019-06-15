import logging
from collections import namedtuple

from models.live_report import LiveReport
from converters.live_report_converter import convert_live_report
from reports.report_firebase import ReportFireBaseImpl
from reports.report_mongo import ReportMongoImpl

from db.exceptions import DatabaseException


from config.settings import MAX_DATABASE_CREATION_ERRORS
from config.settings import NO_ERRORS_OCCURRED


CreateResponse = namedtuple('CreateResponse', ['errors_count', 'databases', 'failed_databases'])


def get_report_db_implementations():
    return [ReportMongoImpl(), ReportFireBaseImpl()]


class ReportCreate(object):

    def __init__(self, max_creations_errors=MAX_DATABASE_CREATION_ERRORS, no_errors_occurred=NO_ERRORS_OCCURRED):
        self.max_creation_errors = max_creations_errors
        self.no_errors_occurred = no_errors_occurred

    def convert_and_create_report(self, live_report_dict):
        """
        Loading report dict to LiveReport Object
        Converts live_report to converted_live_report
        Creates converted_report to db
        :param live_report_dict:
        :return: create_response: CreateResponse, was_created_successfully: bool
        """
        parsed_report = LiveReport.load_live_report(live_report_dict)
        converted_report = convert_live_report(parsed_report)
        create_response = self.create_report_to_databases(converted_report)
        return create_response, create_response.errors_count == self.no_errors_occurred

    def create_report_to_databases(self, live_report):
        """
        Creates the report for each database
        :param live_report:
        :return: error_count : int
        """
        errors_count = 0
        databases_response = dict()
        failed_databases = list()
        for report_db_impl in get_report_db_implementations():
            try:
                inserted_id = report_db_impl.convert_and_create_report(live_report)
                logging.info('Created %s for db %s Successfully' % (inserted_id, report_db_impl.name))
                databases_response[report_db_impl.name] = inserted_id
            except DatabaseException as e:
                errors_count += 1
                logging.error('Could not save to %s database error:%s report \n %s' % (report_db_impl.name, e, live_report.to_dict()))
                failed_databases.append(report_db_impl.name)
                if errors_count > self.max_creation_errors:
                    break
        return CreateResponse(errors_count=errors_count,
                              databases=databases_response,
                              failed_databases=failed_databases)
