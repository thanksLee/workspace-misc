from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from core.loggers.manager import app_logger


class TransactionManager:
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory()
        self._app_logger = app_logger

    @contextmanager
    def get_transaction(self, external_session=None):
        # 만약 external_session이 제공되지 않았다면 새로운 세션을 생성
        session = external_session or self._session_factory
        new_transaction = external_session is None
        try:
            self._app_logger.info(f'Starting session: {session}')
            yield session
            # 여기서 트랜잭션 블록을 호출자에게 반환
            if new_transaction:
                session.commit()  # 새로운 트랜잭션인 경우 커밋
        except Exception as e:
            if new_transaction:
                session.rollback()  # 예외 발생 시 롤백
            self._app_logger.error(f'Session rollback due to exception: {e}')
            raise
        finally:
            if new_transaction:
                session.close()  # 새로운 트랜잭션인 경우 세션 종료
            self._app_logger.info(f'Closed session: {session}')

    def get_session(self) -> sessionmaker:
        return self._session_factory  # 새로운 세션을 생성하여 반환
