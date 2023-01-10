from pydantic import *
from typing import *
from datetime import datetime
from pydantic import BaseModel

class AppointmentConsulting(BaseModel):
    token: Optional[str]
    especialidade: Optional[str]
    doctor: Optional[str]
    data_consulta:Optional[datetime]
    doenca: Optional[str]
    horario_consulta: Optional[datetime]

# class Header(BaseModel):
#     token:


class Login(BaseModel):
    email: Optional[str]
    password: Optional[str]


class Pacient(BaseModel):
    token: Optional[str]
    password: Optional[str]
    email: Optional[str]
    nome: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[datetime]
    appointment = []


class Horarios(BaseModel):
    finalDate: Optional[datetime]
    initialDate: Optional[datetime]


class Doctor_consulta(BaseModel):
    valor_hora: Optional[int]
    areas_atuacao: Optional[Any]
    agenda: Optional[Horarios]


class Doctor(BaseModel):
    token: Optional[str]
    password: Optional[str]
    email: Optional[str]
    nome: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[datetime]
    dados_consulta = {}



    # dia_semana = datetime
# class Paciente2(BaseModel):
#     nome: Optional[str]
#     cpf: Optional[str]
#     especialidade: Optional[str] = None
#     createdAt: Optional[datetime] = datetime.utcnow()



# class Doctor(BaseModel):
#     email: Optional[str]
#     nome: Optional[str]
#     cpf: Optional[str]
#     rg: Optional[str]
#     especialidade: Optional[str]
#     crm: Optional[str]
#     horarios_disponiveis =  []
#     valor_consulta: float


class TokenData(BaseModel):
    username: Optional[str] = None

class SchemaConsulting(BaseModel):
    especialidade: Optional[str]
    doctor: Optional[str]
    data_consulta:Optional[datetime]
    doenca: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str



