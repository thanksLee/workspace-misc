from abc import ABC, abstractmethod

from core.loggers.logger_manager import app_logger


class BaseDatabaseManager(ABC):

    def __init__(self):
        self._app_logger = app_logger

    @abstractmethod
    def create_db(self):
        pass

    @abstractmethod
    def test_connection(self):
        pass
