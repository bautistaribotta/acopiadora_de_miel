from model.entidades import Operacion, DetalleOperacion
from model.operaciones_db import *
from tkinter import messagebox


def mostrar_listado_operaciones(id_cliente):
    try:
        operaciones = buscar_operaciones_cliente(id_cliente)
        return operaciones
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar las operaciones: {e}")
        return None


def mostrar_operacion(id_operacion):
    try:
        data_operacion = obtener_operacion_por_id(id_operacion)
        if not data_operacion:
            return None

        detalles = obtener_detalles_operacion(id_operacion)

        return {
            "operacion": data_operacion,
            "detalles": detalles
        }

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la operación: {e}")
        return None


def crear_nueva_operacion(id_cliente, monto_total, lista_items_carrito, valor_dolar, valor_kilo_miel, observaciones=""):
    # 1. Validaciones
    if not id_cliente:
        messagebox.showwarning("Error", "Debe seleccionar un cliente.")
        return False

    if not lista_items_carrito:
        messagebox.showwarning("Error", "El carrito de productos está vacío.")
        return False

    try:
        # 2. Crear el objeto Operacion (La cabecera)
        # Nota: La fecha la pone la base de datos automáticamente
        nueva_op = Operacion(
            id_cliente=id_cliente,
            monto_total=monto_total,
            valor_dolar=valor_dolar,
            valor_kilo_miel=valor_kilo_miel,
            observaciones=observaciones
        )

        # 3. Convertir los items del carrito a objetos DetalleOperacion
        lista_detalles = []
        for item in lista_items_carrito:
            # item es un diccionario: {'id': ..., 'cantidad': ...}
            detalle = DetalleOperacion(
                id_operacion=None,
                id_producto=item['id'],
                cantidad=item['cantidad']
            )
            lista_detalles.append(detalle)

        # 4. Llamar al modelo para guardar todo en una transacción
        nueva_operacion(nueva_op, lista_detalles)

        messagebox.showinfo("Exito", "Operación registrada correctamente.")
        return True

    except Exception as e:
        # Si algo falla en la base de datos, mostramos el error
        messagebox.showerror("Error", f"Ocurrió un error al guardar la operación: {e}")
        return False


def ejecutar_edicion_operacion(id_operacion, monto_total, lista_items_carrito, observaciones=""):
    if not lista_items_carrito:
        messagebox.showwarning("Error", "El carrito de productos está vacío.")
        return False

    # Creo el objeto Operacion y le paso "valores dummy" los cuales no
    # seran utilizados en la consulta a la base de datos
    try:
        op_actualizada = Operacion(
            id_cliente=0,
            observaciones=observaciones,
            monto_total=monto_total,
            valor_dolar=0,
            valor_kilo_miel=0
        )

        lista_detalles = []
        for item in lista_items_carrito:
            detalle = DetalleOperacion(
                id_operacion=id_operacion,
                id_producto=item['id'],
                cantidad=item['cantidad']
            )
            lista_detalles.append(detalle)

        editar_operacion(id_operacion, op_actualizada, lista_detalles)
        messagebox.showinfo("Exito", "Operación editada correctamente.")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al editar la operación: {e}")
        return False


def ejecutar_eliminacion_operacion(id_operacion):
    try:
        eliminar_operacion(id_operacion)
        messagebox.showinfo("Exito", "Operacion eliminada correctamente")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error al eliminar la operacion: {e}")
        return False