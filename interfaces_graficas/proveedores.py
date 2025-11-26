import tkinter as tk
from utilidades.configuracion import *

def proveedores():
    ventana_proveedores = tk.Toplevel()
    ventana_proveedores.title("Proveedores")
    ventana_proveedores.minsize(450, 600)
    ventana_proveedores.resizable(False, False)

if __name__ == "__main__" :
    proveedores()