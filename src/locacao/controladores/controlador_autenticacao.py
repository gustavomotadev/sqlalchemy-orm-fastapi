from fastapi import HTTPException, status, Depends, Response
from typing import List, Optional
from typing_extensions import Annotated
from locacao.viewmodels.vms_autenticacao import *
from locacao.repositorios.repositorio_usuario import RepositorioUsuario
from locacao.repositorios.repositorio_pessoa import RepositorioPessoa
from locacao.controladores.controlador_base import ControladorBase
from locacao.util.util import Utilidades
from locacao.dependencias.singletons import repositorio_usuario, repositorio_pessoa, autenticador
from fastapi.security import OAuth2PasswordRequestForm
from locacao.autenticacao.autenticacao import Autenticador

class ControladorAutenticacao(ControladorBase):

    def __init__(self) -> None:        
        self.endpoints = [self.cadastro, self.login, self.perfil, self.logado,
            self.colaborador_logado]

    async def cadastro(self, aut: Annotated[Autenticador, Depends(autenticador)], 
        repo_usuario: Annotated[RepositorioUsuario, Depends(repositorio_usuario)],
        repo_pessoa: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)],
        dados_cadastro: VMCadastroUsuario) -> VMUsuario:

        pessoa = repo_pessoa.filtrar(uuid=str(dados_cadastro.uuid_pessoa))

        if not pessoa:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 
                detail='Pessoa não cadastrada no sistema')
        
        uuid = Utilidades.uuid36()
        salt = aut.obter_salt()
        hash_senha = aut.obter_hash_senha(
            dados_cadastro.senha.get_secret_value(), salt)
        usuario = repo_usuario.inserir(uuid, str(dados_cadastro.uuid_pessoa), 
            dados_cadastro.acesso, salt, hash_senha)
        
        return VMUsuario.converter_modelo(usuario, pessoa)
    cadastro.rota = {'path': '/autenticacao/cadastro', 'methods': ['POST'],
        'status_code': status.HTTP_201_CREATED}

    async def login(self, aut: Annotated[Autenticador, Depends(autenticador)], 
        repo_usuario: Annotated[RepositorioUsuario, Depends(repositorio_usuario)],
        repo_pessoa: Annotated[RepositorioPessoa, Depends(repositorio_pessoa)],
        dados_formulario: Annotated[OAuth2PasswordRequestForm, Depends()]) -> VMBearerToken:

        salt_usuario = repo_usuario.obter_salt(dados_formulario.username)

        if salt_usuario is None:
            raise self.ErroAutenticacao("Usuário não existe")
        
        hash_senha = aut.obter_hash_senha(dados_formulario.password, salt_usuario)
        usuario = repo_usuario.obter_por_credencial(dados_formulario.username, salt_usuario, hash_senha)

        if usuario is None:
            raise self.ErroAutenticacao("Senha incorreta")
        
        pessoa = repo_pessoa.filtrar(uuid = usuario.uuid_pessoa)[0]
        
        token = aut.gerar_token_jwt({'uuid_usuario': usuario.uuid, 
            'uuid_pessoa': usuario.uuid_pessoa, 'acesso': usuario.acesso,
            'nome': pessoa.nome, 'tipo': pessoa.tipo})
        
        return VMBearerToken(access_token=token)
    login.rota = {'path': '/autenticacao/login', 'methods': ['POST']}

    async def perfil(self, 
        usuario_logado: Annotated[VMUsuario, 
        Depends(ControladorBase.obter_usuario_logado)]) -> VMUsuario:

        return usuario_logado
    perfil.rota = {'path': '/autenticacao/perfil', 'methods': ['GET']}

    async def logado(self) -> None:
        return Response(status_code=status.HTTP_200_OK)
    logado.rota = {'path': '/autenticacao/logado', 'methods': ['GET'], 
        'dependencies': [Depends(ControladorBase.obter_usuario_logado)]}
    
    async def colaborador_logado(self) -> None:
        return Response(status_code=status.HTTP_200_OK)
    colaborador_logado.rota = {'path': '/autenticacao/colaborador_logado', 'methods': ['GET'], 
        'dependencies': [Depends(ControladorBase.obter_colaborador_logado)]}