from sqlalchemy import create_engine, Engine, event
from locacao.util.util import Utilidades
from locacao.repositorios.repositorio_locadora import RepositorioLocadora
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.repositorios.repositorio_veiculo import RepositorioVeiculo
from locacao.repositorios.repositorio_usuario import RepositorioUsuario
from locacao.autenticacao.autenticacao import Autenticador
from fastapi.security import OAuth2PasswordBearer

@event.listens_for(Engine, "connect")
def sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

_autenticador = Autenticador(**Utilidades.obter_chaves())

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="v1/autenticacao/login")

_sqlalchemy_engine = create_engine("sqlite:///SQL/locadora.sqlite", echo=False)

_repositorio_locadora = RepositorioLocadora(_sqlalchemy_engine)
_repositorio_pessoa = RepositorioPessoa(_sqlalchemy_engine)
_repositorio_veiculo = RepositorioVeiculo(_sqlalchemy_engine)
_repositorio_usuario = RepositorioUsuario(_sqlalchemy_engine)

repositorio_locadora = lambda: _repositorio_locadora
repositorio_pessoa = lambda: _repositorio_pessoa
repositorio_veiculo = lambda: _repositorio_veiculo
repositorio_usuario = lambda: _repositorio_usuario

autenticador = lambda: _autenticador
