from src.database.database import ConnectionHandler
from src.models.schemas import SchemaConsulting
from fastapi.exceptions import HTTPException
from src.database.database import Repository
import json
import bcrypt

class PacientController:

    
    @classmethod
    async def create(cls, paciente):
        collection = 'Paciente'
        user = await Repository.get_user_email(collection, paciente.email)
        paciente.password = cls.db.get_password_hash(paciente.password)

        # try:
        #     await cls.db.insert_by_collection(collection, paciente.dict())
        # except HTTPException:
        #     raise HTTPException(status_code=409,
        #                         detail="User already registered.")

        print(user)
        if user is not None:
            return "User already registered."
        else:
            signup = await cls.db.insert_by_collection(collection, paciente.dict())
            return f'The pacient was successfully created'

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        user = await Repository.get_user_email('Paciente', email)
        print(user.to_list(1))
        if not user:
            return False
        if not await Repository.verify_password(password, user['password']):
            return False
        return user

    @classmethod
    async def make_an_appointment(cls,token,header):
        collection = 'Pacient'
        header = header.dict()

        user = {'token': token}
        schedule = SchemaConsulting()
        schedule.especialidade = header['especialidade']
        schedule.doenca = header['doenca']
        schedule.data_consulta = header['data_consulta']
        schedule.doctor = header['doctor']

        # especialidade: Optional[str]
        # doctor: Optional[str]
        # data_consulta: Optional[datetime]
        # doenca: Optional[str]
        # horario_consulta: Optional[str]

        await cls.db.insert_appointment(token, schedule)
        # await cls.db.set_params(collection, user, cpf, nome, data)
        return 'appointment'

    @classmethod
    async def list_schedules(cls,id):
        appointments_list = await Repository.list_appointments(id)
        return appointments_list






