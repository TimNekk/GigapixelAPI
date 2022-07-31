from datetime import datetime

from pydantic import BaseModel

from app.schemas.getter_dict import PeeweeGetterDict


class Queue(BaseModel):
    id: int
    create_at: datetime
    state: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class QueueCreate(BaseModel):
    image_base64: str
    scale: str
    mode: str
