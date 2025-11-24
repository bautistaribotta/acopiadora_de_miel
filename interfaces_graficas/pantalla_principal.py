import tkinter as tk
from utilidades.configuracion import *


def pantalla_principal():
    ventana_principal = tk.Tk()
    ventana_principal.configure(bg=color_principal)
    ventana_principal.state("zoomed")
    ventana_principal.title("Menu principal")
    ventana_principal.resizable(False, False)

    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    # fill x hace que ocupes todo el ancho y side top que vaya arriba
    opciones_top.pack(fill="x", side="top")

    ventana_principal.mainloop()


if __name__ == "__main__":
    pantalla_principal()