from sqlalchemy.engine import Engine
from typing import List, Optional
from locacao.modelos.usuario import Usuario
from locacao.repositorios.repositorio_base import RepositorioBase
from locacao.util.util import Utilidades

class RepositorioUsuario(RepositorioBase):
    
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Usuario)

    def listar_todos(self) -> List[Usuario]:
        return super().listar_todos()
    
    def inserir(self, uuid: str, uuid_pessoa: str, acesso: str, 
                salt_senha: bytes, hash_senha: bytes) -> Usuario:
        return super().inserir(uuid=uuid, uuid_pessoa=uuid_pessoa, 
                acesso=acesso, salt_senha=salt_senha, hash_senha=hash_senha)
    
    def alterar(self, editado: Usuario) -> Usuario:
        return super().alterar(editado)
    
    def remover(self, apagado: Usuario) -> Usuario:
        return super().remover(apagado)
    
    def filtrar(self, uuid: Optional[str] = None, uuid_pessoa: Optional[str] = None, 
                acesso: Optional[str] = None,  salt_senha: Optional[bytes] = None, 
                hash_senha: Optional[bytes] = None) -> List[Usuario]:
        argumentos = {'uuid': uuid, 'uuid_pessoa': uuid_pessoa, 'acesso': acesso,
                      'salt_senha': salt_senha, 'hash_senha': hash_senha}
        return super().filtrar(**Utilidades.remover_none_dict(argumentos))
        