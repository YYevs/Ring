from peewee import SqliteDatabase, Model, CharField, TextField


db = SqliteDatabase('cities.db')


class City(Model):
    name = CharField(index=True, unique=True)
    graph = TextField(null=False)
    intermediary_info = TextField(null=False)
    mapping = TextField(null=False)

    class Meta:
        database = db
