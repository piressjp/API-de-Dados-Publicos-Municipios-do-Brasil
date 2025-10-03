from sqlalchemy import Column, Integer, String, DateTime
from app.Data.context import Base


class Municipio(Base):
    __tablename__ = "municipios"
    id = Column(Integer, primary_key=True, index=True)
    codigo_tom = Column(String(50), index=True, nullable=True)
    codigo_ibge = Column(String(50), index=True, nullable=True)
    municipio_tom = Column(String(200), nullable=True)
    municipio_ibge = Column(String(200), nullable=True)
    uf = Column(String(5), nullable=True)