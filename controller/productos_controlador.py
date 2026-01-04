from model.entidades import Producto
from model.productos_db import listar_producto_db, nuevo_producto, eliminar_producto
from tkinter import messagebox


def nuevo_producto_controlador(nombre, categoria, unidad_medida, precio_unidad, cantidad, ventana, callback=None):
    if not nombre or not categoria or not unidad_medida or not precio_unidad or not cantidad:
        messagebox.showwarning("Faltan datos", "Por favor complete los campos obligatorios.")
        return

    nuevo_obj_producto = Producto(nombre, categoria, unidad_medida, precio_unidad, cantidad)

    try:
        nuevo_producto(nuevo_obj_producto)
        messagebox.showinfo("Exito", "Producto creado correctamente.")
        # Si callback se mantienen en None, no ejecuta nada
        if callback:
            callback()
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error:", f"No se puede guardar el producto: {e}")


def eliminar_producto_controlador(id_producto):
    try:
        eliminar_producto(id_producto)
        messagebox.showinfo("Exito", "Cliente eliminado correctamente.")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"El cliente no pudo ser eliminado: {e}")
        return False


def listar_productos_controlador():
    return listar_producto_db()