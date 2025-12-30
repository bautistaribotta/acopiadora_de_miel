import mysql.connector


def buscar_producto_nombre(nombre_producto):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = "SELECT id, nombre, categoria, cantidad FROM productos WHERE nombre LIKE %s"
    valor = (f"%{nombre_producto}%",)

    cursor.execute(instruccion_sql, valor)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados


def buscar_producto_id(id_producto):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = "SELECT id, nombre, categoria, cantidad FROM productos WHERE id LIKE %s"
    valor = (f"%{id_producto}%",)

    cursor.execute(instruccion_sql, valor)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados


def insertar_producto(nombre, categoria, unidad_medida, precio, cantidad):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = """INSERT INTO productos (nombre, categoria, unidad_medida, precio, cantidad) 
                        VALUES (%s, %s, %s, %s, %s)"""
    valores = (nombre, categoria, unidad_medida, precio, cantidad)
    cursor.execute(instruccion_sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def eliminar_producto(id_producto):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    instruccion_sql = """DELETE FROM productos WHERE id = %s"""
    valor = (id_producto,)
    cursor.execute(instruccion_sql, valor)
    conexion.commit()

    cursor.close()
    conexion.close()