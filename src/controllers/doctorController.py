from src.database.database import Mongo
from src.services.api_crm import Crm


class DoctorController:
    db = Mongo()

    @classmethod
    async def create(cls, doctor):
        collection = 'Medico'
        user = await cls.db.get_user_email(collection, doctor.email)
        doctor.password = cls.db.get_password_hash(doctor.password)
        print(user)
        if user is not None:
            return "User already registered."
        else:
            signup = await cls.db.insert_by_collection(collection, doctor.dict())
            return f'The user was successfully created'

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        user = await cls.db.get_user_email('Medico', email)
        if not user:
            return False
        if not cls.db.verify_password(password, user['password']):
            return False
        return user

    @classmethod
    async def index(cls):
        return await cls.db.lista_medicos()

    @classmethod
    async def verify_crm(cls, name, crm):
        status = await Crm.consulting_crm(name, crm)
        return status

    @classmethod
    async def dados_consulta(cls, token,dados):
        await cls.db.insert_agenda(token, dados)