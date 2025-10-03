from typing import Optional
from sqlalchemy.orm import Session
from app.Models import Municipio

# Municipios
def create_municipio(db: Session, obj_in: dict):
    m = Municipio(**obj_in)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def list_municipios(db: Session, skip: int = 0, limit: int = 100, uf: Optional[str] = None):
    q = db.query(Municipio)
    if uf:
        q = q.filter(Municipio.uf == uf.upper())
    return q.offset(skip).limit(limit).all()


def get_municipio(db: Session, id: int):
    return db.get(Municipio, id)
