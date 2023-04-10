from bcrypt import gensalt, hashpw

class Autenticador(object):

    def __init__(self, algoritmo_chave, chave_privada, chave_publica, dificuldade_salt=12) -> None:
        self.algoritmo_chave = algoritmo_chave
        self.chave_privada = chave_privada
        self.chave_publica = chave_publica
        self.dificuldade_salt = dificuldade_salt
    
    def obter_salt(self) -> bytes:
        return gensalt(self.dificuldade_salt)

    def obter_hash_senha(self, senha: str, salt: bytes) -> bytes:
        return hashpw(bytes(senha, encoding='utf-8'), salt)
    
    def verificar_senha(self, senha: str, salt: bytes, hash_senha: bytes) -> bool:
        resultado = self.obter_hash_senha(senha, salt)
        return hash_senha == resultado