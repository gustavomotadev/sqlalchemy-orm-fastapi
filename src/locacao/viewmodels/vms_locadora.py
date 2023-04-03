from datetime import time
from uuid import uuid1
from pydantic import BaseModel, Field, UUID1, validator
from locacao.modelos.locadora import Locadora

def _validar_horario(horario: time) -> time:
    if horario < time(5) or horario > time(22) or int(horario.minute) % 15 != 0:
        raise ValueError
    else:
        return horario

class VMLocadora(BaseModel):
    uuid: UUID1 = Field(default_factory=uuid1)
    nome: str = Field(max_length=100)
    horario_abertura: time
    horario_fechamento: time
    endereco: str = Field(max_length=255)

    @validator('horario_abertura', 'horario_fechamento')
    def validar_horario(horario: time) -> time: 
        return _validar_horario(horario)

    @staticmethod
    def converter_modelo(modelo: Locadora):
        return VMLocadora(uuid=modelo.uuid, nome=modelo.nome, 
            horario_abertura=modelo.horario_abertura, 
            horario_fechamento=modelo.horario_fechamento,
            endereco=modelo.endereco)

class VMLocadoraSemUUID(BaseModel):
    nome: str = Field(max_length=100)
    horario_abertura: time
    horario_fechamento: time
    endereco: str = Field(max_length=255)

    @validator('horario_abertura', 'horario_fechamento')
    def validar_horario(horario: time) -> time:
        return _validar_horario(horario)

class VMLocadoraHorarios(BaseModel):
    horario_abertura: time
    horario_fechamento: time

    @validator('horario_abertura', 'horario_fechamento')
    def validar_horario(horario: time) -> time:
        return _validar_horario(horario)