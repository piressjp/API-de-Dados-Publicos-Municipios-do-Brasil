from app.Data.context import SessionLocal, init_db
from app import schemas
from app.Data.Repo import user_repo

init_db()
db = SessionLocal()

admin_in = schemas.UserCreate(username="admin", password="admin123", role="admin")

if not user_repo.get_user_by_username(db, "admin"):
    user_repo.create_user(db, admin_in)

print("Usuários criados")
db.close()
