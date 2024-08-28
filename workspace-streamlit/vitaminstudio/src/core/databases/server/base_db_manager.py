from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from core.loggers.logger_manager import app_logger, logger_manager


class DBConfig(BaseModel):
    database_url: str
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 1800
    pool_pre_ping: bool = True
    echo: bool = False


class BaseDBManager:
    def __init__(self, db_type: str, config: DBConfig):
        self._db_type = db_type
        self._config = config
        self._engine = None
        self._session_factory = None
        self._app_logger = app_logger

    def initialize(self):
        self._engine = create_engine(
            url=self._config.database_url,
            pool_size=self._config.pool_size,
            max_overflow=self._config.max_overflow,
            pool_timeout=self._config.pool_timeout,
            pool_recycle=self._config.pool_recycle,
            pool_pre_ping=self._config.pool_pre_ping,
            echo=self._config.echo
        )
        self._session_factory = sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)
        self._app_logger.debug(f'Database {self._db_type} initialized with engine: {self._engine}')
        self._app_logger.debug(f'session_factory: {self._session_factory}')

        logger_manager.setup_sqlalchemy_logging(self._engine)

    def close(self):
        if self._engine:
            self._engine.dispose()
            self._app_logger.debug(f'Engine {self._engine} disposed.')

    def get_session(self):
        return self._session_factory()

    @property
    def get_session_factory(self):
        return self._session_factory


# Create the base class for declarative models
Base = declarative_base()
