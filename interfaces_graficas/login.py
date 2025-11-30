import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def centrar_ventana(ventana, aplicacion_ancho, aplicacion_alto):
    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()
    x = int(ancho / 2) - int(aplicacion_ancho / 2)
    y = int(alto / 2) - int(aplicacion_alto / 2) - 40 # Resto 40 para que quede mas arriba
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_alto}+{x}+{y}")


def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.resizable(False, False)


    # LLAMO A LA FUNCION PARA DEJAR LA VENTANA CENTRADA Y CONFIGURO EL GRID
    centrar_ventana(ventana_login, 960, 600)
    ventana_login.grid_columnconfigure(0, weight=3, minsize=576)  # 60% de 960
    ventana_login.grid_columnconfigure(1, weight=2, minsize=384)  # 40% de 960
    ventana_login.grid_rowconfigure(0, weight=1)


    # IZQUIERDA
    frame_imagen_izquierda = tk.Frame(ventana_login, bg=color_primario)
    frame_imagen_izquierda.grid(row=0, column=0, sticky="nsew")

    # Espacio para colocar la imagen

    # DERECHA
    frame_login_derecha = tk.Frame(ventana_login, bg=color_secundario)
    frame_login_derecha.grid(row=0, column=1, sticky="nsew")

    label_cartel_bienvenida = tk.Label(frame_login_derecha, text="Inicio de sesion", font="Arial, 35", bg=color_secundario)
    label_cartel_bienvenida.grid(row=10, column=5, padx=30, pady=(150, 75))

    opciones = ["Administrador", "Usuario"]
    opciones_usuario = ttk.Combobox(frame_login_derecha, values=opciones, state="readonly")
    opciones_usuario.config(font=fuente1)
    opciones_usuario.current(1)
    opciones_usuario.grid(row=15, column=5, padx=30, pady=10)

    entry_contrasenia = ttk.Entry(frame_login_derecha, width=21, font=fuente1, show="*")
    entry_contrasenia.grid(row=25, column=5, padx=30, pady=10)

    boton_inicio_sesion = ttk.Button(frame_login_derecha, text="Entrar")
    boton_inicio_sesion.grid(row=50, column=5,padx=30, pady=10)

    ventana_login.mainloop()

if __name__ == "__main__":
    mostrar_login()