import datetime
from sqlalchemy.engine import Engine
from typing import List, Optional
from locacao.modelos.locadora import Locadora
from locacao.repositorios.repositorio_base import RepositorioBase

class RepositorioLocadora(RepositorioBase):
    
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Locadora)

    def listar_todos(self) -> List[Locadora]:
        return super().listar_todos()
    
    def inserir(self, uuid: str, nome: str, horario_abertura: datetime.time,
                horario_fechamento: datetime.time, endereco: str) -> Locadora:
        return super().inserir(uuid=uuid, nome=nome, horario_abertura=horario_abertura,
                horario_fechamento=horario_fechamento, endereco=endereco)
    
    def alterar(self, editado: Locadora) -> Locadora:
        return super().alterar(editado)
    
    def remover(self, apagado: Locadora) -> Locadora:
        return super().remover(apagado)
    
    def filtrar(self, uuid: Optional[str] = None, nome: Optional[str] = None, 
                horario_abertura: Optional[datetime.time] = None,
                horario_fechamento: Optional[datetime.time] = None, 
                endereco: Optional[str] = None) -> List[Locadora]:
        argumentos = {'uuid': uuid, 'nome': nome, 'horario_abertura': horario_abertura,
                      'horario_fechamento': horario_fechamento, 'endereco': endereco}
        filtrados = {k: v for k, v in argumentos.items() if v is not None}
        return super().filtrar(**filtrados)
        