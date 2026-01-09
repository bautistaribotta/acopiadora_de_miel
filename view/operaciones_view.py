import tkinter as tk
from tkinter import ttk
from estilos import *


def nueva_operacion():
    ventana_nueva_operacion = tk.Toplevel()
    ventana_nueva_operacion.title("Nueva Operación")
    ventana_nueva_operacion.config(bg=color_primario)
    ventana_nueva_operacion.resizable(False, False)
    ventana_nueva_operacion.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana(ventana_nueva_operacion, ancho_ventana, alto_ventana)

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

    boton_agregar_producto = tk.Button(frame_botones_acciones, text="Agregar", font=fuente_texto,
                                       bg=color_secundario, fg=color_primario,
                                       width=12, cursor="hand2")
    boton_agregar_producto.pack(side="left", padx=5)

    boton_quitar_producto = tk.Button(frame_botones_acciones, text="Quitar", font=fuente_texto,
                                      bg=color_secundario, fg=color_primario,
                                      width=12, cursor="hand2")
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
    columnas_productos = ("id", "nombre", "categoria", "cantidad", "precio_unitario")
    tabla_productos = ttk.Treeview(frame_tree_container, columns=columnas_productos,
                                   show="headings", yscrollcommand=scrollbar_tabla.set, height=10)

    # Configurar encabezados
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("cantidad", text="Cantidad")
    tabla_productos.heading("precio_unitario", text="Precio Unit.")

    # Configurar columnas
    tabla_productos.column("id", width=30, anchor="center")
    tabla_productos.column("nombre", width=200, anchor="w")
    tabla_productos.column("categoria", width=120, anchor="w")
    tabla_productos.column("cantidad", width=80, anchor="center")
    tabla_productos.column("precio_unitario", width=100, anchor="e")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.config(command=tabla_productos.yview)


    # ==================== FRAME BOTONES FINALES ====================
    frame_botones_finales = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_botones_finales.grid(row=2, column=0, pady=(10, 20))

    # Botón Guardar
    boton_guardar = tk.Button(frame_botones_finales, text="Guardar",
                              font=fuente_texto, bg=color_secundario, fg=color_primario,
                              width=18, cursor="hand2")
    boton_guardar.pack(side="left", padx=10)

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_botones_finales, text="Cancelar",
                               font=fuente_texto, bg=color_secundario, fg=color_primario,
                               width=18, cursor="hand2",
                               command=ventana_nueva_operacion.destroy)
    boton_cancelar.pack(side="left", padx=10)


def editar_operacion():
    ventana_nueva_operacion = tk.Toplevel()
    ventana_nueva_operacion.title("Editar operacion")
    ventana_nueva_operacion.config(bg=color_primario)
    ventana_nueva_operacion.resizable(False, False)
    ventana_nueva_operacion.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")

    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana(ventana_nueva_operacion, ancho_ventana, alto_ventana)

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

    boton_agregar_producto = tk.Button(frame_botones_acciones, text="Agregar", font=fuente_texto,
                                       bg=color_secundario, fg=color_primario,
                                       width=12, cursor="hand2")
    boton_agregar_producto.pack(side="left", padx=5)

    boton_quitar_producto = tk.Button(frame_botones_acciones, text="Quitar", font=fuente_texto,
                                      bg=color_secundario, fg=color_primario,
                                      width=12, cursor="hand2")
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
    columnas_productos = ("id", "nombre", "categoria", "cantidad", "precio_unitario")
    tabla_productos = ttk.Treeview(frame_tree_container, columns=columnas_productos,
                                   show="headings", yscrollcommand=scrollbar_tabla.set, height=10)

    # Configurar encabezados
    tabla_productos.heading("id", text="ID")
    tabla_productos.heading("nombre", text="Nombre")
    tabla_productos.heading("categoria", text="Categoría")
    tabla_productos.heading("cantidad", text="Cantidad")
    tabla_productos.heading("precio_unitario", text="Precio Unit.")

    # Configurar columnas
    tabla_productos.column("id", width=30, anchor="center")
    tabla_productos.column("nombre", width=200, anchor="w")
    tabla_productos.column("categoria", width=120, anchor="w")
    tabla_productos.column("cantidad", width=80, anchor="center")
    tabla_productos.column("precio_unitario", width=100, anchor="e")

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.config(command=tabla_productos.yview)

    # ==================== FRAME BOTONES FINALES ====================
    frame_botones_finales = tk.Frame(ventana_nueva_operacion, bg=color_primario)
    frame_botones_finales.grid(row=2, column=0, pady=(10, 20))

    # Botón Guardar
    boton_guardar = tk.Button(frame_botones_finales, text="Guardar",
                              font=fuente_texto, bg=color_secundario, fg=color_primario,
                              width=18, cursor="hand2")
    boton_guardar.pack(side="left", padx=10)

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_botones_finales, text="Cancelar",
                               font=fuente_texto, bg=color_secundario, fg=color_primario,
                               width=18, cursor="hand2",
                               command=ventana_nueva_operacion.destroy)
    boton_cancelar.pack(side="left", padx=10)


if __name__ == "__main__":
    nueva_operacion()