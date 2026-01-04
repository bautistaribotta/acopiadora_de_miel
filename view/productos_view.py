from tkinter import ttk
from controller.productos_controlador import listar_productos_controlador, nuevo_producto_controlador, eliminar_producto_controlador
from estilos_view import *
from controller.validaciones import *
import tkinter as tk


def listado_productos():
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
    label_buscar = tk.Label(frame_superior, text="Buscar:")
    label_buscar.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_buscar.pack(side="left", padx=(0, 10))

    entry_buscar = ttk.Entry(frame_superior, font=fuente_texto, width=25)
    entry_buscar.pack(side="left")


    # BOTONES
    boton_eliminar = tk.Button(frame_superior, text="Eliminar", font=fuente_texto)
    boton_eliminar.config(bg=color_secundario, fg=color_primario, width=10,
                          cursor="hand2", command=ejecutar_eliminacion)
    boton_eliminar.pack(side="right", padx=(5, 0))

    boton_editar = tk.Button(frame_superior, text="Editar", font=fuente_texto)
    boton_editar.config(bg=color_secundario, fg=color_primario, width=10, command=editar_producto, cursor="hand2")
    boton_editar.pack(side="right", padx=5)

    boton_agregar = tk.Button(frame_superior, text="Añadir", font=fuente_texto)
    boton_agregar.config(bg=color_secundario, fg=color_primario, width=10,
                        command=lambda: nuevo_producto(actualizar_tabla), cursor="hand2")
    boton_agregar.pack(side="right", padx=5)


    # FRAME TABLA
    frame_tabla = tk.Frame(ventana_productos, bg=color_primario)
    frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # SCROLLBAR
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")


    # TREEVIEW (TABLA)
    columnas = ("id", "nombre", "categoria", "precio", "cantidad")
    tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                   yscrollcommand=scrollbar.set, height=20)

    # MOSTRAR LOS DATOS EN EL TREEVIEW
    def actualizar_tabla():
        # Limpia la tabla
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)
        # Vuelve a escribirla pero actualizada
        clientes = listar_productos_controlador()
        for cliente in clientes:
            tabla_productos.insert("", "end", values=cliente)
    actualizar_tabla()


    # FUNCION ELIMINAR
    def ejecutar_eliminacion():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return

        # Obtenemos el ID del item seleccionado (columna 0)
        item_id = tabla_productos.item(seleccion[0])['values'][0]

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?")
        if confirmar:
            if eliminar_producto_controlador(item_id):
                actualizar_tabla()


    # MENU CONTEXTUAL (Clic derecho)
    menu_contextual = tk.Menu(ventana_productos, tearoff=0)
    menu_contextual.add_command(label="Editar",
                                command="")  # IMPLEMENTAR FUNCION DE EDITAR
    menu_contextual.add_command(label="Eliminar", command=ejecutar_eliminacion)


    def mostrar_menu(event):
        item = tabla_productos.identify_row(event.y)
        if item:
            tabla_productos.selection_set(item)
            menu_contextual.post(event.x_root, event.y_root)


    # CONFIGURAR COLUMNAS
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("precio", text="Precio")
    tabla_productos.heading("cantidad", text="Cantidad")

    tabla_productos.column("id", width=80, anchor="center")
    tabla_productos.column("nombre", width=250, anchor="w")
    tabla_productos.column("categoria", width=200, anchor="w")
    tabla_productos.column("precio", width=100, anchor="e")
    tabla_productos.column("cantidad", width=100, anchor="center")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tabla_productos.yview)


def nuevo_producto(callback):
    ventana_nuevo_producto = tk.Toplevel()
    ventana_nuevo_producto.title("Nuevo producto")
    ventana_nuevo_producto.configure(bg=color_primario)
    ventana_nuevo_producto.geometry("400x600+850+85")
    ventana_nuevo_producto.resizable(False, False)


    # CONFIGURACION DEL GRID
    ventana_nuevo_producto.grid_columnconfigure(0, weight=1)
    ventana_nuevo_producto.grid_columnconfigure(1, weight=2)


    # LABEL TITULO
    label_titulo = tk.Label(ventana_nuevo_producto, text="REGISTRAR PRODUCTO")
    label_titulo.config(bg=color_primario, fg=color_secundario, font=fuente_titulos)
    label_titulo.grid(row=0, column=0, columnspan=2, padx=20 ,pady=(50, 40))


    # NOMBRE
    label_nombre = tk.Label(ventana_nuevo_producto, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = tk.Entry(ventana_nuevo_producto, font=fuente_texto, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # CATEGORIA + MENU DESPLEGABLE
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
    cmd_validar_numeros = ventana_nuevo_producto.register(validar_solo_numeros)

    label_cantidad = tk.Label(ventana_nuevo_producto, text="Cantidad:")
    label_cantidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_cantidad.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_cantidad = tk.Entry(ventana_nuevo_producto, font=fuente_texto, width=20)
    entry_cantidad.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))
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


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_nuevo_producto)
    frame_botones.config(bg=color_primario, height= 20)
    frame_botones.grid(row=9, column=0, columnspan=2, pady=30)


    # BOTONES
    boton_guardar = tk.Button(frame_botones, text="Guardar", font=fuente_texto)
    boton_guardar.config(bg=color_secundario, fg=color_primario, width=12,
                         cursor="hand2", command=realizar_guardado)
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=fuente_texto)
    boton_cancelar.config(bg=color_secundario, fg=color_primario, width=12,
                          cursor="hand2", command=ventana_nuevo_producto.destroy)
    boton_cancelar.pack(side="left", padx=5)


def editar_producto():
    ventana_editar_producto = tk.Toplevel()
    ventana_editar_producto.title("Editar producto")
    ventana_editar_producto.configure(bg=color_primario)
    ventana_editar_producto.geometry("400x600+850+85")
    ventana_editar_producto.resizable(False, False)


    # CONFIGURACION DEL GRID
    ventana_editar_producto.grid_columnconfigure(0, weight=1)
    ventana_editar_producto.grid_columnconfigure(1, weight=2)


    # LABEL TITULO
    label_titulo = tk.Label(ventana_editar_producto, text="EDITAR PRODUCTO")
    label_titulo.config(bg=color_primario, fg=color_secundario, font=fuente_titulos)
    label_titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=(50, 40))


    # NOMBRE
    label_nombre = tk.Label(ventana_editar_producto, text="Nombre:")
    label_nombre.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_nombre.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_nombre = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=10)


    # CATEGORIA + MENU DESPLEGABLE
    label_categoria = tk.Label(ventana_editar_producto, text="Categoria:")
    label_categoria.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_categoria.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=10)


    # ---------------- FALTAN MAS CATEGORIAS ----------------
    lista_categorias = ["Alimento", "Cera", "Estampa", "Insumos", "Madera", "Medicamentos", "Miel"]
    combobox_categoria = ttk.Combobox(ventana_editar_producto)
    combobox_categoria.config(font=fuente_texto, values=lista_categorias, state="readonly")
    combobox_categoria.grid(row=2, column=1, sticky="w", padx=(0, 30), pady=10)


    # UNIDAD DE MEDIDA
    label_unidad_medida = tk.Label(ventana_editar_producto, text="Unidad de medida:")
    label_unidad_medida.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_unidad_medida.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=10)

    lista_unidad_medidas = ["Unidades", "Kilos", "Litros"]
    combobox_unidad_medida = ttk.Combobox(ventana_editar_producto)
    combobox_unidad_medida.config(font=fuente_texto, values=lista_unidad_medidas, state="readonly")
    combobox_unidad_medida.grid(row=3, column=1, sticky="w", padx=(0, 30), pady=10)


    # PRECIO
    cmd_validar_precio = ventana_editar_producto.register(validar_solo_numeros_punto)

    label_precio = tk.Label(ventana_editar_producto, text="Precio por unidad:")
    label_precio.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_precio.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_precio = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_precio.config(validate="key", validatecommand=(cmd_validar_precio, '%P'))
    entry_precio.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=10)


    # CANTIDAD
    cmd_validar_numeros = ventana_editar_producto.register(validar_solo_numeros)

    label_cantidad = tk.Label(ventana_editar_producto, text="Cantidad:")
    label_cantidad.config(font=fuente_texto, bg=color_primario, fg=color_secundario)
    label_cantidad.grid(row=5, column=0, sticky="e", padx=(20, 10), pady=10)

    entry_cantidad = tk.Entry(ventana_editar_producto, font=fuente_texto, width=20)
    entry_cantidad.config(validate="key", validatecommand=(cmd_validar_numeros, '%P'))
    entry_cantidad.grid(row=5, column=1, sticky="w", padx=(0, 20), pady=10)


    # FRAME BOTONES
    frame_botones = tk.Frame(ventana_editar_producto)
    frame_botones.config(bg=color_primario, height=20)
    frame_botones.grid(row=9, column=0, columnspan=2, pady=30)


    # BOTONES
    boton_guardar = tk.Button(frame_botones, text="Guardar", font=fuente_texto)
    boton_guardar.config(bg=color_secundario, fg=color_primario, width=12, cursor="hand2")
    boton_guardar.pack(side="left", padx=5)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=fuente_texto)
    boton_cancelar.config(bg=color_secundario, fg=color_primario, width=12,
                          cursor="hand2", command=ventana_editar_producto.destroy)
    boton_cancelar.pack(side="left", padx=5)


if __name__ == "__main__":
    root = tk.Tk() # Crea una ventana principal oculta
    root.withdraw() # La oculta (porque no la necesito visible)
    listado_productos() # Abre la ventana Toplevel de productos
    root.mainloop() # Mantiene la aplicación corriendo