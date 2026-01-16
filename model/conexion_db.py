from contextlib import contextmanager
import mysql.connector

# --- CONFIGURACION DE LA BASE DE DATOS ---
DB_CONFIG = {
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
    
    Uso:
        with abrir_conexion() as (cursor, conexion):
            cursor.execute(...)
            ...
    (No olvides hacer conexion.commit() si modificas datos)
    """
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        yield cursor, conexion
    except mysql.connector.Error as err:
        if conexion:
            conexion.rollback()
        raise err
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
