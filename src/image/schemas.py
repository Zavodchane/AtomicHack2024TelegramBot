from datetime import date

from pydantic import BaseModel


class Image(BaseModel):
    name: str
    size: int

    created_at: date

    user_id: str
