from fastapi import HTTPException, status, Depends, Response
from typing import List, Optional, Annotated
from locacao.viewmodels.vms_autenticacao import *
from locacao.repositorios.repositorio_usuario import RepositorioUsuario
from locacao.controladores.controlador_base import ControladorBase
from locacao.util.util import Utilidades
from locacao.dependencias.singletons import repositorio_usuario, autenticador
from fastapi.security import OAuth2PasswordRequestForm
from locacao.autenticacao.autenticacao import Autenticador

class ControladorAutenticacao(ControladorBase):

    def __init__(self) -> None:        
        self.endpoints = [self.login, self.perfil, self.validar]

    async def login(self, aut: Annotated[Autenticador, Depends(autenticador)], 
        repo: Annotated[RepositorioUsuario, Depends(repositorio_usuario)],
        dados_formulario: Annotated[OAuth2PasswordRequestForm, Depends()]) -> VMBearerToken:

        salt_usuario = repo.obter_salt(dados_formulario.username)

        if salt_usuario is None:
            raise self.ErroAutenticacao("Usuário não existe")
        
        hash_senha = aut.obter_hash_senha(dados_formulario.password, salt_usuario)
        usuario = repo.obter_por_credencial(dados_formulario.username, salt_usuario, hash_senha)

        if usuario is None:
            raise self.ErroAutenticacao("Senha incorreta")
        
        token = aut.gerar_token_jwt({'uuid_usuario': usuario.uuid, 
            'uuid_pessoa': usuario.uuid_pessoa, 'acesso': usuario.acesso})
        
        return VMBearerToken(access_token=token)
    login.rota = {'path': '/autenticacao/login', 'methods': ['POST']}

    async def perfil(self, 
        usuario_logado: Annotated[VMUsuarioLogado, 
        Depends(ControladorBase.obter_usuario_logado)]) -> VMUsuarioLogado:

        return usuario_logado
    perfil.rota = {'path': '/autenticacao/perfil', 'methods': ['GET']}

    async def validar(self) -> None:
        return Response(status_code=status.HTTP_200_OK)
    validar.rota = {'path': '/autenticacao/validar', 'methods': ['GET'], 
        'dependencies': [Depends(ControladorBase.obter_usuario_logado)]}