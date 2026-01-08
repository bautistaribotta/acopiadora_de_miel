from model.entidades import Cliente
from model.clientes_db import *
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
        # Si callback se mantienen en None, no ejecuta nada
        if callback:
            callback()
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")


def informacion_cliente_controlador(id_cliente):
    resultado = buscar_cliente_id(id_cliente)

    nombre = resultado[1]
    apellido = resultado[2]
    telefono = resultado[3]
    localidad = resultado[4]
    direccion = resultado[5]
    factura_produccion = resultado[6]
    cuit = resultado[7]

    cliente = Cliente(nombre, apellido, telefono,localidad,direccion,factura_produccion, cuit)
    return cliente


def eliminar_cliente_controlador(id_cliente):
    try:
        eliminar_cliente(id_cliente)
        messagebox.showinfo("Exito", "Cliente eliminado correctamente")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"El cliente no pudo ser eliminado: {e}")
        return False


def listar_clientes_controlador():
    return listar_clientes_db()