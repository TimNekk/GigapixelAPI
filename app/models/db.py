from datetime import datetime

from peewee import SqliteDatabase, Model, DateTimeField, AutoField

db = SqliteDatabase("db.sqlite")


class BaseModel(Model):
    id = AutoField()
    create_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db
