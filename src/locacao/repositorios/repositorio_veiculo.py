from sqlalchemy.engine import Engine
from typing import List, Optional
from locacao.modelos.veiculo import Veiculo
from locacao.repositorios.repositorio_base import RepositorioBase
from locacao.util.util import Utilidades

class RepositorioVeiculo(RepositorioBase):
    
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Veiculo)

    def listar_todos(self) -> List[Veiculo]:
        return super().listar_todos()
    
    def inserir(self, uuid: str, uuid_condutor: str, placa: str, 
            modelo: str, tipo: str, combustivel: str, capacidade: int,
            cor: str) -> Veiculo:
        return super().inserir(uuid=uuid, uuid_condutor=uuid_condutor, 
                placa=placa, modelo=modelo, tipo=tipo, 
                combustivel=combustivel, capacidade=capacidade, cor=cor)
    
    def alterar(self, editado: Veiculo) -> Veiculo:
        return super().alterar(editado)
    
    def remover(self, apagado: Veiculo) -> Veiculo:
        return super().remover(apagado)
    
    def filtrar(self, uuid: Optional[str] = None, 
            uuid_condutor: Optional[str] = None, placa: Optional[str] = None, 
            modelo: Optional[str] = None, tipo: Optional[str] = None, 
            combustivel: Optional[str] = None, capacidade: Optional[int] = None,
            cor: Optional[str] = None) -> List[Veiculo]:
        argumentos = {'uuid': uuid, 'uuid_condutor': uuid_condutor, 
            'placa': placa, 'modelo': modelo, 'tipo': tipo, 
            'combustivel': combustivel, 'capacidade': capacidade, 'cor': cor}
        return super().filtrar(**Utilidades.remover_none_dict(argumentos))