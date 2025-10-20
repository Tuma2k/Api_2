import mysql.connector as mq
import mysql.connector.errors as mqE
from datetime import datetime

db_config = {
    "host": "localhost",
    "user": "apikey",
    "password": "mirame",
    "database": "eva01"
}

def ValidarApiKeyPost(apikey: str):
    resultado = []
    try:
        bbdd = mq.connect(**db_config)
        cursor = bbdd.cursor()
        consulta = "SELECT apikey FROM ApikeyPost WHERE apikey = %s"       
        cursor.execute(consulta, (apikey,)) 
        resultado = cursor.fetchall()    
    except mqE.Error as err:
        print(f"Error al validar API Key POST: {err}")
        return False
    finally:
        if 'bbdd' in locals() and bbdd.is_connected():
            cursor.close()
            bbdd.close()
    return len(resultado) > 0


def ValidarApiKeyGet(apikey: str):
    resultado = []
    try:
        bbdd = mq.connect(**db_config)
        cursor = bbdd.cursor()
        consulta = "SELECT apikey FROM ApikeyGet WHERE apikey = %s"
        cursor.execute(consulta, (apikey,)) 
        resultado = cursor.fetchall()
    except mqE.Error as err:
        print(f"Error al validar API Key GET: {err}")
        return False
    finally:
        if 'bbdd' in locals() and bbdd.is_connected():
            cursor.close()
            bbdd.close()
    return len(resultado) > 0

def InsertarDatos(humedad: float, temperatura: float, estado_boton: int, apikey: str):
    try: 
        bbdd = mq.connect(**db_config)
        cursor = bbdd.cursor()
        
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()

        consulta = (
            "INSERT INTO regDatos (Humedad, Temperatura, EstadoBoton, Origen, fecha, hora) "
            "VALUES (%s, %s, %s, (SELECT id_disp FROM ApikeyPost WHERE apikey = %s), %s, %s)"
        )
        datos = (humedad, temperatura, estado_boton, apikey, fecha_actual, hora_actual)
        
        cursor.execute(consulta, datos)
        bbdd.commit()
        return True
    except mqE.Error as err:
        print(f"Error de base de datos al insertar: {err}")
        bbdd.rollback()
        return False
    finally:
        if 'bbdd' in locals() and bbdd.is_connected():
            cursor.close()
            bbdd.close()

def ConsultarUltimosDiezDatos(id_dispositivo: str):
    try:
        bbdd = mq.connect(**db_config)
        cursor = bbdd.cursor(dictionary=True) 

        consulta = (
            "SELECT Humedad, Temperatura, EstadoBoton, fecha, CAST(hora AS CHAR) AS hora "
            "FROM regDatos WHERE Origen = %s "
            "ORDER BY fecha DESC, hora DESC LIMIT 10"
        )    
        cursor.execute(consulta, (id_dispositivo,))
        resultados = cursor.fetchall() 
        
        return {"registros": resultados}
    except mqE.Error as err:
        print(f"Error de base de datos al consultar últimos 10: {err}")
        return {"registros": []}
    finally:
        if 'bbdd' in locals() and bbdd.is_connected():
            cursor.close()
            bbdd.close()

def ConsultarUltimoDato(id_dispositivo: str):
    try:
        bbdd = mq.connect(**db_config)
        cursor = bbdd.cursor(dictionary=True)      
        consulta = (
            "SELECT Humedad, Temperatura, EstadoBoton, fecha, CAST(hora AS CHAR) AS hora "
            "FROM regDatos WHERE Origen = %s "
            "ORDER BY fecha DESC, hora DESC LIMIT 1"
        )        
        cursor.execute(consulta, (id_dispositivo,))
        resultado = cursor.fetchone() 
        
        if resultado:
            return {"registros": [resultado]} 
        else:
            return {"registros": []}
            
    except mqE.Error as err:
        print(f"Error de base de datos al consultar último dato: {err}")
        return {"registros": []}
    finally:
        if 'bbdd' in locals() and bbdd.is_connected():
            cursor.close()
            bbdd.close()
