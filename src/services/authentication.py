from src.database.database import Repository
from src.database.connection import ConnectionHandler
from passlib.context import CryptContext
from datetime import datetime,timedelta
from fastapi.exceptions import HTTPException
from jwt.exceptions import PyJWTError
from fastapi import status
import os
import jwt

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication:
        
    db = ConnectionHandler.connection()
    @classmethod
    async def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def get_password_hash(cls, password):
        return pwd_context.hash(password)

    @classmethod
    async def authenticate_user(cls, db, email: str, password: str):
        
        user = await Repository.get_user_email('Paciente', email)
        if not user:
            return False
        if not cls.verify_password(password, user.password):
            return False
        return user

    @classmethod
    def create_access_token(cls, *, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    def decode_access_token(cls, db, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            
        except PyJWTError:
            raise credentials_exception
        user = Repository.get_user_by_email(db,'definir depois')
        if user is None:
            raise credentials_exception
        return user
