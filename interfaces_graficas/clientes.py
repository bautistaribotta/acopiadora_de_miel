import tkinter as tk
from utilidades.configuracion import *


def clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Clientes")
    ventana_clientes.minsize(450, 600) # Configurar
    ventana_clientes.resizable(False, False)

    # GEOMETRIA Y POSICION
    ventana_clientes.grid()


if __name__ == "__main__":
    clientes()