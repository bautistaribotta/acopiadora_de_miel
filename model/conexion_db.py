from contextlib import contextmanager
import mysql.connector

# --- CONFIGURACION DE LA BASE DE DATOS ---
db_configuracion = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "southern_honey_group"
}


@contextmanager
def abrir_conexion():
    """
    Context manager para gestionar la conexión a la base de datos de manera eficiente.
    Abre la conexión, crea el cursor y se asegura de cerrarlos 
    correctamente incluso si ocurre un error (usando try/finally).

    (No olvidar hacer conexion.commit() si modifico datos)
    """
    conexion = None
    cursor = None
    try:
        # "**" asteriscos se usan para desglosar un diccionario
        conexion = mysql.connector.connect(**db_configuracion)
        cursor = conexion.cursor()
        # Yield pausa la ejecucion de la conexion y entrega las variables de la conexion
        yield cursor, conexion

    except mysql.connector.Error as e:
        if conexion:
            # Rollback permite deshacer los cambios si algo sale mal
            conexion.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()