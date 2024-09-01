from common.schemas.dto.common_response_dto import CommonResponseDTO

from ..vo.worddict_list_vo import WordDictListVO


class WordDictListReponseDTO(CommonResponseDTO):
    def __post_init__(self):
        # UserDetailSchema의 인스턴스를 생성하여 detail 필드에 추가
        if isinstance(self.detail, WordDictListVO):
            # detail이 UserDetailSchema 타입인 경우 딕셔너리로 변환
            self.detail = self.detail.to_dict()
        else:
            raise ValueError("detail must be an instance of UserDetailSchema")
