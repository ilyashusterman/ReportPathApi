import logging
from collections import namedtuple

from models.live_report import LiveReport
from converters.live_report_converter import convert_live_report
from db.exceptions import DatabaseException

from db.config import get_databases
from config.settings import MAX_DATABASE_CREATION_ERRORS
from config.settings import NO_ERRORS_OCCURRED


CreateResponse = namedtuple('CreateResponse', ['errors_count', 'databases', 'failed_databases'])


class ReportCreate(object):

    def __init__(self, max_creations_errors=MAX_DATABASE_CREATION_ERRORS, no_errors_occurred=NO_ERRORS_OCCURRED):
        self.max_creation_errors = max_creations_errors
        self.no_errors_occurred = no_errors_occurred

    def convert_and_create_report(self, live_report_dict):
        """
        converts  each live_report object to converted_report
        creates converted_report
        :param live_report:
        :return: was_created_successfully: bool
        """
        parsed_report = LiveReport.load_live_report(live_report_dict)
        converted_report = convert_live_report(parsed_report)
        create_response = self.create_report_to_databases(converted_report)
        return create_response, create_response.errors_count == self.no_errors_occurred

    def create_report_to_databases(self, live_report):
        """
        creates the report for each database with its implementations
        :param live_report:
        :return: error_count : int for how many errors occured for counted databases
        """
        errors_count = 0
        databases_response = dict()
        failed_databases = list()
        for database_api in get_databases():
            try:
                inserted_id = database_api.convert_and_create_report(live_report)
                logging.info('Created %s for db %s Successfully' % (inserted_id, database_api.name))
                databases_response[database_api.name] = inserted_id
            except DatabaseException as e:
                errors_count += 1
                logging.error('Could not save to %s database error:%s report \n %s' % (database_api.name, e, live_report.to_json_string()))
                failed_databases.append(database_api.name)
                if errors_count > self.max_creation_errors:
                    break
        return CreateResponse(errors_count=errors_count,
                              databases=databases_response,
                              failed_databases=failed_databases)
