import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def productos():
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Productos")
    ventana_productos.geometry("800x600+0+85")
    ventana_productos.resizable(False, False)
    ventana_productos.configure(bg=color_principal)


    # CONFIGURACION DEL GRID
    ventana_productos.grid_rowconfigure(0, weight=0)  # Buscador
    ventana_productos.grid_rowconfigure(1, weight=0)  # Botones
    ventana_productos.grid_rowconfigure(2, weight=1)  # Tabla
    ventana_productos.grid_columnconfigure(0, weight=1)


    # FRAME SUPERIOR - BUSCADOR
    frame_buscador = tk.Frame(ventana_productos, bg=color_principal)
    frame_buscador.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    label_buscar = tk.Label(frame_buscador, text="Buscar:", font=fuente1, bg=color_principal, fg=color_secundario)
    label_buscar.pack(side="left", padx=(0, 10))

    entry_buscar = ttk.Entry(frame_buscador, font=fuente1, width=40)
    entry_buscar.pack(side="left", fill="x", expand=True)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_productos, bg=color_principal)
    frame_botones.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

    boton_agregar = tk.Button(frame_botones, text="Añadir", font=fuente1, bg=color_secundario, fg=color_principal, width=15)
    boton_agregar.config(command=nuevo_producto)
    boton_agregar.pack(side="left", padx=5)

    boton_editar = tk.Button(frame_botones, text="Editar", font=fuente1, bg=color_secundario, fg=color_principal, width=15)
    boton_editar.config()
    boton_editar.pack(side="left", padx=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", font=fuente1,bg=color_secundario, fg=color_principal, width=15)
    boton_eliminar.config()
    boton_eliminar.pack(side="left", padx=5)


    # FRAME TABLA
    frame_tabla = tk.Frame(ventana_productos, bg=color_principal)
    frame_tabla.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))

    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")

    # TREEVIEW (TABLA)
    columnas = ("cantidad", "nombre", "categoria")
    tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                   yscrollcommand=scrollbar.set, height=20)

    # CONFIGURAR COLUMNAS
    tabla_productos.heading("cantidad", text="Cantidad")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")

    tabla_productos.column("cantidad", width=100, anchor="center")
    tabla_productos.column("nombre", width=300, anchor="w")
    tabla_productos.column("categoria", width=200, anchor="w")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tabla_productos.yview)


def nuevo_producto():
    ventana_nuevo_producto = tk.Toplevel()
    ventana_nuevo_producto.configure(bg=color_principal)


if __name__ == "__main__":
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk() # Crea una ventana principal oculta
    #root.withdraw() # La oculta (porque no la necesito visible)
    productos() # Abre la ventana Toplevel de productos
    root.mainloop() # Mantiene la aplicación corriendo