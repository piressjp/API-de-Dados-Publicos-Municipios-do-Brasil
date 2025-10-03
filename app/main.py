from fastapi import FastAPI
from app.Views import auth_view as auth_router, users as users_router, data as data_router
from app.Data.context import init_db

app = FastAPI(title="API de Dados Públicos - Municípios do Brasil")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(data_router.router)

@app.get("/")
def root():
    return {"message": "API de Dados Públicos rodando. Veja /docs para Swagger UI."}
