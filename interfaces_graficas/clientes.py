import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("800x600+550+85")
    ventana_clientes.resizable(False, False)
    ventana_clientes.configure(bg=color_primario)


    # CONFIGURACION DEL GRID DE LA VENTANA
    ventana_clientes.grid_rowconfigure(0, weight=0)  # Buscador y Botones
    ventana_clientes.grid_rowconfigure(1, weight=1)  # Tabla
    ventana_clientes.grid_columnconfigure(0, weight=1)


    # FRAME SUPERIOR - BUSCADOR Y BOTONES
    frame_superior = tk.Frame(ventana_clientes, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))


    # BUSCADOR
    label_busqueda = tk.Label(frame_superior, text="Buscar:", font=fuente1, bg=color_primario, fg=color_secundario)
    label_busqueda.pack(side="left", padx=(0, 10))
    barra_busqueda = tk.Entry(frame_superior, bg=color_secundario, fg=color_primario, font=fuente1, width=25)
    barra_busqueda.pack(side="left")


    # BOTONES
    boton_eliminar = tk.Button(frame_superior, bg=color_secundario, fg=color_primario, text="Eliminar", width=10,
                               font=fuente1)
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = tk.Button(frame_superior, bg=color_secundario, fg=color_primario, text="Editar", width=10,
                             font=fuente1)
    boton_editar.pack(side="right", padx=5)

    boton_agregar = tk.Button(frame_superior, bg=color_secundario, fg=color_primario, text="Añadir", width=10,
                              font=fuente1)
    boton_agregar.pack(side="right", padx=5)


    # FRAME TABLA
    frame_tabla = tk.Frame(ventana_clientes, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")


    # TREEVIEW (TABLA)
    columnas = ("id", "nombre", "localidad", "telefono")
    tabla_clientes = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                     yscrollcommand=scrollbar.set, height=20)


    # CONFIGURAR COLUMNAS
    tabla_clientes.heading("id", text="ID")
    tabla_clientes.heading("nombre", text="Nombre")
    tabla_clientes.heading("localidad", text="Localidad")
    tabla_clientes.heading("telefono", text="Teléfono")

    tabla_clientes.column("id", width=80, anchor="center")
    tabla_clientes.column("nombre", width=250, anchor="w")
    tabla_clientes.column("localidad", width=200, anchor="w")
    tabla_clientes.column("telefono", width=150, anchor="center")

    tabla_clientes.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tabla_clientes.yview)


def nuevo_cliente():
    ventana_nuevo_cliente = tk.Toplevel()
    ventana_nuevo_cliente.config(bg=color_primario)



if __name__ == "__main__":
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk()  # Crea una ventana principal oculta
    # root.withdraw()  # La oculta (porque no la necesito visible)
    clientes()  # Abre la ventana Toplevel de proveedores
    root.mainloop()  # Mantiene la aplicación corriendo