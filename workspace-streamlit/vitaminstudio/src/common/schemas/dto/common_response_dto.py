from pydantic.dataclasses import dataclass
from typing import Optional, List, Union

from common.schemas.base_schema import BaseSchema


@dataclass
class CommonResponseDTO(BaseSchema):
    def __init__(self):
        super().__init__()

    status: int
    message: str
    code: str
    detail: Optional[Union[dict, List[dict]]] = None
