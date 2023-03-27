import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine import Engine
from typing import List, Optional
from locacao.modelos.usuario import Usuario
from locacao.repositorios.repositorio_base import RepositorioBase
from locacao.util.util import Utilidades

class RepositorioUsuario(RepositorioBase):
    
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, Usuario)

    def listar_todos(self) -> List[Usuario]:

        with orm.Session(self.engine, expire_on_commit=False) as session:
            listados = session.execute(
                sa.select(Usuario.uuid, Usuario.uuid_pessoa, Usuario.acesso
                    )).all()
            
        return list(map(lambda u: Usuario(uuid=u[0], uuid_pessoa=u[1], 
            acesso=u[2], salt_senha=None, hash_senha=None), listados))
    
    def inserir(self, uuid: str, uuid_pessoa: str, acesso: str, 
                salt_senha: bytes, hash_senha: bytes) -> Usuario:
        return super().inserir(uuid=uuid, uuid_pessoa=uuid_pessoa, 
                acesso=acesso, salt_senha=salt_senha, hash_senha=hash_senha)
    
    def alterar(self, editado: Usuario) -> Usuario:
        return super().alterar(editado)
    
    def remover(self, apagado: Usuario) -> Usuario:
        return super().remover(apagado)
    
    def filtrar(self, uuid: Optional[str] = None, uuid_pessoa: Optional[str] = None, 
                acesso: Optional[str] = None) -> List[Usuario]:
        
        argumentos = {'uuid': uuid, 'uuid_pessoa': uuid_pessoa, 'acesso': acesso}

        with orm.Session(self.engine, expire_on_commit=False) as session:
            filtrados = session.execute(sa.select(Usuario.uuid, Usuario.uuid_pessoa, 
                Usuario.acesso).filter_by(**Utilidades.remover_none_dict(
                argumentos))).all()
            
        return list(map(lambda u: Usuario(uuid=u[0], uuid_pessoa=u[1], 
            acesso=u[2], salt_senha=None, hash_senha=None), filtrados))
    
    def obter_salt(self, acesso: str):
        with orm.Session(self.engine, expire_on_commit=False) as session:
            filtrado = session.execute(sa.select(Usuario.salt_senha
                ).filter_by(acesso=acesso)).scalar_one_or_none()
        return filtrado
    
    def obter_por_credencial(self, acesso: str, salt_senha: bytes, 
            hash_senha: bytes):
        
        with orm.Session(self.engine, expire_on_commit=False) as session:
            existe = session.execute(sa.select(Usuario.uuid, Usuario.uuid_pessoa, 
                Usuario.acesso).where(Usuario.acesso == acesso,
                Usuario.salt_senha == salt_senha, Usuario.hash_senha == hash_senha
                )).one_or_none()
            
        if existe is not None:
            existe = Usuario(uuid=existe[0], uuid_pessoa=existe[1], 
            acesso=existe[2], salt_senha=None, hash_senha=None)

        return existe

        