import streamlit as st
from typing import Optional, List, Union


from ..schemas.dto.worddict_response_dto import CommonResponseDTO, WordDictReponseDTO
from ..schemas.dto.worddict_list_request_dto import WordDictListRequestDto
from ..controllers.worddict_controller import WordDictController


class WordDictFilterForm:
    def __init__(self, db_url: str):
        self._db_url = db_url

    def render(self):
        with st.form(key='word_dic_cate_filter'):
            with st.expander(label='상세 필터', expanded=False):
                col_1, col_2, col_3 = st.columns(3)
                with col_1:
                    word_dict_cate: list = load_word_dict_cate_list(self._db_url)
                    word_dict_cate_option = st.selectbox('분류 선택', word_dict_cate)
                with col_2:
                    word_flg: list = load_word_flg_list(self._db_url)
                    word_flg_option = st.selectbox('단어 구분 선택', word_flg)
                with col_3:
                    word_type: list = load_word_type_list(self._db_url)
                    word_type_option = st.selectbox('단어 유형 선택', word_type)

            col_4, col_5, col_6 = st.columns([6, 2, 1])

            with col_4:
                filter_options = st.multiselect('검색 필터', ['0:한글명', '1:영문명', '2:영문약어명'], ['0:한글명'], label_visibility="collapsed")
            with col_5:
                search_text = st.text_input('검색어 입력', label_visibility="collapsed")
            with col_6:
                search_submit = st.form_submit_button('검색')
                if search_submit:
                    req_param = WordDictListRequestDto(
                        display_cate_nm=word_dict_cate_option,
                        search_txt=search_text,
                        filter_list=filter_options,
                        word_flg_cd_nm=word_flg_option,
                        kor_word_type_cd_nm=word_type_option
                    )

                    ret_val = load_word_dict_list(self._db_url, req_param)
                    return ret_val.detail


@st.cache_data
def load_word_dict_cate_list(db_url: str) -> list:
    # get word dict cate list
    req_wordic_cate_list = WordDictController(db_url).handle_word_dict_cate_list()

    ret_val = __build_list(req_wordic_cate_list, 'dspy_cate_nm')
    return ret_val


@st.cache_data
def load_word_flg_list(db_url: str) -> list:
    req_word_flg_list = WordDictController(db_url).handle_word_flg_list()

    ret_val = __build_list(req_word_flg_list, 'dspy_cd_nm_1')
    return ret_val


@st.cache_data
def load_word_type_list(db_url: str) -> list:
    req_word_type_list = WordDictController(db_url).handle_word_type_list()

    ret_val = __build_list(req_word_type_list, 'dspy_cd_nm_1')
    return ret_val


def __build_list(req_list: Union[CommonResponseDTO, WordDictReponseDTO], dspy_nm: str):
    ret_val: Optional[List] = []

    for _item in req_list.detail:
        ret_val.append(_item[dspy_nm])

    return ret_val


@st.cache_data
def load_word_dict_list(db_url: str, _req_param: WordDictListRequestDto) -> list:
    ret_val = WordDictController(db_url).handle_word_dict_list(_req_param)

    return ret_val
