from model.conexion_db import abrir_conexion
from model.entidades import Operacion, DetalleOperacion


def buscar_operaciones_cliente(id_cliente):
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = "SELECT * FROM operaciones WHERE id_cliente = %s"
        cursor.execute(intruccion_sql, id_cliente)
        resultados = cursor.fetchall()
        return resultados


def nueva_operacion(operacion: Operacion, lista_detalles: list):
    with abrir_conexion() as (cursor, conexion):
        sql_operacion = """
            INSERT INTO operaciones 
            (id_cliente, monto_total, valor_dolar, valor_kilo_miel) 
            VALUES (%s, %s, %s, %s)
        """
        valores_operacion = (
            operacion.id_cliente,
            operacion.monto_total,
            operacion.valor_dolar,
            operacion.valor_kilo_miel
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