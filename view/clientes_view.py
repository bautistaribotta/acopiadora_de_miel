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
    label_busqueda = tk.Label(frame_superior, text="Buscar:", font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_busqueda.pack(side="left", padx=(0, 10))
    barra_busqueda = tk.Entry(frame_superior, bg=color_secundario, fg=color_primario, font=fuente_texto, width=25)
    barra_busqueda.pack(side="left")


    # BOTONES
    boton_eliminar = tk.Button(frame_superior, text="Eliminar")
    boton_eliminar.config(bg=color_secundario, fg=color_primario, width=10,
                          font=fuente_texto, cursor="hand2")
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = tk.Button(frame_superior, text="Editar")
    boton_editar.config(bg=color_secundario, fg=color_primario, width=10,
                        font=fuente_texto, command=editar_cliente, cursor="hand2")
    boton_editar.pack(side="right", padx=5)

    boton_agregar = tk.Button(frame_superior, text="Agregar")
    boton_agregar.config(bg=color_secundario, fg=color_primario, text="Añadir", width=10,
                         font=fuente_texto, command=nuevo_cliente, cursor="hand2")
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
    label_titulo = tk.Label(ventana_nuevo_cliente, text="REGISTRAR CLIENTE")
    label_titulo.config(font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(50, 40), padx=20)


    # NOMBRE
    label_nombre = tk.Label(ventana_nuevo_cliente, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    variable_control_entry = tk.StringVar()
    entry_nombre = ttk.Entry(ventana_nuevo_cliente, textvariable=variable_control_entry)
    variable_control_entry.trace("w", lambda *args: controlador_entry_no_numeros(variable_control_entry))
    entry_nombre.config(font=fuente_texto, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # APELLIDO
    label_apellido = tk.Label(ventana_nuevo_cliente, text="Apellido:")
    label_apellido.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_apellido.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_apellido = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_apellido.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)


    # TELEFONO
    label_telefono = tk.Label(ventana_nuevo_cliente, text="Teléfono:")
    label_telefono.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_telefono.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_telefono = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_telefono.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)


    # LOCALIDAD
    label_localidad = tk.Label(ventana_nuevo_cliente, text="Localidad:")
    label_localidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_localidad.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_localidad = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_localidad.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CALLE
    label_calle = tk.Label(ventana_nuevo_cliente, text="Calle:")
    label_calle.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_calle.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_calle = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_calle.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # FACTURA
    label_factura = tk.Label(ventana_nuevo_cliente, text="Fac. Produccion:")
    label_factura.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_factura.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)

    opciones_factura = ["No", "Sí"]
    combobox_factura = ttk.Combobox(ventana_nuevo_cliente, values=opciones_factura)
    combobox_factura.config(state="readonly", font=fuente_texto, width=18)
    combobox_factura.current(0)
    combobox_factura.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)


    # CUIT (inicialmente oculto)
    label_cuit = tk.Label(ventana_nuevo_cliente, text="CUIT:")
    label_cuit.config(font=fuente_texto, bg=color_primario, fg=color_secundario)

    entry_cuit = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_nuevo_cliente, bg=color_primario)
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 20))

    boton_guardar = tk.Button(frame_botones, text="Guardar", font=fuente_texto)
    boton_guardar.config(bg=color_secundario, fg=color_primario, width=12, cursor="hand2")
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=fuente_texto)
    boton_cancelar.config(bg=color_secundario, fg=color_primario, width=12, cursor="hand2")
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


def editar_cliente():
    ventana_editar_cliente = tk.Toplevel()
    ventana_editar_cliente.title("Editar cliente")
    ventana_editar_cliente.config(bg=color_primario)
    ventana_editar_cliente.geometry("400x600+120+85")
    ventana_editar_cliente.resizable(False, False)


    # CONFIGURACION DEL GRID
    ventana_editar_cliente.grid_columnconfigure(0, weight=1)
    ventana_editar_cliente.grid_columnconfigure(1, weight=2)


    # LABEL TITULO
    label_titulo = tk.Label(ventana_editar_cliente, text="EDITAR CLIENTE")
    label_titulo.config(font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(50, 40), padx=20)


    # NOMBRE
    label_nombre = tk.Label(ventana_editar_cliente, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    variable_control_entry = tk.StringVar()
    entry_nombre = ttk.Entry(ventana_editar_cliente, textvariable=variable_control_entry)
    variable_control_entry.trace("w", lambda *args: controlador_entry_no_numeros(variable_control_entry))
    entry_nombre.config(font=fuente_texto, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # APELLIDO
    label_apellido = tk.Label(ventana_editar_cliente, text="Apellido:")
    label_apellido.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_apellido.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_apellido = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_apellido.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)


    # TELEFONO
    label_telefono = tk.Label(ventana_editar_cliente, text="Teléfono:")
    label_telefono.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_telefono.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_telefono = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_telefono.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)


    # LOCALIDAD
    label_localidad = tk.Label(ventana_editar_cliente, text="Localidad:")
    label_localidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_localidad.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_localidad = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_localidad.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CALLE
    label_calle = tk.Label(ventana_editar_cliente, text="Calle:")
    label_calle.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_calle.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_calle = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_calle.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # FACTURA
    label_factura = tk.Label(ventana_editar_cliente, text="Fac. Produccion:")
    label_factura.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_factura.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)

    opciones_factura = ["No", "Sí"]
    combobox_factura = ttk.Combobox(ventana_editar_cliente, values=opciones_factura)
    combobox_factura.config(state="readonly", font=fuente_texto, width=18)
    combobox_factura.current(0)
    combobox_factura.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)


    # CUIT (inicialmente oculto)
    label_cuit = tk.Label(ventana_editar_cliente, text="CUIT:")
    label_cuit.config(font=fuente_texto, bg=color_primario, fg=color_secundario)

    entry_cuit = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_editar_cliente, bg=color_primario)
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 20))

    boton_guardar = tk.Button(frame_botones, text="Guardar", font=fuente_texto)
    boton_guardar.config(bg=color_secundario, fg=color_primario, width=12, cursor="hand2")
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=fuente_texto)
    boton_cancelar.config(bg=color_secundario, fg=color_primario, width=12, cursor="hand2")
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


def informacion_cliente():
    ventana_info_cliente = tk.Toplevel(root)
    ventana_info_cliente.title("Informacion del cliente")
    ventana_info_cliente.configure(bg=color_primario)

    # Dimensiones y centrado
    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana(ventana_info_cliente, ancho_ventana, alto_ventana)


    # --- FRAME SUPERIOR (Datos y Botones) ---
    frame_superior = tk.Frame(ventana_info_cliente, bg=color_primario)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)


    # --- SUB-FRAME DATOS DEL CLIENTE --- (Izquierda)
    frame_datos = tk.Frame(frame_superior, bg=color_primario)
    frame_datos.pack(side="left", fill="both", expand=True)


    # --- FILA 0: ID | Nombre | Apellido ---

    # ID
    label_id_titulo = tk.Label(frame_datos, text="ID:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_id_titulo.grid(row=0, column=0, sticky="w", pady=5, padx=(0, 5))
    label_id_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_id_valor.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 20))

    # NOMBRE
    label_nombre_titulo = tk.Label(frame_datos, text="Nombre:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_nombre_titulo.grid(row=0, column=2, sticky="w", pady=5, padx=(10, 5))
    label_nombre_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_nombre_valor.grid(row=0, column=3, sticky="w", pady=5, padx=(0, 20))

    # APELLIDO
    label_apellido_titulo = tk.Label(frame_datos, text="Apellido:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_apellido_titulo.grid(row=0, column=4, sticky="w", pady=5, padx=(10, 5))
    label_apellido_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_apellido_valor.grid(row=0, column=5, sticky="w", pady=5, padx=(0, 0))


    # --- FILA 1: Telefono | Localidad | Calle ---

    # TELEFONO
    label_telefono_titulo = tk.Label(frame_datos, text="Teléfono:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_telefono_titulo.grid(row=1, column=0, sticky="w", pady=5, padx=(0, 5))
    label_telefono_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_telefono_valor.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 20))


    # LOCALIDAD
    label_localidad_titulo = tk.Label(frame_datos, text="Localidad:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_localidad_titulo.grid(row=1, column=2, sticky="w", pady=5, padx=(10, 5))
    label_localidad_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_localidad_valor.grid(row=1, column=3, sticky="w", pady=5, padx=(0, 20))


    # CALLE
    label_calle_titulo = tk.Label(frame_datos, text="Calle:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_calle_titulo.grid(row=1, column=4, sticky="w", pady=5, padx=(10, 5))
    label_calle_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_calle_valor.grid(row=1, column=5, sticky="w", pady=5, padx=(0, 0))


    # --- FILA 2: Factura | CUIT ---

    # FACTURA
    label_factura_titulo = tk.Label(frame_datos, text="Factura:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_factura_titulo.grid(row=2, column=0, sticky="w", pady=5, padx=(0, 5))
    label_factura_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_factura_valor.grid(row=2, column=1, sticky="w", pady=5, padx=(0, 20))


    # CUIT
    label_cuit_titulo = tk.Label(frame_datos, text="CUIT:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_cuit_titulo.grid(row=2, column=2, sticky="w", pady=5, padx=(10, 5))
    label_cuit_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
    label_cuit_valor.grid(row=2, column=3, sticky="w", pady=5, padx=(0, 20))


    # Configuración de pesos para que las columnas de valores se expandan si sobra espacio
    frame_datos.grid_columnconfigure(1, weight=1)
    frame_datos.grid_columnconfigure(3, weight=1)
    frame_datos.grid_columnconfigure(5, weight=1)


    # --- SUB-FRAME BOTONES --- (Derecha)
    frame_derecho = tk.Frame(frame_superior, bg=color_primario)
    frame_derecho.pack(side="right", fill="y", expand=False, padx=(30, 0))
    frame_derecho.grid_columnconfigure(0, weight=1)
    frame_derecho.grid_rowconfigure(0, weight=1)


    # FRAME BOTONES
    frame_botones = tk.Frame(frame_derecho, bg=color_primario)
    frame_botones.grid(row=0, column=0)


    # BOTONES
    boton_nueva = tk.Button(frame_botones, text="Nueva", font=fuente_texto,
                            bg=color_secundario, fg=color_primario,width=10, cursor="hand2")
    boton_nueva.pack(side="left", padx=5)

    boton_editar = tk.Button(frame_botones, text="Editar", font=fuente_texto,
                             bg=color_secundario, fg=color_primario, width=10, cursor="hand2")
    boton_editar.pack(side="left", padx=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", font=fuente_texto,
                               bg=color_secundario, fg=color_primario,width=10, cursor="hand2")
    boton_eliminar.pack(side="left", padx=5)


    # --- FRAME MEDIO (Tabla Debe/Haber) ---
    frame_medio = tk.Frame(ventana_info_cliente, bg=color_secundario)
    frame_medio.pack(side="top", fill="both", expand=True, padx=20, pady=(10, 30))


    # TREEVIEW
    columnas = ("fecha", "detalle", "debe", "haber", "saldo")
    tabla_transacciones = ttk.Treeview(frame_medio, columns=columnas, show="headings")


    # ESTILO PARA EL TREEVIEW
    estilo = ttk.Style()
    estilo.configure("Treeview", font=("Arial", 10), rowheight=22)
    estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    tabla_transacciones.heading("fecha", text="Fecha")
    tabla_transacciones.heading("detalle", text="Detalle")
    tabla_transacciones.heading("debe", text="Debe")
    tabla_transacciones.heading("haber", text="Haber")
    tabla_transacciones.heading("saldo", text="Saldo")

    tabla_transacciones.column("fecha", width=100, anchor="center")
    tabla_transacciones.column("detalle", width=350, anchor="w")
    tabla_transacciones.column("debe", width=100, anchor="e")
    tabla_transacciones.column("haber", width=100, anchor="e")
    tabla_transacciones.column("saldo", width=100, anchor="e")

    scrollbar = ttk.Scrollbar(frame_medio, orient="vertical", command=tabla_transacciones.yview)
    tabla_transacciones.configure(yscroll=scrollbar.set)

    tabla_transacciones.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk()  # Crea una ventana principal oculta
    root.withdraw()  # La oculta (porque no la necesito visible)
    clientes()  # Abre la ventana Toplevel de proveedores
    root.mainloop()  # Mantiene la aplicación corriendo