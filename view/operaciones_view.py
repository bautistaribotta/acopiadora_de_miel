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

    # Tabla Resultados Busqueda
    frame_tabla_busqueda = tk.Frame(frame_izq, bg=color_primario)
    frame_tabla_busqueda.pack(fill="both", expand=True)

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

    # Frame Agregar (Cantidad y Boton)
    frame_agregar = tk.Frame(frame_izq, bg=color_primario)
    frame_agregar.pack(fill="x", pady=15)
    
    tk.Label(frame_agregar, text="Cantidad:", bg=color_primario, fg="white", font=fuente_texto).pack(side="left", padx=(0,5))
    entry_cantidad = ttk.Entry(frame_agregar, width=10, font=fuente_texto)
    entry_cantidad.pack(side="left", padx=(0, 15))
    
    # Cargar icono carrito
    img_carrito = Image.open(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\carrito.ico")
    img_carrito = img_carrito.resize((20, 20))
    icono_carrito = ImageTk.PhotoImage(img_carrito)

    btn_agregar = ttk.Button(frame_agregar, image=icono_carrito, style="BotonSecundario.TButton")
    btn_agregar.image = icono_carrito 
    btn_agregar.config(cursor="hand2")
    btn_agregar.pack(side="left")


    # ========================== COLUMNA DERECHA: DETALLE OPERACION (CARRITO) ==========================
    frame_der = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Header Derecho (Alineado con el Buscador de la izquierda)
    frame_header_der = tk.Frame(frame_der, bg=color_primario)
    frame_header_der.pack(fill="x", pady=(10, 20)) # Mismo padding que search bar izquierda
    
    # Titulo centrado
    tk.Label(frame_header_der, text="Listado de compra", font=fuente_titulos, bg=color_primario, fg=color_secundario).pack(anchor="center")

    # Tabla Carrito
    frame_tabla_carrito = tk.Frame(frame_der, bg=color_primario)
    frame_tabla_carrito.pack(fill="both", expand=True)

    scrollbar_carrito = ttk.Scrollbar(frame_tabla_carrito)
    scrollbar_carrito.pack(side="right", fill="y")
    
    cols_carrito = ("nombre", "cantidad", "subtotal")
    tabla_carrito = ttk.Treeview(frame_tabla_carrito, columns=cols_carrito, show="headings", 
                                 yscrollcommand=scrollbar_carrito.set, height=15)
    
    tabla_carrito.heading("nombre", text="Producto")
    tabla_carrito.heading("cantidad", text="Cantidad")
    tabla_carrito.heading("subtotal", text="Sub Total")
    
    tabla_carrito.column("nombre", width=180, anchor="center")
    tabla_carrito.column("cantidad", width=80, anchor="center")
    tabla_carrito.column("subtotal", width=100, anchor="center")
    
    tabla_carrito.pack(side="left", fill="both", expand=True)
    scrollbar_carrito.config(command=tabla_carrito.yview)

    # Botones y Totales del Carrito
    frame_acciones_carrito = tk.Frame(frame_der, bg=color_primario)
    frame_acciones_carrito.pack(fill="x", pady=10)
    
    # Cargar icono tacho
    img_tacho = Image.open(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\tacho.ico")
    img_tacho = img_tacho.resize((20, 20))
    icono_tacho = ImageTk.PhotoImage(img_tacho)
    
    # Boton Eliminar (Derecha)
    btn_quitar = ttk.Button(frame_acciones_carrito, image=icono_tacho, style="BotonSecundario.TButton")
    btn_quitar.image = icono_tacho 
    btn_quitar.config(cursor="hand2")
    btn_quitar.pack(side="right", padx=(10, 0))

    # Total (A la izquierda del boton)
    # Packeamos de derecha a izquierda: Primero el valor, luego la etiqueta
    lbl_total_pesos = tk.Label(frame_acciones_carrito, text="$ 0.00", bg=color_primario, fg="white", font=("Arial", 12, "bold"))
    lbl_total_pesos.pack(side="right", padx=(5, 0))
    
    tk.Label(frame_acciones_carrito, text="Total:", bg=color_primario, fg="white", font=("Arial", 12)).pack(side="right")


    # ========================== FRAME INFERIOR: ACCIONES FINALES ==========================
    frame_final = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_final.grid(row=1, column=0, columnspan=2, pady=20)
    
    btn_guardar_op = ttk.Button(frame_final, text="Guardar", style="BotonSecundario.TButton")
    btn_guardar_op.config(cursor="hand2", width=8)
    btn_guardar_op.pack(side="left", padx=10)

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