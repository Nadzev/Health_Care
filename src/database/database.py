from asyncio import AbstractEventLoop
from src.utils.enviroment import env
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from jose import  jwt
from datetime import datetime
from datetime import datetime, timedelta
from src.database.connection import health_care
from passlib.context import CryptContext

import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_index(sio):

    db = health_care
    await db['Paciente'].create_index([('email', ASCENDING)], unique=True)
    await db['Medico'].create_index([('email', ASCENDING)], unique=True)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


class Repository:
    # database_name: str = env('DATABASE_NAME')

    # def __new__(cls, loop=None, *args, **kwargs):
    #     cls.database_name = env('DATABASE_NAME')

    #     return cls
    # def __init__(self):
    
    db = health_care
    
    @classmethod
    async def get_user_email(cls,collection, email):
        # db = await ConnectionHandler.database()
        query = {'email': email}
        print(query)
        user = cls.db[collection].find(query)
        print(user.to_list(1))
        return user

  
    
    
    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    @classmethod
    def get_password_hash(cls, password):
        return pwd_context.hash(password)

    @classmethod
    async def get_user_name(cls,collection, nome):
        db = await ConnectionHandler.database()
        query = {'nome': nome}
        user = await cls.find_one(collection, query)
        return user

    @classmethod
    async def insert_embedded(cls, collection,doc,query):
        db = await ConnectionHandler.database()
        await db[collection].update_one(doc,query)

    @classmethod
    async def find_one(cls, collection, query):
        db = await ConnectionHandler.database()
        print(collection)
        # db: AsyncIOMotorClient = await cls.database()
        return await db[collection].find(query)

    @classmethod
    async def insert_appointment(cls,nome, appointment):
        collection = 'Pacient'
        # query = {'nome': appointment.nome}
        # doc = await cls.find_one(collection,query)
        doc = {'token': nome}
        query = {'$push': {'appointment': appointment.dict()}}
        await cls.insert_embedded('Paciente', doc, query)
        # doc['appointment'].append(appointment)

    @classmethod
    async def set_params(cls, collection, user,cpf,nome,data):
        # db: AsyncIOMotorClient = await cls.database()
        db = await ConnectionHandler.database()
        sett = {'$set': {'cpf': cpf, 'nome': nome, 'data_nascimento': data}}
        await db[collection].update_one(user, sett)

    @classmethod
    async def set_token(cls, collection, user, token):
        db: AsyncIOMotorClient = await cls.database()
        sett = {'$set': {'token': token}}
        await db[collection].update_one(user, sett)

    @classmethod
    async def set_token(cls,collection,user,token):
        db = await ConnectionHandler.database()
        sett = {'$set':{'token':token}}
        await db.update_one(user, sett)

    @classmethod
    async def list_appointments(cls, token):
        db = await ConnectionHandler.database()
        cursor = db['Paciente']
        query = {'token': token}
        pacient = await cls.db.find_one('Paciente', query)
        lista = pacient['appointment']
        return lista

    @classmethod
    async def lista_medicos(cls):
        collect = cls.db['Medico']
        result = collect.find()
        return result


    @classmethod
    async def insert_agenda(cls, token,dados):
        doc = {'token': token}
        sett = {'$set': {'areas_atuacao': dados['areas_atuacao']}}
        d = dados['agenda']
        query = {'$set': {'agenda': d}}
        await cls.insert_embedded('Medico', doc, query)
        await cls.db['Medico'].update_one(doc, sett)
        await cls.db['Medico'].update_one(doc, query)
    
    @classmethod
    async def insert_by_collection(collection, data):
        pass











