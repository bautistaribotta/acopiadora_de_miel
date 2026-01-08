import mysql.connector


def inicion_sesion(usuario, clave):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = "SELECT usuario, clave FROM usuarios WHERE usuario=%s AND clave=%s"
    valores = (usuario, clave)
    cursor.execute(instruccion_sql, valores)

    # Si encontro el usuario con su contraseña, retorna los valores, si no, retorna NONE
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado