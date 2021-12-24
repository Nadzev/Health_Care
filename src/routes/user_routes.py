import json

from fastapi import APIRouter, status, Body, Depends, Request
from src.models.schemas import SchemaConsulting, Pacient, TokenData, AppointmentConsulting,Login
from src.controllers.pacientController import PacientController
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from src.database.database import Mongo
import jwt
from src.models.schemas import Collection
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
routes = APIRouter()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = Mongo.get_user_name('Paciente', token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





@routes.get('/WebMedic', status_code=status.HTTP_200_OK)
async def init():
    return status.HTTP_200_OK


@routes.post('/WebMedic/Paciente-Register', status_code=status.HTTP_201_CREATED)
async def register_paciente(data: Pacient):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": data.email}, expires_delta=access_token_expires
    )
    data.token = access_token
    user = await PacientController.create(data)
    return access_token


@routes.post('/WebMedic/Paciente-login')
async def login(login:Login):
    user = await PacientController.authenticate_user(login.email, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )

    userr = {'email': login.email}
    await Mongo.set_token('Paciente', userr, access_token)
    return {"access_token": access_token, "token_type": "bearer", "user": "paciente"}


@routes.post('/WebMedic/Paciente/appointment')
async def appointment(req: Request):
    token = req.headers['Authorization']
    print(req)
    schedule = SchemaConsulting()
    body = await req.body()
    body = json.loads(body)
    print(body)
    schedule.especialidade = body['especialidade']
    schedule.doctor = body['doctor']
    schedule.doenca = body['doenca']
    schedule.data_consulta = body['data_consulta']
    await PacientController.make_an_appointment(token, schedule)

@routes.get('/WebMedic/minhas-consultas/{id}')
async def schedules(id):
    return await PacientController.list_schedules(id)







