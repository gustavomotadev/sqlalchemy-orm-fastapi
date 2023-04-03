import datetime
import re
from dotenv import dotenv_values
from uuid import uuid1
from bcrypt import gensalt, hashpw
from typing import Dict

class Utilidades(object):

    _regex_cnh = re.compile(r'[0-9]{11}')
    _regex_placa = re.compile(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}')

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
    
    @staticmethod
    def remover_none_dict(dic: Dict):
        return {k: v for k, v in dic.items() if v is not None}
    
    @staticmethod
    def validar_horario(horario: datetime.time) -> datetime.time:
        if (horario < datetime.time(5) or 
            horario > datetime.time(22) or 
            int(horario.minute) % 15 != 0):
            raise ValueError
        else:
            return horario

    @classmethod
    def validar_cnh(cls, cnh: str) -> str:

        # Verifica comprimento da string
        # E se todos os caracteres são dígitos
        if re.fullmatch(cls._regex_cnh, cnh) is None:
            raise ValueError
        
        _cnh = [int(d) for d in cnh]
        
        aux = 0
        
        soma_dv_1 = 0
        for i in range(9):
            soma_dv_1 += _cnh[i] * (9-i)

        dv_1_valido = soma_dv_1 % 11
        
        if dv_1_valido >= 10:
            dv_1_valido = 0
            aux = 2
        
        soma_dv_2 = 0
        for i in range(9):
            soma_dv_2 += _cnh[i] * (1+i)

        dv_2_valido = soma_dv_2 % 11
        
        dv_2_valido = 0 if dv_2_valido >= 10 else dv_2_valido - aux
        
        if _cnh[9] == dv_1_valido and _cnh[10] == dv_2_valido:
            return cnh
        else:
            raise ValueError
    
    # Valida uma placa de veículo brasileira ou do Mercosul.
    @classmethod
    def validar_placa(cls, placa):

        if re.fullmatch(cls._regex_placa, placa) is not None:
            return placa
        else:
            raise ValueError
