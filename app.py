import logging
import os

from aiohttp import web
from aiohttp.web import Response
from dotenv import load_dotenv
from peewee import *
from peewee import CharField, ForeignKeyField, Model, PostgresqlDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

db = PostgresqlDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT'))
)


# MODELS
class ApiUser(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
        table_name: str = 'api_user'


class Location(Model):
    name = CharField()

    class Meta:
        database = db
        table_name: str = 'location'


class Device(Model):
    name = CharField()
    device_type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

    class Meta:
        database = db
        table_name: str = 'device'

    @staticmethod
    def current_device_info(device: dict[str, int | str]) -> Response[dict[str, int | str]]:
        return web.json_response({
            'id': device.id,
            'name': device.name,
            'device_type': device.device_type,
            'login': device.login,
            'password': device.password,
            'location_id': device.location.id,
            'api_user_id': device.api_user.id
        })


app = web.Application()


# TEST
async def hello(request) -> Response[str]:
    return web.Response(text='Server is running!')


# POST (CREATE)
async def post_device(request) -> Response[dict[str, int | str]]:
    data: dict[str, int | str] = await request.json()
    logger.info('Received data to create device: %s', data)

    try:
        if not all(key in data for key in ['name', 'device_type', 'login', 'password', 'location_id', 'api_user_id']):
            raise ValueError('Missing required fields!')

        if not Location.select().where(Location.id == data['location_id']).exists():
            raise ValueError('Invalid location_id!')

        if not ApiUser.select().where(ApiUser.id == data['api_user_id']).exists():
            raise ValueError('Invalid api_user_id')

        device: dict[str, int | str] = Device.create(
            name=data['name'],
            device_type=data['device_type'],
            login=data['login'],
            password=data['password'],
            location=data['location_id'],
            api_user=data['api_user_id']
        )
        logger.info('Device created successfully: %s', device.id)
        return Device.current_device_info(device)

    except ValueError as e:
        logger.error('Error creating device: %s', str(e))
        return web.json_response({'error': str(e)}, status=400)

    except Exception as e:
        logger.error('Failed to create device: %s', str(e))
        return web.json_response({'error': 'Failed to create device: {}!'.format(str(e))}, status=500)


# GET ALL (READ)
async def get_all_devices(request) -> Response[dict[str, int | str]]:
    logger.info('Retrieving all devices')

    try:
        devices = Device.select()
        devices_list: list[dict[str, int | str]] = [
            {
                'id': device.id,
                'name': device.name,
                'device_type': device.device_type,
                'login': device.login,
                'password': device.password,
                'location_id': device.location.id,
                'api_user_id': device.api_user.id
            } for device in devices
        ]

        logger.info('Retrieved %d devices', len(devices_list))
        return web.json_response(devices_list)

    except Exception as e:
        logger.error('Failed to retrieve devices: %s', str(e))
        return web.json_response({'error': 'Failed to retrieve devices!'}, status=500)


# GET by ID (READ)
async def get_device_by_id(request) -> Response[dict[str, int | str]]:
    device_id: int = request.match_info.get('id')
    logger.info('Retrieving device by id: %s', device_id)

    try:
        device: int = Device.get(Device.id == device_id)
        logger.info('Device retrieved: %s', device.id)
        return Device.current_device_info(device)

    except Device.DoesNotExist:
        logger.warning('Device not found: %s', device_id)
        return web.json_response({'error': 'Device not found!'}, status=404)


# PUT by ID (major-UPDATE)
async def put_device_by_id(request) -> Response[dict[str, int | str]]:
    device_id: int = request.match_info.get('id')
    data: dict[str, int | str] = await request.json()
    logger.info('Updating device %s with data: %s', device_id, data)

    try:
        if not all(key in data for key in ['name', 'device_type', 'login', 'password', 'location_id', 'api_user_id']):
            raise ValueError('Missing required fields!')

        if not Location.select().where(Location.id == data['location_id']).exists():
            raise ValueError('Invalid location_id!')

        if not ApiUser.select().where(ApiUser.id == data['api_user_id']).exists():
            raise ValueError('Invalid api_user_id!')

        device_query: dict[str, int | str] = Device.update(
            name=data['name'],
            device_type=data['device_type'],
            login=data['login'],
            password=data['password'],
            location=data['location_id'],
            api_user=data['api_user_id']
        ).where(Device.id == device_id)
        updated: dict[str, int | str] = device_query.execute()

        if updated:
            updated_device: int = Device.get(Device.id == device_id)
            logger.info('Device updated successfully: %s', device_id)

            return Device.current_device_info(updated_device)
        else:
            logger.warning('Device not found for update: %s', device_id)
            return web.json_response({'error': 'Device not found!'}, status=404)

    except ValueError as e:
        logger.error('Error updating device: %s', str(e))
        return web.json_response({'error': str(e)}, status=400)

    except Exception as e:
        logger.error('Failed to update device: %s', str(e))
        return web.json_response({'error': 'Failed to update device!'}, status=500)


# PATCH by ID (minor-UPDATE)
async def patch_device_by_id(request) -> Response[dict[str, int | str]]:
    device_id: int = request.match_info.get('id')
    data: dict[str, int | str] = await request.json()
    logger.info('Patching device %s with data: %s', device_id, data)

    try:
        updates: dict = {}

        if 'name' in data:
            updates['name'] = data['name']

        if 'device_type' in data:
            updates['device_type'] = data['device_type']

        if 'login' in data:
            updates['login'] = data['login']

        if 'password' in data:
            updates['password'] = data['password']

        if 'location_id' in data:
            if not Location.select().where(Location.id == data['location_id']).exists():
                raise ValueError('Invalid location_id!')
            updates['location'] = data['location_id']

        if 'api_user_id' in data:
            if not ApiUser.select().where(ApiUser.id == data['api_user_id']).exists():
                raise ValueError('Invalid api_user_id')
            updates['api_user'] = data['api_user_id']

        if not updates:
            logger.warning('No fields to update for device: %s', device_id)
            return web.json_response({'error': 'No fields to update!'}, status=400)

        query: dict[str, int | str] = Device.update(**updates).where(Device.id == device_id)
        updated = query.execute()

        if updated:
            updated_device: dict[str, int | str] = Device.get(Device.id == device_id)
            logger.info('Device patched successfully: %s', device_id)
            return Device.current_device_info(updated_device)
        else:
            logger.warning('Device not found for patching: %s', device_id)
            return web.json_response({'error': 'Device not found!'}, status=404)

    except ValueError as e:
        logger.error('Error patching device: %s', str(e))
        return web.json_response({'error': str(e)}, status=400)

    except Exception as e:
        logger.error('Failed to patch device: %s', str(e))
        return web.json_response({'error': 'Failed to patch device!'}, status=500)


# DELETE by ID
async def delete_device_by_id(request) -> Response[dict[str, int | str]]:
    device_id: int = request.match_info.get('id')
    logger.info('Deleting device by id: %s', device_id)

    try:
        query: dict[str, int | str] = Device.delete().where(Device.id == device_id)
        deleted: dict[str, int | str] = query.execute()

        if deleted:
            logger.info('Device deleted successfully: %s', device_id)
            return web.json_response({'message': f'Device with id {device_id} was successfully deleted!'})
        else:
            logger.warning('Device not found for deletion: %s', device_id)
            return web.json_response({'error': 'Device not found!'}, status=404)

    except Exception as e:
        logger.error('Failed to delete device: %s', str(e))
        return web.json_response({'error': 'Failed to delete device: {}!'.format(str(e))}, status=500)


# ROUTERS
app.router.add_get('/', hello)

app.router.add_post('/devices/', post_device)
app.router.add_get('/devices/', get_all_devices)
app.router.add_get('/devices/{id}/', get_device_by_id)
app.router.add_put('/devices/{id}/', put_device_by_id)
app.router.add_patch('/devices/{id}/', patch_device_by_id)
app.router.add_delete('/devices/{id}/', delete_device_by_id)


def create_tables():
    with db.connection_context():
        if not db.get_tables():
            db.create_tables([ApiUser, Location, Device])
            print("Tables created successfully")
        else:
            print("Tables already exist")


# RUN
if __name__ == '__main__':
    create_tables()
    db.connect()
    logger.info('Starting server at http://127.0.0.1:8080')
    web.run_app(app, host='127.0.0.1', port=8080)
