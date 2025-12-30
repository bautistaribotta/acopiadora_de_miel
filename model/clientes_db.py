import mysql.connector

def buscar_cliente():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()


def nuevo_cliente(nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    sql = ("""INSERT INTO clientes (nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""")
    valores = (nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit)

    cursor.execute(sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_cliente():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()