from pydantic import BaseModel, Field, UUID1, SecretStr, validator
from typing import Literal
from locacao.util.util import Utilidades
from locacao.modelos.usuario import Usuario

class VMBearerToken(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = Field(default='bearer')

class VMUsuario(BaseModel):
    uuid_usuario: UUID1
    uuid_pessoa: UUID1
    acesso: str = Field(min_length=6, max_length=20)

    @validator('acesso')
    def validar_acesso(acesso: str) -> str: 
        return Utilidades.validar_acesso(acesso)
    
    @staticmethod
    def converter_modelo(modelo: Usuario):
        return VMUsuario(uuid_usuario=modelo.uuid,
            uuid_pessoa=modelo.uuid_pessoa, acesso=modelo.acesso)

class VMCadastroUsuario(BaseModel):
    uuid_pessoa: UUID1
    acesso: str = Field(min_length=6, max_length=20)
    senha: SecretStr = Field(min_length=6, max_length=20)

    @validator('acesso')
    def validar_acesso(acesso: str) -> str: 
        return Utilidades.validar_acesso(acesso)
    
    @validator('senha')
    def validar_senha(senha: str) -> str: 
        return Utilidades.validar_senha(senha)
