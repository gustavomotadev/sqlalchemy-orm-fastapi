from fastapi import HTTPException, status, Depends
from typing import List, Optional, Annotated
from locacao.viewmodels.vms_veiculo import *
from locacao.repositorios.repositorio_veiculo import RepositorioVeiculo
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.controladores.controlador_base import ControladorBase
from locacao.util.util import Utilidades
from locacao.dependencias.singletons import repositorio_veiculo, repositorio_pessoa

class ControladorVeiculo(ControladorBase):

    def __init__(self) -> None:        
        self.endpoints = [self.listar_veiculos, self.consultar_veiculo,
            self.cadastrar_veiculo, self.alterar_veiculo, 
            self.remover_veiculo, self.alterar_condutor_veiculo]

    async def listar_veiculos(self, 
        repo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)],
        uuid_condutor: Optional[str] = None, placa: Optional[str] = None, 
        modelo: Optional[str] = None, tipo: Optional[str] = None, 
        combustivel: Optional[str] = None, capacidade: Optional[int] = None, 
        cor: Optional[str] = None) -> List[VMVeiculo]:

        encontrados = repo.filtrar(uuid_condutor=uuid_condutor, placa=placa, 
            modelo=modelo, tipo=tipo, combustivel=combustivel, 
            capacidade=capacidade, cor=cor)
        return list(map(VMVeiculo.converter_modelo, encontrados))
    listar_veiculos.rota = {'path': '/veiculo/', 'methods': ['GET']}

    async def consultar_veiculo(self, uuid: str, 
        repo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)]) -> VMVeiculo:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            return VMVeiculo.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    consultar_veiculo.rota = {'path': '/veiculo/{uuid}', 'methods': ['GET']}

    async def cadastrar_veiculo(self, vm: VMVeiculoSemUUID, 
        repo_veiculo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)], 
        repo_pessoa: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)], 
        util: Annotated[Utilidades, Depends(Utilidades)]) -> VMVeiculo:
        
        condutor_encontrado = repo_pessoa.filtrar(uuid=str(vm.uuid_condutor))
        if not condutor_encontrado:
            raise HTTPException(400)
        
        uuid = util.uuid36()
        inserido = repo_veiculo.inserir(uuid, str(vm.uuid_condutor), vm.placa, 
            vm.modelo, vm.tipo, vm.combustivel, vm.capacidade, vm.cor)
        return VMVeiculo.converter_modelo(inserido)
    cadastrar_veiculo.rota = {'path': '/veiculo/', 'methods': ['POST'], 
        'status_code': status.HTTP_201_CREATED}

    async def alterar_veiculo(self, uuid: str, vm: VMVeiculoSemUUIDs, 
        repo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)]) -> VMVeiculo:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            alterado = encontrados[0]
            alterado.placa = vm.placa
            alterado.modelo = vm.modelo
            alterado.tipo = vm.tipo
            alterado.combustivel = vm.combustivel
            alterado.capacidade = vm.capacidade
            alterado.cor = vm.cor
            repo.alterar(alterado)
            return VMVeiculo.converter_modelo(alterado)
        else:
            raise HTTPException(404)
    alterar_veiculo.rota = {'path': '/veiculo/{uuid}', 'methods': ['PUT']}

    async def remover_veiculo(self, uuid: str, 
        repo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)]) -> VMVeiculo:

        encontrados = repo.filtrar(uuid=uuid)
        if encontrados:
            repo.remover(encontrados[0])
            return VMVeiculo.converter_modelo(encontrados[0])
        else:
            raise HTTPException(404)
    remover_veiculo.rota = {'path': '/veiculo/{uuid}', 'methods': ['DELETE']}

    async def alterar_condutor_veiculo(self, uuid: str, vm: VMVeiculoCondutor, 
        repo_veiculo: Annotated[RepositorioVeiculo, Depends(repositorio_veiculo)], 
        repo_pessoa: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)]) -> VMVeiculo:
        
        veiculo_encontrado = repo_veiculo.filtrar(uuid=uuid)
        if veiculo_encontrado:

            condutor_encontrado = repo_pessoa.filtrar(uuid=str(vm.uuid_condutor))
            if not condutor_encontrado:
                raise HTTPException(400)

            alterado = veiculo_encontrado[0]
            alterado.uuid_condutor = str(vm.uuid_condutor)
            repo_veiculo.alterar(alterado)
            return VMVeiculo.converter_modelo(alterado)
        else:
            raise HTTPException(404)
    alterar_condutor_veiculo.rota = {'path': '/locadora/{uuid}', 'methods': ['PATCH']}