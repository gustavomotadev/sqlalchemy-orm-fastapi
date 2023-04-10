from pydantic import BaseModel, Field, UUID1
from typing import Literal

class VMBearerToken(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = Field(default='bearer')

class VMUsuarioLogado(BaseModel):
    uuid_usuario: UUID1
    uuid_pessoa: UUID1
    acesso: str = Field(max_length=20)