from model.entidades import Cliente
from model.clientes_db import nuevo_cliente_db, listar_clientes_db
from tkinter import messagebox


def nuevo_cliente_controlador(nombre, apellido, telefono, localidad, direccion, factura, cuit, ventana, callback=None):
    if not nombre or not apellido or not telefono:
        messagebox.showwarning("Faltan datos", "Por favor complete los campos obligatorios.")
        return
    factura = 1 if factura == "Si" else 0
    nuevo_obj_cliente = Cliente(nombre, apellido, telefono, localidad, direccion, factura, cuit)

    try:
        nuevo_cliente_db(nuevo_obj_cliente)
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
        if callback:
            callback()
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")


def listar_clientes_controlador():
    return listar_clientes_db()