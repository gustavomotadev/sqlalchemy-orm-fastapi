from fastapi import HTTPException, status, Depends
from typing import List, Optional, Annotated
from locacao.viewmodels.vms_locadora import *
from locacao.repositorios.repositorio_locadora import RepositorioLocadora
from locacao.controladores.controlador_base import ControladorBase
from locacao.util.util import Utilidades
from locacao.dependencias.singletons import repositorio_locadora

class ControladorLocadora(ControladorBase):

    def __init__(self) -> None:        
        self.endpoints = [self.listar_locadoras, self.consultar_locadora,
            self.cadastrar_locadora, self.alterar_locadora, 
            self.remover_locadora, self.alterar_horarios_locadora]

    async def listar_locadoras(self, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)],
        nome: Optional[str] = None,
        horario_abertura: Optional[str] = None,
        horario_fechamento: Optional[str] = None,
        endereco: Optional[str] = None) -> List[VMLocadora]:

        encontrados = repo.filtrar(nome=nome, horario_abertura=horario_abertura, 
            horario_fechamento=horario_fechamento, endereco=endereco)
        return list(map(VMLocadora.converter_modelo, encontrados))
    listar_locadoras.rota = {'path': '/locadora/', 'methods': ['GET']}

    async def consultar_locadora(self, uuid: str, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)]) -> VMLocadora:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            return VMLocadora.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    consultar_locadora.rota = {'path': '/locadora/{uuid}', 'methods': ['GET']}

    async def cadastrar_locadora(self, vm: VMLocadoraSemUUID, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)], 
        util: Annotated[Utilidades, Depends(Utilidades)]) -> VMLocadora:

        uuid = util.uuid36()
        inserido = repo.inserir(uuid, vm.nome, vm.horario_abertura,
            vm.horario_fechamento, vm.endereco)
        return VMLocadora.converter_modelo(inserido)
    cadastrar_locadora.rota = {'path': '/locadora/', 'methods': ['POST'], 
        'status_code': status.HTTP_201_CREATED}

    async def alterar_locadora(self, uuid: str, vm: VMLocadoraSemUUID, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)]) -> VMLocadora:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            alterado = encontrados[0]
            alterado.nome = vm.nome
            alterado.horario_abertura = vm.horario_abertura
            alterado.horario_fechamento = vm.horario_fechamento
            alterado.endereco = vm.endereco
            repo.alterar(alterado)
            return VMLocadora.converter_modelo(alterado)
        else:
            raise HTTPException(404)
    alterar_locadora.rota = {'path': '/locadora/{uuid}', 'methods': ['PUT']}

    async def remover_locadora(self, uuid: str, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)]) -> VMLocadora:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            repo.remover(encontrados[0])
            return VMLocadora.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    remover_locadora.rota = {'path': '/locadora/{uuid}', 'methods': ['DELETE']}

    async def alterar_horarios_locadora(self, uuid: str, vm: VMLocadoraHorarios, 
        repo: Annotated[RepositorioLocadora, Depends(repositorio_locadora)]) -> VMLocadora:
        
        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            alterado = encontrados[0]
            alterado.horario_abertura = vm.horario_abertura
            alterado.horario_fechamento = vm.horario_fechamento
            repo.alterar(alterado)
            return VMLocadora.converter_modelo(alterado)
        else:
            raise HTTPException(404)
    alterar_horarios_locadora.rota = {'path': '/locadora/{uuid}', 'methods': ['PATCH']}