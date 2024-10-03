import streamlit as st
import pandas as pd
from typing import Optional

from ..constants import WORD_DICT_LIST_HEADER


class WordDictListForm:
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._df = None
        self._word_dict_data = None

    def render(self, word_dict_values: Optional[list]):
        # list_header_container = st.container(border=True)
        # with list_header_container:
        #    pass

        self.load_word_dict_list(word_dict_values)

    def load_word_dict_list(self, values: Optional[list]):
        if values:
            # 데이터프레임 생성
            self._df = pd.DataFrame(values)

            # 컬럼명 변경 및 설정
            self._df = self._df.rename(columns=WORD_DICT_LIST_HEADER)

            # 특정 컬럼("단어 종류")의 값에 따라 스타일 적용
            styled_df = self._df.style.apply(self.highlight_word_flg_column, subset=["word_flg_cd_nm"])

            col_config = WORD_DICT_LIST_HEADER['columns']
            self._word_dict_data = st.dataframe(styled_df,
                                                column_config=col_config,
                                                on_select='rerun',
                                                selection_mode='multi-row'
                                                )
            self.handle_select()

    def highlight_word_flg_column(self, col):
        ''' "단어 종류" 컬럼에서 "금칙어"가 포함된 셀을 강조 '''
        return ['color: red' if '금칙어' in str(v) else '' for v in col]

    def handle_select(self):
        selected_idx = self._word_dict_data.selection.rows
        if len(selected_idx) > 0:
            selected_rows = []
            for idx in selected_idx:
                selected_row = {
                    'eng_word_seq': str(self._df.iloc[idx]["eng_word_seq"]),
                    'eng_abbr_seq': str(self._df.iloc[idx]["eng_abbr_seq"]),
                    'kor_word_seq': str(self._df.iloc[idx]["kor_word_seq"]),
                }

                selected_rows.append(selected_row)

            st.write(selected_rows)
