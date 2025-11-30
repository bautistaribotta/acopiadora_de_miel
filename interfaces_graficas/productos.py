import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def productos():
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Productos")
    ventana_productos.geometry("800x600+0+85")
    ventana_productos.resizable(False, False)
    ventana_productos.configure(bg=color_primario)


    # CONFIGURACION DEL GRID
    ventana_productos.grid_rowconfigure(0, weight=0)  # Buscador y Botones
    ventana_productos.grid_rowconfigure(1, weight=1)  # Tabla
    ventana_productos.grid_columnconfigure(0, weight=1)


    # FRAME SUPERIOR - BUSCADOR Y BOTONES
    frame_superior = tk.Frame(ventana_productos, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))


    # BUSCADOR
    label_buscar = tk.Label(frame_superior, text="Buscar:", font=fuente1, bg=color_primario, fg=color_secundario)
    label_buscar.pack(side="left", padx=(0, 10))
    entry_buscar = ttk.Entry(frame_superior, font=fuente1, width=25)
    entry_buscar.pack(side="left")


    # BOTONES
    boton_eliminar = tk.Button(frame_superior, text="Eliminar", font=fuente1, bg=color_secundario, fg=color_primario, width=10)
    boton_eliminar.config()
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = tk.Button(frame_superior, text="Editar", font=fuente1, bg=color_secundario, fg=color_primario, width=10)
    boton_editar.config()
    boton_editar.pack(side="right", padx=5)

    boton_agregar = tk.Button(frame_superior, text="Añadir", font=fuente1, bg=color_secundario, fg=color_primario, width=10)
    boton_agregar.config(command=nuevo_producto)
    boton_agregar.pack(side="right", padx=5)


    # FRAME TABLA
    frame_tabla = tk.Frame(ventana_productos, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")


    # TREEVIEW (TABLA)
    columnas = ("id", "nombre", "categoria", "cantidad")
    tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                   yscrollcommand=scrollbar.set, height=20)


    # CONFIGURAR COLUMNAS
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("cantidad", text="Cantidad")

    tabla_productos.column("id", width=80, anchor="center")
    tabla_productos.column("nombre", width=250, anchor="w")
    tabla_productos.column("categoria", width=200, anchor="w")
    tabla_productos.column("cantidad", width=100, anchor="center")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tabla_productos.yview)


def nuevo_producto():
    ventana_nuevo_producto = tk.Toplevel()
    ventana_nuevo_producto.title("Nuevo producto")
    ventana_nuevo_producto.configure(bg=color_primario)
    ventana_nuevo_producto.geometry("400x600+850+85")


    # BOTONES


    ventana_nuevo_producto.mainloop()


if __name__ == "__main__":
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk() # Crea una ventana principal oculta
    root.withdraw() # La oculta (porque no la necesito visible)
    productos() # Abre la ventana Toplevel de productos
    root.mainloop() # Mantiene la aplicación corriendo