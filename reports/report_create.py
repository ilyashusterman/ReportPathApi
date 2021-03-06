import logging
from collections import namedtuple

from converters.live_report_converter import ReportConverter
from models.live_report import LiveReport

from reports.db_implementations.report_firebase_impl import ReportFireBaseImpl
from reports.db_implementations.report_mongo_impl import ReportMongoImpl


from config.settings import MAX_DATABASE_CREATION_ERRORS
from config.settings import NO_ERRORS_OCCURRED


CreateResponse = namedtuple('CreateResponse', ['errors_count', 'saved_ids', 'failed_databases'])


def get_report_db_implementations():
    #TODO should look for every class that inherit
    # from BaseReportDatabase class, instead for this hard coded if there are more to come
    return [ReportMongoImpl(), ReportFireBaseImpl()]


class ReportCreate(object):

    def __init__(self, max_creations_errors=MAX_DATABASE_CREATION_ERRORS, no_errors_occurred=NO_ERRORS_OCCURRED):
        self.max_creation_errors = max_creations_errors
        self.no_errors_occurred = no_errors_occurred

    def convert_and_create_one_report(self, live_report_dict):
        """
        Loading report dict to LiveReport Object
        Converts live_report to converted_live_report
        Creates converted_report to db
        :param live_report_dict:
        :return: create_response: CreateResponse, was_created_successfully: bool
        """
        parsed_report = LiveReport.load_live_report(live_report_dict)
        converted_report = ReportConverter.convert_live_report(parsed_report)
        create_response = self.create_one_report_to_databases(converted_report)
        return create_response, create_response.errors_count == self.no_errors_occurred

    def create_one_report_to_databases(self, live_report):
        """
        Creates the report for each database
        :param live_report:
        :return: error_count : int
        """
        errors_count = 0
        saved_ids = dict()
        failed_databases = list()
        for report_db_impl in get_report_db_implementations():
            try:
                inserted_id = report_db_impl.convert_and_create_report(live_report)
                logging.info('Created %s for db %s Successfully' % (inserted_id, report_db_impl.name))
                saved_ids[report_db_impl.name] = inserted_id
            except Exception as e:
                errors_count += 1
                logging.error('Could not save to %s error:%s report \n %s' % (report_db_impl.name, e, live_report.to_dict()))
                failed_databases.append(report_db_impl.name)
                if errors_count > self.max_creation_errors:
                    break
        return CreateResponse(errors_count=errors_count,
                              saved_ids=saved_ids,
                              failed_databases=failed_databases)
