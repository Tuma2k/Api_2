from pydantic import BaseModel
from datetime import datetime, date, time # <-- IMPORTAMOS DATE Y TIME
from typing import List, Any 

# (pa_reception y respuesta se quedan igual)
class pa_reception(BaseModel):
    Humedad: float
    Temperatura: float
    EstadoBoton: int

class respuesta(BaseModel):
    respuesta: str
    fechahora: datetime

# --- CAMBIOS AQUÍ ---

class Registro(BaseModel):
    Humedad: float
    Temperatura: float
    EstadoBoton: int
    fecha: date # <-- Columna de fecha
    hora: time  # <-- Columna de hora

class respGet(BaseModel):
    registros: List[Registro] # Usa el nuevo modelo 'Registro'