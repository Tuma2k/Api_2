from fastapi import APIRouter, Depends, HTTPException, status
from .seguridad import validar_acceso_get
from utils.connectBBD import ConsultarUltimoDato, ConsultarUltimosDiezDatos
from models.paquete import respGet 

router = APIRouter()

@router.get(
    "/datos/ultimo", 
    response_model=respGet 
)
async def obtener_ultimo_dato(
    id_dispositivo: str,
    api_key: str = Depends(validar_acceso_get)
):
    datos = ConsultarUltimoDato(id_dispositivo)
    # --- CAMBIO: Verificamos la clave 'registros' ---
    if not datos["registros"]: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No se encontraron datos para el dispositivo especificado")
    return datos

@router.get(
    "/datos/ultimos-diez", 
    response_model=respGet 
)
async def obtener_ultimos_diez(
    id_dispositivo: str, 
    api_key: str = Depends(validar_acceso_get)
):
    
    datos = ConsultarUltimosDiezDatos(id_dispositivo)
    # --- CAMBIO: Verificamos la clave 'registros' ---
    if not datos["registros"]: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No se encontraron datos para el dispositivo especificado")
    return datos