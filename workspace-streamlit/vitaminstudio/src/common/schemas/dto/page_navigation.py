from pydantic.dataclasses import dataclass
from pydantic import Field

from common.schemas import BaseSchema


@dataclass
class PageNaviagtionDTO(BaseSchema):
    def __init__(self):
        super().__init__()

    page_idx: int = Field(title='현재 페이지 번호', default=1)
    page_next: int = Field(title='Next 클릭시 증가', default=0)
    min_page: int = Field(title='현재페이지에서 가장 작은 페이지 번호', default=1)
    max_page: int = Field(title='현재 페이지에서 가장 큰 페이지 번호', default=5)
    display_cnt: int = Field(title='화면에 표시할 개수', default=20)
