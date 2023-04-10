from typing import Annotated
from fastapi import Depends, HTTPException, status
from locacao.autenticacao.autenticacao import Autenticador
from locacao.dependencias.singletons import autenticador, esquema_oauth2
from locacao.viewmodels.vms_autenticacao import VMUsuario

class ControladorBase(object):

    class ErroAutenticacao(HTTPException):
        def __init__(self, detalhe: str) -> None:
            super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=detalhe, headers={"WWW-Authenticate": "Bearer"})
    
    @classmethod
    async def obter_usuario_logado(cls, 
        aut: Annotated[Autenticador, Depends(autenticador)], 
        token: Annotated[str, Depends(esquema_oauth2)]) -> VMUsuario:

        dados = aut.validar_token_jwt(token)
        if dados is None:
            raise cls.ErroAutenticacao(detalhe='Não foi possível validar o token')
        
        return VMUsuario(**dados)