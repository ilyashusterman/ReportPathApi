from reports.report_mongo import ReportMongoImpl
from db.test.DatabaseTestCase import TestDatabaseTestCase


class TestMongoDataBase(TestDatabaseTestCase):

    def setUp(self):
        super(TestMongoDataBase, self).setUp()
        self.mongo_db = ReportMongoImpl()

    def test_validate_report(self):
        self.assertTrue(self.mongo_db.validate_report(self.converted_report))

    def test_is_connection_off(self):
        """
        for now the database for test environment shoudl be off
        :return:
        """
        self.assertTrue(self.mongo_db.db.is_connection_off())

    def test_get_converted_report(self):
        converted_report_mongo = self.mongo_db.get_converted_report(self.converted_report)
        self.assertSequenceEqual(converted_report_mongo.keys(), self.converted_report.to_dict().keys())