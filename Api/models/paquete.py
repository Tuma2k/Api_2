from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List

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
    fecha: date
    hora: time

class respGet(BaseModel):
    registros: List[Registro]