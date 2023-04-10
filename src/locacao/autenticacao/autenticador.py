import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from bcrypt import gensalt, hashpw
from typing import Optional

class Autenticador(object):

    def __init__(self, algoritmo_chave, chave_privada, chave_publica, validade_token=60, dificuldade_salt=12) -> None:
        self._algoritmo_chave = algoritmo_chave
        self._chave_privada = chave_privada
        self._chave_publica = chave_publica
        self._validade_token = validade_token
        self._dificuldade_salt = dificuldade_salt
    
    def obter_salt(self) -> bytes:
        return gensalt(self._dificuldade_salt)

    def obter_hash_senha(self, senha: str, salt: bytes) -> bytes:
        return hashpw(bytes(senha, encoding='utf-8'), salt)
    
    def verificar_senha(self, senha: str, salt: bytes, hash_senha: bytes) -> bool:
        resultado = self.obter_hash_senha(senha, salt)
        return hash_senha == resultado
    
    def gerar_token_jwt(self, dados: dict, 
        validade_minutos: Optional[int] = None) -> str:

        if validade_minutos is None:
            validade_minutos = self._validade_token
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=validade_minutos)
        payload = {**dados, 'iat': iat, 'exp': exp}
        token = jwt.encode(payload, self._chave_privada, self._algoritmo_chave)