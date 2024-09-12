import sys
from sqlalchemy import event
from sqlalchemy.engine import Engine

from core.constants.global_enum import LoggerName
from core.loggers import ConsoleLogger, AppLogger, loguru_logger


class LoggerManager:
    def __init__(self):
        self._loggers = {
            # LoggerName.CONSOLE: ConsoleLogger(),
            LoggerName.APP: AppLogger()
        }

        self.__set_global_exception_handler()

    def set_log_level(self, logger_name: LoggerName, level):
        if logger_name in self._loggers:
            self._loggers[logger_name].set_level(level)
        else:
            raise ValueError(f"Logger '{logger_name.value}' not found")

    def get_logger(self, logger_name: LoggerName) -> loguru_logger:
        if logger_name in self._loggers:
            return self._loggers[logger_name].get_logger()
        else:
            raise ValueError(f"Logger '{logger_name.value}' not found")

    def setup_sqlalchemy_logging(self, engine: Engine):
        sql_logger = self.get_logger(LoggerName.APP)

        @event.listens_for(engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            sql_logger.info(f"Executing SQL: {statement}")
            sql_logger.debug(f"Parameters: {parameters}")

        @event.listens_for(engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            sql_logger.info("SQL Execution complete")

        @event.listens_for(engine, "handle_error")
        def handle_error(context):
            sql_logger.error(f"SQL Error: {context.original_exception}")

    def __set_global_exception_handler(self):
        def exception_handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            self.get_logger(LoggerName.APP).error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = exception_handler


class LoggerType:
    # app_logger 에서 hint가 나오지 않아 type을 지정
    def debug(self, message: str, *args, **kwargs): ...
    def info(self, message: str, *args, **kwargs): ...
    def warning(self, message: str, *args, **kwargs): ...
    def error(self, message: str, *args, **kwargs): ...
    def critical(self, message: str, *args, **kwargs): ...
    def exception(self, message: str, *args, **kwargs): ...
    def log(self, level, message: str, *args, **kwargs): ...


# LoggerManager 인스턴스 생성
logger_manager = LoggerManager()
app_logger: LoggerType = logger_manager.get_logger(LoggerName.APP)

if __name__ == '__main__':
    app_logger.debug('Debug message for app logger')
    app_logger.info('Info message for app logger')
    app_logger.error('Error message for app logger')
    app_logger.exception('Exception message for app logger')
    app_logger.critical('Critical message for app logger')
