from fastapi import FastAPI
from database import init_db

app = FastAPI(title="Сириус Аренда API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}
