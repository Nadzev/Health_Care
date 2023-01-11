from pydantic import *

# from src.database.database import PyObjectId
# from bson.objectid import ObjectId

#
# class ObjectId(ObjectId):
#     pass
#


class Pacient(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    nome: str = Field(...)
    registro_geral: str = Field(...)
    idade: int = Field(...)
    nacionalidade: str = Field(...)
    cpf: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        schema_extra = {
            "examples": {
                #     escrever exemplos depois
            }
        }
