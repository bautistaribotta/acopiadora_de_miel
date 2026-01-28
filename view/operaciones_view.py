import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from view.estilos import *
from controller.cotizaciones import get_cotizacion_oficial_venta, get_cotizacion_miel_clara
from controller.clientes_controlador import listar_clientes_controlador, buscador_clientes_controlador
from controller.operaciones_controlador import crear_nueva_operacion
from controller.productos_controlador import informacion_producto_controlador


ventana_nueva_operacion_instancia = None
ventana_editar_operacion_instancia = None


def guardar_y_remito(listado_items, id_cliente, total, metodo_pago, nombre, apellido, telefono, localidad, domicilio, observaciones):
    valor_dolar = get_cotizacion_oficial_venta()
    valor_kilo_miel = get_cotizacion_miel_clara()

    # Desgloso el carrito, resto            # --- NUEVO: El stock se descuenta automáticamente en la transacción de DB ---

    # Llamo al controlador para que cree la operacion y los detalles de la misma
    crear_nueva_operacion(id_cliente, listado_items, total, metodo_pago, valor_dolar, valor_kilo_miel, observaciones)


def nueva_operacion(parent=None):
    global ventana_nueva_operacion_instancia
    if ventana_nueva_operacion_instancia is not None and ventana_nueva_operacion_instancia.winfo_exists():
        ventana_nueva_operacion_instancia.lift()
        return

    ventana_nueva_operacion = tk.Toplevel(parent)
    ventana_nueva_operacion_instancia = ventana_nueva_operacion

    ventana_nueva_operacion.title("Nueva Operación")
    ventana_nueva_operacion.config(bg=color_primario)
    ventana_nueva_operacion.resizable(False, False)
    try:
        ventana_nueva_operacion.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass

    # Configuro el tamaño inicial más chico para selección de cliente
    ancho_ventana = 500
    alto_ventana = 500
    # Permito redimensionar para evitar problemas de visualización
    ventana_nueva_operacion.resizable(True, True)
    centrar_ventana_interna(ventana_nueva_operacion, ancho_ventana, alto_ventana)
    
    # Variables de estado
    cliente_seleccionado_id = None
    cliente_seleccionado_nombre = None
    
    # Variables de UI para la interfaz de operación (necesarias para nonlocal)
    entry_buscar = None
    tabla_busqueda = None
    tabla_carrito = None
    boton_quitar = None

    # Configuro el frame contenedor principal para poder cambiar vistas
    frame_principal = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_principal.pack(fill="both", expand=True)

    # Estado compartido simplificado
    items_carrito = {}

    def mostrar_seleccion_cliente(carrito_data=None):
        # Limpio el frame principal
        for widget in frame_principal.winfo_children():
            widget.destroy()
        
        # Guardo el carrito si viene
        nonlocal items_carrito
        if carrito_data is not None:
            items_carrito = carrito_data

        # Actualizo el título de la ventana
        ventana_nueva_operacion.title("Nueva Operación - 2: Selección del cliente y detalles")

        # Configuro el layout principal
        frame_principal.grid_columnconfigure(0, weight=1) # Columna Izquierda
        frame_principal.grid_columnconfigure(1, weight=1) # Columna Derecha
        frame_principal.grid_rowconfigure(0, weight=0) # Títulos
        frame_principal.grid_rowconfigure(1, weight=0) # Search / Spacer
        frame_principal.grid_rowconfigure(2, weight=1) # Table / Details
        frame_principal.grid_rowconfigure(3, weight=0) # Botones

        # --- TITULOS (Row 0) ---
        tk.Label(frame_principal, text="Seleccione un cliente", font=fuente_titulos, bg=color_primario, fg=color_secundario).grid(row=0, column=0, pady=(20, 10))
        tk.Label(frame_principal, text="Detalles de la Operación", font=fuente_titulos, bg=color_primario, fg=color_secundario).grid(row=0, column=1, pady=(20, 10))

        # --- COLUMNA IZQUIERDA (Search Row 1, Table Row 2) ---
        # Buscador
        frame_buscador = tk.Frame(frame_principal, bg=color_primario)
        frame_buscador.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        tk.Label(frame_buscador, text="Buscar:", font=fuente_titulos, bg=color_primario, fg=color_secundario).pack(side="left", padx=(0, 10))
        entry_buscar_cli = ttk.Entry(frame_buscador, font=fuente_texto, width=25)
        entry_buscar_cli.pack(side="left", fill="x", expand=True)

        # Tabla Clientes
        frame_tabla_wrapper = tk.Frame(frame_principal, bg=color_primario)
        frame_tabla_wrapper.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        scrollbar_cli = ttk.Scrollbar(frame_tabla_wrapper)
        scrollbar_cli.pack(side="right", fill="y")
        
        cols_cli = ("id", "nombre")
        tabla_cli = ttk.Treeview(frame_tabla_wrapper, columns=cols_cli, show="headings", yscrollcommand=scrollbar_cli.set, height=8)
        
        tabla_cli.heading("id", text="ID")
        tabla_cli.heading("nombre", text="Nombre")
        tabla_cli.column("id", width=50, anchor="center")
        tabla_cli.column("nombre", width=280, anchor="w")
        
        tabla_cli.pack(side="left", fill="both", expand=True)
        scrollbar_cli.config(command=tabla_cli.yview)

        # --- COLUMNA DERECHA ---
        # Label Observaciones (Row 1 para alinear con buscador)
        frame_lbl_obs = tk.Frame(frame_principal, bg=color_primario)
        frame_lbl_obs.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 10))
        tk.Label(frame_lbl_obs, text="Observaciones", font=fuente_titulos, bg=color_primario, fg=color_secundario).pack(anchor="w")

        # Detalle (Text area) en Row 2 (alineado arriba con Tabla)
        frame_detalles = tk.Frame(frame_principal, bg=color_primario)
        frame_detalles.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20)) 
        
        txt_detalle = tk.Text(frame_detalles, font=fuente_texto, height=8, width=40)
        txt_detalle.pack(fill="x", pady=(0, 10))

        # Metodo de Pago
        tk.Label(frame_detalles, text="Método de Pago:", font=fuente_texto, bg=color_primario, fg="white").pack(anchor="w", pady=(10, 5))
        combo_pago = ttk.Combobox(frame_detalles, values=["Contado", "Cuenta Corriente"], state="readonly", font=fuente_texto)
        combo_pago.pack(fill="x", pady=(0, 20))
        combo_pago.current(0)
        
        # --- BOTONES (Row 3 - Spanning) ---
        frame_botones = tk.Frame(frame_principal, bg=color_primario)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Lógica de selección de cliente
        def on_cliente_select(event):
            selection = tabla_cli.selection()
            if selection:
                nonlocal cliente_seleccionado_id, cliente_seleccionado_nombre
                item = tabla_cli.item(selection[0])
                vals = item['values']
                cliente_seleccionado_id = vals[0]
                cliente_seleccionado_nombre = vals[1]
                
        tabla_cli.bind("<<TreeviewSelect>>", on_cliente_select)

        # Funcionalidad del Botón Guardar
        def guardar_y_remito():
            if not cliente_seleccionado_id:
                messagebox.showwarning("Error", "Seleccione un cliente.", parent=ventana_nueva_operacion)
                return

            metodo = combo_pago.get()
            if not metodo:
                 messagebox.showwarning("Error", "Seleccione un método de pago.", parent=ventana_nueva_operacion)
                 return
            
            obs = txt_detalle.get("1.0", "end-1c")

            # Armar lista_items_carrito
            lista_items = []
            monto_total_calc = 0.0
            
            for pid, cant in items_carrito.items():
                lista_items.append({'id': pid, 'cantidad': cant})
                # Calcular precio
                prod = informacion_producto_controlador(pid)
                if prod:
                    try:
                        stock_or_cant = float(cant)
                        precio = float(prod.precio)
                        monto_total_calc += precio * stock_or_cant
                    except:
                        pass

            # Obtener cotizaciones
            dolar = get_cotizacion_oficial_venta()
            kilo_miel = get_cotizacion_miel_clara()

            exito = crear_nueva_operacion(
                id_cliente=cliente_seleccionado_id,
                monto_total=monto_total_calc,
                lista_items_carrito=lista_items,
                valor_dolar=dolar,
                valor_kilo_miel=kilo_miel,
                metodo_de_pago=metodo,
                observaciones=obs
            )

            if exito:
                ventana_nueva_operacion.destroy()

        # Boton Guardar y Remito
        btn_guardar = ttk.Button(frame_botones, text="Guardar y Remito", style="BotonSecundario.TButton", command=guardar_y_remito)
        btn_guardar.pack(side="left", padx=(0, 10))
        
        # Boton Cancelar
        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", style="BotonSecundario.TButton", command=ventana_nueva_operacion.destroy)
        btn_cancelar.pack(side="left", padx=(0, 10))

        # Lógica de carga de clientes
        def llenar_tabla_clientes(filtro=""):
            for item in tabla_cli.get_children():
                tabla_cli.delete(item)
            if filtro:
                clientes = buscador_clientes_controlador(filtro)
            else:
                clientes = listar_clientes_controlador()   
            for cli in clientes:
                c_id, c_nom, c_ape = cli[0], cli[1], cli[2]
                vals = (c_id, f"{c_nom} {c_ape}")
                tabla_cli.insert("", "end", values=vals)

        llenar_tabla_clientes()
        entry_buscar_cli.bind("<KeyRelease>", lambda e: llenar_tabla_clientes(entry_buscar_cli.get()))

        
    def mostrar_interfaz_operacion():
        # Aumento el tamaño para vista completa
        centrar_ventana_interna(ventana_nueva_operacion, 950, 600)
        ventana_nueva_operacion.resizable(True, True)

        # Limpio el frame principal
        for widget in frame_principal.winfo_children():
            widget.destroy()
            
        # Actualizo el título de la ventana
        ventana_nueva_operacion.title("Nueva Operación - 1: Selección de Productos")

        # Re-creo la interfaz de operación dentro de frame_principal
        frame_principal.grid_columnconfigure(0, weight=1) 
        frame_principal.grid_columnconfigure(1, weight=1) 
        frame_principal.grid_rowconfigure(0, weight=1) 
        frame_principal.grid_rowconfigure(1, weight=0)

        # ========================== Configuro Columna Izquierda ==========================
        frame_izq = tk.Frame(frame_principal, bg=color_primario)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configuro el buscador
        frame_search = tk.Frame(frame_izq, bg=color_primario)
        frame_search.pack(fill="x", pady=(10, 20))
        
        label_buscar = tk.Label(frame_search, text="Buscar:", font=fuente_titulos, bg=color_primario, fg=color_secundario)
        label_buscar.pack(side="left", padx=(0, 10))
        
        nonlocal entry_buscar, tabla_busqueda, tabla_carrito, boton_quitar
        
        entry_buscar = ttk.Entry(frame_search, font=fuente_texto, width=25)
        entry_buscar.pack(side="left")

        # Configuro el frame de tabla de búsqueda
        frame_tabla_busqueda = tk.Frame(frame_izq, bg=color_primario)
        scrollbar_busqueda = ttk.Scrollbar(frame_tabla_busqueda)
        scrollbar_busqueda.pack(side="right", fill="y")
        
        cols_busqueda = ("id", "nombre", "stock", "precio")
        tabla_busqueda = ttk.Treeview(frame_tabla_busqueda, columns=cols_busqueda, show="headings", yscrollcommand=scrollbar_busqueda.set, height=10)
        
        tabla_busqueda.heading("id", text="ID")
        tabla_busqueda.heading("nombre", text="Nombre")
        tabla_busqueda.heading("stock", text="Stock")
        tabla_busqueda.heading("precio", text="Precio")
        
        tabla_busqueda.column("id", width=80, anchor="center")
        tabla_busqueda.column("nombre", width=200, anchor="center")
        tabla_busqueda.column("stock", width=80, anchor="center")
        tabla_busqueda.column("precio", width=80, anchor="center")
        
        tabla_busqueda.pack(side="left", fill="both", expand=True)
        scrollbar_busqueda.config(command=tabla_busqueda.yview)

        # Configuro el frame para agregar
        frame_agregar = tk.Frame(frame_izq, bg=color_primario)
        frame_agregar.pack(side="bottom", fill="x", pady=15)
        
        img_carrito = Image.open(obtener_ruta_recurso("carrito.ico"))
        img_carrito = img_carrito.resize((20, 20))
        icono_carrito = ImageTk.PhotoImage(img_carrito)
        boton_agregar = ttk.Button(frame_agregar, image=icono_carrito, text=" Agregar al carrito", compound="left", style="BotonSecundario.TButton")
        boton_agregar.image = icono_carrito
        boton_agregar.pack(side="left")

        frame_tabla_busqueda.pack(fill="both", expand=True) # Empaqueto la tabla

        # ========================== Configuro Columna Derecha ==========================
        frame_der = tk.Frame(frame_principal, bg=color_primario)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(frame_der, text="Listado de compra", font=fuente_titulos, bg=color_primario, fg=color_secundario).pack(pady=(10, 20))

        frame_acciones_carrito = tk.Frame(frame_der, bg=color_primario)
        frame_acciones_carrito.pack(side="bottom", fill="x", pady=15)

        img_tacho = Image.open(obtener_ruta_recurso("tacho.ico"))
        img_tacho = img_tacho.resize((20, 20))
        icono_tacho = ImageTk.PhotoImage(img_tacho)
        boton_quitar = ttk.Button(frame_acciones_carrito, image=icono_tacho, style="BotonSecundario.TButton")
        boton_quitar.image = icono_tacho
        boton_quitar.pack(side="right", padx=(10, 0))

        lbl_total_pesos = tk.Label(frame_acciones_carrito, text="$ 0.00", bg=color_primario, fg="white", font=("Arial", 12, "bold"))
        lbl_total_pesos.pack(side="right", padx=(5, 0))
        tk.Label(frame_acciones_carrito, text="Total:", bg=color_primario, fg="white", font=("Arial", 12)).pack(side="right")

        frame_tabla_carrito = tk.Frame(frame_der, bg=color_primario)
        frame_tabla_carrito.pack(fill="both", expand=True)
        
        scrollbar_carrito = ttk.Scrollbar(frame_tabla_carrito)
        scrollbar_carrito.pack(side="right", fill="y")
        
        cols_carrito = ("id", "nombre", "cantidad")
        tabla_carrito = ttk.Treeview(frame_tabla_carrito, columns=cols_carrito, show="headings", yscrollcommand=scrollbar_carrito.set, height=10)
        tabla_carrito["displaycolumns"] = ("cantidad", "nombre")
        
        tabla_carrito.heading("nombre", text="Producto")
        tabla_carrito.heading("cantidad", text="Cant.")
        tabla_carrito.column("nombre", width=200, anchor="w")
        tabla_carrito.column("cantidad", width=30, anchor="center")
        
        tabla_carrito.pack(side="left", fill="both", expand=True)
        scrollbar_carrito.config(command=tabla_carrito.yview)

        # ========================== Configuro Frame Inferior ==========================
        frame_final = tk.Frame(frame_principal, bg=color_primario)
        frame_final.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Función para ir a la siguiente pantalla (Selección Cliente)
        def ir_siguiente():
            # Extraigo los items del carrito para pasarlos
            datos_carrito = {}
            for item in tabla_carrito.get_children():
                # values = (id, nombre, cantidad)
                vals = tabla_carrito.item(item)['values']
                datos_carrito[vals[0]] = vals[2] # id: cantidad
            
            if not datos_carrito:
                messagebox.showwarning("Atención", "No se seleccionó ningún producto.", parent=ventana_nueva_operacion)
                return

            mostrar_seleccion_cliente(datos_carrito)

        boton_siguiente = ttk.Button(frame_final, text="Siguiente", style="BotonSecundario.TButton", cursor="hand2", command=ir_siguiente)
        boton_siguiente.pack(side="left", padx=10)
        
        boton_cancelar = ttk.Button(frame_final, text="Cancelar", style="BotonSecundario.TButton", cursor="hand2", command=ventana_nueva_operacion.destroy)
        boton_cancelar.pack(side="left", padx=10)

        # --- Conecto lógica funcional ---
        setup_logica_operacion(entry_buscar, tabla_busqueda, tabla_carrito, boton_agregar, boton_quitar, ventana_nueva_operacion)


    # Inicio el flujo mostrando primero la interfaz de operacion (Productos)
    mostrar_interfaz_operacion()


def setup_logica_operacion(entry_buscar, tabla_busqueda, tabla_carrito, btn_agregar, btn_quitar, ventana_root):
    from controller.productos_controlador import buscador_productos_controlador

    def obtener_cantidades_carrito():
        """Retorna un diccionario {id_producto: cantidad_en_carrito}"""
        cantidades = {}
        for item in tabla_carrito.get_children():
            valores = tabla_carrito.item(item)['values']
            try:
                item_id = valores[0]
                cantidad = int(valores[2])
            except:
                continue
            
            # Convertimos a string para usar como clave consistente
            item_id = str(valores[0])
            
            if item_id in cantidades:
                cantidades[item_id] += cantidad
            else:
                cantidades[item_id] = cantidad
        return cantidades


    def actualizar_listado_busqueda(filtro=""):
        # Obtener lo que ya esta en el carrito para restarlo visualmente
        en_carrito = obtener_cantidades_carrito()

        # Limpiar tabla
        for item in tabla_busqueda.get_children():
            tabla_busqueda.delete(item)
            
        productos = buscador_productos_controlador(filtro)
        for prod in productos:
            # prod = (id, nombre, categoria, precio, stock, ...)
            p_id = prod[0]
            p_nombre = prod[1]
            p_stock_real = prod[4]
            p_precio = prod[3]

            # Calcular stock visual
            try:
                # Convertimos explícitamente a str ambos lados para asegurar el match en el diccionario
                stock_visual = int(float(p_stock_real) - en_carrito.get(str(p_id), 0))
            except:
                stock_visual = 0

            valores_mostrar = (p_id, p_nombre, stock_visual, f"${p_precio}")
            tabla_busqueda.insert("", "end", values=valores_mostrar)

    def on_buscar_keyrelease(event):
        actualizar_listado_busqueda(entry_buscar.get())
        
    entry_buscar.bind("<KeyRelease>", on_buscar_keyrelease)
    
    # Cargar inicio (diferido)
    ventana_root.after(100, lambda: actualizar_listado_busqueda(""))

    # --- FUNCIONES POPUP CANTIDAD ---
    def confirmar_agregar(cantidad, valores_producto, ventana_popup):
        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            return 
        
        id_prod = valores_producto[0]
        nombre = valores_producto[1] 
        cant_nueva = int(cantidad)

        # Validacion de stock
        try:
            stock_disponible = int(valores_producto[2])
            if cant_nueva > stock_disponible:
                messagebox.showwarning("Error de stock", f"No hay suficiente stock. Disponible: {stock_disponible}", parent=ventana_popup)
                return
        except ValueError:
            pass # Si por alguna razon el stock no es numero, pasamos (o manejamos error)
        
        # Verificar si ya existe en el carrito
        item_existente = None
        cant_actual = 0
        
        for item in tabla_carrito.get_children():
            vals = tabla_carrito.item(item)['values']
            if str(vals[0]) == str(id_prod):
                item_existente = item
                cant_actual = int(vals[2])
                break
        
        if item_existente:
            nueva_total = cant_actual + cant_nueva
            tabla_carrito.item(item_existente, values=(id_prod, nombre, nueva_total))
        else:
            tabla_carrito.insert("", "end", values=(id_prod, nombre, cant_nueva))
            
        ventana_popup.destroy()
        actualizar_listado_busqueda(entry_buscar.get())

    def abrir_popup_cantidad(event=None):
        seleccion = tabla_busqueda.selection()
        if not seleccion: return
        
        valores = tabla_busqueda.item(seleccion[0])['values']
        
        popup = tk.Toplevel(ventana_root)
        popup.title("Cantidad")
        popup.config(bg=color_primario)
        popup.resizable(False, False)
        try:
            popup.iconbitmap(obtener_ruta_recurso("colmena.ico"))
        except: pass
        centrar_ventana_interna(popup, 300, 150)
        
        tk.Label(popup, text=f"Producto: {valores[1]}", bg=color_primario, fg="white", font=fuente_texto).pack(pady=(15, 10))
        
        frame_input = tk.Frame(popup, bg=color_primario)
        frame_input.pack(pady=5)
        tk.Label(frame_input, text="Cantidad:", bg=color_primario, fg="white", font=fuente_texto).pack(side="left", padx=5)
        
        entry_cant = ttk.Entry(frame_input, width=10, font=fuente_texto)
        entry_cant.pack(side="left", padx=5)
        entry_cant.focus_set()
        
        def on_confirm():
            confirmar_agregar(entry_cant.get(), valores, popup)
            
        btn_ok = ttk.Button(popup, text="Agregar", style="BotonSecundario.TButton", command=on_confirm)
        btn_ok.pack(pady=15)
        popup.bind('<Return>', lambda e: on_confirm())

    tabla_busqueda.bind("<Double-1>", abrir_popup_cantidad)
    btn_agregar.config(command=abrir_popup_cantidad)

    # --- LOGICA QUITAR DEL CARRITO ---
    def quitar_item_carrito_wrapper(event=None):
        seleccion = tabla_carrito.selection()
        if seleccion:
            tabla_carrito.delete(seleccion[0])
            actualizar_listado_busqueda(entry_buscar.get())
            
    tabla_carrito.bind("<Double-1>", quitar_item_carrito_wrapper)
    btn_quitar.config(command=quitar_item_carrito_wrapper)

    # --- EDITAR CANTIDAD CARRITO ---
    def editar_cantidad_carrito():
        seleccion = tabla_carrito.selection()
        if not seleccion: return
            
        item_c = tabla_carrito.item(seleccion[0])
        valores = item_c['values']
        item_id = valores[0]
        nombre_prod = valores[1]
        cant_actual = valores[2]

        popup = tk.Toplevel(ventana_root)
        popup.title("Editar Cantidad")
        popup.config(bg=color_primario)
        try:
            popup.iconbitmap(obtener_ruta_recurso("colmena.ico"))
        except: pass
        popup.resizable(False, False)
        centrar_ventana_interna(popup, 300, 150)
        
        tk.Label(popup, text=f"Producto: {nombre_prod}", bg=color_primario, fg="white", font=fuente_texto).pack(pady=(15, 10))
        
        frame_input = tk.Frame(popup, bg=color_primario)
        frame_input.pack(pady=5)
        tk.Label(frame_input, text="Cantidad:", bg=color_primario, fg="white", font=fuente_texto).pack(side="left", padx=5)
        
        entry_cant = ttk.Entry(frame_input, width=10, font=fuente_texto)
        entry_cant.insert(0, str(cant_actual))
        entry_cant.pack(side="left", padx=5)
        entry_cant.focus_set()
        entry_cant.select_range(0, tk.END)
        
        def on_confirm_edit():
            nueva_cant = entry_cant.get()
            if not nueva_cant or not nueva_cant.isdigit() or int(nueva_cant) <= 0: return
            
            tabla_carrito.item(seleccion[0], values=(item_id, nombre_prod, nueva_cant))
            popup.destroy()
            actualizar_listado_busqueda(entry_buscar.get())

        btn_ok = ttk.Button(popup, text="Confirmar", style="BotonSecundario.TButton", command=on_confirm_edit)
        btn_ok.pack(pady=15)
        popup.bind('<Return>', lambda e: on_confirm_edit())

    # MENU CONTEXTUAL
    menu_carrito = tk.Menu(ventana_root, tearoff=0)
    menu_carrito.add_command(label="Editar cant.", command=editar_cantidad_carrito) 
    menu_carrito.add_command(label="Eliminar", command=quitar_item_carrito_wrapper)

    def mostrar_menu_carrito(event):
        item = tabla_carrito.identify_row(event.y)
        if item:
            tabla_carrito.selection_set(item)
            menu_carrito.post(event.x_root, event.y_root)

    tabla_carrito.bind("<Button-3>", mostrar_menu_carrito)


def editar_operacion():
    global ventana_editar_operacion_instancia
    if ventana_editar_operacion_instancia is not None and ventana_editar_operacion_instancia.winfo_exists():
        ventana_editar_operacion_instancia.lift()
        return

    ventana_editar_operacion = tk.Toplevel()
    ventana_editar_operacion_instancia = ventana_editar_operacion

    ventana_editar_operacion.title("Editar operacion")
    ventana_editar_operacion.config(bg=color_primario)
    ventana_editar_operacion.resizable(False, False)
    try:
        ventana_editar_operacion.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass

    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana_interna(ventana_editar_operacion, ancho_ventana, alto_ventana)

    # Configuro el grid principal
    ventana_editar_operacion.grid_rowconfigure(0, weight=0)  # Header con título, observaciones, búsqueda y botones
    ventana_editar_operacion.grid_rowconfigure(1, weight=1)  # Tabla productos
    ventana_editar_operacion.grid_rowconfigure(2, weight=0)  # Botones finales
    ventana_editar_operacion.grid_columnconfigure(0, weight=1)

    # ==================== Configuro Frame Superior - Matriz 2x2 ====================
    frame_superior = tk.Frame(ventana_editar_operacion, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    # Configuro el grid del frame superior (2 columnas)
    frame_superior.grid_columnconfigure(0, weight=1)
    frame_superior.grid_columnconfigure(1, weight=1)

    # Fila 0, Columna 0 - Título
    label_titulo_tabla = tk.Label(frame_superior, text="Editar operación",
                                  font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo_tabla.grid(row=0, column=0, sticky="w", pady=(0, 15))

    # Fila 1, Columna 0 - Búsqueda
    frame_busqueda = tk.Frame(frame_superior, bg=color_primario)
    frame_busqueda.grid(row=1, column=0, sticky="w")

    label_buscar_producto = tk.Label(frame_busqueda, text="Buscar producto:",
                                     font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_buscar_producto.pack(side="left", padx=(0, 10))

    entry_buscar_producto = ttk.Entry(frame_busqueda, font=fuente_texto, width=30)
    entry_buscar_producto.pack(side="left")

    # Fila 1, Columna 1 - Botones Agregar/Quitar
    frame_botones_acciones = tk.Frame(frame_superior, bg=color_primario)
    frame_botones_acciones.grid(row=1, column=1, sticky="e")

    boton_agregar_producto = ttk.Button(frame_botones_acciones, text="Agregar", style="BotonSecundario.TButton")
    boton_agregar_producto.config(cursor="hand2")
    boton_agregar_producto.pack(side="left", padx=5)

    boton_quitar_producto = ttk.Button(frame_botones_acciones, text="Quitar", style="BotonSecundario.TButton")
    boton_quitar_producto.config(cursor="hand2")
    boton_quitar_producto.pack(side="left", padx=5)

    # ==================== Configuro Frame Tabla - Productos Agregados ====================
    frame_tabla = tk.Frame(ventana_editar_operacion, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 10))

    # Configuro el frame contenedor del Treeview
    frame_tree_container = tk.Frame(frame_tabla, bg=color_primario)
    frame_tree_container.pack(side="top", fill="both", expand=True)

    # Añado el scrollbar
    scrollbar_tabla = ttk.Scrollbar(frame_tree_container)
    scrollbar_tabla.pack(side="right", fill="y")

    # Configuro el Treeview - Tabla de productos
    columnas_productos = ("id", "nombre", "categoria", "precio", "cantidad")
    tabla_productos = ttk.Treeview(frame_tree_container, columns=columnas_productos,
                                   show="headings", yscrollcommand=scrollbar_tabla.set, height=10)

    # Configuro encabezados
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("precio", text="Precio")
    tabla_productos.heading("cantidad", text="Cantidad")

    # Configuro columnas
    tabla_productos.column("id", width=30, anchor="center")
    tabla_productos.column("nombre", width=200, anchor="w")
    tabla_productos.column("categoria", width=120, anchor="w")
    tabla_productos.column("precio", width=80, anchor="center")
    tabla_productos.column("cantidad", width=100, anchor="e")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.config(command=tabla_productos.yview)

    # ==================== Configuro Frame Botones Finales ====================
    frame_botones_finales = tk.Frame(ventana_editar_operacion, bg=color_primario)
    frame_botones_finales.grid(row=2, column=0, pady=(10, 20))

    # Botón Guardar
    boton_guardar = ttk.Button(frame_botones_finales, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2")
    boton_guardar.pack(side="left", padx=10)

    # Botón Cancelar
    boton_cancelar = ttk.Button(frame_botones_finales, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2",
                               command=ventana_editar_operacion.destroy)
    boton_cancelar.pack(side="left", padx=10)




def ver_detalle_operacion(id_operacion):
    from controller.operaciones_controlador import mostrar_operacion
    import datetime
    
    data = mostrar_operacion(id_operacion)
    if not data:
        return

    op = data['operacion']
    # op structure assumption based on existing code:
    # 0: id, 1: id_cliente, 2: fecha, 3: observaciones, 4: monto_total, 5: valor_dolar, 6: valor_kilo_miel, 7: metodo_de_pago
    
    op_id = op[0]
    fecha_val = op[2]
    
    if isinstance(fecha_val, str):
         fecha_str = fecha_val
    elif isinstance(fecha_val, datetime.date) or isinstance(fecha_val, datetime.datetime):
         fecha_str = fecha_val.strftime("%d/%m/%Y")
    else:
         fecha_str = str(fecha_val)
         
    obs = op[3] if len(op) > 3 else ""
    val_dolar = op[4] if len(op) > 4 else 0
    metodo_pago = op[5] if len(op) > 5 else "N/A"
    val_miel = op[6] if len(op) > 6 else 0
    # op[7] is monto_total

    ventana_detalle = tk.Toplevel()
    ventana_detalle.title(f"Detalle Operación #{id_operacion}")
    ventana_detalle.config(bg=color_primario)
    
    ancho_ventana = 800
    alto_ventana = 600
    centrar_ventana_interna(ventana_detalle, ancho_ventana, alto_ventana)
    
    try:
        ventana_detalle.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass

    # Main Layout
    ventana_detalle.grid_rowconfigure(0, weight=0) # Info Superior
    ventana_detalle.grid_rowconfigure(1, weight=1) # Table
    ventana_detalle.grid_rowconfigure(2, weight=0) # Bottom Spacer/Frame
    ventana_detalle.grid_columnconfigure(0, weight=1)

    # --- FRAME SUPERIOR ---
    frame_superior = tk.Frame(ventana_detalle, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
    
    # Styles
    estilo_lbl_titulo = {"font": ("Arial", 10, "bold"), "bg": color_primario, "fg": "white"}
    estilo_lbl_valor = {"font": ("Arial", 10), "bg": color_primario, "fg": "white"}

    # Grid Info
    # Row 0: ID | Fecha | Metodo Pago
    tk.Label(frame_superior, text="ID Operación:", **estilo_lbl_titulo).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame_superior, text=str(op_id), **estilo_lbl_valor).grid(row=0, column=1, sticky="w", padx=(0, 20), pady=5)

    tk.Label(frame_superior, text="Fecha:", **estilo_lbl_titulo).grid(row=0, column=2, sticky="w", padx=5, pady=5)
    tk.Label(frame_superior, text=fecha_str, **estilo_lbl_valor).grid(row=0, column=3, sticky="w", padx=(0, 20), pady=5)

    tk.Label(frame_superior, text="Método de Pago:", **estilo_lbl_titulo).grid(row=0, column=4, sticky="w", padx=5, pady=5)
    tk.Label(frame_superior, text=str(metodo_pago), **estilo_lbl_valor).grid(row=0, column=5, sticky="w", padx=5, pady=5)

    # Row 1: Valor Dolar | Valor Miel (Swapped with Observations)
    tk.Label(frame_superior, text="Valor Dólar:", **estilo_lbl_titulo).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame_superior, text=f"$ {val_dolar}", **estilo_lbl_valor).grid(row=1, column=1, sticky="w", padx=(0, 20), pady=5)
    
    tk.Label(frame_superior, text="Valor Kilo Miel:", **estilo_lbl_titulo).grid(row=1, column=2, sticky="w", padx=5, pady=5)
    tk.Label(frame_superior, text=f"$ {val_miel}", **estilo_lbl_valor).grid(row=1, column=3, sticky="w", padx=(0, 20), pady=5)

    # Row 2: Observaciones (Full Width)
    tk.Label(frame_superior, text="Observaciones:", **estilo_lbl_titulo).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    lbl_obs = tk.Label(frame_superior, text=str(obs), **estilo_lbl_valor, wraplength=600, justify="left")
    lbl_obs.grid(row=2, column=1, columnspan=5, sticky="w", padx=(0, 5), pady=5)

    # --- FRAME MEDIO (TABLA) ---
    frame_medio = tk.Frame(ventana_detalle, bg=color_primario)
    frame_medio.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
    
    # Scrollbar
    scrollbar_det = ttk.Scrollbar(frame_medio)
    scrollbar_det.pack(side="right", fill="y")
    
    # Treeview
    cols_det = ("id_prod", "nombre", "cantidad")
    tabla_detalles = ttk.Treeview(frame_medio, columns=cols_det, show="headings", yscrollcommand=scrollbar_det.set)
    
    tabla_detalles.heading("id_prod", text="ID Producto")
    tabla_detalles.heading("nombre", text="Nombre Producto")
    tabla_detalles.heading("cantidad", text="Cantidad")
    
    tabla_detalles.column("id_prod", width=80, anchor="center")
    tabla_detalles.column("nombre", width=300, anchor="w")
    tabla_detalles.column("cantidad", width=100, anchor="center")
    
    tabla_detalles.pack(side="left", fill="both", expand=True)
    scrollbar_det.config(command=tabla_detalles.yview)


    # --- FRAME INFERIOR (VACIO) ---
    frame_inferior = tk.Frame(ventana_detalle, bg=color_primario, height=50)
    frame_inferior.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
    # Placeholder vacío


if __name__ == "__main__":
    nueva_operacion()