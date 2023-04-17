from fastapi import HTTPException, status, Depends
from typing import List, Optional
from typing_extensions import Annotated
from locacao.viewmodels.vms_pessoa import *
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.controladores.controlador_base import ControladorBase
from locacao.util.util import Utilidades
from locacao.dependencias.singletons import repositorio_pessoa

class ControladorPessoa(ControladorBase):

    def __init__(self) -> None:        
        self.endpoints = [self.listar_pessoas, self.consultar_pessoa,
            self.cadastrar_pessoa, self.alterar_pessoa, self.remover_pessoa]

    async def listar_pessoas(self, 
        repo: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)],
        cnh: Optional[str] = None, tipo: Optional[str] = None,
        nome: Optional[str] = None) -> List[VMPessoa]:
        
        encontrados = repo.filtrar(cnh=cnh, tipo=tipo, nome=nome)
        return list(map(VMPessoa.converter_modelo, encontrados))
    listar_pessoas.rota = {'path': '/pessoa/', 'methods': ['GET']}

    async def consultar_pessoa(self, uuid: str, 
        repo: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)]) -> VMPessoa:
        
        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            return VMPessoa.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    consultar_pessoa.rota = {'path': '/pessoa/{uuid}', 'methods': ['GET']}

    async def cadastrar_pessoa(self, vm: VMPessoaSemUUID, 
        repo: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)],
        util: Annotated[Utilidades, Depends(Utilidades)]) -> VMPessoa:

        uuid = util.uuid36()
        inserido = repo.inserir(uuid, vm.cnh, vm.tipo, vm.nome)
        return VMPessoa.converter_modelo(inserido)
    cadastrar_pessoa.rota = {'path': '/pessoa/', 'methods': ['POST'], 
        'status_code': status.HTTP_201_CREATED}

    async def alterar_pessoa(self, uuid: str, vm: VMPessoaSemUUID, 
        repo: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)]) -> VMPessoa:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            alterado = encontrados[0]
            alterado.cnh = vm.cnh
            alterado.tipo = vm.tipo
            alterado.nome = vm.nome
            repo.alterar(alterado)
            return VMPessoa.converter_modelo(alterado)
        else:
            raise HTTPException(404)
    alterar_pessoa.rota = {'path': '/pessoa/{uuid}', 'methods': ['PUT']}

    async def remover_pessoa(self, uuid: str, 
        repo: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)]) -> VMPessoa:
        
        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            repo.remover(encontrados[0])
            return VMPessoa.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    remover_pessoa.rota = {'path': '/pessoa/{uuid}', 'methods': ['DELETE']}