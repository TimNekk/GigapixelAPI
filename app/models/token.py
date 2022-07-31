from peewee import TextField, IntegerField

from app.models.db import BaseModel


class Token(BaseModel):
    token = TextField(unique=True, null=False)
    quota = IntegerField(default=0)

    class Meta:
        table_name = "Token"
