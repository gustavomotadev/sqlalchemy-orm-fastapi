import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import List
from locacao.modelos.modelo_base import ModeloBase

class Pessoa(ModeloBase):
    __tablename__ = "pessoa"

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), primary_key=True)
    cnh: orm.Mapped[str] = orm.mapped_column(sa.String(11), unique=True)
    tipo: orm.Mapped[str] = orm.mapped_column(sa.String(30))
    nome: orm.Mapped[str] = orm.mapped_column(sa.String(100))

    # usuario: orm.Mapped["Usuario"] = orm.relationship(back_populates="pessoa")
    # veiculos: orm.Mapped[List["Veiculo"]] = orm.relationship(back_populates="pessoa")

    def __init__(self, uuid: str, cnh: str, tipo: str, nome: str):
        super().__init__()
        self.uuid = uuid
        self.cnh = cnh
        self.tipo = tipo
        self.nome = nome

    def __repr__(self) -> str:
        return (f"Pessoa(uuid={self.uuid}, cnh={self.cnh}, " + 
                f"tipo={self.tipo}, nome={self.nome})")
