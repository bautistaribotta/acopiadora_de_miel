import tkinter as tk
from utilidades.configuracion import *

def clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Clientes")
    ventana_clientes.minsize(300, 300) # Configurar
    ventana_clientes.resizable(False, False)

if __name__ == "__main__":
    clientes()