from typing import List
from sqlalchemy import text

from common.schemas.vo.common_code import CommonCodeVO
from common.mappers import CommonMapper


class CommonCodeMapper(CommonMapper):
    def __init__(self, db_session):
        super().__init__(db_session)

    def select_common_code_list(self) -> List[CommonCodeVO]:
        qry_stmt = f'''
            /* CommonCodeMapper.get_common_code_list */
            select key_cd
                 , type_cd
                 , cd_nm_1
                 , cd_nm_2
                 , use_yn
                 , dspy_yn
                 , sort_order
              from base_cmn_cd

        '''

        qry_result = self._db_session.execute(text(qry_stmt)).fetchall()
        return self.map_result_to_model(qry_result, CommonCodeVO)
