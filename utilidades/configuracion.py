import tkinter as tk
from tkinter import messagebox


def controlador_entry_no_numeros(variable_control , name=None, index=None, mode=None):
    """
    Funcion para que un entry no pueda recibir un numero
    variable_control = Un StringVar
    name = Parametro obligatorio aunque no se use
    index = Parametro obligatorio aunque no se use
    mode = Parametro obligatorio aunque no se use
    """
    texto = variable_control.get()
    for caracter in texto:
        if caracter.isdigit():
            messagebox.showwarning("Error nombre", "El nombre no puede contener numeros")
            variable_control.set(texto[:-1])



def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40 # Resto 40 para que quede mas arriba
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


# Guardo el color y las fuentes en un solo archivo para hacer mas facil las modificaciones
color_primario = "#2B303A"
color_secundario = "#EEE5E9"
color_terciario = ""

fuente_titulos = "Arial", 16, "bold"
fuente_texto = "Arial", 12, "bold"