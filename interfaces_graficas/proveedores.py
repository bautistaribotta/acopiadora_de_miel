import tkinter as tk
from utilidades.configuracion import *


def proveedores():
    ventana_proveedores = tk.Toplevel()
    ventana_proveedores.title("Proveedores")
    ventana_proveedores.geometry("800x600+550+85")
    ventana_proveedores.resizable(False, False)
    ventana_proveedores.configure(bg=color_principal)
    # CONFIGURACION DEL GRID DE LA VENTANA
    ventana_proveedores.grid_rowconfigure(0, weight=1)
    ventana_proveedores.grid_columnconfigure(0, weight=1)


    # FRAME SUPERIOR
    frame_superior = tk.Frame(ventana_proveedores, bg=color_secundario)
    frame_superior.configure(height=40, padx=20, pady=20)
    frame_superior.grid(row=0, column=0, sticky="nwe")


    # BARRA DE BUSQUEDA
    barra_busqueda = tk.Entry(frame_superior, bg=color_secundario, fg=color_principal, font=fuente1)
    barra_busqueda.pack(side="right")
    label_busqueda = tk.Label(frame_superior, text="Buscar:", font=fuente1, bg= color_secundario, fg=color_principal)
    label_busqueda.pack(side="top")


    # BOTONES
    boton_agregar = tk.Button(frame_superior, bg=color_secundario, fg=color_principal, text="Añadir")
    boton_agregar.config(width=15, font=fuente1)
    boton_agregar.pack(side="left", padx=5)

    boton_editar = tk.Button(frame_superior, bg=color_secundario, fg=color_principal, text="Editar")
    boton_editar.config(width=15, font=fuente1)
    boton_editar.pack(side="left", padx=5)

    boton_eliminar = tk.Button(frame_superior, bg=color_secundario, fg=color_principal, text="Eliminar")
    boton_eliminar.config(width=15, font=fuente1)
    boton_eliminar.pack(side="left", padx=5)


if __name__ == "__main__" :
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk()  # Crea una ventana principal oculta
    #root.withdraw()  # La oculta (porque no la necesito visible)
    proveedores()  # Abre la ventana Toplevel de proveedores
    root.mainloop()  # Mantiene la aplicación corriendo