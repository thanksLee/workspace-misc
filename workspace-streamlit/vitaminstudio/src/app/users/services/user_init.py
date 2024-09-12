from sqlalchemy import text
from typing import Optional

from common.services import CommonService
from common.services.common_code import CommonCodeService

from core.configs.base import base_config
from core.utilities.files import get_file_list, load_sql_file
from core.exceptions import ExistsDatabase
from core.sessions.schemas.current_db_conn import CurrentDBConnSchema
from core.databases.server.transaction_manager import TransactionManager
from core.constants.global_enum import ServerType
from core.constants import CURRENT_DB_CONN

from app.users.mappers import UserMapper


class UserInitService(CommonService):
    def __init__(self, tr_manager: TransactionManager):
        super().__init__(tr_manager)

    def sql_file_execute(self, db_type: str, db_schema: str):
        ret_val = self._vs_msg.VS_SUCCESS_001.value
        try:
            # 테이블 존재 여부 확인
            table_exists = self.get_table_exists(db_type, db_schema) is not None

            if not table_exists:
                # 테이블이 없을 경우 먼저 SQL 파일을 실행하여 테이블을 생성
                self.execute_sql_files(db_type)

            # 공통 코드를 메모리에 로드
            self.load_common_code_to_memory()

            # DB 연결 정보 설정
            self.set_db_conn_info()

            if table_exists:
                # 테이블이 존재하는 경우 예외를 발생시킴
                raise ExistsDatabase(f'{self._vs_msg.VS_SUCCESS_002.name} : {self._vs_msg.VS_SUCCESS_002.value}')

        except ExistsDatabase as edb:
            self._app_logger.info(edb)
            raise
        except Exception as ex:
            self._app_logger.error(ex)
            raise

        return ret_val

    def load_common_code_to_memory(self):
        """공통 코드를 로드하는 메서드."""
        CommonCodeService(self._tr_manager).load_and_set_memory()

    def execute_sql_files(self, db_type: str):
        """SQL 파일을 읽어와 실행하는 메서드."""
        sql_file_path = f'{base_config.sql_file_path}/{db_type}'
        sql_file_list = get_file_list(sql_file_path)

        for sql_file in sql_file_list:
            query_list = load_sql_file(f'{sql_file_path}/{sql_file}')
            with self._tr_manager.get_transaction() as tran_session:
                for query_statement in query_list:
                    try:
                        # self._app_logger.debug(f'Executing SQL statement: {query_statement}')
                        tran_session.execute(text(query_statement))
                    except Exception as e:
                        self._app_logger.error(f'SQL loader failed: {e}')
                        raise

    def get_table_exists(self, db_type: str, db_schema: str) -> Optional[dict]:
        """특정 테이블이 존재하는지 확인하는 메서드."""
        ret_val: Optional[dict] = None
        with self._tr_manager.get_transaction() as tran_session:
            qry_result = UserMapper(tran_session).select_table_exists_check(db_type, db_schema)

        if qry_result._mapping['table_cnt'] > 0:
            self._app_logger.debug(f"Table count: {qry_result._mapping['table_cnt']}")
            return qry_result._mapping

        return ret_val

    def set_db_conn_info(self):
        """DB 연결 정보를 설정하는 메서드."""
        db_session_url = self._tr_manager._session_factory.bind.url
        current_db = CurrentDBConnSchema(
            server_type=ServerType.LOCAL if db_session_url.host is None else ServerType.SERVER,
            db_type=db_session_url.drivername,
            db_url=str(db_session_url),
            db_conn_status=True
        )

        # streamlit session에 DB 접속 정보를 저장한다.
        self._session_state_manager.set_session_state(CURRENT_DB_CONN, current_db.model_dump())

        self._app_logger.debug(self._session_state_manager.get_session_state())
