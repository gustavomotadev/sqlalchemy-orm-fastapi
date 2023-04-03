print('singletons.py start')

from sqlalchemy import create_engine
from locacao.util.util import Utilidades
from locacao.repositorios.repositorio_locadora import RepositorioLocadora

_sqlalchemy_engine = create_engine(Utilidades.obter_connection_string(), echo=False)

_repositorio_locadora = RepositorioLocadora(_sqlalchemy_engine)

repositorio_locadora = lambda: _repositorio_locadora

print('singletons.py end')
