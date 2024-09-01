from typing import Optional
from common.services.common_service import CommonService
from core.databases.server.transaction_manager import TransactionManager

from ..mappers.worddict_mapper import WordDictMapper
from ..schemas.dto.worddict_response_dto import WordDictReponseDTO
from ..schemas.dto.worddict_list_request_dto import WordDictListRequestDto


class WordDictListService(CommonService):
    def __init__(self, tr_manager: TransactionManager):
        super().__init__(tr_manager)

    def get_word_dict_list(self, req_param: WordDictListRequestDto):
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
                    "word_list": [
                        {
                            "rnum": "1",
                            "kor_word_nm": "1회섭취참고량",
                            "eng_word_nm": "reference amount for one serving",
                            "eng_abbr_nm": "rafos",
                            "kor_word_type_cd": "1",
                            "word_flg_cd": "1",
                            "cate_nm": "공공데이터 공통표준용어",
                            "term_kor_nm_list": "1회섭취참고량 명",
                            "total_cnt": "1797",
                            "kor_word_seq": "1",
                            "eng_word_seq": "1",
                            "eng_abbr_seq": "1701",
                            "cate_seq": "1"
                        }
                    ]
                }
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
            qry_results = WordDictMapper(tran_session).select_word_dict_list(req_param)

            word_list: Optional[list] = []
            for qry_result in qry_results:
                word_list.append(qry_result.to_dict())

                ret_val = WordDictReponseDTO(
                    status=self._ret_status.SUCCESS,
                    message=self._vs_msg.VS_SUCCESS_000.value,
                    code=self._vs_msg.VS_SUCCESS_000.name,
                    detail=word_list
                )
            return ret_val
