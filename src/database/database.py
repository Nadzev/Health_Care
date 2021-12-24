from asyncio import AbstractEventLoop
from src.utils.enviroment import env
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
import asyncio
from datetime import datetime
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_index(sio):

    db = await Mongo.database()
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


class Mongo:
    loop: AbstractEventLoop = None
    database_name: str = env('DATABASE_NAME')

    def __new__(cls, loop=None, *args, **kwargs):
        cls.loop = loop or asyncio.get_running_loop()
        cls.database_name = env('DATABASE_NAME')
        # cls.database_name = 'guardiao-database'

        return cls

    @classmethod
    async def get_user_email(cls,collection, email):
        query = {'email': email}
        user = await cls.find_one(collection, query)
        return user

    @classmethod
    async def connection(cls):

        connection = AsyncIOMotorClient(
            host=env('DATABASE_HOST'),
            port=int(env('DATABASE_PORT')),
            username=env('DATABASE_USER'),
            password=env('DATABASE_PASS'),
            authSource='admin',
            io_loop=cls.loop
        )

        return connection
    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    @classmethod
    def get_password_hash(cls, password):
        return pwd_context.hash(password)

    @classmethod
    async def get_user_name(cls,collection, nome):
        query = {'nome': nome}
        user = await cls.find_one(collection, query)
        return user

    @classmethod
    async def database(cls):
        client = await cls.connection()
        return client[cls.database_name]

    @classmethod
    async def insert_by_collection(cls, collection, data):
        db: AsyncIOMotorClient = await cls.database()
        return await db[collection].insert_one(data)

    @classmethod
    async def insert_embedded(cls, collection,doc,query):
        db: AsyncIOMotorClient = await cls.database()
        document = db[collection]
        await document.update_one(doc,query)

    @classmethod
    async def find_one(cls, collection, query):
        db: AsyncIOMotorClient = await cls.database()
        return await db[collection].find_one(query)

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
        db: AsyncIOMotorClient = await cls.database()
        sett = {'$set': {'cpf': cpf, 'nome': nome, 'data_nascimento': data}}
        await db[collection].update_one(user, sett)

    @classmethod
    async def set_token(cls, collection, user, token):
        db: AsyncIOMotorClient = await cls.database()
        sett = {'$set': {'token': token}}
        await db[collection].update_one(user, sett)

    # @classmethod
    # async def set_token(cls,collection,user,token):
    #     db: AsyncIOMotorClient = await cls.database()
    #     sett = {'$set':{'token':token}}
    #     await db[collection].update_one(user, sett)

    @classmethod
    async def list_appointments(cls, token):
        db: AsyncIOMotorClient = await cls.database()
        cursor = db['Paciente']
        query = {'token': token}
        pacient = await cls.find_one('Paciente', query)
        lista = pacient['appointment']
        return lista

    @classmethod
    async def lista_medicos(cls):
        db: AsyncIOMotorClient = await cls.database()
        collect = db['Medico']
        result = collect.find()
        return result


    @classmethod
    async def insert_agenda(cls, token,dados):
        db: AsyncIOMotorClient = await cls.database()
        doc = {'token': token}
        sett = {'$set': {'areas_atuacao': dados['areas_atuacao']}}
        d = dados['agenda']
        query = {'$set': {'agenda': d}}
        await cls.insert_embedded('Medico', doc, query)
        await db['Medico'].update_one(doc, sett)
        await db['Medico'].update_one(doc, query)
        # await cls.insert_embedded('Medico', doc, query)









