from enum import Enum
from pydantic import BaseModel


class StatusType(int, Enum):
    OK = 200
    CREATED = 201
    ERROR = 400
    # NOT_FOUND = 404

class Status(BaseModel):
    type: StatusType
    detail: str | None = None
