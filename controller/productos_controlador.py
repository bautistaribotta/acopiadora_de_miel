from model.entidades import Producto
from model.productos_db import *
from tkinter import messagebox


def nuevo_producto_controlador(nombre, categoria, unidad_medida, precio_unidad, cantidad, ventana, callback=None):
    if not nombre or not categoria or not unidad_medida or not precio_unidad or not cantidad:
        messagebox.showwarning("Faltan datos",
                               "Por favor complete los campos obligatorios.", parent=ventana)
        return

    nuevo_obj_producto = Producto(nombre, categoria, unidad_medida, precio_unidad, cantidad)

    try:
        nuevo_producto(nuevo_obj_producto)
        messagebox.showinfo("Exito", "Producto creado correctamente.", parent=ventana)
        # Si callback se mantienen en None, no ejecuta nada
        if callback:
            callback()
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error:", f"No se puede guardar el producto: {e}", parent=ventana)


def eliminar_producto_controlador(id_producto, ventana):
    try:
        eliminar_producto(id_producto)
        messagebox.showinfo("Exito", "Producto eliminado correctamente.", parent=ventana)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"El producto no pudo ser eliminado: {e}", parent=ventana)
        return False


def buscador_productos_controlador(criterio):
    if criterio.isdigit():
        return buscador_producto_por_id(criterio)
    else:
        return buscador_producto_por_nombre(criterio)


def listar_productos_controlador():
    return listar_producto_db()