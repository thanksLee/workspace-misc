from pydantic.dataclasses import dataclass
from typing import Optional
import json


@dataclass
class CommonResponseDTO:
    status: int
    message: str
    code: str
    detail: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return self.__dict__

    def to_json(self) -> str:
        """Convert the instance to a JSON string."""
        return json.dumps(self.to_dict())
