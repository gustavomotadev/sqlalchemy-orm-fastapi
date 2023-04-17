from pydantic import BaseModel, Field, UUID1, SecretStr, validator
from typing_extensions import Literal
from locacao.util.util import Utilidades
from locacao.modelos.usuario import Usuario
from locacao.modelos.pessoa import Pessoa

class VMBearerToken(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = Field(default='bearer')

class VMUsuario(BaseModel):
    uuid_usuario: UUID1
    uuid_pessoa: UUID1
    acesso: str = Field(min_length=6, max_length=20)
    tipo: str = Field(max_length=30)
    nome: str = Field(max_length=100)

    @validator('acesso')
    def validar_acesso(acesso: str) -> str: 
        return Utilidades.validar_acesso(acesso)
    
    @staticmethod
    def converter_modelo(modelo_usuario: Usuario, modelo_pessoa: Pessoa):
        return VMUsuario(uuid_usuario=modelo_usuario.uuid,
            uuid_pessoa=modelo_usuario.uuid_pessoa, 
            acesso=modelo_usuario.acesso,
            tipo=modelo_pessoa.tipo, nome=modelo_pessoa.nome)

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
