import mysql.connector
from model.entidades import Cliente


def nuevo_cliente_db(cliente : Cliente):
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

    valores = (cliente.nombre, cliente.apellido, cliente.telefono,
               cliente.localidad, cliente.direccion,
               cliente.factura_produccion, cliente.cuit)

    cursor.execute(instruccion_sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def editar_cliente(id_cliente, cliente : Cliente):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    intruccion_sql = ("UPDATE clientes SET nombre=%s, apellido=%s, telefono=%s, "
                      "localidad=%s, direccion=%s, factura_produccion=%s, cuit=%s WHERE id = %s")

    valores = (cliente.nombre, cliente.apellido,
               cliente.telefono, cliente.localidad, cliente.direccion,
               cliente.factura_produccion, cliente.cuit, id_cliente)
    cursor.execute(intruccion_sql, valores)

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

    instruccion_sql = "DELETE FROM clientes WHERE id = %s"
    # Debe llevar una "," al final para ser tomado como tupla
    valores = (id_cliente,)
    cursor.execute(instruccion_sql, valores)
    conexion.commit()

    cursor.close()
    conexion.close()


def listar_clientes_db():
    """
    Esta funcion se usa para mostrar los datos de todos los clientes en el treeview
    """
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    # Selecciono las columnas separadas para concatenar en el frontend y permitir busquedas separadas pero mostrar igual
    instruccion = "SELECT id, nombre, apellido, localidad, telefono FROM clientes"
    cursor.execute(instruccion)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados


def buscar_cliente_id(id_cliente):
    """
    Tener en cuenta que esta funcion usa el = es para solo usar uno, para buscar entre los clientes
    en un buscador en tiempo real, se debe usar la funcion "buscador_cliente_por_id"
    Esta sirve para buscar un cliente solo en la DB, no en la tabla, y eliminarlo o editarlo
    """
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    intruccion_sql = f"SELECT * FROM clientes WHERE id = %s"
    valor = (id_cliente,)
    cursor.execute(intruccion_sql, valor)
    resultados = cursor.fetchone()

    cursor.close()
    conexion.close()
    return resultados


def buscador_cliente_por_id(id_cliente):
    """Tener en cuenta que esta funcion usa LIKE ya que hace una busqueda en tiempo real"""
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    intruccion_sql = f"SELECT id, nombre, apellido, localidad, telefono FROM clientes WHERE id LIKE %s"
    valor = (f"%{id_cliente}%",)
    cursor.execute(intruccion_sql, valor)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados


def buscador_cliente_por_nombre(criterio):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="southern_honey_group"
    )
    cursor = conexion.cursor()

    # Buscar en nombre O apellido
    intruccion_sql = "SELECT id, nombre, apellido, localidad, telefono FROM clientes WHERE nombre LIKE %s OR apellido LIKE %s"
    valor = (f"%{criterio}%", f"%{criterio}%")
    cursor.execute(intruccion_sql, valor)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()
    return resultados