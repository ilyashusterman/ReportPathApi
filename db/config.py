from db.firebase.firebase_api import FireBaseDataBase
from db.mongo.mongo_api import MongoDataBase

DATABASES_API = [MongoDataBase(), FireBaseDataBase()]