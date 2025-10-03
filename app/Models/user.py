from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.Data.context import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="leitor")  # 'admin' ou 'leitor'
    created_at = Column(DateTime(timezone=True), server_default=func.now())