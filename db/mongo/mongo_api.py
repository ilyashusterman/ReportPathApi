from pymongo import MongoClient

from db.base_database import BaseDatabase
from db.exceptions import DatabaseException


class MongoDataBase(BaseDatabase):

    def __init__(self, host='localhost', port=27017, database_name='test_database'):
        self.client = MongoClient(host=host, port=port, connect=False)
        self.connection_working = self.client is not None
        self.database_name = database_name
        self.db = self.client[self.database_name]

    def validate_report(self, report):
        return True

    def get_converted_report(self, report):
        return report.to_json_string()

    def create_report_to_db(self, converted_report):
        if self.is_connection_off():
            raise DatabaseException('Mongo couldnt connect to client db', self.database_name)
        return self.save('reports', converted_report)

    def is_connection_off(self):
        #TODO should check if mongo db connection is working or not
        return True

    def save(self, table_name, dict_entity):
        table = self.db[table_name]
        return table.insert(dict_entity).inserted_id
