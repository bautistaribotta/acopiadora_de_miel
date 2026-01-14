import tkinter as tk
from tkinter import ttk
from estilos import *

ventana_listado_deudores_instancia = None


def listado_deudores():
    global ventana_listado_deudores_instancia
    if ventana_listado_deudores_instancia is not None and ventana_listado_deudores_instancia.winfo_exists():
        ventana_listado_deudores_instancia.lift()
        return

    ventana_listado_deudores = tk.Toplevel()
    ventana_listado_deudores_instancia = ventana_listado_deudores
    ventana_listado_deudores.title("Listado de deudores")
    ventana_listado_deudores.configure(bg=color_primario)
    ventana_listado_deudores.resizable(False, False)
    
    # Aumentamos el ancho para que entren todas las columnas
    ancho_ventana = 1200
    alto_ventana = 600
    centrar_ventana_interna(ventana_listado_deudores, ancho_ventana, alto_ventana)

    # CONFIGURACION DEL GRID
    ventana_listado_deudores.grid_rowconfigure(0, weight=0)  # Frame Superior
    ventana_listado_deudores.grid_rowconfigure(1, weight=1)  # Frame Tabla
    ventana_listado_deudores.grid_columnconfigure(0, weight=1)

    # FRAME SUPERIOR
    frame_superior = tk.Frame(ventana_listado_deudores, bg=color_primario, height=50)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
    # BUSCADOR
    label_busqueda = tk.Label(frame_superior, text="Buscar cliente:", font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_busqueda.pack(side="left", padx=(0, 10))

    entry_buscar = tk.Entry(frame_superior, bg=color_secundario, fg=color_primario, font=fuente_texto, width=25)
    entry_buscar.pack(side="left") 


    # FRAME TABLA
    frame_tabla_deudores = tk.Frame(ventana_listado_deudores, bg=color_primario)
    frame_tabla_deudores.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame_tabla_deudores)
    scrollbar.pack(side="right", fill="y")


    # TREEVIEW (Tabla)
    columnas = ("id", "nombre", "monto_pesos", "monto_dolares_hist", "monto_dolares_actual", "monto_miel_hist", "monto_miel_actual")
    
    tabla_deudores = ttk.Treeview(frame_tabla_deudores, columns=columnas, show="headings", 
                                  yscrollcommand=scrollbar.set, height=20)

    # Definicion de Cabeceras
    tabla_deudores.heading("id", text="ID")
    tabla_deudores.heading("nombre", text="Nombre")
    tabla_deudores.heading("monto_pesos", text="Pesos")
    tabla_deudores.heading("monto_dolares_hist", text="USD (Hist)")
    tabla_deudores.heading("monto_dolares_actual", text="USD (Hoy)")
    tabla_deudores.heading("monto_miel_hist", text="Kg Miel (Hist)")
    tabla_deudores.heading("monto_miel_actual", text="Kg Miel (Hoy)")

    # Definicion de Columnas
    tabla_deudores.column("id", width=50, anchor="center")
    tabla_deudores.column("nombre", width=250, anchor="w")
    tabla_deudores.column("monto_pesos", width=120, anchor="e")
    tabla_deudores.column("monto_dolares_hist", width=120, anchor="e")
    tabla_deudores.column("monto_dolares_actual", width=120, anchor="e")
    tabla_deudores.column("monto_miel_hist", width=120, anchor="e")
    tabla_deudores.column("monto_miel_actual", width=120, anchor="e")

    # Aplicar Zebra Striping
    tabla_deudores.tag_configure("impar", background=color_zebra)

    tabla_deudores.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tabla_deudores.yview)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    listado_deudores()
    root.mainloop()