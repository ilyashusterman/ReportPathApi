from db.test.DatabaseTestCase import TestDatabaseTestCase
from db.firebase.firebase_api import FireBaseDataBase
from db.exceptions import DatabaseException


class TestFireBaseDataBase(TestDatabaseTestCase):

    def setUp(self):
        super(TestFireBaseDataBase, self).setUp()
        self.firebase_db = FireBaseDataBase()

    def test_get_converted_report(self):
        converted_report_firebase = self.firebase_db.get_converted_report(self.converted_report)
        self.assertIn('color', converted_report_firebase)
        self.assertIn('title', converted_report_firebase)
        self.assertIn('subtitle', converted_report_firebase)
        self.assertIn('time', converted_report_firebase)
        self.assertIsInstance(converted_report_firebase['time'], float)

    def test_validate_report(self):
        self.assertTrue(self.firebase_db.validate_report(self.converted_report))

    def test_create_report_to_db(self):
        """
        should fail and raise DatabaseException
        because for test environment mongo db is not yet utilized
        :return:
        """
        with self.assertRaises(DatabaseException):
            converted_report_firebase = self.firebase_db.get_converted_report(self.converted_report)
            self.firebase_db.create_report_to_db(converted_report_firebase)