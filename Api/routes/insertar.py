from fastapi import APIRouter, Depends, HTTPException, status
from models.paquete import pa_reception, respuesta 
from datetime import datetime
from .seguridad import validar_acceso_post
from utils.connectBBD import InsertarDatos

router = APIRouter()

@router.post('/reception')
def reception(data: pa_reception, api_key: str = Depends(validar_acceso_post)):

    if not InsertarDatos(data.Humedad, data.Temperatura, data.EstadoBoton, api_key):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                              detail="Error al insertar los datos en la base de datos")

    return respuesta(respuesta='Dato recibido', fechahora=datetime.now())