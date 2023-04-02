import sqlalchemy as sa
import sqlalchemy.orm as orm
from locacao.modelos.modelo_base import ModeloBase

class Usuario(ModeloBase):
    __tablename__ = "usuario"

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), primary_key=True)
    uuid_pessoa: orm.Mapped[str] = orm.mapped_column(sa.ForeignKey("pessoa.uuid"))
    acesso: orm.Mapped[str] = orm.mapped_column(sa.String(20))
    salt_senha: orm.Mapped[bytes] = orm.mapped_column(sa.BINARY(29))
    hash_senha: orm.Mapped[bytes] = orm.mapped_column(sa.BINARY(60))

    # pessoa: orm.Mapped["Pessoa"] = orm.relationship(back_populates="usuario")

    def __repr__(self) -> str:
        return (f"Usuario(uuid={self.uuid}, uuid_pessoa={self.uuid_pessoa}, " + 
                f"acesso={self.acesso}, salt_senha=*, hash_senha=*)")
