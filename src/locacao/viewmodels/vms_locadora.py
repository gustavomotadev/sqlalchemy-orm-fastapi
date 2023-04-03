import datetime
from pydantic import BaseModel
from locacao.modelos.locadora import Locadora

class VMLocadora(BaseModel):
    uuid: str
    nome: str
    horario_abertura: datetime.time
    horario_fechamento: datetime.time
    endereco: str

    @staticmethod
    def converter_modelo(modelo: Locadora):
        return VMLocadora(uuid=modelo.uuid, nome=modelo.nome, 
            horario_abertura=modelo.horario_abertura, 
            horario_fechamento=modelo.horario_fechamento,
            endereco=modelo.endereco)

class VMLocadoraSemUUID(BaseModel):
    nome: str
    horario_abertura: datetime.time
    horario_fechamento: datetime.time
    endereco: str

class VMLocadoraHorarios(BaseModel):
    horario_abertura: datetime.time
    horario_fechamento: datetime.time