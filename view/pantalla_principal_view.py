import tkinter as tk
from tkinter import ttk
from view.estilos import color_primario, color_secundario, fuente_texto, configurar_estilos


# --- FUNCIONES WRAPPERS PARA LAZY LOADING ---
def abrir_productos():
    from view.productos_view import listado_productos
    listado_productos()


def abrir_clientes():
    from view.clientes_view import listado_clientes
    listado_clientes()


def abrir_deudores():
    try:
        from view.deudores_view import listado_deudores
    except ImportError:
        # Fallback por si el archivo esta en root
        from deudores_view import listado_deudores
    listado_deudores()


def abrir_remitos():
    from view.operaciones_view import nueva_operacion
    nueva_operacion()


# --- VISTAS PRINCIPALES ---

def pantalla_administrador():
    # Importamos cotizaciones al momento de abrir la pantalla, no al inicio de la app
    from controller.cotizaciones import get_cotizacion_oficial_venta, get_cotizacion_blue_venta

    ventana_principal = tk.Tk()
    configurar_estilos(ventana_principal)
    ventana_principal.configure(bg=color_primario)
    ventana_principal.resizable(True, True)
    ventana_principal.title("Menu principal - Administrador")
    ventana_principal.state("zoomed")
    # ventana_principal.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")

    # CONFIGURACION DEL GRID DE LA VENTANA
    ventana_principal.grid_rowconfigure(0, weight=0)  # Barra: tamaño fijo
    ventana_principal.grid_rowconfigure(1, weight=1)  # Contenido: se expande
    ventana_principal.grid_columnconfigure(0, weight=1)  # Ancho completo

    # BARRA SUPERIOR
    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    opciones_top.grid_propagate(False)
    opciones_top.grid(row=0, column=0, sticky="ew")

    # CONFIGURACION DEL GRID DEL FRAME SUPERIOR
    opciones_top.grid_columnconfigure(4, weight=1)  # Espacio expandible entre botones y valores

    # BOTONES (Usan los wrappers lazy)
    boton_productos = ttk.Button(opciones_top, text="PRODUCTOS", style="BotonPrimario.TButton")
    boton_productos.configure(command=abrir_productos, cursor="hand2")
    boton_productos.grid(row=0, column=0, padx=20, pady=15)

    boton_clientes = ttk.Button(opciones_top, text="CLIENTES", style="BotonPrimario.TButton")
    boton_clientes.configure(command=abrir_clientes, cursor="hand2")
    boton_clientes.grid(row=0, column=1, padx=20, pady=15)

    boton_deudores = ttk.Button(opciones_top, text="DEUDORES", style="BotonPrimario.TButton")
    boton_deudores.configure(cursor="hand2", command=abrir_deudores)
    boton_deudores.grid(row=0, column=2, padx=20, pady=15)

    boton_remitos = ttk.Button(opciones_top, text="REMITOS", style="BotonPrimario.TButton")
    boton_remitos.configure(command=abrir_remitos, cursor="hand2")
    boton_remitos.grid(row=0, column=3, padx=20, pady=15)

    # FRAME DERECHO - VALORES DOLAR
    frame_valores = tk.Frame(opciones_top)
    frame_valores.configure(bg=color_secundario)
    frame_valores.grid(row=0, column=5, padx=(0, 20), pady=15, sticky="e")

    # DOLAR OFICIAL
    label_oficial = tk.Label(frame_valores, text="Oficial:")
    label_oficial.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_oficial.grid(row=0, column=0, padx=(0, 5), sticky="e")

    dolar_oficial = get_cotizacion_oficial_venta()
    label_valor_oficial = tk.Label(frame_valores, text=f"{dolar_oficial}")
    label_valor_oficial.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_valor_oficial.grid(row=0, column=1, padx=(0, 20), sticky="w")

    # DOLAR BLUE
    label_blue = tk.Label(frame_valores, text="Blue:")
    label_blue.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_blue.grid(row=0, column=2, padx=(0, 5), sticky="e")

    dolar_blue = get_cotizacion_blue_venta()
    label_valor_blue = tk.Label(frame_valores, text=f"{dolar_blue}")
    label_valor_blue.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_valor_blue.grid(row=0, column=3, padx=(0, 0), sticky="w")

    ventana_principal.mainloop()


def pantalla_usuario():
    ventana_principal = tk.Tk()
    configurar_estilos(ventana_principal)
    ventana_principal.configure(bg=color_primario)
    ventana_principal.resizable(True, True)
    ventana_principal.title("Menu principal - Usuario")
    ventana_principal.state("zoomed")
    # ventana_principal.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")

    # CONFIGURACION DEL GRID DE LA VENTANA
    ventana_principal.grid_rowconfigure(0, weight=0)  # Barra: tamaño fijo
    ventana_principal.grid_rowconfigure(1, weight=1)  # Contenido: se expande
    ventana_principal.grid_columnconfigure(0, weight=1)  # Ancho completo

    # BARRA SUPERIOR
    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    opciones_top.grid_propagate(False)
    opciones_top.grid(row=0, column=0, sticky="ew")

    # CONFIGURACION DEL GRID DEL FRAME SUPERIOR
    opciones_top.grid_columnconfigure(4, weight=1)  # Espacio expandible entre botones y valores

    # BOTONES (Usan los wrappers lazy)
    boton_productos = ttk.Button(opciones_top, text="PRODUCTOS", style="BotonPrimario.TButton")
    boton_productos.configure(command=abrir_productos, cursor="hand2")
    boton_productos.grid(row=0, column=0, padx=20, pady=15)

    boton_clientes = ttk.Button(opciones_top, text="CLIENTES", style="BotonPrimario.TButton")
    boton_clientes.configure(command=abrir_clientes, cursor="hand2")
    boton_clientes.grid(row=0, column=1, padx=20, pady=15)

    boton_remitos = ttk.Button(opciones_top, text="REMITOS", style="BotonPrimario.TButton")
    boton_remitos.configure(command=abrir_remitos, cursor="hand2")
    boton_remitos.grid(row=0, column=2, padx=20, pady=15)

    # FRAME DERECHO - VALORES DOLAR
    frame_valores = tk.Frame(opciones_top)
    frame_valores.configure(bg=color_secundario)
    frame_valores.grid(row=0, column=5, padx=(0, 20), pady=15, sticky="e")

    ventana_principal.mainloop()


if __name__ == "__main__":
    pantalla_administrador()