from sqlalchemy.orm import Session
from sqlalchemy import select
from app import schemas
from app.Models import User
from app.auth import get_password_hash

# Users
def get_user_by_username(db: Session, username: str):
    return db.execute(select(User).filter_by(username=username)).scalar_one_or_none()

def create_user(db: Session, user_in: schemas.UserCreate):
    user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role or "leitor"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
