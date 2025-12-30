import mysql.connector

def buscar_cliente(nombre):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    intruccion_sql = f"SELECT (id, nombre, localidad, telefono) FROM clientes WHERE nombre = {nombre}"


def insertar_cliente(nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = """INSERT INTO clientes 
                    (nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit)

    cursor.execute(instruccion_sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_cliente(id_cliente):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = "DELETE FROM clientes WHERE ID = %s"
    # Debe llevar una "," al final para ser tomado como tupla
    valores = (id_cliente,)

    cursor.execute(instruccion_sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()