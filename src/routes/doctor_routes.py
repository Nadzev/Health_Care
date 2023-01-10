from fastapi import APIRouter,Path, status, Depends
from src.models.schemas import Doctor, TokenData, Login
from src.controllers.doctorController import DoctorController
from src.database.database import Repository
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from typing import Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
import json


doctor_routes = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
routes = APIRouter()


@doctor_routes.post('/WebMedic/Medico-Register')
async def register_medico(doctor: Doctor):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": doctor.email}, expires_delta=access_token_expires
    )
    doctor.token = access_token
    user = await DoctorController.create(doctor)
    return access_token


@doctor_routes.post('/check_crm')
async def check_crm(name, crm):
    response = await DoctorController.verify_crm(name,crm)
    return response


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
    user = Repository.get_user_name('Medico', token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@doctor_routes.get('/WebMedic', status_code=status.HTTP_200_OK)
async def init():
    print('init')
    return status.HTTP_200_OK


@doctor_routes.post('/WebMedic/Medico-login')
async def login(login: Login):
    user = await DoctorController.authenticate_user(login.email, login.password)
    print(user)
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

    await Repository.set_token('Medico', userr, access_token)

    return {"access_token": access_token, "token_type": "bearer", "user":"medico"}


@doctor_routes.post('/WebMedic/Medico-agenda/{token}')
async def insert_consulta_horarios(req:Request,token):
    # token = req.headers['Authorization']
    print(req)

    body = await req.body()
    body = json.loads(body)
    # schedule = Doctor_consulta()
    print(body)
    # schedule.valor_hora = body['valor_hora']
    # schedule.areas_atuacao = body['areas_atuacao']
    # schedule.agenda = body['agenda']
    await DoctorController.dados_consulta(token, body)



@doctor_routes.get('/WebMedic/Medicos')
async def lista_medicos():
    return await DoctorController.index()
# def verify_token(req: Request):
#     print(req.headers)
#     token = req.headers["authorization"]
