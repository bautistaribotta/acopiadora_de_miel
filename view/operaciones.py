import tkinter as tk
from tkinter import ttk
from recursos import *
from utilidades.configuracion import *


def nueva_operacion():
    ventana_nueva_operacion = tk.Toplevel(root)
    ventana_nueva_operacion.title("Nueva operacion")
    ventana_nueva_operacion.config()

    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana(ventana_nueva_operacion, ancho_ventana, alto_ventana)

    ventana_nueva_operacion.mainloop()


def editar_operacion():
    pass


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    nueva_operacion()
    root.mainloop()