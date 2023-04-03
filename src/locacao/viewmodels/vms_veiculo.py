from pydantic import BaseModel, Field, UUID1, validator
from locacao.modelos.veiculo import Veiculo
from locacao.util.util import Utilidades

class VMVeiculo(BaseModel):
    uuid: UUID1
    uuid_condutor: UUID1
    placa: str = Field(min_length=7, max_length=7)
    modelo: str = Field(max_length=30)
    tipo: str = Field(max_length=30)
    combustivel: str = Field(max_length=30)
    capacidade: int = Field(ge=0)
    cor: str = Field(max_length=30)
    
    @validator('placa')
    def validar_placa(placa: str) -> str: 
        return Utilidades.validar_placa(placa)

    @staticmethod
    def converter_modelo(modelo: Veiculo):
        return VMVeiculo(uuid=modelo.uuid, 
            uuid_condutor=modelo.uuid_condutor, 
            placa=modelo.placa, modelo=modelo.modelo, 
            tipo=modelo.tipo, combustivel=modelo.combustivel,
            capacidade=modelo.capacidade, cor=modelo.cor)
    
class VMVeiculoSemUUID(BaseModel):
    uuid_condutor: UUID1
    placa: str = Field(min_length=7, max_length=7)
    modelo: str = Field(max_length=30)
    tipo: str = Field(max_length=30)
    combustivel: str = Field(max_length=30)
    capacidade: int = Field(ge=0)
    cor: str = Field(max_length=30)
    
    @validator('placa')
    def validar_placa(placa: str) -> str: 
        return Utilidades.validar_placa(placa)
    
class VMVeiculoCondutor(BaseModel):
    uuid_condutor: UUID1
