from pydantic import BaseModel

class Aluno(BaseModel):
    nome: str
    idade: int

class AlunoIdade(BaseModel):
    idade: int