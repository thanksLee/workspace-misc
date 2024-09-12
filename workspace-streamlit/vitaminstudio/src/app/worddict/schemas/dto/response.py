from typing import Union
from common.schemas.vo.common_code import CommonCodeVO
from common.schemas.dto.response import CommonResponseDTO

from ..vo.cate import WordDictCateVO


class WordDictReponseDTO(CommonResponseDTO):
    def __post_init__(self):
        # UserDetailSchema의 인스턴스를 생성하여 detail 필드에 추가
        if isinstance(self.detail, Union[WordDictCateVO, CommonCodeVO]):
            # detail이 UserDetailSchema 타입인 경우 딕셔너리로 변환
            self.detail = self.detail.to_dict()
        else:
            raise ValueError("detail must be an instance of UserDetailSchema")
