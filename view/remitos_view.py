import tkinter as tk
from estilos import *

ventana_remitos_instancia = None



def remitos():
    global ventana_remitos_instancia
    if ventana_remitos_instancia is not None and ventana_remitos_instancia.winfo_exists():
        ventana_remitos_instancia.lift()
        return

    ventana_remitos = tk.Toplevel()
    ventana_remitos_instancia = ventana_remitos

    ventana_remitos.title("Remitos")
    ventana_remitos.resizable(False, False)
    ventana_remitos.config(bg=color_primario)
    ventana_remitos.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    # POSICION Y TAMAÑO
    ancho = ventana_remitos.winfo_screenwidth()
    alto = ventana_remitos.winfo_screenheight()
    x = int(ancho / 2) - int(400 / 2)
    y = int(alto / 2) - int(600 / 2)
    ventana_remitos.geometry(f"{400}x{600}+{x}+{y}")


if __name__ == "__main__":
    remitos()