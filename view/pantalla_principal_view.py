import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from view.estilos import color_primario, color_secundario, fuente_texto, configurar_estilos, obtener_ruta_recurso


# --- Defino las funciones wrappers para lazy loading ---
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
        # Implemento un fallback por si el archivo está en root
        from deudores_view import listado_deudores
    listado_deudores()


def abrir_remitos():
    from view.operaciones_view import nueva_operacion
    nueva_operacion()


# --- Defino las vistas principales ---

def mostrar_logo_central(ventana):
    # Configuro el frame para el contenido central
    frame_central = tk.Frame(ventana, bg=color_primario)
    frame_central.grid(row=1, column=0, sticky="nsew")
    frame_central.grid_rowconfigure(0, weight=1)
    frame_central.grid_columnconfigure(0, weight=1)

    try:
        ruta_logo = obtener_ruta_recurso("logo_grande.ico")
        imagen_pil = Image.open(ruta_logo)
        # Redimensiono la imagen si es necesario
        imagen_pil = imagen_pil.resize((400, 400), Image.Resampling.LANCZOS)
        imagen_logo = ImageTk.PhotoImage(imagen_pil)
        
        label_logo = tk.Label(frame_central, image=imagen_logo, bg=color_primario)
        label_logo.image = imagen_logo  # Mantengo referencia
        label_logo.grid(row=0, column=0)
    except Exception:
        # Si falla la imagen, muestro un texto o nada
        tk.Label(frame_central, text="Southern Honey Group", font=("Arial", 30, "bold"), 
                 bg=color_primario, fg=color_secundario).grid(row=0, column=0)


def pantalla_administrador():
    # Importo cotizaciones al momento de abrir la pantalla, no al inicio de la app
    try:
        from controller.cotizaciones import get_cotizacion_oficial_venta, get_cotizacion_blue_venta
    except ImportError:
        def get_cotizacion_oficial_venta(): return "Error"
        def get_cotizacion_blue_venta(): return "Error"

    ventana_principal = tk.Tk()
    configurar_estilos(ventana_principal)
    ventana_principal.configure(bg=color_primario)
    ventana_principal.resizable(True, True)
    ventana_principal.title("Menu principal - Administrador")
    ventana_principal.state("zoomed")
    try:
        ventana_principal.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass

    # Configuro el grid de la ventana
    ventana_principal.grid_rowconfigure(0, weight=0)  # Barra: establezco tamaño fijo
    ventana_principal.grid_rowconfigure(1, weight=1)  # Contenido: permito que se expanda
    ventana_principal.grid_columnconfigure(0, weight=1)  # Reservo el ancho completo

    # Configuro la barra superior
    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    opciones_top.grid_propagate(False)
    opciones_top.grid(row=0, column=0, sticky="ew")

    # Configuro el grid del frame superior
    opciones_top.grid_columnconfigure(4, weight=1)  # Defino un espacio expandible entre botones y valores

    # Configuro los botones (uso los wrappers lazy)
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

    # Configuro el frame derecho para los valores del dólar
    frame_valores = tk.Frame(opciones_top)
    frame_valores.configure(bg=color_secundario)
    frame_valores.grid(row=0, column=5, padx=(0, 20), pady=15, sticky="e")

    # Muestro el Dólar Oficial
    label_oficial = tk.Label(frame_valores, text="Oficial:")
    label_oficial.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_oficial.grid(row=0, column=0, padx=(0, 5), sticky="e")

    try:
        dolar_oficial = get_cotizacion_oficial_venta()
    except:
        dolar_oficial = "S/C"

    label_valor_oficial = tk.Label(frame_valores, text=f"{dolar_oficial}")
    label_valor_oficial.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_valor_oficial.grid(row=0, column=1, padx=(0, 20), sticky="w")

    # Muestro el Dólar Blue
    label_blue = tk.Label(frame_valores, text="Blue:")
    label_blue.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_blue.grid(row=0, column=2, padx=(0, 5), sticky="e")

    try:
        dolar_blue = get_cotizacion_blue_venta()
    except:
        dolar_blue = "S/C"

    label_valor_blue = tk.Label(frame_valores, text=f"{dolar_blue}")
    label_valor_blue.configure(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_valor_blue.grid(row=0, column=3, padx=(0, 0), sticky="w")
    
    # Muestro el logo central
    mostrar_logo_central(ventana_principal)

    ventana_principal.mainloop()


def pantalla_usuario():
    ventana_principal = tk.Tk()
    configurar_estilos(ventana_principal)
    ventana_principal.configure(bg=color_primario)
    ventana_principal.resizable(True, True)
    ventana_principal.title("Menu principal - Usuario")
    ventana_principal.state("zoomed")
    try:
        ventana_principal.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass

    # Configuro el grid de la ventana
    ventana_principal.grid_rowconfigure(0, weight=0)  # Barra: establezco tamaño fijo
    ventana_principal.grid_rowconfigure(1, weight=1)  # Contenido: permito que se expanda
    ventana_principal.grid_columnconfigure(0, weight=1)  # Reservo el ancho completo

    # Configuro la barra superior
    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    opciones_top.grid_propagate(False)
    opciones_top.grid(row=0, column=0, sticky="ew")

    # Configuro el grid del frame superior
    opciones_top.grid_columnconfigure(4, weight=1)  # Defino un espacio expandible entre botones y valores

    # Configuro los botones (uso los wrappers lazy)
    boton_productos = ttk.Button(opciones_top, text="PRODUCTOS", style="BotonPrimario.TButton")
    boton_productos.configure(command=abrir_productos, cursor="hand2")
    boton_productos.grid(row=0, column=0, padx=20, pady=15)

    boton_clientes = ttk.Button(opciones_top, text="CLIENTES", style="BotonPrimario.TButton")
    boton_clientes.configure(command=abrir_clientes, cursor="hand2")
    boton_clientes.grid(row=0, column=1, padx=20, pady=15)

    boton_remitos = ttk.Button(opciones_top, text="REMITOS", style="BotonPrimario.TButton")
    boton_remitos.configure(command=abrir_remitos, cursor="hand2")
    boton_remitos.grid(row=0, column=2, padx=20, pady=15)

    # Configuro el frame derecho para los valores del dólar (Vacío para usuario, o se puede ocultar)
    frame_valores = tk.Frame(opciones_top)
    frame_valores.configure(bg=color_secundario)
    frame_valores.grid(row=0, column=5, padx=(0, 20), pady=15, sticky="e")
    
    # Muestro el logo central
    mostrar_logo_central(ventana_principal)

    ventana_principal.mainloop()


if __name__ == "__main__":
    pantalla_administrador()