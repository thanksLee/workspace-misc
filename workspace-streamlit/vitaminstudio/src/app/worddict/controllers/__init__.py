from common.controllers import CommonController
from ..services.cate import WordDictCateService
from ..services.list import WordDictListService


class WordDictController(CommonController):
    def __init__(self, db_url: str):
        super().__init__(db_url)

    def handle_word_dict_cate_list(self):
        """단어 사전 분류 리스트 함수"""
        ret_val = WordDictCateService(self._tr_manager).get_word_dict_cate_list()

        return ret_val

    def handle_word_flg_list(self):
        """단어 구분 리스트 함수"""
        ret_val = WordDictCateService(self._tr_manager).get_word_flg_lis()

        return ret_val

    def handle_word_type_list(self):
        """단어 유형 리스트 함수"""
        ret_val = WordDictCateService(self._tr_manager).get_word_type_lis()

        return ret_val

    def handle_word_dict_list(self, req_param):
        ret_val = WordDictListService(self._tr_manager).get_word_dict_list(req_param)

        return ret_val
