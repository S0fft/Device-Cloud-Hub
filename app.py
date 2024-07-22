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


async def post_device(request):
    data = await request.json()

    try:
        if not all(key in data for key in ['name', 'device_type', 'login', 'password', 'location_id', 'api_user_id']):
            raise ValueError('Missing required fields')

        if not Location.select().where(Location.id == data['location_id']).exists():
            raise ValueError('Invalid location_id')

        if not ApiUser.select().where(ApiUser.id == data['api_user_id']).exists():
            raise ValueError('Invalid api_user_id')

        device = Device.create(
            name=data['name'],
            device_type=data['device_type'],
            login=data['login'],
            password=data['password'],
            location=data['location_id'],
            api_user=data['api_user_id']
        )

        return web.json_response({
            'id': device.id,
            'name': device.device_type,
            "login": device.login,
            "password": device.password,
            "location_id": device.location_id,
            "api_user_id": device.api_user_id
        })

    except ValueError as e:
        return web.json_response({'error': str(e)}, status=400)
    except Exception as e:
        return web.json_response({'error': 'Failed to create device: {}'.format(str(e))}, status=500)

app.router.add_get('/', hello)
app.router.add_post('/devices/', post_device)

if __name__ == '__main__':
    db.connect()
    web.run_app(app, host='127.0.0.1', port=8080)
