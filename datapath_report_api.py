import json
import logging

from converters.live_report_converter import convert_live_report
from db.exceptions import DatabaseException
from models.live_report import LiveReport

from config.settings import MAX_DATABASE_CREATION_ERRORS
from config.settings import NO_ERRORS_OCCURRED
from db.config import DATABASES_API


class ReportCreate(object):

    def __init__(self, max_creations_errors=MAX_DATABASE_CREATION_ERRORS):
        self.max_creation_errors = max_creations_errors

    def convert_and_create_report(self, live_report):
        """
        converts  each live_report object to converted_report
        creates converted_report
        :param live_report:
        :return: was_created_successfully: bool
        """
        converted_report = convert_live_report(live_report)
        errors_count = self.create_report_to_databases(converted_report)
        return errors_count == NO_ERRORS_OCCURRED

    def create_report_to_databases(self, live_report):
        """
        creates the report for each database with its implementations
        :param live_report:
        :return: error_count : int for how many errors occured for counted databases
        """
        errors_count = 0
        for database_api in DATABASES_API:
            try:
                inserted_id = database_api.convert_and_create_report(live_report)
                logging.info('Created %s for db %s Successfully' % (inserted_id, database_api.name))
            except DatabaseException as e:
                errors_count += 1
                logging.error('Could not save to %s database error:%s report \n %s' % (database_api.name, e, live_report.to_json_string()))
                if errors_count > self.max_creation_errors:
                    break
        return errors_count


class DataPathReportApi(object):

    def __init__(self):
        self.report_creator = ReportCreate()

    def create_report(self, raw_live_report):
        live_report = LiveReport.load_live_report(raw_live_report)
        created_successfully = self.report_creator.convert_and_create_report(live_report)
        return live_report, created_successfully

    def remove_report(self, live_report):
        """

        :param live_report: # LiveReport
        :return: if was removed successfully from all dependencies
        """
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open('./input.json') as json_data:
        live_report_raw = json.load(json_data)
        logging.info('Raw Report \n %s' % json.dumps(live_report_raw, indent=2))
        datapath_api_handler = DataPathReportApi()
        live_report, did_created_successfully = datapath_api_handler.create_report(live_report_raw)
        logging.info('live_report %s' % live_report.to_json_string())
        logging.info('did_created_successfully=%s' % did_created_successfully)







