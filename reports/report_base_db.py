from abc import abstractmethod

from db.base_database import BasicDB


class BaseReportDatabase(BasicDB):
    """
    Responsible for persisting report to its implementing instance
    """
    def convert_and_create_report(self, report):
        """
        Creates validated report to db # throws error if report is not valid
        :param report:
        :return: inserted_id
        """
        converted_report = self.convert_report(report)
        self.validate_report(converted_report)
        return self.create_db_report(converted_report)

    @abstractmethod
    def validate_report(self, converted_report):
        """
        Validate the report required attributes are initialized properly to
        be created in the database, throws # DatabaseException
        :param report: LiveReport
        :return: bool
        """
        raise NotImplementedError

    @abstractmethod
    def convert_report(self, report):
        """
        Modifies the ReportLive object for the specific DB
        :param report: LiveReport
        :return: LiveReport
        """
        raise NotImplementedError

    @abstractmethod
    def create_db_report(self, converted_report_dict):
        """
        Creates the converted report dict to the database
        throws # DatabaseException
        :param converted_report_dict: dict
        :return: the inserted_id # int/str for the database source row
        """
        raise NotImplementedError
