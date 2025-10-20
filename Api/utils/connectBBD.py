import mysql.connector as mq
import mysql.connector.errors as mqE

db_config = {
    "host": "localhost",
    "user": "apikey",
    "password": "miraculos",
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
        consulta = (
            "INSERT INTO regDatos (Humedad, Temperatura, EstadoBoton, Origen) "
            "VALUES (%s, %s, %s, (SELECT id_disp FROM ApikeyPost WHERE apikey = %s))"
        )
        datos = (humedad, temperatura, estado_boton, apikey)
        cursor.execute(consulta, datos)
        bbdd.commit()
        return True
    except mqE.Error as err:
        print(f"Error de base de datos al insertar: {err}")
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
            "SELECT Humedad, Temperatura, EstadoBoton, instantelectura "
            "FROM regDatos WHERE Origen = %s "
            "ORDER BY instantelectura DESC LIMIT 10"
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
            "SELECT Humedad, Temperatura, EstadoBoton, instantelectura "
            "FROM regDatos WHERE Origen = %s "
            "ORDER BY instantelectura DESC LIMIT 1"
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