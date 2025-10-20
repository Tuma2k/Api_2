from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from utils.connectBBD import ValidarApiKeyPost, ValidarApiKeyGet

apikey_header = APIKeyHeader(name='API-Key', auto_error=False) 


def validar_acceso_post(api_key: str = Depends(apikey_header)):

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no encontrada en la cabecera"
        )   
    if ValidarApiKeyPost(api_key):
        return api_key  
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API Key inválida o sin permisos para esta operación (POST)"
    )


def validar_acceso_get(api_key: str = Depends(apikey_header)):

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no encontrada en la cabecera"
        )
    if ValidarApiKeyGet(api_key):
        return api_key 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API Key inválida o sin permisos para esta operación (GET)"
    )