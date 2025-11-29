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


    # FRAME SUPERIOR - Este frame solo debe contener el label y el entry
    frame_superior = tk.Frame(ventana_proveedores, bg=color_secundario)
    frame_superior.configure(height=40, padx=20, pady=20)
    frame_superior.grid(row=0, column=0, sticky="nwe")

    # BARRA DE BUSQUEDA
    label_busqueda = tk.Label(frame_superior, text="Buscar:", font=fuente1, bg=color_secundario, fg=color_principal)
    label_busqueda.pack(side="left")
    barra_busqueda = tk.Entry(frame_superior, bg=color_secundario, fg=color_principal, font=fuente1)
    barra_busqueda.pack(side="left")


    # FRAME MEDIO - Este frame debe contener a los botones
    frame_medio = tk.Frame(ventana_proveedores, bg=color_secundario)
    frame_medio.configure(height=40, padx=20, pady=20)
    frame_medio.grid(row=1, column=0, sticky="nwe")

    # BOTONES
    boton_agregar = tk.Button(frame_medio, bg=color_secundario, fg=color_principal, text="Añadir")
    boton_agregar.config(width=15, font=fuente1)
    boton_agregar.pack(side="left", padx=(100, 5), pady=5)

    boton_editar = tk.Button(frame_medio, bg=color_secundario, fg=color_principal, text="Editar")
    boton_editar.config(width=15, font=fuente1)
    boton_editar.pack(side="left", padx=5, pady=5)

    boton_eliminar = tk.Button(frame_medio, bg=color_secundario, fg=color_principal, text="Eliminar")
    boton_eliminar.config(width=15, font=fuente1)
    boton_eliminar.pack(side="left", padx=(5, 100), pady=5)


if __name__ == "__main__" :
    # ESTO ES SOLO A MODO DE PRUEBA, PARA NO ABRIR TODO EL TIEMPO LA PANTALLA PRINCIPAL
    root = tk.Tk()  # Crea una ventana principal oculta
    #root.withdraw()  # La oculta (porque no la necesito visible)
    proveedores()  # Abre la ventana Toplevel de proveedores
    root.mainloop()  # Mantiene la aplicación corriendo