from fastapi import HTTPException
from locacao.dtos.dtos_aluno import Aluno, AlunoIdade
from locacao.controladores.controlador_base import ControladorBase

class ControladorAluno(ControladorBase):

    def __init__(self) -> None:
        self.alunos = {0: {'nome': 'Jorge', 'idade': 20},
            1: {'nome': 'Maria', 'idade': 22},
            2: {'nome': 'Pedro', 'idade': 33}}
        
        self.endpoints = [self.listar_alunos, self.consultar_aluno,
            self.cadastrar_aluno, self. alterar_aluno, 
            self.remover_aluno, self.alterar_idade_aluno]

    async def listar_alunos(self):
        return self.alunos
    listar_alunos.rota = '/alunos/'
    listar_alunos.metodos = ['GET']

    async def consultar_aluno(self, id: int):
        if id in self.alunos:
            return self.alunos[id]
        else:
            raise HTTPException(404)
    consultar_aluno.rota = '/aluno/{id}'
    consultar_aluno.metodos = ['GET']

    async def cadastrar_aluno(self, aluno: Aluno):
        id = max(self.alunos.keys(), default=-1) + 1
        self.alunos[id] = aluno.dict()
        return self.alunos[id]
    cadastrar_aluno.rota = '/aluno/'
    cadastrar_aluno.metodos = ['POST']

    async def alterar_aluno(self, id: int, aluno: Aluno):
        if id in self.alunos:
            self.alunos[id] = aluno.dict()
            return self.alunos[id]
        else:
            raise HTTPException(404)
    alterar_aluno.rota = '/aluno/{id}'
    alterar_aluno.metodos = ['PUT']

    async def remover_aluno(self, id: int):
        if id in self.alunos:
            return self.alunos.pop(id)
        else:
            raise HTTPException(404)
    remover_aluno.rota = '/aluno/{id}'
    remover_aluno.metodos = ['DELETE']

    async def alterar_idade_aluno(self, id: int, idade: AlunoIdade):
        if id in self.alunos:
            self.alunos[id]['idade'] = idade.idade
            return self.alunos[id]
        else:
            raise HTTPException(404)
    alterar_idade_aluno.rota = '/aluno/{id}'
    alterar_idade_aluno.metodos = ['PATCH']