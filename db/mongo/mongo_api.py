from pymongo import MongoClient

from db.base_database import BaseDatabase


class MongoDataBase(BaseDatabase):

    def __init__(self, host='localhost', port=27017, database='test_database'):
        self.client = MongoClient(host=host, port=port, connect=False)
        self.db = self.client[database]

    def validate_report(self, report):
        pass

    def get_converted_report(self, report):
        return report.to_json_string()

    def create_report_to_db(self, converted_report):
        converted_report_dict = {}
        self.save('reports', converted_report_dict)

    def save(self, table_name, dict_entity):
        table = self.db[table_name]
        return table.insert(dict_entity).inserted_id
