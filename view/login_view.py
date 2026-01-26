import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from view.estilos import color_primario, color_secundario, fuente_texto, configurar_estilos, centrar_ventana, obtener_ruta_recurso
from controller.login_controlador import verificacion_inicio_sesion


def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.resizable(False, False)
    
    try:
        ventana_login.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except Exception as e:
        messagebox.showwarning("Error", "No se pudo cargar el icono: ")
        
    configurar_estilos(ventana_login)


    # Centro la ventana y configuro el grid
    centrar_ventana(ventana_login, 960, 600)
    ventana_login.grid_columnconfigure(0, weight=3, minsize=576)  # 60% de 960
    ventana_login.grid_columnconfigure(1, weight=2, minsize=384)  # 40% de 960
    ventana_login.grid_rowconfigure(0, weight=1)


    # Defino el espacio para colocar la imagen
    ruta_imagen_logo = obtener_ruta_recurso("logo_grande.ico")


    # Configuro el panel izquierdo
    frame_imagen_izquierda = tk.Frame(ventana_login, bg=color_primario)
    frame_imagen_izquierda.grid(row=0, column=0, sticky="nsew")


    # Configuro el panel derecho
    frame_login_derecha = tk.Frame(ventana_login, bg=color_secundario)
    frame_login_derecha.grid(row=0, column=1, sticky="nsew")

    # Configuro el grid para centrar el contenido
    frame_login_derecha.grid_rowconfigure(0, weight=1)
    frame_login_derecha.grid_columnconfigure(0, weight=1)

    contenedor_login = tk.Frame(frame_login_derecha, bg=color_secundario)
    contenedor_login.grid(row=0, column=0)

    # Agrego el título
    label_cartel_bienvenida = tk.Label(contenedor_login, text="Inicio de sesion")
    label_cartel_bienvenida.config(font=("Arial", 28, "bold"), bg=color_secundario, fg=color_primario)
    label_cartel_bienvenida.pack(pady=(0, 20))

    # Cargo y muestro el icono
    try:
        ruta_user_ico = obtener_ruta_recurso("usuario.ico")
        imagen_user_pil = Image.open(ruta_user_ico)
        imagen_user_pil = imagen_user_pil.resize((100, 100), Image.Resampling.LANCZOS)
        imagen_user = ImageTk.PhotoImage(imagen_user_pil)
        
        label_icono = tk.Label(contenedor_login, image=imagen_user, bg=color_secundario)
        label_icono.image = imagen_user
        label_icono.pack(pady=(0, 30))
    except Exception:
        pass

    # Configuro el formulario de login
    frame_form = tk.Frame(contenedor_login, bg=color_secundario)
    frame_form.pack(pady=(0, 20))

    # Añado el campo de usuario
    label_usuario = tk.Label(frame_form, text="Usuario:")
    label_usuario.config(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_usuario.grid(row=0, column=0, sticky="e", padx=10, pady=10)

    opciones = ["Administrador", "Usuario"]
    opciones_usuario = ttk.Combobox(frame_form, values=opciones, state="readonly", font=fuente_texto, width=15)
    opciones_usuario.current(1)
    opciones_usuario.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    # Añado el campo de contraseña
    label_clave = tk.Label(frame_form, text="Clave:")
    label_clave.config(bg=color_secundario, fg=color_primario, font=fuente_texto)
    label_clave.grid(row=1, column=0, sticky="e", padx=10, pady=10)

    entry_clave = ttk.Entry(frame_form, width=17, font=fuente_texto, show="*")
    entry_clave.grid(row=1, column=1, sticky="w", padx=10, pady=10)

    def intentar_login(event=None):
        usuario = opciones_usuario.get().lower()
        clave = entry_clave.get()

        if not usuario or not clave:
            messagebox.showwarning("Error", "Debe ingresar ambos campos")
            return

        if not verificacion_inicio_sesion(usuario, clave, ventana_login):
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")

    ventana_login.bind('<Return>', attempting_login_wrapper := lambda event: intentar_login(event))

    boton_inicio_sesion = ttk.Button(contenedor_login, text="Entrar", style="BotonPrimario.TButton")
    boton_inicio_sesion.config(cursor="hand2", command=intentar_login)
    boton_inicio_sesion.pack(ipadx=15, ipady=2)

    ventana_login.mainloop()


if __name__ == "__main__":
    mostrar_login()