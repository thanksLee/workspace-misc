from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Union

from core.utilities.strings import split_str


class WordDictListRequestDto(BaseModel):
    display_cate_nm: Optional[str] = Field(title='화면표시 분류 명')
    search_txt: Optional[str] = Field(title='검색 텍스트')
    filter_list: Optional[list] = Field(title='검색 필터')
    # 검색 조건
    cate_seq: Optional[int] = Field(title="분류 일련번호", default='')
    word_flg_cd: Optional[str] = Field(title='단어 구분 코드', max_length=1, default='')
    word_flg_cd_nm: Optional[str] = Field(title='단어 구분 코드 명')
    kor_word_type_cd: Optional[str] = Field(title='한글 단어 유형 코드', max_length=1, default='')
    kor_word_type_cd_nm: Optional[str] = Field(title='한글 단어 유형 코드 명')
    kor_word_nm: Optional[str] = Field(title='한글 단어 명', default='')
    eng_word_nm: Optional[str] = Field(title='영문 단어 명', default='')
    eng_abbr_nm: Optional[str] = Field(title='영문 약어 명', default='')
    # paging 관련
    paging_display_cnt: Optional[Union[int, str]] = Field(title='화면표시 개수', default=20)
    paging_page_idx: Optional[int] = Field(title="페이지 인덱스", default=0)

    @field_validator('paging_display_cnt')
    def validate_paging_display_cnt(cls, value):

        if value == 'all' or value == 'ALL':
            value = 9999999999
        return value

    @model_validator(mode="after")
    def set_common_code(cls, values: 'WordDictListRequestDto'):
        def helper_set_code(source_value: str):
            ret_val = split_str(':', source_value)[0]
            if ret_val == '0':
                ret_val = ''
            return ret_val

        values.cate_seq = helper_set_code(values.display_cate_nm)
        values.word_flg_cd = helper_set_code(values.word_flg_cd_nm)
        values.kor_word_type_cd = helper_set_code(values.kor_word_type_cd_nm)

        for item in values.filter_list:
            tmp_flg = split_str(':', item)[0]
            if tmp_flg == '0':
                values.kor_word_nm = values.search_txt
            elif tmp_flg == '1':
                values.eng_word_nm = values.search_txt
            elif tmp_flg == '2':
                values.eng_abbr_nm = values.search_txt

        return values
