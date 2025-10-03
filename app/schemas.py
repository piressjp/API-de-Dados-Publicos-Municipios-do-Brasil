from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "leitor"

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes  = True

class MunicipioBase(BaseModel):
    codigo_tom: Optional[str] = None
    codigo_ibge: Optional[str] = None
    municipio_tom: Optional[str] = None
    municipio_ibge: Optional[str] = None
    uf: Optional[str] = None

class MunicipioRead(MunicipioBase):
    id: int
    class Config:
        from_attributes  = True
