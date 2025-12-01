import tkinter as tk
from utilidades.configuracion import *
from interfaces_graficas.clientes import *
from interfaces_graficas.clientes import *
from interfaces_graficas.productos import *
from interfaces_graficas.remitos import *


def pantalla_principal():
    ventana_principal = tk.Tk()
    ventana_principal.configure(bg=color_primario)
    ventana_principal.state("zoomed")
    ventana_principal.title("Menu principal")
    ventana_principal.resizable(False, True)
    # CONFIGURACION DEL GRID DE LA VENTANA
    ventana_principal.grid_rowconfigure(0, weight=0)  # Barra: tamaño fijo
    ventana_principal.grid_rowconfigure(1, weight=1)  # Contenido: se expande
    ventana_principal.grid_columnconfigure(0, weight=1)  # Todo el ancho


    # BARRA SUPERIOR
    opciones_top = tk.Frame(ventana_principal)
    opciones_top.configure(bg=color_secundario, height=60)
    opciones_top.grid_propagate(False)
    opciones_top.grid(row=0, column=0, sticky="ew")


    # BOTONES
    boton_productos = tk.Button(opciones_top, text="PRODUCTOS")
    boton_productos.configure(bg=color_primario, fg=color_secundario, command=productos)
    boton_productos.grid(row=0, column=1, padx=20, pady=15)

    boton_clientes = tk.Button(opciones_top, text="CLIENTES")
    boton_clientes.configure(bg=color_primario, fg=color_secundario, command=clientes)
    boton_clientes.grid(row=0, column=2, padx=20, pady=15)

    boton_remitos = tk.Button(opciones_top, text="REMITOS")
    boton_remitos.configure(bg=color_primario, fg=color_secundario, command=remitos)
    boton_remitos.grid(row=0, column=3, padx=20, pady=15)

    ventana_principal.mainloop()


if __name__ == "__main__":
    pantalla_principal()