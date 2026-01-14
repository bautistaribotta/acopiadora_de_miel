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


def informacion_producto_controlador(id_producto):
    try:
        id_limpio = int(id_producto)
    except ValueError:
        return None

    # (id, nombre, categoria, precio, cantidad, unidad_medida)
    resultado = buscar_producto_id(id_limpio)

    if resultado is None:
        return None

    # Constructor: Producto(nombre, categoria, unidad_medida, precio, cantidad)
    nombre = resultado[1]
    categoria = resultado[2]
    precio = resultado[3]
    cantidad = resultado[4]
    unidad_medida = resultado[5]

    producto = Producto(nombre, categoria, unidad_medida, precio, cantidad)
    return producto


def editar_producto_controlador(id_producto, nombre, categoria, unidad_medida, precio, cantidad, ventana, callback=None):
    if not nombre or not categoria or not unidad_medida or not precio or not cantidad:
        messagebox.showwarning("Faltan datos",
                               "Por favor complete los campos obligatorios.", parent=ventana)
        return

    obj_producto_editado = Producto(nombre, categoria, unidad_medida, precio, cantidad)

    try:
        editar_producto(id_producto, obj_producto_editado)
        messagebox.showinfo("Exito", "Producto editado correctamente.", parent=ventana)

        if callback:
            callback()
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar el producto: {e}", parent=ventana)


def sumar_stock_controlador(id_producto, cantidad, ventana, callback=None):
    try:
        cantidad_float = float(cantidad)
        if cantidad_float <= 0:
            messagebox.showwarning("Atención", "La cantidad a sumar debe ser mayor a 0", parent=ventana)
            return
            
        sumar_stock_db(id_producto, cantidad_float)
        messagebox.showinfo("Éxito", "Stock actualizado correctamente.", parent=ventana)
        
        if callback:
            callback()
        ventana.destroy()

    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor numérico válido", parent=ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el stock: {e}", parent=ventana)