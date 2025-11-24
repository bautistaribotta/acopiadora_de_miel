import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


fuente1 = "Arial", 14


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
    # Llamo a la funcion que deja centrada la ventana
    centrar_ventana(ventana_login, 960, 600)

    # IZQUIERDA
    frame_imagen_izquierda = tk.Frame(ventana_login, bg=color_principal)
    frame_imagen_izquierda.place(x=0, y=0, relwidth=0.6, relheight=1)

    # Espacio para colocar la imagen

    # DERECHA
    frame_login_derecha = tk.Frame(ventana_login, bg=color_secundario)
    frame_login_derecha.place(relx=0.6, y=0, relwidth=0.4, relheight=1)

    label_cartel_bienvenida = tk.Label(frame_login_derecha, text="BIENVENIDO", font="Arial, 40", bg=color_secundario)
    label_cartel_bienvenida.place(x=30, y=150)

    opciones = ["Administrador", "Usuario"]
    opciones_usuario = ttk.Combobox(frame_login_derecha, values=opciones, state="readonly")
    opciones_usuario.config(font=fuente1)
    opciones_usuario.current(1)
    opciones_usuario.place(x=74, y=300)

    entry_contrasenia = ttk.Entry(frame_login_derecha, width=21, font=fuente1, show="*")
    entry_contrasenia.place(x=76, y=350)

    boton_inicio_sesion = ttk.Button(frame_login_derecha, text="Inicio de sesion")
    boton_inicio_sesion.place(x=152, y=400)

    ventana_login.mainloop()

if __name__ == "__main__":
    mostrar_login()