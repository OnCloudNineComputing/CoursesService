from abc import ABC, abstractmethod


class BaseDataException(Exception):

    def __init__(self):
        pass


class BaseDataResource(ABC):

    def __init__(self):
        pass

    @abstractmethod
    @classmethod
    def get_db_connection(cls):
        pass


