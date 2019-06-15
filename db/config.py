from db.firebase.firebase_api import FireBaseDataBase
from db.mongo.mongo_api import MongoDataBase


def get_databases():
    return [MongoDataBase(), FireBaseDataBase()]
