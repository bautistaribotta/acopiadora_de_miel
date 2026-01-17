import tkinter as tk
from view.estilos import *
from tkinter import ttk
from controller.validaciones import *
from controller.productos_controlador import *

ventana_productos_instancia = None
ventana_nuevo_producto_instancia = None
ventana_editar_producto_instancia = None


def listado_productos():
    global ventana_productos_instancia
    if ventana_productos_instancia is not None and ventana_productos_instancia.winfo_exists():
        ventana_productos_instancia.lift()
        return

    ventana_productos = tk.Toplevel()
    ventana_productos_instancia = ventana_productos

    ventana_productos.title("Productos")
    ventana_productos.geometry("800x600+0+85")
    ventana_productos.resizable(False, False)
    ventana_productos.configure(bg=color_primario)
    try:
        ventana_productos.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass


    # Configuro el grid
    ventana_productos.grid_rowconfigure(0, weight=0)  # Buscador y Botones
    ventana_productos.grid_rowconfigure(1, weight=1)  # Tabla
    ventana_productos.grid_columnconfigure(0, weight=1)


    # Configuro el frame para la tabla
    frame_tabla = tk.Frame(ventana_productos, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # Añado el scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")


    # Configuro el Treeview (Tabla)
    columnas = ("id", "nombre", "categoria", "precio", "cantidad")
    tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                   yscrollcommand=scrollbar.set, height=20)
    tabla_productos.tag_configure("impar", background=color_zebra)

    # Defino la función para actualizar la tabla (Treeview)
    def actualizar_tabla():
        # Limpio la tabla
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)
        # Vuelvo a escribirla actualizada
        productos = listar_productos_controlador()
        for i, prod in enumerate(productos):
            # Convierto a lista para modificar visualmente el precio sin afectar datos reales
            datos_visuales = list(prod)
            datos_visuales[3] = f"${datos_visuales[3]}"
            try:
                datos_visuales[4] = int(float(datos_visuales[4]))
            except (ValueError, TypeError):
                pass
            tag = "impar" if i % 2 != 0 else "par"
            tabla_productos.insert("", "end", values=datos_visuales, tags=(tag,))
    actualizar_tabla()


    # Defino la función para eliminar un producto
    def ejecutar_eliminacion():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.",
                                   parent=ventana_productos)
            return

        # Obtengo el ID del ítem seleccionado (columna 0) y el nombre (columna 1)
        valores = tabla_productos.item(seleccion[0])['values']
        item_id = valores[0]
        nombre_producto = valores[1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar '{nombre_producto}'?",
                                        parent=ventana_productos)
        if confirmar:
            if eliminar_producto_controlador(item_id, ventana_productos):
                actualizar_tabla()


    # Defino la función para buscar productos
    def filtrar_tabla(event):
        texto_busqueda = entry_buscar.get()

        if event == "":
            actualizar_tabla()
            return

        productos_encontrados = buscador_productos_controlador(texto_busqueda)

        # Limpio la tabla actual
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)

        # Lleno la tabla con los resultados
        for i, producto in enumerate(productos_encontrados):
            datos_visuales = list(producto)
            datos_visuales[3] = f"${datos_visuales[3]}"
            try:
                datos_visuales[4] = int(float(datos_visuales[4]))
            except (ValueError, TypeError):
                pass
            tag = "impar" if i % 2 != 0 else "par"
            tabla_productos.insert("", "end", values=datos_visuales, tags=(tag,))



    # Defino la función para abrir la edición
    def abrir_editar():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para editar.",
                                   parent=ventana_productos)
            return

        # Obtengo el ID del ítem seleccionado (columna 0)
        item_id = tabla_productos.item(seleccion[0])['values'][0]
        editar_producto_vista(item_id, actualizar_tabla)


    # Defino la función para abrir la edición de stock
    def abrir_editar_stock():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto.", parent=ventana_productos)
            return

        # Obtengo el ID del ítem seleccionado
        valores = tabla_productos.item(seleccion[0])['values']
        item_id = valores[0]
        nombre_producto = valores[1]
        
        modificar_stock_vista(item_id, nombre_producto, actualizar_tabla)


    # Configuro el menú contextual (Clic derecho)
    menu_contextual = tk.Menu(ventana_productos, tearoff=0)
    menu_contextual.add_command(label="Editar stock", command=abrir_editar_stock)
    menu_contextual.add_separator()
    menu_contextual.add_command(label="Editar", command=abrir_editar)
    menu_contextual.add_command(label="Eliminar", command=ejecutar_eliminacion)


    def mostrar_menu(event):
        item = tabla_productos.identify_row(event.y)
        if item:
            tabla_productos.selection_set(item)
            menu_contextual.post(event.x_root, event.y_root)


    # Defino la función para ordenar columnas
    def ordenar_por_columna(tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        # Intento convertir a int para ordenar numéricamente
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # Reordeno los ítems
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Actualizo el comando para invertir el orden en el próximo clic
        tree.heading(col, command=lambda: ordenar_por_columna(tree, col, not reverse))

    # Configuro las columnas de la tabla
    tabla_productos.heading("id", text="ID", command=lambda: ordenar_por_columna(tabla_productos, "id", False))
    tabla_productos.heading("nombre", text="Nombre", command=lambda: ordenar_por_columna(tabla_productos, "nombre", False))
    tabla_productos.heading("categoria", text="Categoría", command=lambda: ordenar_por_columna(tabla_productos, "categoria", False))
    tabla_productos.heading("precio", text="Precio")
    tabla_productos.heading("cantidad", text="Stock")

    tabla_productos.column("id", width=80, anchor="center")
    tabla_productos.column("nombre", width=250, anchor="w")
    tabla_productos.column("categoria", width=200, anchor="center")
    tabla_productos.column("precio", width=100, anchor="center")
    tabla_productos.column("cantidad", width=100, anchor="center")

    tabla_productos.pack(side="left", fill="both", expand=True)
    tabla_productos.bind("<Button-3>", mostrar_menu)
    scrollbar.config(command=tabla_productos.yview)


    # Configuro el frame superior - Buscador y Botones
    frame_superior = tk.Frame(ventana_productos, bg=color_primario)
    frame_superior.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

    # Configuro el buscador
    label_buscar = tk.Label(frame_superior, text="Buscar:")
    label_buscar.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_buscar.pack(side="left", padx=(0, 10))

    entry_buscar = ttk.Entry(frame_superior, font=fuente_texto, width=25)
    entry_buscar.bind("<KeyRelease>", filtrar_tabla)
    entry_buscar.pack(side="left")

    # Configuro los botones
    boton_eliminar = ttk.Button(frame_superior, text="Eliminar", style="BotonSecundario.TButton")
    boton_eliminar.config(cursor="hand2", command=ejecutar_eliminacion)
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = ttk.Button(frame_superior, text="Editar", style="BotonSecundario.TButton")
    boton_editar.config(command=abrir_editar, cursor="hand2")
    boton_editar.pack(side="right", padx=5)

    boton_nuevo_producto = ttk.Button(frame_superior, text="Nuevo", style="BotonSecundario.TButton")
    boton_nuevo_producto.config(command=lambda: nuevo_producto_vista(actualizar_tabla), cursor="hand2")
    boton_nuevo_producto.pack(side="right", padx=5)


def nuevo_producto_vista(callback):
    global ventana_nuevo_producto_instancia
    if ventana_nuevo_producto_instancia is not None and ventana_nuevo_producto_instancia.winfo_exists():
        ventana_nuevo_producto_instancia.lift()
        return

    ventana_nuevo_producto = tk.Toplevel()
    ventana_nuevo_producto_instancia = ventana_nuevo_producto

    ventana_nuevo_producto.title("Nuevo producto")
    ventana_nuevo_producto.configure(bg=color_primario)
    ventana_nuevo_producto.geometry("400x600+850+85")
    ventana_nuevo_producto.resizable(False, False)
    try:
        ventana_nuevo_producto.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass


    # Configuro el grid
    ventana_nuevo_producto.grid_columnconfigure(0, weight=1)
    ventana_nuevo_producto.grid_columnconfigure(1, weight=2)


    # Añado el título
    label_titulo = tk.Label(ventana_nuevo_producto, text="REGISTRAR PRODUCTO")
    label_titulo.config(bg=color_primario, fg=color_secundario, font=fuente_titulos)
    label_titulo.grid(row=0, column=0, columnspan=2, padx=20 ,pady=(50, 40))


    # NOMBRE
    label_nombre = tk.Label(ventana_nuevo_producto, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = tk.Entry(ventana_nuevo_producto, font=fuente_texto, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # Configuro categoría y menú desplegable
    label_categoria = tk.Label(ventana_nuevo_producto, text="Categoria:")
    label_categoria.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_categoria.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)

    lista_categorias = ["Alimento", "Cera", "Estampa", "Insumos", "Madera", "Medicamentos", "Miel", "Otros"]
    combobox_categoria = ttk.Combobox(ventana_nuevo_producto)
    combobox_categoria.config(font=fuente_texto, values=lista_categorias, state="readonly")
    combobox_categoria.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=10)


    # UNIDAD DE MEDIDA
    label_unidad_medida = tk.Label(ventana_nuevo_producto, text="Unidad de medida:")
    label_unidad_medida.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_unidad_medida.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    lista_unidad_medidas = ["Unidades", "Kilos", "Litros"]
    combobox_unidad_medida = ttk.Combobox(ventana_nuevo_producto)
    combobox_unidad_medida.config(font=fuente_texto, values=lista_unidad_medidas, state="readonly")
    combobox_unidad_medida.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=10)


    # PRECIO
    cmd_validar_precio = ventana_nuevo_producto.register(validar_solo_numeros_punto)

    label_precio = tk.Label(ventana_nuevo_producto, text="Precio por unidad:")
    label_precio.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_precio.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_precio = tk.Entry(ventana_nuevo_producto, font=fuente_texto, width=20)
    entry_precio.config(validate="key", validatecommand=(cmd_validar_precio, '%P'))
    entry_precio.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CANTIDAD
    cmd_validar_numeros_punto = ventana_nuevo_producto.register(validar_solo_numeros_punto)

    label_cantidad = tk.Label(ventana_nuevo_producto, text="Cantidad:")
    label_cantidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_cantidad.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_cantidad = tk.Entry(ventana_nuevo_producto, font=fuente_texto, width=20)
    entry_cantidad.config(validate="key", validatecommand=(cmd_validar_numeros_punto, '%P'))
    entry_cantidad.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    def realizar_guardado():
        nuevo_producto_controlador(
            entry_nombre.get(),
            combobox_categoria.get(),
            combobox_unidad_medida.get(),
            entry_precio.get(),
            entry_cantidad.get(),
            ventana_nuevo_producto,
            callback
        )


    # Configuro el frame de botones
    frame_botones = tk.Frame(ventana_nuevo_producto)
    frame_botones.config(bg=color_primario, height= 20)
    frame_botones.grid(row=9, column=0, columnspan=2, pady=30)


    # Agrego los botones
    boton_guardar = ttk.Button(frame_botones, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2", command=realizar_guardado)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = ttk.Button(frame_botones, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2", command=ventana_nuevo_producto.destroy)
    boton_cancelar.pack(side="left", padx=5)


def editar_producto_vista(id_producto, callback=None):
    global ventana_editar_producto_instancia
    if ventana_editar_producto_instancia is not None and ventana_editar_producto_instancia.winfo_exists():
        ventana_editar_producto_instancia.lift()
        return

    ventana_editar_producto = tk.Toplevel()
    ventana_editar_producto_instancia = ventana_editar_producto

    ventana_editar_producto.title("Editar producto")
    ventana_editar_producto.configure(bg=color_primario)
    ventana_editar_producto.geometry("400x600+850+85")
    ventana_editar_producto.resizable(False, False)
    try:
        ventana_editar_producto.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass


    # Configuro el grid
    ventana_editar_producto.grid_columnconfigure(0, weight=1)
    ventana_editar_producto.grid_columnconfigure(1, weight=2)


    # Añado el título
    label_titulo = tk.Label(ventana_editar_producto, text="EDITAR PRODUCTO")
    label_titulo.config(bg=color_primario, fg=color_secundario, font=fuente_titulos)
    label_titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=(50, 40))

    # Busco los datos
    producto_a_editar = informacion_producto_controlador(id_producto)

    # NOMBRE
    label_nombre = tk.Label(ventana_editar_producto, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_nombre.insert(0, producto_a_editar.nombre)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # Configuro categoría y menú desplegable
    label_categoria = tk.Label(ventana_editar_producto, text="Categoria:")
    label_categoria.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_categoria.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)


    # ---------------- Faltan más categorías ----------------
    lista_categorias = ["Alimento", "Cera", "Estampa", "Insumos", "Madera", "Medicamentos", "Miel", "Otros"]
    combobox_categoria = ttk.Combobox(ventana_editar_producto)
    combobox_categoria.config(font=fuente_texto, values=lista_categorias, state="readonly")
    combobox_categoria.set(producto_a_editar.categoria)
    combobox_categoria.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=10)


    # UNIDAD DE MEDIDA
    label_unidad_medida = tk.Label(ventana_editar_producto, text="Unidad de medida:")
    label_unidad_medida.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_unidad_medida.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    lista_unidad_medidas = ["Unidades", "Kilos", "Litros"]
    combobox_unidad_medida = ttk.Combobox(ventana_editar_producto)
    combobox_unidad_medida.config(font=fuente_texto, values=lista_unidad_medidas, state="readonly")
    combobox_unidad_medida.set(producto_a_editar.unidad_medida)
    combobox_unidad_medida.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=10)


    # PRECIO
    cmd_validar_precio = ventana_editar_producto.register(validar_solo_numeros_punto)

    label_precio = tk.Label(ventana_editar_producto, text="Precio por unidad:")
    label_precio.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_precio.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_precio = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_precio.config(validate="key", validatecommand=(cmd_validar_precio, '%P'))
    entry_precio.insert(0, str(producto_a_editar.precio))
    entry_precio.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CANTIDAD
    cmd_validar_numeros_punto = ventana_editar_producto.register(validar_solo_numeros_punto)

    label_cantidad = tk.Label(ventana_editar_producto, text="Cantidad:")
    label_cantidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_cantidad.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_cantidad = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_cantidad.config(validate="key", validatecommand=(cmd_validar_numeros_punto, '%P'))
    entry_cantidad.insert(0, str(producto_a_editar.cantidad))
    entry_cantidad.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # Capturo los datos editados
    def capturar_datos_edicion():
        editar_producto_controlador(
            id_producto,
            entry_nombre.get(),
            combobox_categoria.get(),
            combobox_unidad_medida.get(),
            entry_precio.get(),
            entry_cantidad.get(),
            ventana_editar_producto,
            callback
        )


    # Configuro el frame de botones
    frame_botones = tk.Frame(ventana_editar_producto)
    frame_botones.config(bg=color_primario, height=20)
    frame_botones.grid(row=9, column=0, columnspan=2, pady=30)


    # Agrego los botones
    boton_guardar = ttk.Button(frame_botones, text="Guardar", style="BotonSecundario.TButton")
    boton_guardar.config(cursor="hand2", command=capturar_datos_edicion)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = ttk.Button(frame_botones, text="Cancelar", style="BotonSecundario.TButton")
    boton_cancelar.config(cursor="hand2", command=ventana_editar_producto.destroy)
    boton_cancelar.pack(side="left", padx=5)


if __name__ == "__main__":
    listado_productos()


def modificar_stock_vista(id_producto, nombre_producto, callback=None):
    ventana_stock = tk.Toplevel()
    ventana_stock.title("Editar Stock")
    ventana_stock.config(bg=color_primario)
    ventana_stock.geometry("300x200")
    centrar_ventana_interna(ventana_stock, 300, 200)
    ventana_stock.resizable(False, False)
    
    # Label Titulo
    tk.Label(ventana_stock, text=f"Producto: {nombre_producto}", 
             font=("Arial", 12, "bold"), bg=color_primario, fg=color_secundario).pack(pady=(20, 10))
    
    # Entry Cantidad
    frame_entry = tk.Frame(ventana_stock, bg=color_primario)
    frame_entry.pack(pady=10)
    
    # Label explicativo
    tk.Label(frame_entry, text="Cantidad (+/-):", font=("Arial", 10), bg=color_primario, fg="white").pack(side="left", padx=5)
    
    entry_cantidad = ttk.Entry(frame_entry, width=10, font=("Arial", 12))
    entry_cantidad.pack(side="left", padx=5)
    entry_cantidad.focus_set() # Foco automatico
    
    def confirmar(event=None):
        cantidad = entry_cantidad.get()
        sumar_stock_controlador(id_producto, cantidad, ventana_stock, callback)
        
    # Bind Enter key
    ventana_stock.bind('<Return>', confirmar)
    
    # Boton Confirmar
    btn_confirmar = ttk.Button(ventana_stock, text="Confirmar", style="BotonSecundario.TButton", command=confirmar)
    btn_confirmar.pack(pady=10)