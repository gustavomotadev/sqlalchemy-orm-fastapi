import datetime
import re
from dotenv import dotenv_values
from uuid import uuid1
from typing import Dict
from pydantic import SecretStr

class Utilidades(object):

    _regex_cnh = re.compile(r'[0-9]{11}')
    _regex_placa = re.compile(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}')
    _regex_acesso = re.compile(r'[a-zA-Z][a-zA-Z0-9_]{5,19}')
    _regex_senha = re.compile(r'[a-zA-Z0-9._?!@#$%&-+*=]{6,20}')

    @staticmethod
    def obter_connection_string() -> str:
        ambiente = dotenv_values()
        return f"{ambiente.get('SQLA_DIALECT')}+{ambiente.get('SQLA_DRIVER')}://{ambiente.get('DB_USER')}:{ambiente.get('DB_PASSWORD')}@{ambiente.get('DB_HOST')}:{ambiente.get('DB_PORT')}/{ambiente.get('DB_NAME')}"
    
    @staticmethod
    def obter_chaves() -> Dict[str, str | None]:
        ambiente = dotenv_values()
        return {'algoritmo_chave': ambiente.get('KEY_ALGORITHM'), 
            'chave_privada': ambiente.get('PRIVATE_KEY'), 
            'chave_publica': ambiente.get('PUBLIC_KEY'),
            'validade_token': int(ambiente.get('TOKEN_EXP_TIME')) if ambiente.get('TOKEN_EXP_TIME') else None}

    @staticmethod
    def uuid36() -> str:
        return str(uuid1())
    
    @staticmethod
    def remover_none_dict(dic: Dict) -> Dict:
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
    def validar_placa(cls, placa: str) -> str:

        if re.fullmatch(cls._regex_placa, placa) is not None:
            return placa
        else:
            raise ValueError
        
    @classmethod
    def validar_acesso(cls, acesso: str) -> str:
        if re.fullmatch(cls._regex_acesso, acesso) is not None:
            return acesso
        else:
            raise ValueError
        
    @classmethod
    def validar_senha(cls, senha: SecretStr) -> SecretStr:
        if re.fullmatch(cls._regex_senha, senha.get_secret_value()) is not None:
            return senha
        else:
            raise ValueError
