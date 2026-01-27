from model.conexion_db import abrir_conexion
from model.entidades import Operacion


def buscar_operaciones_cliente(id_cliente):
    # Esta funcion se utiliza para mostrar en la vista de infomarcion_cliente
    # un listado de todas las operaciones que hizo
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = "SELECT * FROM operaciones WHERE id_cliente = %s"
        cursor.execute(intruccion_sql, (id_cliente,))
        resultados = cursor.fetchall()
        return resultados


def obtener_operacion_por_id(id_operacion):
    # Esta funcion se utiliza para mostrar la informacion de una operacion
    with abrir_conexion() as (cursor, conexion):
        sql = "SELECT * FROM operaciones WHERE id = %s"
        cursor.execute(sql, (id_operacion,))
        return cursor.fetchone()


def obtener_detalles_operacion(id_operacion):
    # Esta funcion se utiliza para mostrar la informacion de los detalles de una operacion
    with abrir_conexion() as (cursor, conexion):
        sql = """
            SELECT do.id_producto, p.nombre, do.cantidad, p.precio 
            FROM detalle_operaciones do
            JOIN productos p ON do.id_producto = p.id
            WHERE do.id_operacion = %s
        """
        cursor.execute(sql, (id_operacion,))
        return cursor.fetchall()


def nueva_operacion(operacion: Operacion, lista_detalles: list):
    with abrir_conexion() as (cursor, conexion):
        sql_operacion = """
            INSERT INTO operaciones (id_cliente, monto_total, valor_dolar, valor_kilo_miel, observaciones) VALUES (%s, %s, %s, %s, %s)
        """
        valores_operacion = (
            operacion.id_cliente,
            operacion.monto_total,
            operacion.valor_dolar,
            operacion.valor_kilo_miel,
            operacion.observaciones
        )
        cursor.execute(sql_operacion, valores_operacion)

        # 2. Recuperar ID
        id_nueva_operacion = cursor.lastrowid

        # 3. Insertar detalles
        sql_detalle = """
            INSERT INTO detalle_operaciones (id_operacion, id_producto, cantidad) 
            VALUES (%s, %s, %s)
        """

        datos_detalles = []
        for detalle in lista_detalles:
            datos_detalles.append((id_nueva_operacion, detalle.id_producto, detalle.cantidad))

        cursor.executemany(sql_detalle, datos_detalles)
        conexion.commit()


def editar_operacion(id_operacion, operacion : Operacion, lista_detalles: list):
    with abrir_conexion() as (cursor, conexion):
        # 1 - Actualizo la operacion
        sql_operacion = """ 
        UPDATE operaciones SET observaciones=%s, monto_total=%s 
        WHERE id=%s
        """
        valores = (operacion.observaciones, operacion.monto_total, id_operacion)
        cursor.execute(sql_operacion, valores)

        # 2 - Borro el detalle de la operacion antes de volver a crearlo
        sql_borrar_detalle = "DELETE FROM detalle_operaciones WHERE id_operacion=%s"
        cursor.execute(sql_borrar_detalle, (id_operacion,))

        # 3 - Inserto los nuevos detalles
        sql_operacion = """
            INSERT INTO detalle_operaciones (id_operacion, id_producto, cantidad) 
            VALUES (%s, %s, %s)"""

        datos_detalle = []
        for detalle in lista_detalles:
            datos_detalle.append((id_operacion, detalle.id_producto, detalle.cantidad))

        cursor.executemany(sql_operacion, datos_detalle)
        conexion.commit()


def eliminar_operacion(id_operacion):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = "DELETE FROM operaciones WHERE id=%s"
        cursor.execute(instruccion_sql, (id_operacion,))

        conexion.commit()

