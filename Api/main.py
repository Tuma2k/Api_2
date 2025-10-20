from fastapi import FastAPI
# 1. Importa los routers de insertar y el nuevo de consultar
from routes import insertar
from routes import consultar 

app = FastAPI()

app.include_router(insertar.router)
app.include_router(consultar.router)

