import sys
import os
from datetime import datetime
from loguru import logger as loguru_logger

from core.configs.configs import base_config


class BaseLogger:
    def __init__(self,
                 logger_level: str,
                 logger_format: str,
                 log_dir: str = None,
                 rotation: str = None,
                 retention: str = None,
                 prefix: str = None):
        self._base_log_dir = base_config.log_file_path
        self._log_dir = f'{self._base_log_dir}/{log_dir}' if log_dir else None
        self._rotation = rotation
        self._retention = retention
        self._logger_level = logger_level
        self._logger_format = logger_format
        self._prefix = prefix
        self._logger = loguru_logger

        self._handler_id = None
        self._initialize_logger()

    def _generate_log_file_path(self):
        # TODO :  좀더 고민이 필요함
        # now = datetime.now()
        # date_str = now.strftime('%Y/%m/%d')
        # time_str = now.strftime('%H%M')

        # directory = os.path.join(self._log_dir, date_str)
        # os.makedirs(directory, exist_ok=True)

        # return os.path.join(directory, f'{self._prefix}_{time_str}.log')

        return os.path.join(self._log_dir, f'{self._prefix}.log')

    def _initialize_logger(self):
        self.remove_handler()

        if self._log_dir:
            log_file = self._generate_log_file_path()
            self._handler_id = loguru_logger.add(sink=log_file,
                                                 rotation=self._rotation,
                                                 retention=self._retention,
                                                 level=self._logger_level,
                                                 format=self._logger_format,
                                                 encoding="utf-8",
                                                 backtrace=False,
                                                 enqueue=True,
                                                 catch=True)
        else:
            self._handler_id = loguru_logger.add(sys.stdout,
                                                 level=self._logger_level,
                                                 format=self._logger_format,
                                                 backtrace=False,
                                                 enqueue=True,
                                                 catch=True)

    def set_level(self, logger_level):
        self._logger_level = logger_level
        self._initialize_logger()

    def set_log_dir(self, log_dir):
        self._log_dir = log_dir
        self._initialize_logger()

    def remove_handler(self):
        if self._handler_id is not None:
            loguru_logger.remove(self._handler_id)

    def get_logger(self) -> loguru_logger:
        return self._logger
