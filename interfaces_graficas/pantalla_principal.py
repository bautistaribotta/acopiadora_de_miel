import tkinter as tk
from utilidades.configuracion import *
from interfaces_graficas.proveedores import *
from interfaces_graficas.clientes import *


def pantalla_principal():
    ventana_principal = tk.Tk()
    ventana_principal.configure(bg=color_principal)
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
    boton_proveedores = tk.Button(opciones_top, text="PROVEEDORES")
    boton_proveedores.configure(bg=color_principal, fg=color_secundario, command=proveedores)
    boton_proveedores.grid(row=0, column=0, padx=20, pady=15)

    boton_clientes = tk.Button(opciones_top, text="CLIENTES")
    boton_clientes.configure(bg=color_principal, fg=color_secundario)
    boton_clientes.grid(row=0, column=1, padx=20, pady=15)

    boton_productos = tk.Button(opciones_top, text="PRODUCTOS")
    boton_productos.configure(bg=color_principal, fg=color_secundario)
    boton_productos.grid(row=0, column=2, padx=20, pady=15)

    boton_remitos = tk.Button(opciones_top, text="REMITOS")
    boton_remitos.configure(bg=color_principal, fg=color_secundario)
    boton_remitos.grid(row=0, column=3, padx=20, pady=15)

    ventana_principal.mainloop()

if __name__ == "__main__":
    pantalla_principal()