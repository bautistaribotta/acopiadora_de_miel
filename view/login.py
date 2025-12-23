import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.resizable(False, False)
    ventana_login.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")


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

    label_cartel_bienvenida = tk.Label(frame_login_derecha, text="Inicio de sesion")
    label_cartel_bienvenida.config(font="Arial, 35", bg=color_secundario)
    label_cartel_bienvenida.grid(row=10, column=5, padx=30, pady=(150, 75))


    # USUARIO
    label_usuario = tk.Label(frame_login_derecha, text="Usuario:")
    label_usuario.config(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_usuario.grid(row=15, column=5, padx=(0, 160), pady=10)

    opciones = ["Administrador", "Usuario"]
    opciones_usuario = ttk.Combobox(frame_login_derecha, values=opciones, state="readonly")
    opciones_usuario.config(font=fuente_texto, width=15)
    opciones_usuario.current(1)
    opciones_usuario.grid(row=15, column=5, padx=(90, 10), pady=10)


    # CONTRASEÑA
    label_clave = tk.Label(frame_login_derecha, text="Clave:")
    label_clave.config(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_clave.grid(row=25, column=5, padx=(0, 140), pady=0)

    entry_clave = ttk.Entry(frame_login_derecha, width=17, font=fuente_texto, show="*")
    entry_clave.grid(row=25, column=5, padx=(80, 0), pady=0)

    boton_inicio_sesion = ttk.Button(frame_login_derecha, text="Entrar")
    boton_inicio_sesion.config(cursor="hand2")
    boton_inicio_sesion.grid(row=50, column=5, padx=(90, 8), pady=15)

    ventana_login.mainloop()

if __name__ == "__main__":
    mostrar_login()