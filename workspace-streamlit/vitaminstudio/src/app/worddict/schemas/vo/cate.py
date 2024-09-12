from pydantic import Field, model_validator
from typing import Optional

from common.schemas.vo.base import BaseVO


class WordDictCateVO(BaseVO):
    rnum: int = Field(..., title='순번', examples=1)
    cate_nm: str = Field(..., title='분류 명', examples='공공데이터 공통표준용어')
    cate_seq: int = Field(..., title='분류 일련번호', examples='0')
    dspy_cate_nm: Optional[str] = Field(title='화면표시 분류 명', examples='1:공공데이터 공통표준용어', default=None)

    @model_validator(mode='after')
    def set_display_cate_nm(cls, values: 'WordDictCateVO'):

        values.dspy_cate_nm = f'{values.cate_seq}:{values.cate_nm}'

        cls._app_logger.debug(f"Values after modification: {values.model_dump()}")
        return values
