import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from estilos import *

ventana_nueva_operacion_instancia = None
ventana_editar_operacion_instancia = None


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
    ventana_nueva_operacion.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")

    # Aumentamos tamaño para layout dividido
    ancho_ventana = 1200
    alto_ventana = 600
    centrar_ventana_interna(ventana_nueva_operacion, ancho_ventana, alto_ventana)

    # LAYOUT PRINCIPAL: 2 Columnas (Izquierda: Buscador/Seleccion, Derecha: Carrito/Totales)
    ventana_nueva_operacion.grid_columnconfigure(0, weight=1) # Left
    ventana_nueva_operacion.grid_columnconfigure(1, weight=1) # Right
    ventana_nueva_operacion.grid_rowconfigure(0, weight=1) # Main Content
    ventana_nueva_operacion.grid_rowconfigure(1, weight=0) # Bottom Actions

    # ========================== COLUMNA IZQUIERDA: BUSCADOR DE PRODUCTOS ==========================
    frame_izq = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_izq.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    # Buscador (Altura controlada para alinear con columna derecha)
    frame_search = tk.Frame(frame_izq, bg=color_primario)
    frame_search.pack(fill="x", pady=(10, 20)) # Padding aumentado
    
    label_buscar = tk.Label(frame_search, text="Buscar:", font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = ttk.Entry(frame_search, font=fuente_texto, width=25) # Ancho reducido
    entry_buscar.pack(side="left")

    # CREAMOS PRIMERO LA TABLA Y EL POPUP PARA PODER USARLAS
    # PERO NO LAS EMPAQUETAMOS TODAVIA
    frame_tabla_busqueda = tk.Frame(frame_izq, bg=color_primario)
    # Empaquetado diferido...

    scrollbar_busqueda = ttk.Scrollbar(frame_tabla_busqueda)
    scrollbar_busqueda.pack(side="right", fill="y")
    
    cols_busqueda = ("id", "nombre", "stock", "precio")
    tabla_busqueda = ttk.Treeview(frame_tabla_busqueda, columns=cols_busqueda, show="headings", 
                                  yscrollcommand=scrollbar_busqueda.set, height=15)
    
    tabla_busqueda.heading("id", text="ID")
    tabla_busqueda.heading("nombre", text="Nombre")
    tabla_busqueda.heading("stock", text="Stock")
    tabla_busqueda.heading("precio", text="Precio")
    
    tabla_busqueda.column("id", width=50, anchor="center")
    tabla_busqueda.column("nombre", width=200, anchor="center")
    tabla_busqueda.column("stock", width=80, anchor="center")
    tabla_busqueda.column("precio", width=80, anchor="center")
    
    tabla_busqueda.pack(side="left", fill="both", expand=True)
    scrollbar_busqueda.config(command=tabla_busqueda.yview)

    # ----------------------------------------------------------------------------------
    # --- LOGICA DE ACTUALIZACION DE STOCK VISUAL ---
    # ----------------------------------------------------------------------------------
    from controller.productos_controlador import buscador_productos_controlador

    def obtener_cantidades_carrito():
        """Retorna un diccionario {id_producto: cantidad_en_carrito}"""
        cantidades = {}
        for item in tabla_carrito.get_children():
            valores = tabla_carrito.item(item)['values']
            # valores ahorea seran (id, nombre, cantidad)
            try:
                item_id = valores[0]
                cantidad = int(valores[2])
            except:
                continue
            
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
                stock_visual = int(float(p_stock_real) - en_carrito.get(p_id, 0))
            except:
                stock_visual = 0

            # La tabla espera: (id, nombre, stock, precio)
            valores_mostrar = (p_id, p_nombre, stock_visual, f"${p_precio}")
            tabla_busqueda.insert("", "end", values=valores_mostrar)

    def on_buscar_keyrelease(event):
        actualizar_listado_busqueda(entry_buscar.get())
        
    # Vincular evento de busqueda
    entry_buscar.bind("<KeyRelease>", on_buscar_keyrelease)
    
    # Cargar todos al inicio (diferido para que tabla_carrito exista)
    ventana_nueva_operacion.after(100, lambda: actualizar_listado_busqueda(""))


    # --- FUNCIONES POPUP CANTIDAD ---
    def confirmar_agregar(cantidad, valores_producto, ventana_popup):
        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            return 
        
        id_prod = valores_producto[0]
        nombre = valores_producto[1] 
        cant_nueva = int(cantidad)
        
        # Verificar si ya existe en el carrito para sumar
        item_existente = None
        cant_actual = 0
        
        for item in tabla_carrito.get_children():
            vals = tabla_carrito.item(item)['values']
            # vals = (id, nombre, cantidad)
            if str(vals[0]) == str(id_prod):
                item_existente = item
                cant_actual = int(vals[2])
                break
        
        if item_existente:
            # Actualizar existente
            nueva_total = cant_actual + cant_nueva
            tabla_carrito.item(item_existente, values=(id_prod, nombre, nueva_total))
        else:
            # Insertar nuevo
            tabla_carrito.insert("", "end", values=(id_prod, nombre, cant_nueva))
            
        ventana_popup.destroy()
        
        # ACTUALIZAR STOCK VISUAL
        actualizar_listado_busqueda(entry_buscar.get())

    def abrir_popup_cantidad(event=None):
        seleccion = tabla_busqueda.selection()
        if not seleccion:
            return
        
        valores = tabla_busqueda.item(seleccion[0])['values']
        # valores = [id, nombre, stock, precio]
        
        popup = tk.Toplevel(ventana_nueva_operacion)
        popup.title("Cantidad")
        popup.config(bg=color_primario)
        popup.resizable(False, False)
        try:
            popup.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")
        except: pass
        centrar_ventana_interna(popup, 300, 150)
        
        tk.Label(popup, text=f"Producto: {valores[1]}", bg=color_primario, fg="white", font=fuente_texto).pack(pady=(15, 10))
        
        # Frame para alinear label y entry horizontalmente
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

    # Vincular doble click
    tabla_busqueda.bind("<Double-1>", abrir_popup_cantidad)


    # AHORA SI: FRAME AGREGAR (Boton) AL FINAL DEL FRAME IZQ
    # Lo empaquetamos con side="bottom" para que quede clavado abajo
    frame_agregar = tk.Frame(frame_izq, bg=color_primario)
    frame_agregar.pack(side="bottom", fill="x", pady=15)
    
    # Cargar icono carrito
    img_carrito = Image.open(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\carrito.ico")
    img_carrito = img_carrito.resize((20, 20))
    icono_carrito = ImageTk.PhotoImage(img_carrito)

    btn_agregar = ttk.Button(frame_agregar, image=icono_carrito, text=" Agregar al carrito", compound="left", style="BotonSecundario.TButton")
    btn_agregar.image = icono_carrito 
    btn_agregar.config(cursor="hand2", command=abrir_popup_cantidad)
    # Sin padding horizontal extra para que alinee con el borde de la tabla
    btn_agregar.pack(side="left")


    # FINALMENTE EMPAQUETAMOS LA TABLA PARA QUE OCUPE EL ESPACIO RESTANTE
    frame_tabla_busqueda.pack(fill="both", expand=True)


    # ========================== COLUMNA DERECHA: DETALLE OPERACION (CARRITO) ==========================
    frame_der = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Header Derecho (Alineado con el Buscador de la izquierda)
    frame_header_der = tk.Frame(frame_der, bg=color_primario)
    frame_header_der.pack(fill="x", pady=(10, 20)) # Mismo padding que search bar izquierda
    
    # Titulo centrado
    tk.Label(frame_header_der, text="Listado de compra", font=fuente_titulos, bg=color_primario, fg=color_secundario).pack(anchor="center")

    # Botones y Totales del Carrito (LO CREAMOS Y EMPAQUETAMOS ABAJO PRIMERO)
    frame_acciones_carrito = tk.Frame(frame_der, bg=color_primario)
    frame_acciones_carrito.pack(side="bottom", fill="x", pady=15) # Padding 15 para igualar al lado izquierdo

    # Funcion Quitar del carrito
    def quitar_item_carrito(event=None):
        seleccion = tabla_carrito.selection()
        if seleccion:
            tabla_carrito.delete(seleccion[0])

    # Cargar icono tacho
    img_tacho = Image.open(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\tacho.ico")
    img_tacho = img_tacho.resize((20, 20))
    icono_tacho = ImageTk.PhotoImage(img_tacho)
    
    # Boton Eliminar (Derecha)
    btn_quitar = ttk.Button(frame_acciones_carrito, image=icono_tacho, style="BotonSecundario.TButton")
    btn_quitar.image = icono_tacho 
    btn_quitar.config(cursor="hand2", command=quitar_item_carrito)
    btn_quitar.pack(side="right", padx=(10, 0))

    # Total (A la izquierda del boton)
    # Packeamos de derecha a izquierda: Primero el valor, luego la etiqueta
    lbl_total_pesos = tk.Label(frame_acciones_carrito, text="$ 0.00", bg=color_primario, fg="white", font=("Arial", 12, "bold"))
    lbl_total_pesos.pack(side="right", padx=(5, 0))
    
    tk.Label(frame_acciones_carrito, text="Total:", bg=color_primario, fg="white", font=("Arial", 12)).pack(side="right")


    # Tabla Carrito (AHORA SI EMPAQUETAMOS PARA LLENAR EL CENTRO)
    frame_tabla_carrito = tk.Frame(frame_der, bg=color_primario)
    frame_tabla_carrito.pack(fill="both", expand=True)

    scrollbar_carrito = ttk.Scrollbar(frame_tabla_carrito)
    scrollbar_carrito.pack(side="right", fill="y")
    
    # Agregamos ID a las columnas pero definimos cuales mostrar
    cols_carrito = ("id", "nombre", "cantidad")
    tabla_carrito = ttk.Treeview(frame_tabla_carrito, columns=cols_carrito, show="headings", 
                                 yscrollcommand=scrollbar_carrito.set, height=15)
    
    # Configuramos para mostrar solo nombre y cantidad
    tabla_carrito["displaycolumns"] = ("nombre", "cantidad")
    
    tabla_carrito.heading("nombre", text="Producto")
    tabla_carrito.heading("cantidad", text="Cant.")
    
    tabla_carrito.column("nombre", width=200, anchor="w") 
    tabla_carrito.column("cantidad", width=30, anchor="center") 
    
    tabla_carrito.pack(side="left", fill="both", expand=True)
    
    # ----------------------------------------------------
    # ACTUALIZAR LOGICA QUITAR PARA REFRESCAR LISTA IZQ
    # ----------------------------------------------------
    def quitar_item_carrito_wrapper(event=None):
        seleccion = tabla_carrito.selection()
        if seleccion:
            tabla_carrito.delete(seleccion[0])
            actualizar_listado_busqueda(entry_buscar.get()) # Refrescar lista productos para devolver stock visual
            
    tabla_carrito.bind("<Double-1>", quitar_item_carrito_wrapper)
    btn_quitar.config(command=quitar_item_carrito_wrapper) # Re-vincular boton
    
    scrollbar_carrito.config(command=tabla_carrito.yview)

    # FUNCION EDITAR CANTIDAD CARRITO
    def editar_cantidad_carrito():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            return
            
        item_c = tabla_carrito.item(seleccion[0])
        valores = item_c['values']
        # valores = (id, nombre, cantidad)
        item_id = valores[0]
        nombre_prod = valores[1]
        cant_actual = valores[2]

        popup = tk.Toplevel(ventana_nueva_operacion)
        popup.title("Editar Cantidad")
        popup.config(bg=color_primario)
        try:
            popup.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")
        except: pass
        popup.resizable(False, False)
        centrar_ventana_interna(popup, 300, 150)
        
        tk.Label(popup, text=f"Producto: {nombre_prod}", bg=color_primario, fg="white", font=fuente_texto).pack(pady=(15, 10))
        
        frame_input = tk.Frame(popup, bg=color_primario)
        frame_input.pack(pady=5)

        tk.Label(frame_input, text="Cantidad:", bg=color_primario, fg="white", font=fuente_texto).pack(side="left", padx=5)
        
        entry_cant = ttk.Entry(frame_input, width=10, font=fuente_texto)
        entry_cant.insert(0, str(cant_actual)) # Pre-llenar valor actual
        entry_cant.pack(side="left", padx=5)
        entry_cant.focus_set()
        entry_cant.select_range(0, tk.END) # Seleccionar todo para facilitar edicion rapida
        
        def on_confirm_edit():
            nueva_cant = entry_cant.get()
            if not nueva_cant or not nueva_cant.isdigit() or int(nueva_cant) <= 0:
                return
            
            # Actualizar fila carrito
            tabla_carrito.item(seleccion[0], values=(item_id, nombre_prod, nueva_cant))
            popup.destroy()
            
            # Actualizar stock visual (ahora resta la nueva cantidad)
            actualizar_listado_busqueda(entry_buscar.get())

        btn_ok = ttk.Button(popup, text="Confirmar", style="BotonSecundario.TButton", command=on_confirm_edit)
        btn_ok.pack(pady=15)
        
        popup.bind('<Return>', lambda e: on_confirm_edit())


    # MENU CONTEXTUAL CARRITO
    menu_carrito = tk.Menu(ventana_nueva_operacion, tearoff=0)
    menu_carrito.add_command(label="Editar cant.", command=editar_cantidad_carrito) 
    menu_carrito.add_command(label="Eliminar", command=quitar_item_carrito_wrapper)

    def mostrar_menu_carrito(event):
        item = tabla_carrito.identify_row(event.y)
        if item:
            tabla_carrito.selection_set(item)
            menu_carrito.post(event.x_root, event.y_root)

    tabla_carrito.bind("<Button-3>", mostrar_menu_carrito)


    # ========================== FRAME INFERIOR: ACCIONES FINALES ==========================
    frame_final = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_final.grid(row=1, column=0, columnspan=2, pady=20)

    btn_guardar_remito = ttk.Button(frame_final, text="Guardar y Remito", style="BotonSecundario.TButton")
    btn_guardar_remito.config(cursor="hand2", width=20) # Debe ser mas ancho por el texto
    btn_guardar_remito.pack(side="left", padx=10)
    
    btn_cancelar_op = ttk.Button(frame_final, text="Cancelar", style="BotonSecundario.TButton")
    btn_cancelar_op.config(cursor="hand2", width=8, command=ventana_nueva_operacion.destroy)
    btn_cancelar_op.pack(side="left", padx=10)


def editar_operacion():
    global ventana_editar_operacion_instancia
    if ventana_editar_operacion_instancia is not None and ventana_editar_operacion_instancia.winfo_exists():
        ventana_editar_operacion_instancia.lift()
        return

    ventana_nueva_operacion = tk.Toplevel()
    ventana_editar_operacion_instancia = ventana_nueva_operacion

    ventana_nueva_operacion.title("Editar operacion")
    ventana_nueva_operacion.config(bg=color_primario)
    ventana_nueva_operacion.resizable(False, False)
    ventana_nueva_operacion.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")

    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana_interna(ventana_nueva_operacion, ancho_ventana, alto_ventana)

    # CONFIGURACIÓN DEL GRID PRINCIPAL
    ventana_nueva_operacion.grid_rowconfigure(0, weight=0)  # Header con título, observaciones, búsqueda y botones
    ventana_nueva_operacion.grid_rowconfigure(1, weight=1)  # Tabla productos
    ventana_nueva_operacion.grid_rowconfigure(2, weight=0)  # Botones finales
    ventana_nueva_operacion.grid_columnconfigure(0, weight=1)

    # ==================== FRAME SUPERIOR - MATRIZ 2x2 ====================
    frame_superior = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    # Configurar grid del frame superior (2 columnas)
    frame_superior.grid_columnconfigure(0, weight=1)
    frame_superior.grid_columnconfigure(1, weight=1)

    # FILA 0, COLUMNA 0 - TÍTULO
    label_titulo_tabla = tk.Label(frame_superior, text="Nueva operacion",
                                  font=fuente_titulos, bg=color_primario, fg=color_secundario)
    label_titulo_tabla.grid(row=0, column=0, sticky="w", pady=(0, 15))

    # FILA 1, COLUMNA 0 - BÚSQUEDA
    frame_busqueda = tk.Frame(frame_superior, bg=color_primario)
    frame_busqueda.grid(row=1, column=0, sticky="w")

    label_buscar_producto = tk.Label(frame_busqueda, text="Buscar producto:",
                                     font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_buscar_producto.pack(side="left", padx=(0, 10))

    entry_buscar_producto = ttk.Entry(frame_busqueda, font=fuente_texto, width=30)
    entry_buscar_producto.pack(side="left")

    # FILA 1, COLUMNA 1 - BOTONES AGREGAR/QUITAR
    frame_botones_acciones = tk.Frame(frame_superior, bg=color_primario)
    frame_botones_acciones.grid(row=1, column=1, sticky="e")

    boton_agregar_producto = ttk.Button(frame_botones_acciones, text="Agregar", style="BotonSecundario.TButton")
    boton_agregar_producto.config(cursor="hand2")
    boton_agregar_producto.pack(side="left", padx=5)

    boton_quitar_producto = ttk.Button(frame_botones_acciones, text="Quitar", style="BotonSecundario.TButton")
    boton_quitar_producto.config(cursor="hand2")
    boton_quitar_producto.pack(side="left", padx=5)

    # ==================== FRAME TABLA - PRODUCTOS AGREGADOS ====================
    frame_tabla = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 10))

    # Frame contenedor del Treeview
    frame_tree_container = tk.Frame(frame_tabla, bg=color_primario)
    frame_tree_container.pack(side="top", fill="both", expand=True)

    # Scrollbar
    scrollbar_tabla = ttk.Scrollbar(frame_tree_container)
    scrollbar_tabla.pack(side="right", fill="y")

    # Treeview - Tabla de productos
    columnas_productos = ("id", "nombre", "categoria", "precio", "cantidad")
    tabla_productos = ttk.Treeview(frame_tree_container, columns=columnas_productos,
                                   show="headings", yscrollcommand=scrollbar_tabla.set, height=10)

    # Configurar encabezados
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("precio", text="Precio")
    tabla_productos.heading("cantidad", text="Cantidad")

    # Configurar columnas
    tabla_productos.column("id", width=30, anchor="center")
    tabla_productos.column("nombre", width=200, anchor="w")
    tabla_productos.column("categoria", width=120, anchor="w")
    tabla_productos.column("precio", width=80, anchor="center")
    tabla_productos.column("cantidad", width=100, anchor="e")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.config(command=tabla_productos.yview)

    # ==================== FRAME BOTONES FINALES ====================
    frame_botones_finales = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_botones_finales.grid(row=2, column=0, pady=(10, 20))

    # Botón Guardar
    boton_guardar = ttk.Button(frame_botones_finales, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2")
    boton_guardar.pack(side="left", padx=10)

    # Botón Cancelar
    boton_cancelar = ttk.Button(frame_botones_finales, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2",
                               command=ventana_nueva_operacion.destroy)
    boton_cancelar.pack(side="left", padx=10)


if __name__ == "__main__":
    nueva_operacion()