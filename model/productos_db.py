from model.entidades import Producto
from model.conexion_db import abrir_conexion


def nuevo_producto(producto : Producto):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = """INSERT INTO productos (nombre, categoria, unidad_medida, precio, cantidad) 
                            VALUES (%s, %s, %s, %s, %s)"""

        valores = (producto.nombre, producto.categoria,
                   producto.unidad_medida, producto.precio, producto.cantidad)

        cursor.execute(instruccion_sql, valores)
        conexion.commit()


def editar_producto(id_producto, producto : Producto):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = ("UPDATE productos SET nombre=%s, categoria=%s, unidad_medida=%s, "
                           "precio=%s, cantidad=%s WHERE id = %s")

        valores = (producto.nombre, producto.categoria, producto.unidad_medida,
                   producto.precio, producto.cantidad, id_producto)

        cursor.execute(instruccion_sql, valores)
        conexion.commit()


def eliminar_producto(id_producto):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = """DELETE FROM productos WHERE id = %s"""
        valor = (id_producto,)
        cursor.execute(instruccion_sql, valor)
        conexion.commit()


def sumar_stock_db(id_producto, cantidad):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = "UPDATE productos SET cantidad = cantidad + %s WHERE id = %s"
        valores = (cantidad, id_producto)

        cursor.execute(instruccion_sql, valores)
        conexion.commit()


def listar_producto_db():
    with abrir_conexion() as (cursor, conexion):
        instruccion = "SELECT id, nombre, categoria, precio, cantidad FROM productos"
        cursor.execute(instruccion)
        resultados = cursor.fetchall()
        return resultados


def buscar_producto_id(id_producto):
    """
    Tener en cuenta que esta funcion usa el = es para solo usar uno, para buscar entre los productos
    en un buscador en tiempo real, se debe usar la funcion "buscador_producto_por_id"
    """
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = f"SELECT id, nombre, categoria, precio, cantidad, unidad_medida FROM productos WHERE id = %s"
        valor = (id_producto,)
        cursor.execute(intruccion_sql, valor)
        resultados = cursor.fetchone()
        return resultados


def buscador_producto_por_id(id_producto):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = "SELECT id, nombre, categoria, precio, cantidad FROM productos WHERE id LIKE %s"
        valor = (f"%{id_producto}%",)

        cursor.execute(instruccion_sql, valor)
        resultados = cursor.fetchall()
        return resultados


def buscador_producto_por_nombre(nombre_producto):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = "SELECT id, nombre, categoria, precio, cantidad FROM productos WHERE nombre LIKE %s"
        valor = (f"%{nombre_producto}%",)

        cursor.execute(instruccion_sql, valor)
        resultados = cursor.fetchall()
        return resultados