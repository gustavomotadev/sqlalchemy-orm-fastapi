from pydantic import BaseModel, Field, UUID1, validator
from locacao.modelos.pessoa import Pessoa
from locacao.util.util import Utilidades

class VMPessoa(BaseModel):
    uuid: UUID1
    cnh: str = Field(min_length=11, max_length=11)
    tipo: str = Field(max_length=30)
    nome: str = Field(max_length=100)

    @validator('cnh')
    def validar_cnh(cnh: str) -> str: 
        return Utilidades.validar_cnh(cnh)
    
    @staticmethod
    def converter_modelo(modelo: Pessoa):
        return VMPessoa(uuid=modelo.uuid, cnh=modelo.cnh, 
            tipo=modelo.tipo, nome=modelo.nome)

class VMPessoaSemUUID(BaseModel):
    cnh: str = Field(min_length=11, max_length=11)
    tipo: str = Field(max_length=30)
    nome: str = Field(max_length=100)

    @validator('cnh')
    def validar_cnh(cnh: str) -> str: 
        return Utilidades.validar_cnh(cnh)