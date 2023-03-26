from sqlalchemy.engine import Engine
from typing import List, Optional
from locacao.modelos.pessoa import Pessoa
from locacao.repositorios.repositorio_base import RepositorioBase
from locacao.util.util import Utilidades

class RepositorioPessoa(RepositorioBase):
    
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Pessoa)

    def listar_todos(self) -> List[Pessoa]:
        return super().listar_todos()
    
    def inserir(self, uuid: str, cnh: str, tipo: str, nome: str) -> Pessoa:
        return super().inserir(uuid=uuid, cnh=cnh, tipo=tipo, nome=nome)
    
    def alterar(self, editado: Pessoa) -> Pessoa:
        return super().alterar(editado)
    
    def remover(self, apagado: Pessoa) -> Pessoa:
        return super().remover(apagado)
    
    def filtrar(self, uuid: Optional[str] = None, cnh: Optional[str] = None, 
                tipo: Optional[str] = None, nome: Optional[str] = None
                ) -> List[Pessoa]:
        argumentos = {'uuid': uuid, 'cnh': cnh, 'tipo': tipo, 'nome': nome}
        return super().filtrar(**Utilidades.remover_none_dict(argumentos))
        