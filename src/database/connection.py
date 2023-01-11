from motor.motor_asyncio import AsyncIOMotorClient
from src.utils.enviroment import env


db_client = AsyncIOMotorClient(
    host=env("DATABASE_HOST"),
    port=int(env("DATABASE_PORT")),
    username=env("DATABASE_USER"),
    password=env("DATABASE_PASS"),
    authSource="admin",
)


health_care = db_client.health_care
# collection_pacient = health_care["pacient"]

# class ConnectionHandler:
#     database_name: str = env('DATABASE_NAME')

#     def __new__(cls, loop=None, *args, **kwargs):
#         cls.database_name = env('DATABASE_NAME')

#         return cls

#     @classmethod
#     async def connection(cls):
#         connection =  AsyncIOMotorClient(
#             host=env('DATABASE_HOST'),
#             port=int(env('DATABASE_PORT')),
#             username=env('DATABASE_USER'),
#             password=env('DATABASE_PASS'),
#             authSource='admin',

#         )

#         return connection

#     @classmethod
#     async def database(cls):
#         client = await cls.connection()
#         print(client[cls.database_name])
#         return client[cls.database_name]
