from pydantic import Field, model_validator, field_validator
from typing import Optional

from common.schemas.vo.base_vo import BaseVO


class WordDictListVO(BaseVO):
    rnum: int = Field(..., title='순번')
    kor_word_nm: str = Field(..., title='한글 단어 명')
    eng_word_nm: str = Field(..., title='영문 단어 명')
    eng_abbr_nm: str = Field(..., title='영문 약어 명')
    kor_word_type_cd: str = Field(..., title='한글 단어 유형 코드')
    kor_word_type_cd_nm: Optional[str] = Field(title='한글 단어 유형 코드 명', default=None)
    word_flg_cd: str = Field(..., title='단어 구분 코드')
    word_flg_cd_nm: Optional[str] = Field(title='단어 구분 코드 명', default=None)
    cate_nm: str = Field(..., title='분류 명')
    term_kor_nm_list: Optional[str] = Field(title='용어 한글 명 리스트', default=None)
    total_cnt: int = Field(..., title='전체 로우 수')
    kor_word_seq: int = Field(..., title='한글 단어 일련번호')
    eng_word_seq: int = Field(..., title='영문 단어 일련번호')
    eng_abbr_seq: int = Field(..., title='영문 약어 알련번호')
    cate_seq: int = Field(..., title='분류 일련번호')

    @model_validator(mode='after')
    def set_common_code_name(cls, values: 'WordDictListVO'):

        if values.kor_word_type_cd_nm is None:
            values.kor_word_type_cd_nm = cls._common_code_name(1, 'S02', values.kor_word_type_cd)

        if values.word_flg_cd_nm is None:
            values.word_flg_cd_nm = cls._common_code_name(1, 'S03', values.word_flg_cd)

        cls._app_logger.debug(f"Values after modification: {values.model_dump()}")
        return values
