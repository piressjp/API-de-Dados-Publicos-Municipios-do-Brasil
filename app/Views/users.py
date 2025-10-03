from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, deps
from app.Data.Repo.user_repo import User, create_user
from typing import List
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserRead, dependencies=[Depends(deps.require_admin)])
def create(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    return create_user(db, user_in)

@router.get("/", response_model=List[schemas.UserRead], dependencies=[Depends(deps.require_admin)])
def list(db: Session = Depends(deps.get_db)):
    return db.query(User).all()

@router.delete("/{user_id}", dependencies=[Depends(deps.require_admin)])
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return {"detail": f"Usuário {user_id} deletado com sucesso"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordUpdate(BaseModel):
    new_password: str

@router.put("/{user_id}/password", dependencies=[Depends(deps.require_admin)])
def update_password(user_id: int, password_data: PasswordUpdate, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    hashed_password = pwd_context.hash(password_data.new_password)
    user.password = hashed_password
    db.commit()
    return {"detail": f"Senha do usuário {user_id} atualizada com sucesso"}
