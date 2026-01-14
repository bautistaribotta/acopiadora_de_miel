import tkinter as tk
from tkinter import ttk
from estilos import *


def listado_deudores():
    ventana_listado_deudores = tk.Toplevel(ventana)
    ventana_listado_deudores.title("Listado de deudores")
    ventana_listado_deudores.configure(bg=color_primario)
    ventana_listado_deudores.geometry("800x600")
    ventana_listado_deudores.resizable(False, False)
    centrar_ventana_interna(ventana_listado_deudores, 800, 600)
    ventana_listado_deudores.mainloop()


if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.withdraw()
    listado_deudores()
    ventana.mainloop()