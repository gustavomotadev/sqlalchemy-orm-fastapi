import datetime
import sqlalchemy as sa
from locacao.repositorios.repositorio_base import RepositorioBase
from locacao.util.util import Utilidades
from locacao.repositorios.repositorio_locadora import RepositorioLocadora
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.modelos.usuario import Usuario
from locacao.modelos.veiculo import Veiculo

def main():

    engine = sa.create_engine(Utilidades.obter_connection_string(), echo=False)

    repo_locadora = RepositorioLocadora(engine)
    repo_pessoa = RepositorioPessoa(engine)
    repo_usuario = RepositorioBase(engine, Usuario)
    repo_veiculo = RepositorioBase(engine, Veiculo)

    repo_locadora.inserir(uuid=Utilidades.uuid36(), nome='Nossa Locadora', 
                 horario_abertura=datetime.time(8),
                 horario_fechamento=datetime.time(21),
                 endereco='Rua A, 325')

    repo_pessoa.inserir(uuid=Utilidades.uuid36(), cnh='00000000000', 
                        tipo='Colaborador', nome='Jorge Matos')
    
    repo_pessoa.inserir(uuid=Utilidades.uuid36(), cnh='00000000001', 
                        tipo='Cliente', nome='Carla Santos')

    uuid_temp = repo_pessoa.filtrar(cnh='00000000000')[0].uuid
    salt_temp = Utilidades.obter_salt() 
    repo_usuario.inserir(uuid=Utilidades.uuid36(), uuid_pessoa=uuid_temp,
                         acesso='jmatos', salt_senha=salt_temp,
                         hash_senha=Utilidades.hash_senha(b'123456', salt_temp))
    uuid_temp = repo_pessoa.filtrar(cnh='00000000001')[0].uuid
    salt_temp = Utilidades.obter_salt() 
    repo_usuario.inserir(uuid=Utilidades.uuid36(), uuid_pessoa=uuid_temp,
                         acesso='csantos', salt_senha=salt_temp,
                         hash_senha=Utilidades.hash_senha(b'654321', salt_temp))
    
    tentativa = ('jmatos', b'123456')
    #implementar função para trazer apenas salt
    salt_temp = repo_usuario.filtrar(acesso=tentativa[0])[0].salt_senha
    hash_temp = Utilidades.hash_senha(tentativa[1], salt_temp)
    #implementar função para não trazer salt nem hash
    usuario = repo_usuario.filtrar(acesso='jmatos', hash_senha=hash_temp)
    print(usuario)

    uuid_temp = repo_pessoa.filtrar(cnh='00000000000')[0].uuid
    repo_veiculo.inserir(uuid=Utilidades.uuid36(), uuid_condutor=uuid_temp,
                         placa='PJA1234', modelo='Belta 2014', tipo='Carro',
                         combustivel='Gasolina', capacidade='4',
                         cor='Preto')
    
    uuid_temp = repo_pessoa.filtrar(cnh='00000000001')[0].uuid
    repo_veiculo.inserir(uuid=Utilidades.uuid36(), uuid_condutor=uuid_temp,
                         placa='QJP4321', modelo='Uno 2010', tipo='Carro',
                         combustivel='Gasolina', capacidade='4',
                         cor='Vemelho')

    print(repo_locadora.listar_todos())
    print(repo_pessoa.listar_todos())
    print(repo_usuario.listar_todos())
    print(repo_veiculo.listar_todos())

    print(repo_locadora.filtrar(nome='Nossa Locadora'))

if __name__ == '__main__':
    main()