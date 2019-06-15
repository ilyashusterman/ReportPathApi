from abc import abstractmethod


class BaseDatabase(object):

    def convert_and_create_report(self, report):
        """
        Creates validated report to db # throws error if report is not valid
        :param report:
        :return: inserted_id
        """
        self.validate_report(report)
        converted_report = self.get_converted_report(report)
        return self.create_report_to_db(converted_report)

    @abstractmethod
    def validate_report(self, report):
        """
        Validate the report required attributes are initialized properly to
        be created in the database, throws # DatabaseException
        :param report: LiveReport
        :return: bool
        """
        raise NotImplementedError

    @abstractmethod
    def get_converted_report(self, report):
        """
        Modifies the ReportLive object for the specific DB
        :param report: LiveReport
        :return: LiveReport
        """
        raise NotImplementedError

    @abstractmethod
    def create_report_to_db(self, converted_report_dict):
        """
        Creates the converted report dict to the database
        throws # DatabaseException
        :param converted_report_dict: dict
        :return: the inserted_id # int/str for the database source row
        """
        raise NotImplementedError

    @property
    def name(self):
        """

        :return: name representation for the class implementing
        """
        return self.__class__.__name__
