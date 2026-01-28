from controller.entidades import Cliente
from model.conexion_db import abrir_conexion


def nuevo_cliente_db(cliente : Cliente):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = """INSERT INTO clientes 
                        (nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        valores = (cliente.nombre, cliente.apellido, cliente.telefono,
                   cliente.localidad, cliente.direccion,
                   cliente.factura_produccion, cliente.cuit)

        cursor.execute(instruccion_sql, valores)
        conexion.commit()


def editar_cliente(id_cliente, cliente : Cliente):
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = ("UPDATE clientes SET nombre=%s, apellido=%s, telefono=%s, "
                          "localidad=%s, direccion=%s, factura_produccion=%s, cuit=%s WHERE id = %s")

        valores = (cliente.nombre, cliente.apellido,
                   cliente.telefono, cliente.localidad, cliente.direccion,
                   cliente.factura_produccion, cliente.cuit, id_cliente)
        cursor.execute(intruccion_sql, valores)
        conexion.commit()


def eliminar_cliente(id_cliente):
    with abrir_conexion() as (cursor, conexion):
        instruccion_sql = "DELETE FROM clientes WHERE id = %s"
        # Debe llevar una "," al final para ser tomado como tupla
        valores = (id_cliente,)
        cursor.execute(instruccion_sql, valores)
        conexion.commit()


def listar_clientes_db():
    """
    Uso esta función para mostrar todos los clientes en el treeview
    """
    with abrir_conexion() as (cursor, conexion):
        # Selecciono las columnas separadas para concatenar en el frontend y permitir búsquedas separadas pero mostrar igual
        instruccion = "SELECT id, nombre, apellido, localidad, telefono FROM clientes"
        cursor.execute(instruccion)
        resultados = cursor.fetchall()
        return resultados


def buscar_cliente_id(id_cliente):
    """
    Tengo en cuenta que esta función usa el = para usar solo uno. Para buscar entre los clientes
    en tiempo real, debo usar "buscador_cliente_por_id"
    Esta sirve para buscar un cliente solo en la DB, no en la tabla, para eliminarlo o editarlo
    """
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = f"SELECT * FROM clientes WHERE id = %s"
        valor = (id_cliente,)
        cursor.execute(intruccion_sql, valor)
        resultados = cursor.fetchone()
        return resultados


def buscador_cliente_por_id(id_cliente):
    """Tengo en cuenta que esta función usa LIKE ya que hace una búsqueda en tiempo real"""
    with abrir_conexion() as (cursor, conexion):
        intruccion_sql = f"SELECT id, nombre, apellido, localidad, telefono FROM clientes WHERE id LIKE %s"
        valor = (f"%{id_cliente}%",)
        cursor.execute(intruccion_sql, valor)
        resultados = cursor.fetchall()
        return resultados


def buscador_cliente_por_nombre(criterio):
    with abrir_conexion() as (cursor, conexion):
        # Busco en nombre O apellido
        intruccion_sql = "SELECT id, nombre, apellido, localidad, telefono FROM clientes WHERE nombre LIKE %s OR apellido LIKE %s"
        valor = (f"%{criterio}%", f"%{criterio}%")
        cursor.execute(intruccion_sql, valor)
        resultados = cursor.fetchall()
        return resultados