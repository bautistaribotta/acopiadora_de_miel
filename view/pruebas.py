import tkinter as tk
from tkinter import messagebox
from view.estilos import centrar_ventana_interna, color_primario, color_secundario


class pantalla_principal():
    ventana = tk.Tk()
    ventana.configure(bg=color_primario)
    ventana.title("Pantalla principal")
    centrar_ventana_interna(ventana, 1200, 600)

    try:
        ventana.iconbitmap(r"C:\Users\bauti\PycharmProjects\Acopiadora_de_miel\recursos\colmena.ico")
    except Exception as error:
        messagebox.showerror("Error al cargar icono", f"{error}")

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    frame_botones_superior = tk.Frame(ventana)
    frame_botones_superior.configure(bg=color_secundario, height=80)
    frame_botones_superior.grid_propagate(False)
    frame_botones_superior.grid(row=0, column=0, sticky="ew")
    #frame_botones_superior.pack(fill="x", expand=True, side="top")

    ventana.mainloop()


ventana_pantalla_principal = pantalla_principal()
