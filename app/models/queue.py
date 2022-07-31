from enum import Enum

from peewee import ForeignKeyField, IntegerField

from app.models.db import BaseModel
from app.models.token import Token


class QueueState(Enum):
    WAITING = 0
    FINISHED = 1


class Queue(BaseModel):
    token = ForeignKeyField(Token)
    state = IntegerField(default=QueueState.WAITING.value)

    class Meta:
        table_name = "Queue"
