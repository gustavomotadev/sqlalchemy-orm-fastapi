from pydantic import BaseModel, Field
from typing import Literal

class VMBearerToken(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = Field(default='bearer')