from core.configs.configs import console_logger_config, app_logger_config

from core.loggers.base_logger import BaseLogger, loguru_logger


class ConsoleLogger(BaseLogger):
    def __init__(self):
        super().__init__(logger_level=console_logger_config.level,
                         logger_format=console_logger_config.format)


class AppLogger(BaseLogger):
    def __init__(self):
        super().__init__(logger_level=app_logger_config.level,
                         logger_format=app_logger_config.format,
                         log_dir="app",
                         rotation=app_logger_config.rotation,
                         retention=app_logger_config.retention,
                         prefix="vitamin")

    def get_app_logger(self) -> loguru_logger:
        return super().get_logger()
