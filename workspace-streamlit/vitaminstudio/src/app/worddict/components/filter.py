import streamlit as st
from typing import Union


from ..schemas.dto.response import CommonResponseDTO, WordDictReponseDTO
from ..schemas.dto.request import WordDictListRequestDto
from ..controllers import WordDictController


class WordDictFilterForm:
    def __init__(self, db_url: str):
        self._db_url = db_url

        self._word_dict_cate_option = None
        self._search_text = None
        self._filter_options = None
        self._word_flg_option = None
        self._word_type_option = None
        self._list_count_option = None

    def render(self):
        with st.form(key='word_dict_cate_filter'):
            with st.expander(label='상세 필터', expanded=False):
                self.render_filters()

            col_4, col_5, col_6 = st.columns([6, 2, 1])
            col_7, col_8, col_9, col_10 = st.columns([6, 2, 2, 2])
            new_word_btn, delete_word_btn = self.render_action_button(col_7, col_8, col_9, col_10)
            search_submit = self.render_search_section(col_4, col_5, col_6)

            if search_submit:
                ret_val = self.handle_search()
                return ret_val

            if new_word_btn:
                self.handle_new_word()

            if delete_word_btn:
                self.handle_delete_word()

    def render_filters(self):
        """필터 UI 렌더링 메서드"""
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            word_dict_cate: list = load_word_dict_cate_list(self._db_url)
            self._word_dict_cate_option = st.selectbox('분류 선택', word_dict_cate)
        with col_2:
            word_flg: list = load_word_flg_list(self._db_url)
            self._word_flg_option = st.selectbox('단어 구분 선택', word_flg)
        with col_3:
            word_type: list = load_word_type_list(self._db_url)
            self._word_type_option = st.selectbox('단어 유형 선택', word_type)

    def render_search_section(self, col_4, col_5, col_6):
        """검색 UI 렌더링 메서드"""
        with col_4:
            self._filter_options = st.multiselect('검색 필터', ['0:한글명', '1:영문명', '2:영문약어명'], ['0:한글명'], label_visibility="collapsed")
        with col_5:
            self._search_text = st.text_input('검색어 입력', label_visibility="collapsed")
        with col_6:
            search_submit = st.form_submit_button('검색')

        return search_submit

    def render_action_button(self, col_7, col_8, col_9, col_10):
        """액션 버튼 (new, delete, search) 렌더링"""
        with st.container(border=True):
            with col_7:
                st.caption('')

            with col_8:
                new_word_btn = st.form_submit_button('new', use_container_width=True)

            with col_9:
                delete_word_btn = st.form_submit_button('delete', use_container_width=True)

            with col_10:
                self._list_count_option = st.selectbox('', ('20', '50', '100', '200', 'all'), index=1,
                                                       label_visibility='collapsed')
            return new_word_btn, delete_word_btn

    def handle_search(self):
        """검색 처리 메서드"""
        req_param = WordDictListRequestDto(
            display_cate_nm=self._word_dict_cate_option,
            search_txt=self._search_text,
            filter_list=self._filter_options,
            word_flg_cd_nm=self._word_flg_option,
            kor_word_type_cd_nm=self._word_type_option,
            paging_display_cnt=self._list_count_option
        )

        ret_val = load_word_dict_list(self._db_url, req_param)
        if ret_val:
            return ret_val.detail
        else:
            return ret_val

    def handle_new_word(self):
        """새 단어 추가 처리 (구체적 로직 필요)"""
        st.write("New word handling logic goes here...")

    def handle_delete_word(self):
        """단어 삭제 처리 (구체적 로직 필요)"""
        st.write("Delete word handling logic goes here...")


@st.cache_data
def load_word_dict_cate_list(db_url: str) -> list:
    # get word dict cate list
    req_wordic_cate_list = WordDictController(db_url).handle_word_dict_cate_list()

    ret_val = _build_list(req_wordic_cate_list, 'dspy_cate_nm')
    return ret_val


@st.cache_data
def load_word_flg_list(db_url: str) -> list:
    req_word_flg_list = WordDictController(db_url).handle_word_flg_list()

    ret_val = _build_list(req_word_flg_list, 'dspy_cd_nm_1')
    return ret_val


@st.cache_data
def load_word_type_list(db_url: str) -> list:
    req_word_type_list = WordDictController(db_url).handle_word_type_list()

    ret_val = _build_list(req_word_type_list, 'dspy_cd_nm_1')
    return ret_val


def _build_list(req_list: Union[CommonResponseDTO, WordDictReponseDTO], dspy_nm: str):
    ret_val = []

    for _item in req_list.detail:
        ret_val.append(_item[dspy_nm])

    return ret_val


def load_word_dict_list(db_url: str, _req_param: WordDictListRequestDto) -> list:
    ret_val = WordDictController(db_url).handle_word_dict_list(_req_param)

    return ret_val
