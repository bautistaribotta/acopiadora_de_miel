from model.conexion_db import abrir_conexion


def buscar_operaciones_cliente(id_cliente):
    """
    Esta funcion permite traer todo el listado de operaciones de un cliente
    :param id_cliente:
    :return listado de operaciones del cliente:
    """
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = "SELECT * FROM operaciones WHERE id_cliente = %s"
        cursor.execute(intruccion_sql, id_cliente)
        resultados = cursor.fetchall()
        return resultados


def nueva_operacion(id_cliente):