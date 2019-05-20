from abc import ABC, abstractmethod


class BaseDBHandler(ABC):
    def __init__(self):
        self.db = None

    @abstractmethod
    def init_db(self, path: str):
        pass

    @abstractmethod
    def insert(self, data: dict):
        pass

    @abstractmethod
    def get(self, username: str):
        pass

    @abstractmethod
    def validate(self, data: dict):
        pass


class BaseHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self):
        pass
