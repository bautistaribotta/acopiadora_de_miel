

def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40 # Resto 40 para que quede mas arriba
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


color_primario = "#2B303A"
color_secundario = "#EEE5E9"
color_terciario = ""

fuente_titulos = "Arial", 16, "bold"
fuente_texto = "Arial", 12, "bold"