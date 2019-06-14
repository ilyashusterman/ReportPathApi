class DatabaseException(Exception):

    def __init__(self, message, database_name):
        self.message = message
        self.database_name = database_name

