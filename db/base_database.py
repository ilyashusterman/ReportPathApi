from abc import abstractmethod


class BasicDB(object):

    @property
    def name(self):
        """

        :return: str
        """
        return self.__class__.__name__


class BaseDatabase(BasicDB):

    @abstractmethod
    def save(self, table_name: str, dict_payload: dict):
        """
        save payload dict to table name
        :param table_name: str
        :param dict_payload: dict
        :return: inserted_id
        """
        raise NotImplementedError
