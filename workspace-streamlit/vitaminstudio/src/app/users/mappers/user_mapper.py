from sqlalchemy import text

from common.mappers.common_mapper import CommonMapper
from core.constants.global_enum import ServerDB
from ..schemas.vo.user_vo import UserVO


class UserMapper(CommonMapper):
    def __init__(self, db_session):
        super().__init__(db_session)

    def select_table_exists_check(self, db_type: str, db_schema: str):
        qry_result = None
        qry_sqlite_stmt = '''
            /* UserMapper.table_exists_check */
            select count(1) table_cnt
              from sqlite_master
             where type = 'table'
               and name not like 'sqlite_%'
               and name in ( 'base_cmn_cd', 'base_user')
        '''

        qry_pg_stmt = '''
            /* UserMapper.table_exists_check */
            select count(1) table_cnt
              from information_schema.tables
             where table_name in ( 'base_cmn_cd', 'base_user')
               and table_schema = :table_schema
        '''
        if db_type == ServerDB.SQLITE.value:
            qry_result = (self._db_session.execute(text(qry_sqlite_stmt))).first()
        elif db_type == ServerDB.POSTGRESQL.value:
            qry_param = {
                'table_schema': db_schema
            }
            qry_result = (self._db_session.execute(text(qry_pg_stmt), qry_param)).first()

        return qry_result

    def select_user_login(self, user_id: str) -> UserVO:
        qry_stmt = f'''
            /* UserMapper.user_login */
            select bu.login_pwd
                 , bu.use_yn
                 , bu.user_type_cd
              from base_user bu
             where bu.user_id = :user_id
        '''

        qry_param = {
            'user_id': user_id
        }

        qry_result = (self._db_session.execute(text(qry_stmt), qry_param)).fetchone()

        return self.map_result_to_model(qry_result, UserVO)
