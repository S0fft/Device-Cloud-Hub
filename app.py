import os

from aiohttp import web
from dotenv import load_dotenv
from peewee import *

load_dotenv()

db = PostgresqlDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT'))
)


class ApiUser(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
        table_name = 'api_user'


class Location(Model):
    name = CharField()

    class Meta:
        database = db
        table_name = 'location'


class Device(Model):
    name = CharField()
    device_type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

    class Meta:
        database = db
        table_name = 'device'


app = web.Application()


async def hello(request):
    return web.Response(text="Server is running!")

app.router.add_get('/', hello)

if __name__ == '__main__':
    db.connect()
    web.run_app(app, host='127.0.0.1', port=8080)
