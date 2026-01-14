from operaciones_view import *
from estilos import *
from controller.validaciones import *
from controller.clientes_controlador import *

ventana_clientes_instancia = None
ventana_nuevo_cliente_instancia = None
ventana_editar_cliente_instancia = None
ventana_info_cliente_instancia = None


def listado_clientes():
    global ventana_clientes_instancia
    if ventana_clientes_instancia is not None and ventana_clientes_instancia.winfo_exists():
        ventana_clientes_instancia.lift()
        return

    ventana_clientes = tk.Toplevel()
    ventana_clientes_instancia = ventana_clientes

    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("800x600+550+85")
    ventana_clientes.resizable(False, False)
    ventana_clientes.configure(bg=color_primario)
    ventana_clientes.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    # CONFIGURACION DEL GRID
    ventana_clientes.grid_rowconfigure(0, weight=0)  # Buscador y Botones
    ventana_clientes.grid_rowconfigure(1, weight=1)  # Tabla
    ventana_clientes.grid_columnconfigure(0, weight=1)


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
    tabla_clientes.tag_configure("impar", background=color_zebra)

    # MOSTRAR LOS DATOS EN EL TREEVIEW
    def actualizar_tabla():
        # Limpia la tabla
        for item in tabla_clientes.get_children():
            tabla_clientes.delete(item)
        # Vuelve a escribirla pero actualizada
        clientes = listar_clientes_controlador()
        for i, cliente in enumerate(clientes):
            tag = "impar" if i % 2 != 0 else "par"
            tabla_clientes.insert("", "end", values=cliente, tags=(tag,))
    actualizar_tabla()


    # ELIMINAR CLIENTE
    def ejecutar_eliminacion():
        seleccion = tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente para eliminar.",
                                   parent=ventana_clientes)
            return

        # Obtenemos el ID del item seleccionado (columna 0) y el nombre (columna 1)
        valores = tabla_clientes.item(seleccion[0])['values']
        item_id = valores[0]
        nombre_cliente = valores[1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente '{nombre_cliente}'?",
                                        parent=ventana_clientes)
        if confirmar:
            if eliminar_cliente_controlador(item_id, ventana_clientes):
                actualizar_tabla()


    # FUNCION DE BUSCAR PRODUCTOS
    def filtrar_tabla(event):
        texto_busqueda = entry_buscar.get()

        if event == "":
            actualizar_tabla()
            return

        productos_encontrados = buscador_clientes_controlador(texto_busqueda)

        # Limpiamos la tabla actual
        for item in tabla_clientes.get_children():
            tabla_clientes.delete(item)

        # Llenamos con los resultados de la búsqueda
        for i, producto in enumerate(productos_encontrados):
            tag = "impar" if i % 2 != 0 else "par"
            tabla_clientes.insert("", "end", values=producto, tags=(tag,))


    # FUNCION ABRIR EDITAR
    def abrir_editar():
        seleccion = tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente para editar.",
                                   parent=ventana_clientes)
            return
        
        # Obtenemos el ID (columna 0)
        item_id = tabla_clientes.item(seleccion[0])['values'][0]
        editar_cliente_vista(item_id, actualizar_tabla)


    # MENU CONTEXTUAL (clic derecho)
    menu_contextual = tk.Menu(ventana_clientes, tearoff=0)
    menu_contextual.add_command(label="Editar", command=abrir_editar)
    menu_contextual.add_command(label="Eliminar", command=ejecutar_eliminacion)


    def mostrar_menu(event):
        item = tabla_clientes.identify_row(event.y)
        if item:
            tabla_clientes.selection_set(item)
            menu_contextual.post(event.x_root, event.y_root)


    def captar_id_cliente(event):
        # Verificar que el doble click sea sobre un item y no en los headers
        item = tabla_clientes.identify_row(event.y)
        if not item:
            return

        seleccion = tabla_clientes.selection()
        if seleccion:
            id_cliente = tabla_clientes.item(seleccion[0])['values'][0]

            # GUARDAR GEOMETRIA ORIGINAL
            # Solo si NO estamos ya en modo dividido (ventana info no existe), guardamos la original.
            # Si ya existe, mantenemos la que se guardó la primera vez.
            if ventana_info_cliente_instancia is None or not ventana_info_cliente_instancia.winfo_exists():
                ventana_clientes.geometria_original = ventana_clientes.geometry()

            # --- LOGICA DE POSICIONAMIENTO Y RESIZE ---
            screen_width = ventana_clientes.winfo_screenwidth()
            current_y = ventana_clientes.winfo_y()

            info_width = 900
            info_height = 600
            margin = 20  # Margen para separar de los bordes y entre ventanas
            
            x_info = margin
            # La lista se posiciona después de la info + margen
            x_list = x_info + info_width + margin
            
            # Espacio restante para la lista, restando tambien el margen derecho
            list_width = screen_width - x_list - margin
            
            # Aseguramos un mínimo
            if list_width < 300: list_width = 300
            
            list_height = 600

            def al_cerrar_info():
                try:
                    if ventana_clientes.winfo_exists():
                        tabla_clientes["displaycolumns"] = "#all"
                        entry_buscar.config(width=25)
                        
                        # Restaurar botones
                        boton_eliminar.pack(side="right", padx=(5, 0))
                        boton_editar.pack(side="right", padx=5)
                        boton_agregar.pack(side="right", padx=5)

                        def restaurar():
                            if not ventana_clientes.winfo_exists(): return
                            # Restaurar a geometria original guardada
                            if hasattr(ventana_clientes, 'geometria_original'):
                                ventana_clientes.geometry(ventana_clientes.geometria_original)
                            ventana_clientes.lift()

                        # Usamos un delay para asegurar que el cambio de geometría se aplique
                        # después de que el gestor de ventanas procese el cierre de la otra ventana.
                        ventana_clientes.after(100, restaurar)
                except Exception:
                    pass

            informacion_cliente_vista(id_cliente, ventana_clientes, x_pos=x_info, y_pos=current_y, on_close=al_cerrar_info)

            # Ajustar la ventana de listado
            ventana_clientes.geometry(f"{list_width}x{list_height}+{x_list}+{current_y}")
            # Mostrar solo ID y Nombre
            tabla_clientes["displaycolumns"] = ("id", "nombre")
            
            # Ocultar botones
            boton_agregar.pack_forget()
            boton_editar.pack_forget()
            boton_eliminar.pack_forget()
            
            # Ajustar ancho buscador (menos ancho si se desea, o mantener normal)
            entry_buscar.config(width=20)


    # FUNCION ORDENAR COLUMNA
    def ordenar_por_columna(tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        # Intentar convertir a int para ordenar ID numericamente, sino alfabetico
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # Reordenar items
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Actualizar el comando para invertir el orden en el próximo clic
        tree.heading(col, command=lambda: ordenar_por_columna(tree, col, not reverse))


    # CONFIGURAR COLUMNAS
    tabla_clientes.heading("id", text="ID", command=lambda: ordenar_por_columna(tabla_clientes, "id", False))
    tabla_clientes.heading("nombre", text="Nombre", command=lambda: ordenar_por_columna(tabla_clientes, "nombre", False))
    tabla_clientes.heading("localidad", text="Localidad", command=lambda: ordenar_por_columna(tabla_clientes, "localidad", False))
    tabla_clientes.heading("telefono", text="Teléfono")

    tabla_clientes.column("id", width=80, anchor="center")
    tabla_clientes.column("nombre", width=250, anchor="w")
    tabla_clientes.column("localidad", width=200, anchor="center")
    tabla_clientes.column("telefono", width=150, anchor="center")

    tabla_clientes.pack(side="left", fill="both", expand=True)
    tabla_clientes.bind("<Button-3>", mostrar_menu)
    tabla_clientes.bind("<Double-1>", captar_id_cliente)
    scrollbar.config(command=tabla_clientes.yview)


    # FRAME SUPERIOR - BUSCADOR Y BOTONES
    frame_superior = tk.Frame(ventana_clientes, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    # BUSCADOR
    label_busqueda = tk.Label(frame_superior, text="Buscar:", font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_busqueda.pack(side="left", padx=(0, 10))

    entry_buscar = tk.Entry(frame_superior, bg=color_secundario, fg=color_primario, font=fuente_texto, width=25)
    entry_buscar.bind("<KeyRelease>", filtrar_tabla)
    entry_buscar.pack(side="left")

    # BOTONES
    boton_eliminar = ttk.Button(frame_superior, text="Eliminar", style="BotonSecundario.TButton")
    boton_eliminar.config(cursor="hand2", command=ejecutar_eliminacion)
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = ttk.Button(frame_superior, text="Editar", style="BotonSecundario.TButton")
    boton_editar.config(command=abrir_editar, cursor="hand2")
    boton_editar.pack(side="right", padx=5)

    boton_agregar = ttk.Button(frame_superior, text="Añadir", style="BotonSecundario.TButton")
    boton_agregar.config(command=lambda: nuevo_cliente_vista(actualizar_tabla), cursor="hand2")
    boton_agregar.pack(side="right", padx=5)


def nuevo_cliente_vista(callback=None):
    global ventana_nuevo_cliente_instancia
    if ventana_nuevo_cliente_instancia is not None and ventana_nuevo_cliente_instancia.winfo_exists():
        ventana_nuevo_cliente_instancia.lift()
        return

    ventana_nuevo_cliente = tk.Toplevel()
    ventana_nuevo_cliente_instancia = ventana_nuevo_cliente

    ventana_nuevo_cliente.title("Nuevo Cliente")
    ventana_nuevo_cliente.config(bg=color_primario)
    ventana_nuevo_cliente.geometry("400x600+120+85")
    ventana_nuevo_cliente.resizable(False, False)
    ventana_nuevo_cliente.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    # CONFIGURACION DEL GRID
    ventana_nuevo_cliente.grid_columnconfigure(0, weight=1)
    ventana_nuevo_cliente.grid_columnconfigure(1, weight=2)


    # LABEL TITULO
    label_titulo = tk.Label(ventana_nuevo_cliente, text="REGISTRAR CLIENTE")
    label_titulo.config(font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(50, 40), padx=20)


    # NOMBRE
    cmd_validar_letra = ventana_nuevo_cliente.register(validar_solo_letras)

    label_nombre = tk.Label(ventana_nuevo_cliente, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = ttk.Entry(ventana_nuevo_cliente)
    entry_nombre.config(font=fuente_texto, width=20,
                        validate="key", validatecommand=(cmd_validar_letra, '%P'))
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # APELLIDO
    cmd_validar_letra = ventana_nuevo_cliente.register(validar_solo_letras)

    label_apellido = tk.Label(ventana_nuevo_cliente, text="Apellido:")
    label_apellido.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_apellido.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_apellido = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_apellido.config (font=fuente_texto, width=20,
                        validate="key", validatecommand=(cmd_validar_letra, '%P'))
    entry_apellido.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)


    # TELEFONO
    cmd_validar_numeros = ventana_nuevo_cliente.register(validar_solo_numeros)

    label_telefono = tk.Label(ventana_nuevo_cliente, text="Teléfono:")
    label_telefono.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_telefono.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_telefono = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_telefono.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))
    entry_telefono.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)


    # LOCALIDAD
    label_localidad = tk.Label(ventana_nuevo_cliente, text="Localidad:")
    label_localidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_localidad.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_localidad = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_localidad.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CALLE
    label_direccion = tk.Label(ventana_nuevo_cliente, text="Direccion:")
    label_direccion.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_direccion.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_direccion = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_direccion.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # FACTURA
    label_factura = tk.Label(ventana_nuevo_cliente, text="Fac. Produccion:")
    label_factura.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_factura.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)

    opciones_factura = ["No", "Si"]
    combobox_factura = ttk.Combobox(ventana_nuevo_cliente, values=opciones_factura)
    combobox_factura.config(state="readonly", font=fuente_texto, width=18)
    combobox_factura.current(0)
    combobox_factura.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)


    # CUIT (Inicialmente oculto)
    cmd_validar_numeros = ventana_nuevo_cliente.register(validar_solo_numeros)

    label_cuit = tk.Label(ventana_nuevo_cliente, text="CUIT:")
    label_cuit.config(font=fuente_texto, bg=color_primario, fg=color_secundario)

    entry_cuit = ttk.Entry(ventana_nuevo_cliente, font=fuente_texto, width=20)
    entry_cuit.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))


    # CAPTURA DE DATOS
    def capturar_datos_cliente():
        nom = entry_nombre.get()
        apell = entry_apellido.get()
        tel = entry_telefono.get()
        local = entry_localidad.get()
        direcc = entry_direccion.get()
        fac = combobox_factura.get()
        c_u_i_t = entry_cuit.get()

        if fac == "No":
            c_u_i_t = None

        nuevo_cliente_controlador(nom, apell, tel, local, direcc, fac, c_u_i_t, ventana_nuevo_cliente, callback)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_nuevo_cliente, bg=color_primario)
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 20))

    boton_guardar = ttk.Button(frame_botones, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2", command=capturar_datos_cliente)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = ttk.Button(frame_botones, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2", command=ventana_nuevo_cliente.destroy)
    boton_cancelar.pack(side="left", padx=5)

    # Función para mostrar/ocultar CUIT según la selección del combobox
    def actualizar_cuit(event):
        if combobox_factura.get() == "Si":
            label_cuit.grid(row=7, column=0, sticky="e", padx=(20, 10), pady=10)
            entry_cuit.grid(row=7, column=1, sticky="w", padx=(0, 20), pady=10)
        else:
            label_cuit.grid_remove()
            entry_cuit.grid_remove()

    # Vincular evento al combobox
    combobox_factura.bind("<<ComboboxSelected>>", actualizar_cuit)


def editar_cliente_vista(id_cliente, callback=None):
    global ventana_editar_cliente_instancia
    if ventana_editar_cliente_instancia is not None and ventana_editar_cliente_instancia.winfo_exists():
        ventana_editar_cliente_instancia.lift()
        return

    ventana_editar_cliente = tk.Toplevel()
    ventana_editar_cliente_instancia = ventana_editar_cliente

    ventana_editar_cliente.title("Editar cliente")
    ventana_editar_cliente.config(bg=color_primario)
    ventana_editar_cliente.geometry("400x600+120+85")
    ventana_editar_cliente.resizable(False, False)
    ventana_editar_cliente.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    # CONFIGURACION DEL GRID
    ventana_editar_cliente.grid_columnconfigure(0, weight=1)
    ventana_editar_cliente.grid_columnconfigure(1, weight=2)

    # LABEL TITULO
    label_titulo = tk.Label(ventana_editar_cliente, text="EDITAR CLIENTE")
    label_titulo.config(font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(50, 40), padx=20)

    # BUSCAR DATOS DEL CLIENTE
    cliente_a_editar = informacion_cliente_controlador(id_cliente)

    # NOMBRE
    cmd_validar_letra = ventana_editar_cliente.register(validar_solo_letras)

    label_nombre = tk.Label(ventana_editar_cliente, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = ttk.Entry(ventana_editar_cliente)
    entry_nombre.config(font=fuente_texto, width=20,
                        validate="key", validatecommand=(cmd_validar_letra, '%P'))
    entry_nombre.insert(0, cliente_a_editar.nombre)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)

    # APELLIDO
    cmd_validar_letra = ventana_editar_cliente.register(validar_solo_letras)

    label_apellido = tk.Label(ventana_editar_cliente, text="Apellido:")
    label_apellido.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_apellido.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_apellido = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_apellido.config(font=fuente_texto, width=20,
                          validate="key", validatecommand=(cmd_validar_letra, '%P'))
    entry_apellido.insert(0, cliente_a_editar.apellido)
    entry_apellido.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=10)

    # TELEFONO
    cmd_validar_numeros = ventana_editar_cliente.register(validar_solo_numeros)

    label_telefono = tk.Label(ventana_editar_cliente, text="Teléfono:")
    label_telefono.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_telefono.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_telefono = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_telefono.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))
    entry_telefono.insert(0, cliente_a_editar.telefono)
    entry_telefono.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=10)

    # LOCALIDAD
    label_localidad = tk.Label(ventana_editar_cliente, text="Localidad:")
    label_localidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_localidad.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_localidad = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_localidad.insert(0, cliente_a_editar.localidad)
    entry_localidad.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)

    # CALLE
    label_direccion = tk.Label(ventana_editar_cliente, text="Direccion:")
    label_direccion.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_direccion.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_direccion = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_direccion.insert(0, cliente_a_editar.direccion)
    entry_direccion.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)

    # FACTURA
    label_factura = tk.Label(ventana_editar_cliente, text="Fac. Produccion:")
    label_factura.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_factura.grid(row=6, column=0, sticky="e", padx=(20, 10), pady=10)

    opciones_factura = ["No", "Si"]
    combobox_factura = ttk.Combobox(ventana_editar_cliente, values=opciones_factura)
    combobox_factura.config(state="readonly", font=fuente_texto, width=18)
    
    val_factura = "Si" if cliente_a_editar.factura_produccion == 1 else "No"
    combobox_factura.set(val_factura)
    
    combobox_factura.grid(row=6, column=1, sticky="w", padx=(0, 20), pady=10)

    # CUIT (Inicialmente oculto)
    cmd_validar_numeros = ventana_editar_cliente.register(validar_solo_numeros)

    label_cuit = tk.Label(ventana_editar_cliente, text="CUIT:")
    label_cuit.config(font=fuente_texto, bg=color_primario, fg=color_secundario)

    entry_cuit = ttk.Entry(ventana_editar_cliente, font=fuente_texto, width=20)
    entry_cuit.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))
    
    if cliente_a_editar.cuit:
        entry_cuit.insert(0, cliente_a_editar.cuit)

    # Función para mostrar/ocultar CUIT según la selección del combobox
    def actualizar_cuit(event=None):
        if combobox_factura.get() == "Si":
            label_cuit.grid(row=7, column=0, sticky="e", padx=(20, 10), pady=10)
            entry_cuit.grid(row=7, column=1, sticky="w", padx=(0, 20), pady=10)
        else:
            label_cuit.grid_remove()
            entry_cuit.grid_remove()

    # Vincular evento al combobox
    combobox_factura.bind("<<ComboboxSelected>>", actualizar_cuit)
    # Ejecutar una vez para setear el estado inicial
    actualizar_cuit()


    # CAPTURA DE DATOS EDICION
    def capturar_datos_edicion():
        nom = entry_nombre.get()
        apell = entry_apellido.get()
        tel = entry_telefono.get()
        local = entry_localidad.get()
        direcc = entry_direccion.get()
        fac = combobox_factura.get()
        c_u_i_t = entry_cuit.get()

        if fac == "No":
            c_u_i_t = None
        
        editar_cliente_controlador(id_cliente, nom, apell, tel, local, direcc, fac, c_u_i_t, ventana_editar_cliente, callback)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_editar_cliente, bg=color_primario)
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(30, 20))

    boton_guardar = ttk.Button(frame_botones, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2", command=capturar_datos_edicion)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = ttk.Button(frame_botones, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2", command=ventana_editar_cliente.destroy)
    boton_cancelar.pack(side="left", padx=5)


def informacion_cliente_vista(id_cliente, ventana_clientes, x_pos=None, y_pos=None, on_close=None):
    global ventana_info_cliente_instancia
    
    # Si ya existe una instancia, la destruimos para crear la nueva con el nuevo cliente
    if ventana_info_cliente_instancia is not None and ventana_info_cliente_instancia.winfo_exists():
        ventana_info_cliente_instancia.destroy()


    # BUSCA EL CLIENTE Y LO INSTANCIA
    cliente = informacion_cliente_controlador(id_cliente)

    fac_produccion = cliente.factura_produccion
    if fac_produccion == 1:
        fac_produccion = "Si"
    else:
        fac_produccion = "No"

    cuit = cliente.cuit
    if cuit is None:
        cuit = "N/A"


    # INICIA LA VISTA
    ventana_info_cliente = tk.Toplevel(ventana_clientes)
    ventana_info_cliente_instancia = ventana_info_cliente
    ventana_info_cliente.title("Informacion del cliente")
    ventana_info_cliente.configure(bg=color_primario)
    ventana_info_cliente.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    # Dimensiones y centrado
    # Dimensiones y centrado
    ancho_ventana = 900
    alto_ventana = 600

    if x_pos is not None and y_pos is not None:
        ventana_info_cliente.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
    else:
        centrar_ventana_interna(ventana_info_cliente, ancho_ventana, alto_ventana)

    if on_close:
        def cerrar_wrapper():
            on_close()
            ventana_info_cliente.destroy()
        ventana_info_cliente.protocol("WM_DELETE_WINDOW", cerrar_wrapper)


    # --- FRAME SUPERIOR (Datos y Botones) ---
    frame_superior = tk.Frame(ventana_info_cliente, bg=color_primario)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)


    # --- SUB-FRAME DATOS DEL CLIENTE (Izquierda) ---
    frame_datos = tk.Frame(frame_superior, bg=color_primario)
    frame_datos.pack(side="left", fill="both", expand=True)


    # --- FILA 0: ID | Nombre | Apellido ---

    # ID

    label_id_titulo = tk.Label(frame_datos, text="ID:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_id_titulo.grid(row=0, column=0, sticky="w", pady=5, padx=(0, 5))
    label_id_valor = tk.Label(frame_datos, text=id_cliente, bg=color_primario, fg="white", font=("Arial", 10))
    label_id_valor.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 20))

    # NOMBRE
    label_nombre_titulo = tk.Label(frame_datos, text="Nombre:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_nombre_titulo.grid(row=0, column=2, sticky="w", pady=5, padx=(10, 5))
    label_nombre_valor = tk.Label(frame_datos, text=cliente.nombre, bg=color_primario, fg="white", font=("Arial", 10), wraplength=120, justify="left")
    label_nombre_valor.grid(row=0, column=3, sticky="w", pady=5, padx=(0, 20))

    # APELLIDO
    label_apellido_titulo = tk.Label(frame_datos, text="Apellido:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_apellido_titulo.grid(row=0, column=4, sticky="w", pady=5, padx=(10, 5))
    label_apellido_valor = tk.Label(frame_datos, text=cliente.apellido, bg=color_primario, fg="white", font=("Arial", 10), wraplength=120, justify="left")
    label_apellido_valor.grid(row=0, column=5, sticky="w", pady=5, padx=(0, 0))


    # --- FILA 1: Telefono | Localidad | Calle ---

    # TELEFONO
    label_telefono_titulo = tk.Label(frame_datos, text="Teléfono:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_telefono_titulo.grid(row=1, column=0, sticky="w", pady=5, padx=(0, 5))
    label_telefono_valor = tk.Label(frame_datos, text=cliente.telefono, bg=color_primario, fg="white", font=("Arial", 10))
    label_telefono_valor.grid(row=1, column=1, sticky="w", pady=5, padx=(0, 20))

    # LOCALIDAD
    label_localidad_titulo = tk.Label(frame_datos, text="Localidad:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_localidad_titulo.grid(row=1, column=2, sticky="w", pady=5, padx=(10, 5))
    label_localidad_valor = tk.Label(frame_datos, text=cliente.localidad, bg=color_primario, fg="white", font=("Arial", 10), wraplength=120, justify="left")
    label_localidad_valor.grid(row=1, column=3, sticky="w", pady=5, padx=(0, 20))

    # DIRECCION
    label_direccion_titulo = tk.Label(frame_datos, text="Direccion:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_direccion_titulo.grid(row=1, column=4, sticky="w", pady=5, padx=(10, 5))
    label_direccion_valor = tk.Label(frame_datos, text=cliente.direccion, bg=color_primario, fg="white", font=("Arial", 10), wraplength=120, justify="left")
    label_direccion_valor.grid(row=1, column=5, sticky="w", pady=5, padx=(0, 0))


    # --- FILA 2: Factura | CUIT ---

    # FACTURA
    label_factura_titulo = tk.Label(frame_datos, text="Factura:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_factura_titulo.grid(row=2, column=0, sticky="w", pady=5, padx=(0, 5))
    label_factura_valor = tk.Label(frame_datos, text=fac_produccion, bg=color_primario, fg="white", font=("Arial", 10))
    label_factura_valor.grid(row=2, column=1, sticky="w", pady=5, padx=(0, 20))

    # CUIT
    label_cuit_titulo = tk.Label(frame_datos, text="CUIT:", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
    label_cuit_titulo.grid(row=2, column=2, sticky="w", pady=5, padx=(10, 5))
    label_cuit_valor = tk.Label(frame_datos, text=cuit, bg=color_primario, fg="white", font=("Arial", 10))
    label_cuit_valor.grid(row=2, column=3, sticky="w", pady=5, padx=(0, 20))


    # Configuración de pesos para que las columnas de valores se expandan si sobra espacio
    frame_datos.grid_columnconfigure(1, weight=1)
    frame_datos.grid_columnconfigure(3, weight=1)
    frame_datos.grid_columnconfigure(5, weight=1)


    # --- SUB-FRAME DERECHO (Botones) ---
    frame_derecho = tk.Frame(frame_superior, bg=color_primario)
    frame_derecho.pack(side="right", fill="y", expand=False, padx=(30, 0))

    # Usamos grid dentro del frame derecho para centrar el bloque de botones verticalmente
    frame_derecho.grid_columnconfigure(0, weight=1)
    frame_derecho.grid_rowconfigure(0, weight=1)

    frame_botones = tk.Frame(frame_derecho, bg=color_primario)
    frame_botones.grid(row=0, column=0)


    # BOTONES
    boton_nueva = ttk.Button(frame_botones, text="Nueva", style="BotonSecundario.TButton")
    boton_nueva.config(cursor="hand2", command=lambda: nueva_operacion(ventana_info_cliente), width=8)
    boton_nueva.pack(side="left", padx=(3, 5))

    boton_editar = ttk.Button(frame_botones, text="Editar", style="BotonSecundario.TButton")
    boton_editar.config(cursor="hand2", width=8)
    boton_editar.pack(side="left", padx=5)

    boton_eliminar = ttk.Button(frame_botones, text="Eliminar", style="BotonSecundario.TButton")
    boton_eliminar.config(cursor="hand2", width=8)
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
    listado_clientes()