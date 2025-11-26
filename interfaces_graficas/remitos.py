import tkinter as tk
from utilidades.configuracion import *

def remitos():
    ventana_remitos = tk.Toplevel()
    ventana_remitos.title("Remitos")
    ventana_remitos.minsize(450, 600)
    ventana_remitos.resizable(False, False)

    # GEOMETRIA Y POSICION
    ventana_remitos.grid()

if __name__ == "__main__":
    remitos()