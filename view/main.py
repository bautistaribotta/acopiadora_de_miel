from view.clientes_view import *
from view.productos_view import *
from view.remitos_view import *
from controller.cotizaciones import *


def pantalla_principal():
    ventana_principal = tk.Tk()
    ventana_principal.configure(bg=color_primario)
    ventana_principal.resizable(True, True)
    ventana_principal.title("Menu principal")
    ventana_principal.state("zoomed")

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


    # BOTONES
    boton_productos = tk.Button(opciones_top, text="PRODUCTOS")
    boton_productos.configure(bg=color_primario, fg=color_secundario, command=listado_productos, cursor="hand2")
    boton_productos.grid(row=0, column=0, padx=20, pady=15)

    boton_clientes = tk.Button(opciones_top, text="CLIENTES")
    boton_clientes.configure(bg=color_primario, fg=color_secundario, command=listado_clientes, cursor="hand2")
    boton_clientes.grid(row=0, column=1, padx=20, pady=15)

    boton_remitos = tk.Button(opciones_top, text="REMITOS")
    boton_remitos.configure(bg=color_primario, fg=color_secundario, command=remitos, cursor="hand2")
    boton_remitos.grid(row=0, column=2, padx=20, pady=15)


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


if __name__ == "__main__":
    pantalla_principal()