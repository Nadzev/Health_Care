# from motor.motor_asyncio import AsyncIOMotorClient
# from src.utils.enviroment import env
#
#
# class Mongo:
#
#    @classmethod
#    async def connection(cls):
#         connection = AsyncIOMotorClient(
#             host=env('DATABASE_HOST'),
#             password=env('DATABASE_PASSWORD'),
#             port=env('DATABASE_PORT'),
#             username=env('DATABASE_USER'),
#         )
#         return connection
#
#    @classmethod
#    async def database(cls):
#         database = 'HealthCare'
#         db = await cls.connection()
#         return db[database]
#
#    @classmethod
#    async def get_collection(cls,collection):
#        db = await cls.database()
#        return db[collection]






