from dotenv import dotenv_values
from uuid import uuid1
from bcrypt import gensalt, hashpw

class Utilidades(object):

    @staticmethod
    def obter_connection_string():
        ambiente = dotenv_values()
        return f"{ambiente.get('SQLA_DIALECT')}+{ambiente.get('SQLA_DRIVER')}://{ambiente.get('DB_USER')}:{ambiente.get('DB_PASSWORD')}@{ambiente.get('DB_HOST')}:{ambiente.get('DB_PORT')}/{ambiente.get('DB_NAME')}"
    
    @staticmethod
    def uuid36():
        return str(uuid1())
    
    @staticmethod
    def obter_salt():
        return gensalt()

    @staticmethod
    def hash_senha(senha: str, salt: str):
        return hashpw(senha, salt)
    
    
