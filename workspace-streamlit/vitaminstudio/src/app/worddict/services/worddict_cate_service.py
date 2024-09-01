from typing import Optional
from common.services.common_service import CommonService
from core.databases.server.transaction_manager import TransactionManager
from core.singletons.common_code_store import CommonCodeStore

from ..mappers.worddict_mapper import WordDictMapper
from ..schemas.dto.worddict_response_dto import WordDictReponseDTO


class WordDictCateService(CommonService):
    def __init__(self, tr_manager: TransactionManager):
        super().__init__(tr_manager)

    def get_word_dict_cate_list(self):
        '''
        표준 단어 사전 분류 리스트를 가져오는 함수

        Args:

        Returns
        - json

        - success
            {
            "status": "200",
            "message": "successfully",
            "code": "VS_SUCCESS_000",
            "detail": {
                "word_cate_list": [
                    {
                        "rnum": "1",
                        "cate_nm": "전체",
                        "cate_seq": "0",
                        "display_cate_nm": "0:전체"
                    }
                ]
            }

        - fail
        {
            "status": 400
            "message": 'Failed to retrieve data.'
            "code" : "VS_ERROR_006"
            "detail": {}
        }
        '''
        with self._tr_manager.get_transaction() as tran_session:
            qry_results = WordDictMapper(tran_session).select_word_dict_cate_list()

            word_cate_list: Optional[list] = []
            for qry_result in qry_results:
                word_cate_list.append(qry_result.to_dict())

            ret_val = self.__build_reponse(word_cate_list)

            return ret_val

    def get_word_flg_lis(self):
        '''
        표준 단어 구분 리스트를 가져오는 함수

        Args:

        Returns
        - json

        - success
            {
            "status": "200",
            "message": "successfully",
            "code": "VS_SUCCESS_000",
            "detail": {
                "word_flg_list": [
                    {
                        "key_cd": "S03",
                        "type_cd": "-",
                        "cd_nm_1": "단어구분코드",
                        "cd_nm_2": None,
                        "use_yn" : 'Y',
                        "dspy_yn": 'Y',
                        "sort_order": 6,
                        "dspy_cd_nm_1": "-:단어구분코드",
                        "dspy_cd_nm_2": "-:"
                    }
                ]
            }

        - fail
        {
            "status": 400
            "message": 'Failed to retrieve data.'
            "code" : "VS_ERROR_006"
            "detail": {}
        }
        '''
        ret_val = self.__build_common_code_list('S03')

        return ret_val

    def get_word_type_lis(self):
        '''
        표준 단어 유형 리스트를 가져오는 함수

        Args:

        Returns
        - json

        - success
            {
            "status": "200",
            "message": "successfully",
            "code": "VS_SUCCESS_000",
            "detail": {
                "word_flg_list": [
                    {
                        "key_cd": "S02",
                        "type_cd": "-",
                        "cd_nm_1": "한글단어유형코드",
                        "cd_nm_2": None,
                        "use_yn" : 'Y',
                        "dspy_yn": 'Y',
                        "sort_order": 6,
                        "dspy_cd_nm_1": "-:한글단어유형코드",
                        "dspy_cd_nm_2": "-:"
                    }
                ]
            }

        - fail
        {
            "status": 400
            "message": 'Failed to retrieve data.'
            "code" : "VS_ERROR_006"
            "detail": {}
        }
        '''
        ret_val = self.__build_common_code_list('S02')

        return ret_val

    def __build_common_code_list(self, key_cd: str):

        common_code_store = CommonCodeStore()
        qry_results = common_code_store.get_common_codes_by_key(key_cd)

        word_type_list: Optional[list] = []
        for qry_result in qry_results:
            word_type_list.append(qry_result.to_dict())

        ret_val = self.__build_reponse(word_type_list)
        return ret_val

    def __build_reponse(self, ret_list: Optional[list]):
        ret_val = WordDictReponseDTO(
            status=self._ret_status.SUCCESS,
            message=self._vs_msg.VS_SUCCESS_000.value,
            code=self._vs_msg.VS_SUCCESS_000.name,
            detail=ret_list
        )

        return ret_val
