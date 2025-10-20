from pydantic import BaseModel
from datetime import datetime 
from typing import List, Any 

class pa_reception(BaseModel):
    Humedad: float
    Temperatura: float
    EstadoBoton: int

class respuesta(BaseModel):
    respuesta: str
    fechahora: datetime

class Registro(BaseModel):
    Humedad: float
    Temperatura: float
    EstadoBoton: int
    instantelectura: datetime 

class respGet(BaseModel):
    registros: List[Registro]