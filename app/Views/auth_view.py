from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import auth, deps, schemas
from app.Data.Repo import user_repo
from datetime import timedelta
import os

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = user_repo.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
    token = auth.create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}
