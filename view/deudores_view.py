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


    # Frame tabla
    frame_tabla_deudores = tk.Frame(ventana_listado_deudores)
    frame_tabla_deudores.configure()
    frame_tabla_deudores.pack()

    # Treeview (Tabla)
    columnas = ("id", "nombre", "debe")
    tabla_deudores = ttk.Treeview(frame_tabla_deudores, columns=columnas, show="headings")

    tabla_deudores.heading("id", text="ID")
    tabla_deudores.heading("nombre", text="Nombre")
    tabla_deudores.heading("debe", text="Total adeudado")

    tabla_deudores.column("id", width=80, anchor="center")
    tabla_deudores.column("nombre", width=250, anchor="w")
    tabla_deudores.column("debe", width=300, anchor="center")

    tabla_deudores.pack()



if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.withdraw()
    listado_deudores()
    ventana.mainloop()