import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine import Engine
from typing import List
from locacao.modelos.modelo_base import ModeloBase

class RepositorioBase(object):
    
    def __init__(self, engine: Engine, modelo: ModeloBase) -> None:
        super().__init__()
        self.engine = engine
        self.modelo = modelo

    def listar_todos(self) -> List[ModeloBase]:
        with orm.Session(self.engine, expire_on_commit=False) as session:
            listados = session.execute(
                sa.select(self.modelo)).scalars().all()
        return listados
    
    def inserir(self, **kwargs) -> ModeloBase:
        criado = self.modelo(**kwargs)
        with orm.Session(self.engine, expire_on_commit=False) as session:
            session.add(criado)
            session.commit()
        return criado
    
    def alterar(self, editado: ModeloBase) -> ModeloBase:
        with orm.Session(self.engine, expire_on_commit=False) as session:
            session.add(editado)
            session.commit()
        return editado
    
    def remover(self, apagado: ModeloBase) -> ModeloBase:
        with orm.Session(self.engine, expire_on_commit=False) as session:
            session.delete(apagado)
            session.commit()
        return apagado
    
    def filtrar(self, **kwargs) -> List[ModeloBase]:
        with orm.Session(self.engine, expire_on_commit=False) as session:
            listados = session.execute(sa.select(
                self.modelo).filter_by(**kwargs)).scalars().all()
        return listados