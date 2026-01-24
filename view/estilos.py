import os
from tkinter import ttk


color_primario = "#2B303A"
color_secundario = "#EEE5E9"
color_zebra = "#D3D3D3"

fuente_titulos = "Arial", 16, "bold"
fuente_texto = "Arial", 12, "bold"


def obtener_ruta_recurso(nombre_archivo):
    # Devuelvo la ruta absoluta al recurso en la carpeta 'recursos'
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_recursos = os.path.join(directorio_actual, "..", "recursos")
    return os.path.join(ruta_recursos, nombre_archivo)


def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40 # Resto 40 para que quede más arriba
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


def centrar_ventana_interna(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2)
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


def configurar_estilos(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Configuro Estilo Botón Primario (Fondo Oscuro, Texto Claro)
    style.configure("BotonPrimario.TButton",
                    background=color_primario,
                    foreground=color_secundario,
                    font=("Arial", 10, "bold"),
                    borderwidth=1,
                    focuscolor=color_secundario)
    style.map("BotonPrimario.TButton",
              background=[("active", color_primario)],
              foreground=[("active", color_secundario)])

    # Configuro Estilo Botón Secundario (Fondo Claro, Texto Oscuro)
    style.configure("BotonSecundario.TButton",
                    background=color_secundario,
                    foreground=color_primario,
                    font=("Arial", 10, "bold"),
                    borderwidth=1,
                    focuscolor=color_primario)
    style.map("BotonSecundario.TButton",
              background=[("active", color_secundario)],
              foreground=[("active", color_primario)])