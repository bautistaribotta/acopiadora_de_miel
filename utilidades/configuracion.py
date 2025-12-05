import tkinter as tk
import requests
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


def get_cotizacion_oficial_venta():
    url_dolar_oficial = "https://dolarapi.com/v1/dolares/oficial"
    respuesta = requests.get(url_dolar_oficial, verify=True)

    resp_json = respuesta.json()
    valor_dolar_oficial_venta = resp_json["venta"]
    return valor_dolar_oficial_venta


def get_cotizacion_blue_venta():
    url_dolar_blue = "https://dolarapi.com/v1/dolares/blue"
    respuesta = requests.get(url_dolar_blue, verify=True)

    resp_json = respuesta.json()
    valor_dolar_blue_venta = resp_json["venta"]
    return valor_dolar_blue_venta


# Guardo el color y las fuentes en un solo archivo para hacer mas facil las modificaciones
color_primario = "#2B303A"
color_secundario = "#EEE5E9"
color_terciario = ""

fuente_titulos = "Arial", 16, "bold"
fuente_texto = "Arial", 12, "bold"