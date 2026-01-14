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
    ventana_remitos.config(bg=color_primario)
    ventana_remitos.resizable(False, False)
    centrar_ventana_interna(ventana_remitos, 800, 600)
    ventana_remitos.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


if __name__ == "__main__":
    remitos()