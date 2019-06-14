import json
import logging

from reports.report_create import ReportCreate


class DataPathReportApi(object):

    def __init__(self):
        self.report_creator = ReportCreate()

    def create_report(self, raw_live_report):
        create_response, created_successfully = self.report_creator.convert_and_create_report(raw_live_report)
        return create_response, created_successfully

    def remove_report(self, live_report):
        """

        :param live_report: # LiveReport
        :return: if was removed successfully from all dependencies, used for tests
        """
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open('./input.json') as json_data:
        live_report_raw = json.load(json_data)
        logging.info('Raw Report \n %s' % json.dumps(live_report_raw, indent=2))
        datapath_api_handler = DataPathReportApi()
        create_response, did_created_successfully = datapath_api_handler.create_report(live_report_raw)
        logging.info('create_response %s' % create_response._asdict())
        logging.info('Was created successfully=%s' % did_created_successfully)







