# from firebase.firebase import FirebaseAuthentication
# from firebase.firebase import FirebaseApplication

from db.base_database import BaseDatabase
from db.exceptions import DatabaseException

# from config.settings import FIREBASE_URL
from config.settings import DEFAULT_FIREBASE_SECRET
from config.settings import DEFAULT_FIREBASE_EMAIL


class FireBaseDB(BaseDatabase):

    @classmethod
    def init_firebase_client(cls, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL,
                             debug=False, admin=True):
        """
        Initiating firebase client with parameters
        :param secret: str
        :param email: str
        :param debug: bool
        :param admin: bool
        :return: FirebaseApplication
        """
        # TODO finish implementing firebase with remote testing
        # authentication = FirebaseAuthentication(secret, email, debug, admin)
        # return FirebaseApplication(FIREBASE_URL, authentication)
        return dict()

    def __init__(self, secret=DEFAULT_FIREBASE_SECRET, email=DEFAULT_FIREBASE_EMAIL, debug=False, admin=True):
        self.client = self.init_firebase_client(secret, email, debug, admin)

    def save(self, table_name, payload):
        try:
            #TODO should check update/insert - merge command for mongo
            # if exist for unique keys then should modify/update else should insert
            return self.client.push(path='/%s' % table_name, data=payload)
        except Exception as e:
            raise DatabaseException(e, database_name=self.name)
