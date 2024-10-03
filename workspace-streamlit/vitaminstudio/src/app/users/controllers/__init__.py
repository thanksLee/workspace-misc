from common.controllers import CommonController

from core.databases.server.db_connection_manager import db_manager
from core.sessions.schemas import CurrentDBConnDTO

from ..services.user_init import UserInitService
from ..services.user_login import UserLoginService
from ..schemas.dto.request import LoginFormDTO


class UserController(CommonController):
    def __init__(self, db_url: str):
        super().__init__(db_url)

    def handle_db_conn_click(self, db_conn_info: CurrentDBConnDTO):
        self.__db_initialize(db_conn_info)
        ret_val = self.__create_db(db_conn_info.db_type, db_conn_info.db_schema)
        return ret_val

    def __db_initialize(self, db_conn_info: CurrentDBConnDTO):
        ''' Server Database에 접속할 수 있는 connection을 생성하는 함수'''
        db_manager.add_db_manager(db_conn_info.db_type, db_conn_info.db_url)

    def __create_db(self, db_type: str, db_schema: str):
        ''' Server Database VitaminStudio Table 및 테이터를 생성하는 함수'''
        _user_init_service = UserInitService(self._tr_manager)
        qry_result = _user_init_service.sql_file_execute(db_type, db_schema)

        return qry_result

    def handle_user_login_click(self, user_form: LoginFormDTO):
        ''' Server Database에 접속하는 함수'''
        ret_val = UserLoginService(self._tr_manager).user_login_check(user_form)
        return ret_val
