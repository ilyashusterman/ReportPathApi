from abc import abstractmethod


class BaseDatabase(object):

    def convert_and_create_report(self, report):
        """
        creates validated report to db # throws error if report is not valid
        :param report:
        :return: inserted_id
        """
        self.validate_report(report)
        converted_report = self.get_converted_report(report)
        return self.create_report_to_db(converted_report)

    @abstractmethod
    def validate_report(self, report):
        """
        validate the report if the report entity requires the parameters to
        be created in the database, throws # DatabaseException
        :param report:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_converted_report(self, report):
        """
        convert the report entity for the raw dict that require to be created
        with its specific attributes
        :param report: # LiveReport object
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def create_report_to_db(self, converted_report):
        """
        this method must be overridden for each database implementing for creating
        report entity
        :param report: # converted_report dict
        :return: the inserted_id # int/str for the database source row
        """
        raise NotImplementedError

    @property
    def name(self):
        """

        :return: name representation for the class
        """
        return self.__class__.__name__
