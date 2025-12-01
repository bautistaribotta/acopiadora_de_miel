import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("800x600+550+85")
    ventana_clientes.resizable(False, False)
    ventana_clientes.configure(bg=color_primario)


    # CONFIGURACION DEL GRID
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
    boton_eliminar = tk.Button(frame_superior, text="Eliminar")
    boton_eliminar.config(bg=color_secundario, fg=color_primario, width=10, font=fuente1)
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = tk.Button(frame_superior, text="Editar")
    boton_editar.config(bg=color_secundario, fg=color_primario, width=10, font=fuente1)
    boton_editar.pack(side="right", padx=5)

    boton_agregar = tk.Button(frame_superior, text="Agregar")
    boton_agregar.config(bg=color_secundario, fg=color_primario, text="Añadir", width=10, font=fuente1, command=nuevo_cliente)
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
    ventana_nuevo_cliente.title("Nuevo Cliente")
    ventana_nuevo_cliente.config(bg=color_primario)
    ventana_nuevo_cliente.geometry("400x600+120+85")
    ventana_nuevo_cliente.resizable(False, False)

    # CONFIGURACION DEL GRID
    ventana_nuevo_cliente.grid_columnconfigure(0, weight=1)
    ventana_nuevo_cliente.grid_columnconfigure(1, weight=2)


    # LABEL TITULO
    label_titulo = tk.Label(ventana_nuevo_cliente, text="Registrar Nuevo Cliente")
    label_titulo.config(font=("Arial", 16, "bold"), bg=color_primario, fg=color_secundario)
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(20, 30), padx=20)


    # NOMBRE
    label_nombre = tk.Label(ventana_nuevo_cliente, text="Nombre:")
    label_nombre.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # APELLIDO
    label_apellido = tk.Label(ventana_nuevo_cliente, text="Apellido:")
    label_apellido.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_apellido.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_apellido = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)
    entry_apellido.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)


    # TELEFONO
    label_telefono = tk.Label(ventana_nuevo_cliente, text="Teléfono:")
    label_telefono.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_telefono.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_telefono = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)
    entry_telefono.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)


    # LOCALIDAD
    label_localidad = tk.Label(ventana_nuevo_cliente, text="Localidad:")
    label_localidad.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_localidad.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_localidad = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)
    entry_localidad.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CALLE
    label_calle = tk.Label(ventana_nuevo_cliente, text="Calle:")
    label_calle.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_calle.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_calle = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)
    entry_calle.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # FACTURA
    label_factura = tk.Label(ventana_nuevo_cliente, text="Fac. Produccion:")
    label_factura.config(font=fuente1, bg=color_primario, fg=color_secundario)
    label_factura.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)

    opciones_factura = ["No", "Sí"]
    combobox_factura = ttk.Combobox(ventana_nuevo_cliente, values=opciones_factura)
    combobox_factura.config(state="readonly", font=fuente1, width=18)
    combobox_factura.current(0)
    combobox_factura.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)


    # CUIT (inicialmente oculto)
    label_cuit = tk.Label(ventana_nuevo_cliente, text="CUIT:")
    label_cuit.config(font=fuente1, bg=color_primario, fg=color_secundario)

    entry_cuit = ttk.Entry(ventana_nuevo_cliente, font=fuente1, width=20)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_nuevo_cliente, bg=color_primario)
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 20))

    boton_guardar = tk.Button(frame_botones, text="Guardar", font=fuente1)
    boton_guardar.config(bg=color_secundario, fg=color_primario, width=12)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=fuente1)
    boton_cancelar.config(bg=color_secundario, fg=color_primario, width=12)
    boton_cancelar.pack(side="left", padx=5)

    # Función para mostrar/ocultar CUIT según la selección del combobox
    def actualizar_cuit(event):
        if combobox_factura.get() == "Sí":
            label_cuit.grid(row=7, column=0, sticky="e", padx=(20, 10), pady=10)
            entry_cuit.grid(row=7, column=1, sticky="w", padx=(0, 20), pady=10)
        else:
            label_cuit.grid_remove()
            entry_cuit.grid_remove()

    # Vincular evento al combobox
    combobox_factura.bind("<<ComboboxSelected>>", actualizar_cuit)


if __name__ == "__main__":
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk()  # Crea una ventana principal oculta
    root.withdraw()  # La oculta (porque no la necesito visible)
    clientes()  # Abre la ventana Toplevel de proveedores
    root.mainloop()  # Mantiene la aplicación corriendo