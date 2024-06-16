from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Defects(Enum):
    adj: int = 0
    int: int = 1
    geo: int = 2
    pro: int = 3
    non: int = 4


class Defect(BaseModel):
    class_id: int
    name: str
    rel_x: float
    rel_y: float
    width: float
    height: float
    image_id: UUID
