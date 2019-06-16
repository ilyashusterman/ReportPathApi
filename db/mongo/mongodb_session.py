from pymongo import MongoClient

from db.base_database import DatabaseSession
from db.exceptions import DatabaseException

from config.settings import MONGODB_HOST
from config.settings import MONGODB_PORT
from config.settings import MONGODB_NAME


class MongoDBSession(DatabaseSession):

    def __init__(self, host=MONGODB_HOST, port=MONGODB_PORT, database_name=MONGODB_NAME):
        self.client = MongoClient(host=host, port=port, connect=False)
        self.connection_working = self.client is not None
        self.database_name = database_name
        self.db = self.client[self.database_name]

    def save(self, table_name, dict_payload):
        if self.is_connection_off():
            raise DatabaseException('Could not connect to MongoClient ',self.database_name)
        #TODO should check update/insert - merge command for mongo
        # if exist for unique keys then should modify/update else should insert
        table = self.db[table_name]
        return table.insert(dict_payload).inserted_id

    def is_connection_off(self):
        # TODO should check if mongo db connection is working or not
        return True
