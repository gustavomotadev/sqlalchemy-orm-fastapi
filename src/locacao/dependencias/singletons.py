from sqlalchemy import create_engine
from locacao.util.util import Utilidades
from locacao.repositorios.repositorio_locadora import RepositorioLocadora
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.repositorios.repositorio_veiculo import RepositorioVeiculo
from locacao.autenticacao.autenticador import Autenticador

_autenticador = Autenticador(**Utilidades.obter_chaves())

_sqlalchemy_engine = create_engine(Utilidades.obter_connection_string(), echo=False)

_repositorio_locadora = RepositorioLocadora(_sqlalchemy_engine)
_repositorio_pessoa = RepositorioPessoa(_sqlalchemy_engine)
_repositorio_veiculo = RepositorioVeiculo(_sqlalchemy_engine)

repositorio_locadora = lambda: _repositorio_locadora
repositorio_pessoa = lambda: _repositorio_pessoa
repositorio_veiculo = lambda: _repositorio_veiculo

autenticador = lambda: _autenticador
